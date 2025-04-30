from osgeo import gdal
import numpy as np
import matplotlib.pyplot as plt
from scipy import ndimage as ndi
from skimage.segmentation import watershed
from skimage.feature import peak_local_max
from scipy.ndimage import gaussian_filter
gdal.UseExceptions()
from PySide6.QtCore import Signal
import os

# 定义一个空的信号类
class FakeSignal:
    signal = Signal(int)  # 定义一个信号

    def emit(self, value):
        pass  # 空的 emit，不执行任何操作


def single_wood_division(chm_file=None, file_path=None,file_path_shp=None,progress_updated=None,stop_callback=lambda *args: None):
    # 如果调用时没有受用多线程技术，创建一个空的信号发射函数
    if progress_updated is None:
        progress_updated = FakeSignal()  # 创建一个空的信号对象

    # 读取冠层高度模型CHM

    raster = gdal.Open(chm_file)
    band_data_raster = raster.GetRasterBand(1)


    data_raster = band_data_raster.ReadAsArray()

    # 对CHM进行高斯滤波，平滑数据
    data_raster_gau = gaussian_filter(data_raster, sigma=1)
    progress_updated.emit(10)  # 进度 10%

    # 创建与CHM相同尺寸的空 `markers`
    markers = np.zeros_like(data_raster, dtype=int)

    # 寻找CHM中的局部最大值
    local_maxi = peak_local_max(data_raster_gau, labels=None, footprint=np.ones((3, 3)), threshold_abs=0.1, exclude_border=False)
    progress_updated.emit(30)  # 进度 10%
    # 确保 `local_maxi` 不是空的
    if local_maxi.size > 0:
        markers[tuple(local_maxi.T)] = np.arange(1, len(local_maxi) + 1)

    progress_updated.emit(50)  # 进度 10%
    # 分水岭分割
    labels = watershed(-data_raster_gau, markers, mask=data_raster_gau > 5)

    # import matplotlib.pyplot as plt
    #
    # # 使用 constrained_layout 来避免 tight_layout 警告
    # fig, ax = plt.subplots(1, 3, figsize=(15, 5), constrained_layout=True)
    #
    # # 绘制 CHM
    # cax = ax[0].imshow(data_raster, cmap='viridis')
    # ax[0].set_title('CHM')
    # # 添加颜色条（图例）
    # cbar = plt.colorbar(cax, ax=ax[0])
    # cbar.set_label('CHM')  # 可根据实际单位改成你需要的单位
    #
    # # 绘制高斯滤波后的CHM
    # cax = ax[1].imshow(data_raster_gau, cmap='viridis')
    # ax[1].set_title('CHM (Gaussian Smoothed)')
    # # 添加颜色条（图例）
    # cbar = plt.colorbar(cax, ax=ax[1])
    # cbar.set_label('CHM (Gaussian Smoothed)')  # 可根据实际单位改成你需要的单位
    #
    # # 绘制分割结果
    # cax = ax[2].imshow(labels, cmap='tab20b')
    # ax[2].set_title('Segmented')
    # # 添加颜色条（图例）
    # cbar = plt.colorbar(cax, ax=ax[2])
    # cbar.set_label('Segmented')  # 可根据实际单位改成你需要的单位
    #
    # # 隐藏坐标轴
    # for a in ax:
    #     a.set_axis_off()
    #
    # # 显示图像
    # plt.show()

    if stop_callback():  # 👈 调用中断判断函数
        return None

    progress_updated.emit(80)  # 进度 10%
    if file_path is not None:
        # 储存单木分割的结果为GeoTIFF
        driver = gdal.GetDriverByName('GTiff')
        out_raster = driver.Create(
            file_path,
            raster.RasterXSize,
            raster.RasterYSize,
            1,
            gdal.GDT_Int32  # 保存为整型标签图
        )

        # 设置地理参考信息
        out_raster.SetGeoTransform(raster.GetGeoTransform())
        out_raster.SetProjection(raster.GetProjection())

        # 写入数据
        out_band = out_raster.GetRasterBand(1)
        out_band.WriteArray(labels)
        out_band.SetNoDataValue(0)  # 可选：设置背景为0的区域为无效值

        # 保存并释放资源
        out_band.FlushCache()
        out_raster = None

    if file_path_shp is not None:
        from osgeo import ogr, osr

        # 获取投影和地理变换
        geo_transform = raster.GetGeoTransform()
        projection = raster.GetProjection()

        # 创建 Shapefile 数据源
        driver = ogr.GetDriverByName("ESRI Shapefile")
        if os.path.exists(file_path_shp):
            driver.DeleteDataSource(file_path_shp)
        shapefile = driver.CreateDataSource(file_path_shp)
        srs = osr.SpatialReference()
        srs.ImportFromWkt(projection)
        layer = shapefile.CreateLayer("tree_segments", srs, ogr.wkbPolygon)

        # 添加属性字段
        field_id = ogr.FieldDefn("ID", ogr.OFTInteger)
        layer.CreateField(field_id)

        # 创建内存中的 raster 数据，作为 polygonize 的输入
        mem_driver = gdal.GetDriverByName("MEM")
        mem_raster = mem_driver.Create(
            "", raster.RasterXSize, raster.RasterYSize, 1, gdal.GDT_Int32)
        mem_raster.SetGeoTransform(raster.GetGeoTransform())
        mem_raster.SetProjection(raster.GetProjection())

        mem_band = mem_raster.GetRasterBand(1)
        mem_band.WriteArray(labels)
        mem_band.FlushCache()

        # 用 GDAL Polygonize 转为矢量
        gdal.Polygonize(
            mem_band,
            None,
            layer,
            0,  # 第0个字段是 ID
            [],
            callback=None
        )

        # 清理
        shapefile.Destroy()


    progress_updated.emit(100)  # 进度 10%
    return labels





if __name__ == '__main__':
    single_wood_division(
        chm_file='CHM.tif',
        file_path="single_wood_division.tif",
        file_path_shp="single_wood_division.shp"
    )

