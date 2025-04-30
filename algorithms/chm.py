from algorithms.dem import dem_get
from algorithms.dsm import dsm_get
import numpy as np
from osgeo import osr
from osgeo import gdal
gdal.UseExceptions()
import laspy
from PySide6.QtCore import Signal

# 定义一个空的信号类
class FakeSignal:
    signal = Signal(int)  # 定义一个信号

    def emit(self, value):
        pass  # 空的 emit，不执行任何操作

def chm_get(las_file, grid_size=(1, -1),file_path=None,progress_updated=None,stop_callback=lambda *args: None):
    # 如果调用时没有受用多线程技术，创建一个空的信号发射函数
    if progress_updated is None:
        progress_updated = FakeSignal()  # 创建一个空的信号对象
    # 获取las文件的x, y, z坐标
    points = np.vstack((las_file.x, las_file.y, las_file.z)).T
    # 获取 X 和 Y 的最大最小值
    x_min, y_min = np.min(points[:, :2], axis=0)
    x_max, y_max = np.max(points[:, :2], axis=0)
    # 获取分辨率
    pixel_width = grid_size[0]
    pixel_height = grid_size[1]
    # 计算源点，因为像素坐标从左上开始
    x_origin = x_min
    y_origin = y_max
    # 计算行列数
    cols = int(np.ceil((x_max - x_min) / grid_size[0]))
    rows = int(np.ceil((y_min - y_max) / grid_size[1]))
    progress_updated.emit(30)  # 进度 10%
    if stop_callback():  # 👈 调用中断判断函数
        return ""
    z_min_tmp = dem_get(las_file, grid_size)
    progress_updated.emit(60)  # 进度 10%
    if stop_callback():  # 👈 调用中断判断函数
        return ""
    z_max_tmp = dsm_get(las_file, grid_size)
    progress_updated.emit(90)  # 进度 10%
    if stop_callback():  # 👈 调用中断判断函数
        return ""
    chm_raster = z_max_tmp.reshape(cols, rows) - z_min_tmp.reshape(cols, rows)
    chm_index = chm_raster.flatten()
    chm_tmp = chm_index

    # # 画图查看插值后结果
    # import matplotlib.pyplot as plt
    # fig, ax = plt.subplots()
    # ax = plt.subplot(111)
    # z_reshaped = chm_tmp.reshape(rows, cols)
    # cax=ax.imshow(z_reshaped, interpolation=None, cmap='viridis')
    # plt.title("Canopy Height Model after applying IDW")
    # fig.tight_layout()
    # # 添加颜色条（图例）
    # cbar = plt.colorbar(cax, ax=ax)
    # cbar.set_label('Elevation (m)')  # 可根据实际单位改成你需要的单位
    # plt.show()
    if stop_callback():  # 👈 调用中断判断函数
        return ""
    if file_path is not None:
        # 输出成geoTIFF
        driver = gdal.GetDriverByName('GTiff')
        outRaster = driver.Create(file_path, cols, rows, 1, gdal.GDT_Float32)
        outRaster.SetGeoTransform((x_origin, pixel_width, 0, y_origin, 0, pixel_height))
        outband = outRaster.GetRasterBand(1)
        # flip arrary
        outband.WriteArray(chm_tmp.reshape(rows, cols))
        outRasterSRS = osr.SpatialReference()
        outRasterSRS.ImportFromProj4("+proj=utm +zone=10 +datum=NAD83 +units=m +no_defs")
        outRaster.SetProjection(outRasterSRS.ExportToWkt())
        outband.FlushCache()
        outRaster = None
    progress_updated.emit(100)  # 进度 10%
    return chm_tmp

if __name__ == '__main__':
    # 读取点云文件
    file_path = "E:/数据相关/PCM测试数据/测试数据二（对应菜单栏测试）.las"  # 修改为你的 LAS 文件路径
    las = laspy.read(file_path)
    chm_get(las,file_path='CHM.tif')
