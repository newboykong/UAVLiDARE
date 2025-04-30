from osgeo import ogr
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from PySide6.QtWidgets import QWidget, QVBoxLayout

class VectorWindow(QWidget):
    def __init__(self,  parent=None,shapefile_path=None):
        super().__init__(parent)
        self.setWindowTitle("Shapefile 显示")
        self.setGeometry(200, 200, 800, 600)

        self.figure = Figure(figsize=(8, 6), facecolor='black')
        self.canvas = FigureCanvas(self.figure)
        self.canvas.setStyleSheet("background-color: black;")

        layout = QVBoxLayout(self)
        layout.addWidget(self.canvas)

        if shapefile_path:
            driver = ogr.GetDriverByName("ESRI Shapefile")
            datasource = driver.Open(shapefile_path, 0)
            self.vector_show(datasource)

    def vector_show(self, vector_path,title="Shapefile Map"):
        driver = ogr.GetDriverByName("ESRI Shapefile")
        datasource = driver.Open(vector_path, 0)

        if not datasource:
            print("无法打开 shapefile 文件")
            return

        layer = datasource.GetLayer()

        self.figure.clf()
        ax = self.figure.add_subplot(111)
        self.figure.patch.set_facecolor('black')
        ax.set_facecolor('black')
        ax.tick_params(colors='white')
        for spine in ax.spines.values():
            spine.set_color('white')
        ax.set_title(title, color='white')

        # 坐标范围
        min_x, max_x, min_y, max_y = float('inf'), float('-inf'), float('inf'), float('-inf')

        for feature in layer:
            geom = feature.GetGeometryRef()
            if geom is None:
                continue

            def draw_geom(g):
                nonlocal min_x, max_x, min_y, max_y
                if g.GetGeometryType() in [ogr.wkbPoint, ogr.wkbPoint25D]:
                    x, y = g.GetX(), g.GetY()
                    ax.plot(x, y, marker='o', color='cyan')
                    min_x, max_x = min(min_x, x), max(max_x, x)
                    min_y, max_y = min(min_y, y), max(max_y, y)
                elif g.GetGeometryType() in [ogr.wkbLineString, ogr.wkbLineString25D]:
                    pts = g.GetPoints()
                    xs, ys = zip(*pts)
                    ax.plot(xs, ys, color='cyan')
                    min_x, max_x = min(min_x, min(xs)), max(max_x, max(xs))
                    min_y, max_y = min(min_y, min(ys)), max(max_y, max(ys))
                elif g.GetGeometryType() in [ogr.wkbPolygon, ogr.wkbPolygon25D]:
                    for i in range(g.GetGeometryCount()):
                        ring = g.GetGeometryRef(i)
                        pts = ring.GetPoints()
                        xs, ys = zip(*pts)
                        ax.plot(xs, ys, color='cyan')
                        min_x, max_x = min(min_x, min(xs)), max(max_x, max(xs))
                        min_y, max_y = min(min_y, min(ys)), max(max_y, max(ys))
                elif g.GetGeometryType() == ogr.wkbMultiPoint:
                    for i in range(g.GetGeometryCount()):
                        draw_geom(g.GetGeometryRef(i))

            draw_geom(geom)

        if min_x < max_x and min_y < max_y:
            ax.set_xlim(min_x, max_x)
            ax.set_ylim(min_y, max_y)
        ax.set_aspect('equal', adjustable='datalim')
        self.canvas.draw()

    def clear(self):
        self.figure.clf()

if __name__ == "__main__":
    import sys
    from PySide6.QtWidgets import QApplication

    app = QApplication(sys.argv)
    viewer = VectorWindow(shapefile_path=r"D:\pointCloud\algorithms\single_wood_division.shp")
    viewer.show()
    sys.exit(app.exec())
