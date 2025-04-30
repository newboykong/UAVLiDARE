import laspy
import numpy as np
import pyvista as pv
from scipy.ndimage import convolve
from skimage.morphology import erosion, dilation
from PySide6.QtCore import QThread, Signal


# 定义一个空的信号类
class FakeSignal:
    signal = Signal(int)  # 定义一个信号
    def emit(self, value):
        pass  # 空的 emit，不执行任何操作


# PMF 算法：使用形态学腐蚀和膨胀进行地面点提取
def pmf_filter(las, grid_size=(2, -2), dh_min=0.3, dh_max=25, s=0.2, iterations=3,progress_updated=None,cls_id=None,stop_callback=lambda *args: None):
    # 如果调用时没有受用多线程技术，创建一个空的信号发射函数
    if progress_updated is None:
        progress_updated = FakeSignal()  # 创建一个空的信号对象


    # 获取三维坐标和分类信息
    cls = las.classification

    # 初始化掩码数组，默认所有点都不选中
    cls_mask = np.zeros_like(cls, dtype=bool)
    original_indices=None

    # 如果存在分类信息筛选处理的数据
    if cls_id is not None:
        for i in cls_id:
            cls_mask |= (cls == i)  # 每次把匹配 i 的点并入掩码中
        # 获取las文件的x, y, z坐标
        points = np.vstack((las.x, las.y, las.z)).T
        # 用掩膜筛选
        points = points[cls_mask]
        # 获取原始点索引
        original_indices = np.where(cls_mask)[0]
    else:
        # 获取las文件的x, y, z坐标
        points = np.vstack((las.x, las.y, las.z)).T


    # 获取x,y,z坐标
    x=points[:,0]
    y=points[:,1]
    z=points[:,2]

    # 获取 X 和 Y 的最大最小值
    x_min, y_min = np.min(points[:, :2], axis=0)
    x_max, y_max = np.max(points[:, :2], axis=0)

    # 计算格网的x, y的数量
    grid_x = int(np.ceil((x_max - x_min) / grid_size[0]))
    grid_y = int(np.ceil((y_min - y_max) / grid_size[1]))
    progress_updated.emit(10)  # 进度 10%

    # 将 x, y 值归一化到网格索引
    x_index = np.clip(((x - x_min) / (x_max - x_min) * (grid_x - 1)), 0, grid_x - 1).astype(int)
    y_index = np.clip(((y - y_max) / (y_min - y_max) * (grid_y - 1)), 0, grid_y - 1).astype(int)

    # 创建一个空的网格，初始化为np.inf（表示没有数据）
    grid = np.full((grid_x, grid_y), np.inf)

    # 统计网格中的最低点
    for i in range(len(points)):
        # 获取每个点的网格位置
        grid_cell_x = x_index[i]
        grid_cell_y = y_index[i]

        # 更新该网格的最低点
        grid[grid_cell_x, grid_cell_y] = min(grid[grid_cell_x, grid_cell_y], z[i])


    progress_updated.emit(20)  # 进度 20%

    # 创建一个简单的卷积核，用于邻域均值插值
    kernel = np.ones((3, 3)) / 9.0  # 3x3均值滤波器
    # 对网格进行卷积插值，填补空值
    # 使用该函数填充空值
    grid_filled = fill_na_with_convolution(grid, kernel)

    progress_updated.emit(30)  # 进度 30%

    # 创建储存分类信息的数组
    cls_index = np.zeros_like(cls)

    progress_b=40
    # 设置形态滤波的窗口迭代次数
    for k in range(1, iterations + 1):
        # 发送信号
        if k<=6:
            progress_b+=10
            progress_updated.emit(progress_b)
            if stop_callback():  # 👈 调用中断判断函数
                return None

        # 设置初始窗口大小
        b = 1  # 设置线性增长
        window_size = 2 * k * b + 1
        # 根据窗口大小设置dh的阈值
        if window_size <= 3:
            dh = dh_min
        else:
            window_size_behind = 2 * (k - 1) * b + 1
            dh = s * (window_size - window_size_behind) * grid_size[0] + dh_min
            dh_min = dh
        if dh > dh_max:
            dh = dh_max

        # 对网格数据进行开运算
        struct_elem = np.ones((window_size, window_size))  # 创建结构元素
        # 执行形态学腐蚀和膨胀操作
        eroded_data = erosion(grid_filled, struct_elem)
        opening_data = dilation(eroded_data, struct_elem)
        if stop_callback():  # 👈 调用中断判断函数
            return None

        from collections import defaultdict

        # 提前构建网格索引字典，只做一次
        grid_index_dict = defaultdict(list)
        for idx, (gx, gy) in enumerate(zip(x_index, y_index)):
            grid_index_dict[(gx, gy)].append(idx)

        for x_id in range(grid_x):
            for y_id in range(grid_y):
                if stop_callback():
                    return None

                current_grid_index = grid_index_dict.get((x_id, y_id), [])
                if not current_grid_index:
                    continue  # 该网格无点

                current_grid_z = opening_data[x_id, y_id]
                current_indices = np.array(current_grid_index)

                mask = (z[current_indices] - current_grid_z) < dh
                ground_index = current_indices[mask]

                if ground_index.size > 0:
                    if original_indices is not None:
                        original_ground_index = original_indices[ground_index]
                        cls_index[original_ground_index] = 2
                    else:
                        cls_index[ground_index] = 2


        # 统计非地面点数量
        num_non_ground = np.count_nonzero(cls_index == 2)
    cls[cls_index == 2] = 2
    cls[cls_index != 2] = 4
    las.classification = cls  # 确保分类信息是 uint8 类型
    progress_updated.emit(100) # 程序完成

    return las


