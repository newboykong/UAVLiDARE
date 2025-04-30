import math
import laspy
import numpy as np
from osgeo import gdal
from osgeo import osr
gdal.UseExceptions()
from PySide6.QtCore import Signal
from collections import defaultdict

# 定义一个空的信号类
class FakeSignal:
    signal = Signal(int)  # 定义一个信号
    def emit(self, value):
        pass  # 空的 emit，不执行任何操作


def gp_and_lai(las_file,grid_size=(5,-5),file_path=None,progress_updated=None,stop_callback=lambda *args: None):
    # 如果调用时没有受用多线程技术，创建一个空的信号发射函数
    if progress_updated is None:
        progress_updated = FakeSignal()  # 创建一个空的信号对象

    """1、读取数据"""
    # 获取las文件的x, y, z坐标
    points = np.vstack((las_file.x, las_file.y, las_file.z)).T
    # 获取x,y,z坐标
    x = points[:, 0]
    y = points[:, 1]
    z = points[:, 2]
    cls = las_file.classification
    return_number = las_file.return_num
    scan_angle = las_file.scan_angle_rank

    progress_updated.emit(20)  # 进度 20%

    """2、设置分辨率和计算影像的范围"""
    # 获取 X 和 Y 的最大最小值
    x_min, y_min = np.min(points[:, :2], axis=0)
    x_max, y_max = np.max(points[:, :2], axis=0)
    # 分辨率
    pixel_width, pixel_height = grid_size[0], grid_size[1]  # 分辨率

    progress_updated.emit(40)  # 进度 20%
    if stop_callback():  # 👈 调用中断判断函数
        return None
    """3、计算图像的行数和列数"""
    x_origin = x_min
    y_origin = y_max

    cols = int(math.ceil((x_max - x_min) / pixel_width))
    rows = int(math.ceil((y_max - y_min) / abs(pixel_height)))

    """4、计算栅格偏移量"""
    # x_off_set = (x - x_origin) / pixel_width
    # x_off_set = x_off_set.astype(int)
    # y_off_set = (y - y_origin) / pixel_height
    # y_off_set = y_off_set.astype(int)
    # 将 x, y 值归一化到网格索引
    x_off_set = np.clip(((x - x_min) / (x_max - x_min) * (cols - 1)), 0, cols - 1).astype(int)
    y_off_set = np.clip(((y - y_max) / (y_min - y_max) * (rows - 1)), 0, rows - 1).astype(int)

    progress_updated.emit(60)  # 进度 20%

    """5、初始化Gap Fraction和LAI数组"""
    gp = np.zeros((cols, rows))
    lai = np.zeros((cols, rows))

    """6、计算Gap Fraction和LAI"""
    cell_dict = defaultdict(list)

    for idx in range(len(x_off_set)):
        i = x_off_set[idx]
        j = y_off_set[idx]
        cell_dict[(i, j)].append(idx)

    # 遍历有效格子，进行 Gap Fraction 和 LAI 计算
    for (i, j), indices in cell_dict.items():
        if stop_callback():
            return None

        indices = np.array(indices)
        ttp = len(indices)
        if ttp == 0:
            continue

        z_cell = z[indices]
        angle_cell = scan_angle[indices]

        vp = np.sum(z_cell > 2)
        gp_val = 1 - float(vp) / float(ttp)
        gp[i, j] = gp_val

        if gp_val > 0:
            angle_mean = np.mean(np.abs(angle_cell))
            lai[i, j] = -1 * np.cos(np.deg2rad(angle_mean)) * np.log(gp_val) / 0.5

    progress_updated.emit(80)
    """7、可视化结果"""
    # import matplotlib.pyplot as plt
    # fig, ax = plt.subplots()
    # ax = plt.subplot(111)
    # cax=ax.imshow(np.array(gp), interpolation=None, cmap='viridis')
    # fig.tight_layout()
    # # 添加颜色条（图例）
    # cbar = plt.colorbar(cax, ax=ax)
    # cbar.set_label('Gap fraction')  # 可根据实际单位改成你需要的单位
    # plt.show()
    #
    # fig, ax = plt.subplots()
    # ax = plt.subplot(111)
    # cax=ax.imshow(np.array(lai), interpolation=None, cmap='viridis')
    # fig.tight_layout()
    # # 添加颜色条（图例）
    # cbar = plt.colorbar(cax, ax=ax)
    # cbar.set_label('lAI')  # 可根据实际单位改成你需要的单位
    # plt.show()

    """8、输出GeoTIFF文件"""
    if file_path is not None:
        # 输出为geoTIFF文件
        driver = gdal.GetDriverByName('GTiff')
        out_raster = driver.Create(file_path['gp'], cols, rows, 1, gdal.GDT_Float32)
        out_raster.SetGeoTransform((x_origin, pixel_width, 0, y_origin, 0, pixel_height))
        outband = out_raster.GetRasterBand(1)
        outband.WriteArray(np.transpose(gp))
        out_raster_srs = osr.SpatialReference()
        out_raster_srs.ImportFromProj4("+proj=utm +zone=10 +datum=NAD83 +units=m +no_defs")
        out_raster.SetProjection(out_raster_srs.ExportToWkt())
        outband.FlushCache()
        out_raster = None

        # 输出为geoTIFF文件
        driver = gdal.GetDriverByName('GTiff')
        out_raster = driver.Create(file_path['lai'], cols, rows, 1, gdal.GDT_Float32)
        out_raster.SetGeoTransform((x_origin, pixel_width, 0, y_origin, 0, pixel_height))
        outband = out_raster.GetRasterBand(1)
        outband.WriteArray(np.transpose(lai))
        out_raster_srs = osr.SpatialReference()
        out_raster_srs.ImportFromProj4("+proj=utm +zone=10 +datum=NAD83 +units=m +no_defs")
        out_raster.SetProjection(out_raster_srs.ExportToWkt())
        outband.FlushCache()
        out_raster = None
    progress_updated.emit(100)  # 进度 20%

    return file_path

if __name__ == '__main__':
    # 读取点云文件
    file_path = "测试数据二-normalization.las"  # 修改为你的 LAS 文件路径
    las = laspy.read(file_path)
    gp_and_lai(las)











