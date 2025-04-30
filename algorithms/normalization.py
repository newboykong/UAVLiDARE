import laspy
import numpy as np
from PySide6.QtCore import Signal
from osgeo import gdal
gdal.UseExceptions()


class FakeSignal:
    signal = Signal(int)

    def emit(self, value):
        pass


def normalization(las, dem_path, file_path=None, progress_updated=None, stop_callback=lambda *args: None,
                  handle_nan='remove', nan_value=0.0):
    """
    :param las: laspy LAS对象
    :param dem_path: DEM路径
    :param file_path: 输出LAS路径
    :param progress_updated: 信号回调
    :param stop_callback: 中断回调
    :param handle_nan: 'remove' 删除无效点；'fill' 用 nan_value 替换；默认 'remove'
    :param nan_value: 替代无效点的值（仅当 handle_nan='fill' 时有效）
    """
    if progress_updated is None:
        progress_updated = FakeSignal()

    """1、读取 LAS 点云"""
    # 获取分类信息
    cls = las.classification
    # 获取las文件的x, y, z坐标
    points = np.vstack((las.x, las.y, las.z)).T
    # 获取x,y,z坐标
    x = points[:, 0]
    y = points[:, 1]
    z = points[:, 2]
    # 获取 X 和 Y 的最大最小值
    x_min, y_min = np.min(points[:, :2], axis=0)
    x_max, y_max = np.max(points[:, :2], axis=0)

    """2、读取 DEM 到内存"""
    ds_dem = gdal.Open(dem_path)
    band = ds_dem.GetRasterBand(1)
    dem_array = band.ReadAsArray()
    transform = ds_dem.GetGeoTransform()
    x_origin, pixel_width = transform[0], transform[1]
    y_origin, pixel_height = transform[3], transform[5]
    rows, cols = dem_array.shape
    progress_updated.emit(30)

    """3、计算行列索引"""
    # col_idx = ((x - x_origin) / pixel_width).astype(int)
    # row_idx = ((y - y_origin) / pixel_height).astype(int)
    col_idx = np.clip(((x - x_min) / (x_max - x_min) * (cols - 1)), 0, cols - 1).astype(int)
    row_idx = np.clip(((y - y_max) / (y_min - y_max) * (rows - 1)), 0, rows - 1).astype(int)
    valid_mask = (0 <= row_idx) & (row_idx < rows) & (0 <= col_idx) & (col_idx < cols)
    progress_updated.emit(50)

    """4、批量获取 DEM 值"""
    point_dem = np.full_like(z, np.nan)
    point_dem[valid_mask] = dem_array[row_idx[valid_mask], col_idx[valid_mask]]
    progress_updated.emit(70)

    """5、归一化处理并处理无效值"""
    normalize_z = z - point_dem

    if handle_nan == 'fill':
        normalize_z = np.nan_to_num(normalize_z, nan=nan_value)
        keep_mask = np.ones_like(z, dtype=bool)
    else:  # remove NaN
        keep_mask = ~np.isnan(normalize_z)
        normalize_z = normalize_z[keep_mask]

    progress_updated.emit(90)

    """6、写入新 LAS 文件"""
    out_file = laspy.create(file_version=las.header.version, point_format=las.header.point_format)
    out_file.header = las.header
    out_file.header.offset = [out_file.header.offset[0], out_file.header.offset[1], 0]
    out_file.header.scale = [las.header.scale[0], las.header.scale[1], 0.001]

    # 只保留有效点
    out_file.points = las.points[keep_mask]
    out_file.z = normalize_z

    if file_path is not None:
        out_file.write(file_path)

    progress_updated.emit(100)
    return out_file


if __name__ == '__main__':
    file_path = "E:/数据相关/PCM测试数据/测试数据二（对应菜单栏测试）.las"
    las = laspy.read(file_path)

    normalization(
        las,
        dem_path="DEM.tif",
        file_path='测试数据二-normalization.las',
        handle_nan='remove'  # 或 'fill'
    )
