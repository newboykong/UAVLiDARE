from osgeo import gdal
import numpy as np
from algorithms.single_wood_division import single_wood_division
gdal.UseExceptions()
from PySide6.QtCore import Signal

# 定义一个空的信号类
class FakeSignal:
    signal = Signal(int)  # 定义一个信号

    def emit(self, value):
        pass  # 空的 emit，不执行任何操作


import csv

def extract_tree_parameters(chm_file, csv_path=None,progress_updated=None,stop_callback=lambda *args: None):
    # 如果调用时没有受用多线程技术，创建一个空的信号发射函数
    if progress_updated is None:
        progress_updated = FakeSignal()  # 创建一个空的信号对象

    progress_updated.emit(10)  # 进度 10%
    labels=single_wood_division(chm_file=chm_file)
    # 读取冠层高度模型CHM
    if stop_callback():  # 👈 调用中断判断函数
        return None
    progress_updated.emit(50)  # 进度 10%
    raster = gdal.Open(chm_file)
    band_data_raster = raster.GetRasterBand(1)

    chm_data = band_data_raster.ReadAsArray()
    # 获取唯一标签（每棵树一个标签）
    unique_labels = np.unique(labels)
    tree_parameters = []
    progress_updated.emit(60)  # 进度 10%
    for label in unique_labels:
        if label == 0:  # 跳过背景
            continue

        tree_mask = (labels == label)
        tree_height = chm_data[tree_mask]

        tree_max_height = np.max(tree_height)
        tree_min_height = np.min(tree_height)
        tree_height_diff = tree_max_height - tree_min_height

        # 更精确的计算树冠宽度（计算边界框宽度）
        coords = np.column_stack(np.where(tree_mask))
        min_x, max_x = np.min(coords[:, 1]), np.max(coords[:, 1])
        min_y, max_y = np.min(coords[:, 0]), np.max(coords[:, 0])
        tree_width = max(max_x - min_x, max_y - min_y)
        progress_updated.emit(80)  # 进度 10%
        # 简单估算体积（以像素个数作为体积指标）
        tree_volume = np.sum(tree_mask)
        if stop_callback():  # 👈 调用中断判断函数
            return None
        tree_parameters.append({
            "ID": int(label),
            "Tree_Max_Height": float(tree_max_height),
            "Tree_Height_Diff": float(tree_height_diff),
            "Tree_Width": float(tree_width),
            "Tree_Volume": int(tree_volume)
        })

    # 如果指定了输出路径，保存为 CSV
    if csv_path is not None:
        with open(csv_path, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=["ID", "Tree_Max_Height", "Tree_Height_Diff", "Tree_Width", "Tree_Volume"])
            writer.writeheader()
            for param in tree_parameters:
                writer.writerow(param)

    progress_updated.emit(100)  # 进度 10%
    return tree_parameters




if __name__ == '__main__':
    extract_tree_parameters(
        chm_file='CHM.tif',
        csv_path="my.csv"
    )