# 定义一个函数，用于检查并填充空值
def fill_na_with_convolution(grid, kernel, max_iterations=10):
    for _ in range(max_iterations):
        # 只填充空值，不改变其他值
        if np.isnan(grid).sum() == 0:
            break  # 如果没有空值，停止循环
        # 用卷积填充空值
        grid = convolve(np.nan_to_num(grid, nan=0.0), kernel, mode='nearest')
    return grid


# 4. 可视化点云数据
def visualize_points(las):
    # 获取点云坐标
    points = np.vstack((las.x, las.y, las.z)).T
    # 获取分类信息
    classification = las.classification

    # 创建一个 PyVista 点云对象
    point_cloud = pv.PolyData(points)

    # 定义分类编号与颜色的映射
    category_colors = {
        0: "gray",  # 未分类 (Unclassified)
        1: "white",  # 未分类 (Unclassified)
        2: "brown",  # 地面 (Ground)
        3: "green",  # 低植被 (Low Vegetation)
        4: "lime",  # 中植被 (Medium Vegetation)
        5: "darkgreen"  # 高植被 (High Vegetation)
    }

    # 设置点云颜色（根据分类信息）
    point_cloud["Classification"] = classification
    # 创建渲染窗口
    plotter = pv.Plotter()

    # 存储图例项
    legend_entries = []

    # 根据标签为点云着色
    for i in np.unique(classification):
        mask = np.where(classification == i)[0]  # 获取索引
        sub_cloud = point_cloud.extract_points(mask)
        plotter.add_mesh(sub_cloud, color=category_colors[i], point_size=10)
        legend_entries.append([f'Class {i}', category_colors[i]])  # 手动存储图例项

    # 添加图例
    plotter.add_legend(legend_entries)
    # 添加坐标轴
    plotter.add_axes()
    plotter.show()


def count_classifications(las):
    """统计las点云数据的分类信息"""
    unique_classes, counts = np.unique(las.classification, return_counts=True)
    class_dict = dict(zip(unique_classes, counts))

    print("点云分类统计结果：")
    for cls, count in class_dict.items():
        print(f"类别 {cls}: {count} 个点")

    return class_dict


def point_attribute(las):
    # 计算并输出 las 文件的最大最小 x, y, z
    x_min, x_max = np.min(las.x), np.max(las.x)
    y_min, y_max = np.min(las.y), np.max(las.y)
    z_min, z_max = np.min(las.z), np.max(las.z)

    print(f"x_min: {x_min}, x_max: {x_max}")
    print(f"y_min: {y_min}, y_max: {y_max}")
    print(f"z_min: {z_min}, z_max: {z_max}")


# 5. 主程序
def main():
    # 读取点云文件
    file_path = "E:/数据相关/PCM测试数据/测试数据二（对应菜单栏测试）.las"  # 修改为你的 LAS 文件路径
    las = laspy.read(file_path)

    # 输出带你云属性
    point_attribute(las)
    count_classifications(las)

    # 进行 PMF 滤波，提取地面点
    pmf_filter(las)

    # 可视化点云数据
    visualize_points(las)

    count_classifications(las)


if __name__ == "__main__":
    main()
