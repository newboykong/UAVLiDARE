import sys
import os
import tempfile
import hashlib

from osgeo import ogr, gdal
gdal.UseExceptions()

import matplotlib
matplotlib.use('Agg')  # 非交互后端
import matplotlib.pyplot as plt

from PySide6.QtGui import QImage, QPixmap
from PySide6.QtWidgets import QApplication, QLabel, QVBoxLayout, QWidget, QScrollArea
from PySide6.QtCore import Qt


# 哈希函数用于唯一识别 shapefile 文件路径
def get_hash_key(path):
    return hashlib.md5(path.encode('utf-8')).hexdigest()


# 绘制 Shapefile 到 PNG 文件
def shapefile_to_png(shp_dataset, save_path, title="Shapefile Display"):
    layer = shp_dataset.GetLayer()
    fig, ax = plt.subplots(figsize=(8, 6), dpi=100)
    fig.patch.set_facecolor('black')
    ax.set_facecolor('black')

    for feature in layer:
        geometry = feature.GetGeometryRef()
        geom_type = geometry.GetGeometryName()

        if geom_type == 'POINT':
            x, y = geometry.GetX(), geometry.GetY()
            ax.plot(x, y, 'go')
        elif geom_type == 'LINESTRING':
            points = geometry.GetPoints()
            xs, ys = zip(*points)
            ax.plot(xs, ys, color='lime', linewidth=1)
        elif geom_type == 'POLYGON':
            ring = geometry.GetGeometryRef(0)
            points = ring.GetPoints()
            xs, ys = zip(*points)
            ax.fill(xs, ys, color='cyan', alpha=0.5)
        else:
            print(f"跳过不支持的几何类型: {geom_type}")
            continue

    ax.set_title(title, color="white")
    ax.tick_params(colors="white")
    for spine in ax.spines.values():
        spine.set_edgecolor('white')

    plt.axis("equal")
    plt.tight_layout()
    plt.savefig(save_path, format="png", bbox_inches="tight", pad_inches=0.1)
    plt.close(fig)


# 主窗口
class VectorWindow(QWidget):
    def __init__(self, parent=None, shp_path=None):
        super().__init__(parent)
        self.setWindowTitle("Shapefile 显示")
        self.setGeometry(100, 100, 800, 600)
        self.setStyleSheet("background-color: black;")

        self.cache_dir = os.path.join(tempfile.gettempdir(), "shp_cache")
        os.makedirs(self.cache_dir, exist_ok=True)

        # 滚动区域
        scroll_area = QScrollArea(self)
        scroll_area.setWidgetResizable(True)
        scroll_area.setAlignment(Qt.AlignCenter)

        self.label = QLabel()
        self.label.setStyleSheet("background-color: black;")
        self.label.setScaledContents(False)
        self.label.setAlignment(Qt.AlignCenter)

        scroll_area.setWidget(self.label)
        layout = QVBoxLayout(self)
        layout.addWidget(scroll_area)

        if shp_path:
            self.vector_show(shp_path)

    def vector_show(self, shp_path, title="Shapefile Display"):
        self.label.clear()

        # 获取缓存 PNG 路径
        cache_key = get_hash_key(shp_path)
        cached_png_path = os.path.join(self.cache_dir, f"{cache_key}.png")

        # 如果 PNG 不存在则生成
        if not os.path.exists(cached_png_path):
            driver = ogr.GetDriverByName("ESRI Shapefile")
            datasource = driver.Open(shp_path, 0)
            if not datasource:
                raise Exception(f"无法打开文件: {shp_path}")
            shapefile_to_png(datasource, cached_png_path, title)

        # 显示图像
        image = QImage(cached_png_path)
        self.label.setPixmap(QPixmap.fromImage(image))

    def clear(self):
        self.label.clear()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = VectorWindow(shp_path=r"D:\pointCloud\algorithms\single_wood_division.shp")
    window.show()
    sys.exit(app.exec())
