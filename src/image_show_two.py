import sys
import os
import hashlib
import numpy as np
from osgeo import gdal
import matplotlib.pyplot as plt
from PySide6.QtGui import QImage, QPixmap
from PySide6.QtWidgets import QApplication, QLabel, QVBoxLayout, QWidget, QScrollArea
from PySide6.QtCore import Qt
import matplotlib
matplotlib.use('Agg')  # 使用无界面的后端
import tempfile
gdal.UseExceptions()

# 创建缓存目录
CACHE_DIR = os.path.join(tempfile.gettempdir(), "dem_cache")
os.makedirs(CACHE_DIR, exist_ok=True)

def get_hash_key(path):
    return hashlib.md5(path.encode('utf-8')).hexdigest()

def dem_to_png(dem_data, save_path, title="DEM Elevation Map"):
    band = dem_data.GetRasterBand(1)
    array = band.ReadAsArray()

    fig, ax = plt.subplots(figsize=(8, 6), dpi=100)
    fig.patch.set_facecolor('black')

    cax = ax.imshow(array, interpolation=None, cmap='viridis')
    cbar = plt.colorbar(cax, ax=ax)
    cbar.set_label('Elevation (m)')
    cbar.ax.tick_params(colors='white')
    cbar.outline.set_edgecolor('white')
    for tick_label in cbar.ax.get_yticklabels():
        tick_label.set_color('white')

    ax.set_facecolor('black')
    ax.tick_params(colors='white')
    ax.set_title(title, color='white')

    fig.savefig(save_path, format='png', bbox_inches='tight', pad_inches=0.1)
    plt.close(fig)


class ImageWindow(QWidget):
    def __init__(self, parent=None, file_path=None):
        super().__init__(parent)
        self.setWindowTitle("DEM 显示")
        self.setGeometry(100, 100, 800, 600)
        self.setStyleSheet("background-color: black;")

        # 创建滚动区域
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

        if file_path:
            self.image_show(file_path)

    def image_show(self, file_path, title="DEM Elevation Map"):
        self.label.clear()

        cache_key = get_hash_key(file_path)
        cached_png_path = os.path.join(CACHE_DIR, f"{cache_key}.png")

        if not os.path.exists(cached_png_path):
            dem_data = gdal.Open(file_path)
            if dem_data is None:
                raise Exception(f"无法打开 DEM 文件: {file_path}")
            dem_to_png(dem_data, cached_png_path, title=title)

        image = QImage(cached_png_path)
        self.label.setPixmap(QPixmap.fromImage(image))


    def clear(self):
        self.label.clear()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ImageWindow(file_path=r"D:\pointCloud\algorithms\DEM.tif")
    window.show()
    sys.exit(app.exec())
