import laspy
import numpy as np
import pandas as pd
from PySide6.QtCore import Signal
from scipy import spatial
from osgeo import osr
from osgeo import gdal
gdal.UseExceptions()


# import warnings
# warnings.simplefilter("ignore", RuntimeWarning)

# 定义一个空的信号类
class FakeSignal:
    signal = Signal(int)  # 定义一个信号

    def emit(self, value):
        pass  # 空的 emit，不执行任何操作


def dsm_get(las_file, grid_size=(1, -1),file_path=None,progress_updated=None,stop_callback=lambda *args: None):
    # 如果调用时没有受用多线程技术，创建一个空的信号发射函数
    if progress_updated is None:
        progress_updated = FakeSignal()  # 创建一个空的信号对象

    # 如果调用时没有受用多线程技术，创建一个空的信号发射函数
    if progress_updated is None:
        progress_updated = FakeSignal()  # 创建一个空的信号对象

    # 获取分类信息
    cls = las_file.classification
    # 获取las文件的x, y, z坐标
    points = np.vstack((las_file.x, las_file.y, las_file.z)).T
    # 获取x,y,z坐标
    x = points[:, 0]
    y = points[:, 1]
    z = points[:, 2]
    # 获取 X 和 Y 的最大最小值
    x_min, y_min = np.min(points[:, :2], axis=0)
    x_max, y_max = np.max(points[:, :2], axis=0)
    # 获取回波编号
    return_number = las_file.return_num
    # 获取分辨率
    pixel_width = grid_size[0]
    pixel_height = grid_size[1]
    # 计算源点，因为像素坐标从左上开始
    x_origin = x_min
    y_origin = y_max
    # 计算行列数
    cols = int(np.ceil((x_max - x_min) / grid_size[0]))
    rows = int(np.ceil((y_min - y_max) / grid_size[1]))
    # 发送信号：开始处理
    progress_updated.emit(10)  # 进度 10%
    if stop_callback():  # 👈 调用中断判断函数
        return
    # 将 x, y 值归一化到网格索引
    x_off_set = np.clip(((x - x_min) / (x_max - x_min) * (cols - 1)), 0, cols - 1).astype(int)
    y_off_set = np.clip(((y - y_max) / (y_min - y_max) * (rows - 1)), 0, rows - 1).astype(int)
    # 将z填为空值，以便后面插值做准备
    x_index, y_index = np.meshgrid(np.arange(cols), np.arange(rows))
    fill_value = np.full_like(x_index.flatten(), np.nan, dtype='double')
    filled_points = np.column_stack([x_index.flatten(), y_index.flatten(), fill_value])
    if stop_callback():  # 👈 调用中断判断函数
        return
    progress_updated.emit(20)  # 进度 20%
    # 获取z值，筛选出地面点
    z_ground = z.copy()
    z_ground[return_number != 1] = np.nan
    # 找出每个网格中的最小值，保留网格的空值
    real_points = np.column_stack([x_off_set, y_off_set, z_ground])
    points = np.vstack([real_points, filled_points])
    pts = pd.DataFrame(points, columns=['Off_x', 'Off_y', 'z'])
    max_raster = np.asarray(
        pts.pivot_table(index='Off_y', columns='Off_x', values='z', aggfunc='max', dropna=False)
    )

    progress_updated.emit(50)  # 进度 50%

    # # 画图看DEM结果
    # import matplotlib.pyplot as plt
    # fig, ax = plt.subplots()
    # ax = plt.subplot(111)
    # cax=ax.imshow(np.transpose(np.array(max_raster)), interpolation=None, cmap='viridis')
    # plt.title("Digital Surface Model")
    # fig.tight_layout()
    # # 添加颜色条（图例）
    # cbar = plt.colorbar(cax, ax=ax)
    # cbar.set_label('Elevation (m)')  # 可根据实际单位改成你需要的单位
    # plt.show()

    """IDM插值，去除DSM中的NAN值"""
    # 计算网格中心坐标
    x_index, y_index = np.meshgrid(np.arange(cols), np.arange(rows))  # 保持原样
    x_index = x_index.flatten() * pixel_width + x_origin
    y_index = y_index.flatten() * pixel_height + y_origin

    # 二维转一维
    z_max_tmp = max_raster.flatten()

    if stop_callback():  # 👈 判断是否中断
        return

    # 查找 NaN 索引
    nan_index = np.where(np.isnan(z_max_tmp))[0]
    progress_updated.emit(70)  # 进度更新

    if nan_index.size == 0:
        return

    # 构建 KD 树
    valid_coords = np.column_stack((x_index, y_index))
    tree = spatial.cKDTree(valid_coords)

    # 邻域数
    k = 50

    # 修正 nan_index 超出索引范围
    nan_index = nan_index[nan_index < valid_coords.shape[0]]
    if nan_index.size == 0:
        return

    if stop_callback():
        return

    # 查找邻域
    dist, idx = tree.query(valid_coords[nan_index], k=k + 1)  # 包含自身
    dist, idx = dist[:, 1:], idx[:, 1:]  # 去掉自身

    # 距离处理，避免除以 0
    dist = np.where(dist == 0, 1e-6, dist)
    weights = 1.0 / dist ** 2

    # 获取邻域高程值
    z_neighbors = z_max_tmp[idx]

    # 屏蔽无效点
    valid_mask = ~np.isnan(z_neighbors)
    weights[~valid_mask] = 0
    z_neighbors[~valid_mask] = 0

    # 加权平均插值
    weight_sum = np.sum(weights, axis=1)
    with np.errstate(invalid='ignore', divide='ignore'):
        z_idw = np.sum(weights * z_neighbors, axis=1) / weight_sum

    # 插值质量控制
    valid_counts = np.sum(valid_mask, axis=1)
    z_idw[valid_counts < 5] = np.nan

    # 写回原数组
    z_max_tmp[nan_index] = z_idw

    progress_updated.emit(80)  # 进度 80%

    # # 画图查看插值后结果
    # import matplotlib.pyplot as plt
    # fig, ax = plt.subplots()
    # ax = plt.subplot(111)
    # z_reshaped = z_max_tmp.reshape(rows, cols)
    # cax=ax.imshow(z_reshaped, interpolation=None, cmap='viridis')
    # plt.title("Digital Surface Model after applying IDW")
    # fig.tight_layout()
    # # 添加颜色条（图例）
    # cbar = plt.colorbar(cax, ax=ax)
    # cbar.set_label('Elevation (m)')  # 可根据实际单位改成你需要的单位
    # plt.show()
    if stop_callback():  # 👈 调用中断判断函数
        return
    if file_path is not None:
        # 输出成geoTIFF
        # 创建GDAL驱动
        driver = gdal.GetDriverByName('GTiff')
        # 这里的“1”：指定栅格波段数量（这里是单波段）
        outRaster = driver.Create(file_path, cols, rows, 1, gdal.GDT_Float32)
        # 设置地理变换信息
        outRaster.SetGeoTransform((x_origin, pixel_width, 0, y_origin, 0, pixel_height))
        # 获取第一个波段
        outband = outRaster.GetRasterBand(1)
        # 写入数据
        outband.WriteArray(z_max_tmp.reshape(rows, cols))
        # 创建空间参考对象
        outRasterSRS = osr.SpatialReference()
        # 使用Proj.4字符串定义投影
        # 使用 Proj.4 字符串定义投影，这里定义了 UTM 第 10 带，基准面为 NAD83，大地单位为米。
        outRasterSRS.ImportFromProj4("+proj=utm +zone=10 +datum=NAD83 +units=m +no_defs")
        outRaster.SetProjection(outRasterSRS.ExportToWkt())
        outband.FlushCache()
        outRaster = None

    progress_updated.emit(100)  # 进度 100%

    return z_max_tmp




if __name__ == '__main__':
    # 读取点云文件
    file_path = "E:/数据相关/PCM测试数据/测试数据二（对应菜单栏测试）.las"  # 修改为你的 LAS 文件路径
    las = laspy.read(file_path)
    dsm_get(las)

    # # 输出带你云属性
    # point_attribute(las)
    #
    # count_classifications(las)
    #
    # # 进行 PMF 滤波，提取地面点
    # # pmf_filter(las)
    #
    # # 可视化点云数据
    # visualize_points(las)
    #
    # count_classifications(las)
