import sys


from osgeo import gdal
gdal.UseExceptions()

from matplotlib.figure import Figure
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas

from matplotlib import gridspec

from PySide6.QtWidgets import QApplication, QVBoxLayout, QWidget



class ImageWindow(QWidget):
    def __init__(self, parent=None,file_path=None):
        super().__init__(parent)
        self.setWindowTitle("Image show")
        self.setGeometry(100, 100, 800, 600)

        self.layout = QVBoxLayout(self)

        self.figure = Figure(figsize=(8, 6), facecolor='black')
        self.canvas = FigureCanvas(self.figure)
        self.canvas.setStyleSheet("background-color: black;")  # Qt 层设置黑色背景

        self.layout.addWidget(self.canvas)
        # 确保对象有效后再添加
        if hasattr(self, 'canvas') and self.layout is not None:
            self.layout.addWidget(self.canvas)
        else:
            raise RuntimeError("Failed to initialize canvas or layout")

        if file_path is not None:
            if file_path:
                self.image_show(file_path)
            else:
                print("无法打开 DEM 文件")

    def image_show(self, dem_path, title="DEM Elevation Map"):
        dem_data = gdal.Open(dem_path)
        band = dem_data.GetRasterBand(1)
        array = band.ReadAsArray()

        self.figure.clf()

        # 使用 gridspec 分布图像和 colorbar
        spec = gridspec.GridSpec(ncols=10, nrows=1, figure=self.figure)
        ax = self.figure.add_subplot(spec[0:9])      # 90% 图像区域
        cax = self.figure.add_subplot(spec[9])       # 10% colorbar 区域

        # 绘图
        im = ax.imshow(array, cmap='viridis')

        # 设置黑底白字
        self.figure.patch.set_facecolor('black')
        ax.set_facecolor('black')
        ax.tick_params(colors='white')
        for spine in ax.spines.values():
            spine.set_color('white')
        ax.set_title(title, color='white')

        # 添加 colorbar 并设置白色文字
        cbar = self.figure.colorbar(im, cax=cax)
        cbar.ax.yaxis.label.set_color('white')
        cbar.ax.tick_params(colors='white')

        self.canvas.draw()

    def clear(self):
        self.figure.clear()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ImageWindow(file_path=r"D:\pointCloud\algorithms\DEM.tif")
    window.show()
    sys.exit(app.exec())
