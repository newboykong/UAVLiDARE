import math
import laspy
import numpy as np
from osgeo import osr, gdal
gdal.UseExceptions()
from PySide6.QtCore import Signal

# 定义一个空的信号类
class FakeSignal:
    signal = Signal(int)  # 定义一个信号

    def emit(self, value):
        pass  # 空的 emit，不执行任何操作

def canopy_cover(las_file,grid_size=(5,-5),file_path=None,progress_updated=None,stop_callback=lambda *args: None):
    # 如果调用时没有受用多线程技术，创建一个空的信号发射函数
    if progress_updated is None:
        progress_updated = FakeSignal()  # 创建一个空的信号对象


    """1、读取las信息"""
    x, y, z = las_file.x, las_file.y, las_file.z
    cls = las_file.classification
    return_number = las_file.return_num
    scan_angle = las_file.scan_angle_rank
    progress_updated.emit(10)  # 进度 10%
    if stop_callback():  # 👈 调用中断判断函数
        return ""

    """2、计算栅格尺寸"""
    # 获取点云边界值
    x_max, y_max = las_file.header.max[0:2]
    x_min, y_min = las_file.header.min[0:2]
    # 设置分辨率
    pixel_width, pixel_height = grid_size[0], grid_size[1] # 分辨率
    x_origin = x_min
    y_origin= y_max
    cols = int(math.ceil((x_max - x_min) / pixel_width))
    rows = int(math.ceil((y_max - y_min) / abs(pixel_height)))
    progress_updated.emit(30)  # 进度 10%
    if stop_callback():  # 👈 调用中断判断函数
        return ""

    """3、计算点云落在哪个栅格单元"""
    # x_off_set = (x - x_origin) / pixel_width
    # x_off_set = x_off_set.astype(int)
    # y_off_set = (y - y_origin) / pixel_height
    # y_off_set = y_off_set.astype(int)
    # 将 x, y 值归一化到网格索引
    x_off_set = np.clip(((x - x_min) / (x_max - x_min) * (cols - 1)), 0, cols - 1).astype(int)
    y_off_set = np.clip(((y - y_max) / (y_min - y_max) * (rows - 1)), 0, rows - 1).astype(int)

    progress_updated.emit(50)  # 进度 10%
    if stop_callback():  # 👈 调用中断判断函数
        return ""

    """4、计算树冠覆盖率（Canopy Cover）"""
    # 预设 cc 数组（注意这里用的是 rows 在第二维）
    cc = np.zeros((cols, rows))

    # 步骤 1：筛选所有满足 return_number == 1 的点
    mask_all = (return_number == 1)
    x_all = x_off_set[mask_all]
    y_all = y_off_set[mask_all]

    # 步骤 2：再筛选 z > 2 的，也在 return_number == 1 的前提下
    mask_veg = (return_number == 1) & (z > 2)
    x_veg = x_off_set[mask_veg]
    y_veg = y_off_set[mask_veg]

    # 步骤 3：统计每个格子的总点数（ttp）和植被点数（vp）
    from collections import Counter

    all_counter = Counter(zip(x_all, y_all))
    veg_counter = Counter(zip(x_veg, y_veg))

    # 步骤 4：构造 cc 栅格
    for (i, j), ttp in all_counter.items():
        if stop_callback():  # 中断判断
            return ""
        vp = veg_counter.get((i, j), 0)
        cc[i, j] = float(vp) / float(ttp)

    progress_updated.emit(80)

    """5、可视化树冠覆盖率"""
    # import matplotlib.pyplot as plt
    # fig, ax = plt.subplots()
    # ax = plt.subplot(111)
    # cax=ax.imshow(np.array(cc), interpolation=None, cmap='viridis')
    # fig.tight_layout()
    # # 添加颜色条（图例）
    # cbar = plt.colorbar(cax, ax=ax)
    # cbar.set_label('Canopy_cover')  # 可根据实际单位改成你需要的单位
    # plt.show()
    if stop_callback():  # 👈 调用中断判断函数
        return ""
    """6、输出栅格（GeoTIFF）"""
    if file_path is not None:
        driver = gdal.GetDriverByName('GTiff')
        out_raster = driver.Create(file_path, cols, rows, 1, gdal.GDT_Float32)
        out_raster.SetGeoTransform((x_origin, pixel_width, 0, y_origin, 0, pixel_width))
        outband = out_raster.GetRasterBand(1)

        outband.WriteArray(np.transpose(cc))
        out_raster_srs = osr.SpatialReference()
        out_raster_srs.ImportFromProj4("+proj=utm +zone=10 +datum=NAD83 +units=m +no_defs")
        out_raster.SetProjection(out_raster_srs.ExportToWkt())
        outband.FlushCache()
        out_raster = None

    progress_updated.emit(100)  # 进度 10%
    return file_path


if __name__ == '__main__':
    # 读取点云文件
    file_path = "测试数据二-normalization.las"  # 修改为你的 LAS 文件路径
    las = laspy.read(file_path)
    canopy_cover(las)







