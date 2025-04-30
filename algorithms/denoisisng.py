import laspy
import numpy as np
import pyvista as pv
import vtk
from PySide6.QtCore import Signal
from scipy.spatial import cKDTree


# 定义一个空的信号类
class FakeSignal:
    signal = Signal(int)  # 定义一个信号

    def emit(self, value):
        pass  # 空的 emit，不执行任何操作

# 3. 统计滤波处理，使用 KDTree 优化
def statistical_outlier_removal_kd(las,k_neighbors=50, std_ratio=15,progress_updated=None,stop_callback=lambda *args: None):
    try:
        # 从las对象中获取points对象
        points = np.vstack((las.x, las.y, las.z)).T
    except AttributeError:
        points = las

    # 如果调用时没有受用多线程技术，创建一个空的信号发射函数
    if progress_updated is None:
        progress_updated = FakeSignal()  # 创建一个空的信号对象

    if stop_callback():  # 👈 调用中断判断函数
        return None, None

    # 发送信号：开始处理
    progress_updated.emit(10)  # 进度 10%
    # 使用 KD-tree 进行高效的最近邻查找

    # 使用 KD-tree 进行高效最近邻查找
    tree = cKDTree(points)
    progress_updated.emit(30)  # 进度 30%

    if stop_callback():  # 👈 调用中断判断函数
        return None, None
    # 批量查询 K 近邻
    # tree.query(points, k=k_neighbors + 1)：
    # 对于每个点，查询其 K 个最近邻。+1 是因为包括了点本身（即自己是最近邻之一）。
    # 返回的是每个点到其邻居的距离，以及邻居的索引。使用并行查询
    distances, _ = tree.query(points, k=k_neighbors + 1,workers=4)  # 加 1 是因为包括了点自身
    mean_distances = np.mean(distances[:, 1:], axis=1)  # 排除自己
    # k_dist = np.sum(distances, axis=1)
    progress_updated.emit(50)  # 进度 50%

    if stop_callback():  # 👈 调用中断判断函数
        return None, None
    # 计算均值和标准差
    mean = np.mean(mean_distances)
    std_dev = np.std(mean_distances)
    # mean = np.mean(k_dist)
    # std_dev = np.std(k_dist)
    progress_updated.emit(70)  # 进度 70%

    # 过滤掉远离均值太远的点
    filter_points_index = mean_distances < mean + std_ratio * std_dev
    filter_points = points[mean_distances < mean + std_ratio * std_dev]

    if stop_callback():  # 👈 调用中断判断函数
        return None,None

    progress_updated.emit(100)  # 进度 100%
    return filter_points, filter_points_index


if __name__ == '__main__':
    # 1. 打开 .las 文件并加载点云数据
    las_file = "../pointCloudData/测试数据—林业/Forest_test.las"  # 替换为你自己的文件路径
    las_data = laspy.read(las_file)
    # 获取点云的 x, y, z 坐标
    # 获取点云的 x, y, z 坐标
    # np.vstack（）垂直堆叠
    points = np.vstack([las_data.x, las_data.y, las_data.z]).T

    # 2. 创建 PyVista 点云
    point_cloud = pv.PolyData(points)

    # 4. 使用统计滤波去噪（使用 KDTree）
    filtered_points, filtered_points_index = statistical_outlier_removal_kd(las_data)


    # 创建颜色数组（绿色为正常点，红色为噪声点）
    colors = np.zeros((filtered_points_index.shape[0], 3))
    colors[~filtered_points_index] = [1, 0, 0]  # 红色代表噪声点
    colors[filtered_points_index] = [0, 1, 0]  # 绿色代表正常点

    # 创建 PyVista 点云对象并着色
    point_cloud.point_data['colors'] = colors



    # 6. 可视化点云
    plotter = pv.Plotter()

    # 颜色索引：0 = 噪声点（红色），1 = 正常点（绿色）
    color_indices = np.zeros(points.shape[0], dtype=int)
    color_indices[filtered_points_index] = 1  # 绿色代表正常点

    # 创建 Lookup Table（LUT），仅包含红色和绿色
    lut = vtk.vtkLookupTable()
    lut.SetNumberOfTableValues(2)
    lut.SetTableValue(0, 1, 0, 0, 1)  # 噪声点 = 红色 (R=1, G=0, B=0, A=1)
    lut.SetTableValue(1, 0, 1, 0, 1)  # 正常点 = 绿色 (R=0, G=1, B=0, A=1)
    lut.Build()

    # plotter.add_mesh(point_cloud, scalars="colors",clim=[0, 1], cmap=lut ,rgb=True, point_size=5)

    plotter.add_mesh(
        point_cloud, scalars="colors", clim=[0, 1], rgb=True, point_size=5
    )
    plotter.mapper.SetLookupTable(lut)  # 关键：手动设置 Lookup Table

    # plotter.add_scalar_bar(
    #     title="噪点",
    #     color='white',
    #     background_color='white',
    #     vertical=False,
    #     title_font_size=20,
    #     label_font_size=18,
    #     position_y=0.05,
    #     position_x=0.18,
    # )

    plotter.show()