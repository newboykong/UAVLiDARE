import laspy
import numpy as np
import pandas as pd
from PySide6.QtCore import Signal
from osgeo import gdal
from osgeo import osr
gdal.UseExceptions()
from algorithms.denoisisng import statistical_outlier_removal_kd
from scipy.ndimage import generic_filter
from scipy.spatial import cKDTree


# 定义一个空的信号类
class FakeSignal:
    signal = Signal(int)  # 定义一个信号

    def emit(self, value):
        pass  # 空的 emit，不执行任何操作


def dem_get(las_file, grid_size=(1, -1),file_path=None,progress_updated=None,stop_callback=lambda *args: None):
    # 如果调用时没有受用多线程技术，创建一个空的信号发射函数
    if progress_updated is None:
        progress_updated = FakeSignal()  # 创建一个空的信号对象

    # 获取分类信息
    cls = las_file.classification
    # 获取 las 文件的 x, y, z 坐标
    points = np.vstack((las_file.x, las_file.y, las_file.z)).T
    x, y, z = points[:, 0], points[:, 1], points[:, 2]

    # 获取 X 和 Y 的最大最小值
    x_min, y_min = np.min(points[:, :2], axis=0)
    x_max, y_max = np.max(points[:, :2], axis=0)

    # 获取分辨率
    pixel_width, pixel_height = grid_size

    # 计算源点和行列数
    x_origin = x_min
    y_origin = y_max
    cols = int(np.ceil((x_max - x_min) / pixel_width))
    rows = int(np.ceil((y_min - y_max) / pixel_height))

    progress_updated.emit(10)
    if stop_callback():
        print("用户中断算法")
        return

    # 将 x, y 值映射到网格索引
    x_off_set = np.clip(((x - x_min) / (x_max - x_min) * (cols - 1)), 0, cols - 1).astype(int)
    y_off_set = np.clip(((y - y_max) / (y_min - y_max) * (rows - 1)), 0, rows - 1).astype(int)

    # 构建空值填充区域
    y_index, x_index = np.meshgrid(np.arange(rows), np.arange(cols), indexing='ij')
    fill_value = np.full_like(x_index.flatten(), np.nan, dtype='double')
    filled_points = np.column_stack([x_index.flatten(), y_index.flatten(), fill_value])

    if stop_callback():
        print("用户中断算法")
        return
    progress_updated.emit(20)

    # 提取初步地面点
    z_ground = z.copy()
    if 2 in cls:
        z_ground[cls != 2] = np.nan

    # 创建 DEM 栅格用于滤波
    z_dem_grid = np.full((rows, cols), np.nan)
    z_dem_grid[y_off_set, x_off_set] = z_ground

    # 定义滤波函数（滤除突起的小树）
    def remove_spike(window):
        center = window[len(window) // 2]
        if np.isnan(center):
            return np.nan
        median = np.nanmedian(window)
        if center - median > 1.0:  # 超出中值 1 米的认为是异常
            return np.nan
        return center

    # 滤波去除异常点
    filtered_z_dem_grid = generic_filter(z_dem_grid, remove_spike, size=5, mode='nearest')

    # 扁平化后恢复为点形式
    flat_mask = ~np.isnan(filtered_z_dem_grid)
    z_ground_filtered = filtered_z_dem_grid[flat_mask]
    x_idx_filtered = x_index.flatten()[flat_mask.flatten()]
    y_idx_filtered = y_index.flatten()[flat_mask.flatten()]

    # 组合真实点和空值点
    real_points = np.column_stack([x_idx_filtered, y_idx_filtered, z_ground_filtered])
    all_points = np.vstack([real_points, filled_points])

    # 生成 DataFrame，聚合最小值
    pts = pd.DataFrame(all_points, columns=['Off_x', 'Off_y', 'z'])
    min_raster = np.asarray(
        pts.pivot_table(index='Off_y', columns='Off_x', values='z', aggfunc='min', dropna=False)
    )

    if stop_callback():
        print("用户中断算法")
        return

    progress_updated.emit(50)

    # # 画图看DEM结果
    # import matplotlib.pyplot as plt
    # fig, ax = plt.subplots()
    # ax = plt.subplot(111)
    # cax=ax.imshow(np.transpose(np.array(min_raster)), interpolation=None, cmap='viridis')
    # plt.title("Digital Elevation Model")
    # fig.tight_layout()
    # # 添加颜色条（图例）
    # cbar = plt.colorbar(cax, ax=ax)
    # cbar.set_label('Elevation (m)')  # 可根据实际单位改成你需要的单位
    # plt.show()

    """IDM插值，去除DSM中的NAN值"""
    # 计算网格中心坐标
    # x_index = x_index.flatten() * pixel_width + x_origin
    # y_index = y_index.flatten() * pixel_height + y_origin
    x_index, y_index = np.meshgrid(np.arange(cols), np.arange(rows))  # 保持原样
    x_index = x_index.flatten() * pixel_width + x_origin
    y_index = y_index.flatten() * pixel_height + y_origin

    # 二维变一维
    z_min_index = min_raster.flatten()
    z_min_tmp = z_min_index
    if stop_callback():  # 👈 调用中断判断函数
        print("用户中断算法")
        return
    # 找出 NaN 值索引
    nan_index = np.where(np.isnan(z_min_tmp))[0]
    progress_updated.emit(70)

    if len(nan_index) == 0:
        print("Warning: 没有 NaN 值，无需插值！")
    else:
        if stop_callback():
            print("用户中断算法")
            return

        # ✅ 1. 提取非空点坐标和值，用于构建 KDTree
        valid_mask_all = ~np.isnan(z_min_tmp)
        valid_coords = np.column_stack((x_index[valid_mask_all], y_index[valid_mask_all]))
        valid_values = z_min_tmp[valid_mask_all]

        # ✅ 2. 构建 KDTree，仅使用非 NaN 的点
        tree = cKDTree(valid_coords)

        # ✅ 3. 查询每个 NaN 点的最近 k 个非空邻点
        k = 100  # 你可以根据点密度调整，一般 10~50 足够
        nan_coords = np.column_stack((x_index[nan_index], y_index[nan_index]))
        dist, index = tree.query(nan_coords, k=k)

        # ✅ 4. 处理距离为 0，避免除以 0
        dist = np.where(dist == 0, 1e-6, dist)
        weights = 1.0 / dist  # 权重可改为 1 / dist ** p，p=1~2 更平滑

        # ✅ 5. 获取邻域高程值，并计算加权平均值
        if valid_values.shape[0] == 0:
            print("Warning: No valid values found.")
            return  # 或者 continue，或者用默认值，比如 z_neighbors = np.array([default_value])
        else:
            z_neighbors = valid_values[index]
        weight_sum = np.sum(weights, axis=1)
        z_idw = np.sum(weights * z_neighbors, axis=1) / np.where(weight_sum == 0, 1e-6, weight_sum)

        # ✅ 6. 插值结果填回原数组
        z_min_tmp[nan_index] = z_idw


    progress_updated.emit(80)  # 进度 80%
    if stop_callback():  # 👈 调用中断判断函数
        print("用户中断算法")
        return
    # # 画图查看插值后结果
    # import matplotlib.pyplot as plt
    # fig, ax = plt.subplots()
    # ax = plt.subplot(111)
    # z_reshaped = z_min_tmp.reshape(rows, cols)
    # cax=ax.imshow(z_reshaped, interpolation=None, cmap='viridis')
    # plt.title("Digital Elevation Model after applying IDW")
    # fig.tight_layout()
    # # 添加颜色条（图例）
    # cbar = plt.colorbar(cax, ax=ax)
    # cbar.set_label('Elevation (m)')  # 可根据实际单位改成你需要的单位
    # plt.show()

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
        # outband.WriteArray(np.transpose(z_min_tmp.reshape(cols, rows)))
        outband.WriteArray(z_min_tmp.reshape(rows, cols))
        # 创建空间参考对象
        outRasterSRS = osr.SpatialReference()
        # 使用Proj.4字符串定义投影
        # 使用 Proj.4 字符串定义投影，这里定义了 UTM 第 10 带，基准面为 NAD83，大地单位为米。
        outRasterSRS.ImportFromProj4("+proj=utm +zone=10 +datum=NAD83 +units=m +no_defs")
        outRaster.SetProjection(outRasterSRS.ExportToWkt())
        outband.FlushCache()
        outRaster = None

    progress_updated.emit(100)  # 进度 100%

    return z_min_tmp




if __name__ == '__main__':
    # 读取点云文件
    file_path = r"C:\Users\newbo\Desktop\data\Forest_test.las"  # 修改为你的 LAS 文件路径
    las = laspy.read(file_path)
    dem_get(las,file_path="DEM.tif")

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
