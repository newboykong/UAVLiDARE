from PySide6.QtGui import QGuiApplication
from PySide6.QtWidgets import QApplication


def get_screen_size():
    # 获取应用的主屏幕
    screen = QGuiApplication.primaryScreen()
    # 获取屏幕的可用区域（不包含任务栏等元素）
    rect = screen.availableGeometry()
    print(rect.width(), rect.height())
    return rect.width(), rect.height()


def get_screen_gaps():
    app = QApplication.instance() or QApplication([])

    screens = QGuiApplication.screens()
    screen_geometries = {screen.name(): screen.geometry() for screen in screens}

    print("所有屏幕的坐标信息：")
    for name, geom in screen_geometries.items():
        print(f"{name}: {geom}")

    screen_list = list(screen_geometries.items())

    print("\n屏幕之间的距离差：")
    for i, (name1, geom1) in enumerate(screen_list):
        for j, (name2, geom2) in enumerate(screen_list):
            if i >= j:  # 避免重复计算
                continue
            if geom2.x()>geom1.width()or geom2.x()<-geom1.width():
                # 计算水平间距
                h_gap = geom2.left() - geom1.right() if geom2.left() > geom1.right() else geom1.left() - geom2.right()
                print(f"{name1} 和 {name2} 水平间距: {h_gap} 像素")
            if geom2.y()>geom1.height()or geom2.y()<-geom1.height():
                # 计算垂直间距
                v_gap = geom2.top() - geom1.bottom() if geom2.top() > geom1.bottom() else geom1.top() - geom2.bottom()
                print(f"{name1} 和 {name2}  垂直间距: {v_gap} 像素")

if __name__ == "__main__":
    get_screen_gaps()
    get_screen_size()

# 所有屏幕的坐标信息：
# N156HMA-GA1: PySide6.QtCore.QRect(0, 0, 1536, 864)
# CFORCE: PySide6.QtCore.QRect(0, 1080, 1280, 720)
#
# 屏幕之间的距离差：
# N156HMA-GA1 和 CFORCE 水平间距: -1279 像素, 垂直间距: 217 像素

class GreenParameter:
    def __init__(self, name, value):
        self.app = QApplication.instance() or QApplication([])
        self.screens = QGuiApplication.screens()
        self.screen_geometries = {screen.name(): screen.geometry() for screen in self.screens}


    def get_screen_gaps(self):
        print("\n屏幕之间的距离差：")
        for i, (name1, geom1) in enumerate(self.screen_list):
            for j, (name2, geom2) in enumerate(self.screen_list):
                if i >= j:  # 避免重复计算
                    continue
                if geom2.x() > geom1.width() or geom2.x() < -geom1.width():
                    # 计算水平间距
                    h_gap = geom2.left() - geom1.right() if geom2.left() > geom1.right() else geom1.left() - geom2.right()
                    print(f"{name1} 和 {name2} 水平间距: {h_gap} 像素")
                    return h_gap
                if geom2.y() > geom1.height() or geom2.y() < -geom1.height():
                    # 计算垂直间距
                    v_gap = geom2.top() - geom1.bottom() if geom2.top() > geom1.bottom() else geom1.top() - geom2.bottom()
                    print(f"{name1} 和 {name2}  垂直间距: {v_gap} 像素")
                    return v_gap