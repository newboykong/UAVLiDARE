from PySide6.QtCore import Qt, QPoint
from PySide6.QtGui import QMouseEvent, Qt
from PySide6.QtWidgets import QApplication, QWidget
from PySide6.QtWidgets import QVBoxLayout, QPushButton, QLabel

RangeSize = 8


class ResizableWindow(QWidget):
    def __init__(self, mainWindow):
        super().__init__()

        self.main_window = mainWindow
        self.main_window._drag_position = QPoint()

        # 保存鼠标按下的初始位置和窗口大小
        self.main_window._resizing = False
        self.main_window._resize_direction = None
        self.mouse_pos = None

        self.main_window.mousePressEvent = self.mousePressEvent
        self.main_window.mouseMoveEvent = self.mouseMoveEvent
        self.main_window.mouseReleaseEvent = self.mouseReleaseEvent
        self.main_window.resizeEvent = self.resizeEvent
        self.main_window.last_mouse_pos = None
        self.main_window.start_geometry = None

        self.main_window.setMouseTracking(True)
        for widget in self.main_window.findChildren(QWidget):  # 让所有子控件都能监听鼠标
            widget.setMouseTracking(True)


        self.main_window.installEventFilter(self)  # 安装事件过滤器

    def mousePressEvent(self, event):
        self.mouse_pos = event.globalPosition().toPoint()
        self.main_window._drag_position = event.globalPosition().toPoint()
        self.main_window.start_geometry = self.main_window.geometry()
        """鼠标按下事件，判断是否点击到边界区域"""
        if event.button() == Qt.LeftButton and self.is_change_size():
            self.main_window._resizing = True

    def mouseMoveEvent(self, event):
        ####################设置鼠标样式#####################
        rect = self.main_window.geometry()
        mouse_pos = event.globalPosition().toPoint()
        # print(mouse_pos)
        delta = mouse_pos - self.main_window._drag_position
        geo = self.main_window.start_geometry
        width = None
        height = None
        if geo:
            width = geo.width()
            height = geo.height()

        self.mouse_pos = event.globalPosition().toPoint()
        if rect.right() - RangeSize <= self.mouse_pos.x() <= rect.right() and rect.top() <= self.mouse_pos.y() <= rect.bottom() - RangeSize:
            QApplication.setOverrideCursor(Qt.SizeHorCursor)
        elif rect.bottom() - RangeSize <= self.mouse_pos.y() <= rect.bottom() and rect.left() <= self.mouse_pos.x() <= rect.right() - RangeSize:
            QApplication.setOverrideCursor(Qt.SizeVerCursor)
        elif rect.right() - RangeSize <= self.mouse_pos.x() <= rect.right() and rect.bottom() - RangeSize <= self.mouse_pos.y() <= rect.bottom():
            QApplication.setOverrideCursor(Qt.SizeFDiagCursor)
        else:
            QApplication.setOverrideCursor(Qt.ArrowCursor)


        """鼠标移动事件，调整窗口大小"""
        if self.main_window._resizing and event.buttons() == Qt.LeftButton:

            if self.main_window._resize_direction == 'right':
                # 右边界拖动
                self.main_window.resize(width + delta.x(), height)

            # elif self.main_window._resize_direction == 'left':
            #     # 左边界拖动
            #     self.main_window.resize(width-delta.x(), height)
            #     self.main_window.move(geo.x()+delta.x(), geo.y())

            elif self.main_window._resize_direction == 'bottom':
                # 底边界拖动
                self.main_window.resize(width, height + delta.y())

            elif self.main_window._resize_direction == 'bottom-right':
                # 右下角拖动
                self.main_window.resize(width + delta.x(), height + delta.y())

    def mouseReleaseEvent(self, event: QMouseEvent):
        """鼠标释放事件，停止调整大小"""
        self.main_window._resizing = False
        self.main_window._resize_direction = None
        event.accept()

    def is_change_size(self):
        rect = self.main_window.geometry()
        # 检查是否在右边界、底边界、右下角
        if rect.right() - RangeSize <= self.mouse_pos.x() <= rect.right() and rect.top() <= self.mouse_pos.y() <= rect.bottom() - RangeSize:
            self.main_window._resize_direction = 'right'  # 在右边界
            # print("right")
            return True

        # if rect.left() - RangeSize <= self.mouse_pos.x() <= rect.right()+ RangeSize and rect.top() <= self.mouse_pos.y() <= rect.bottom() - RangeSize:
        #     self.main_window._resize_direction = 'left'  # 在右边界
        #     # print("right")
        #     return True

        elif rect.bottom() - RangeSize <= self.mouse_pos.y() <= rect.bottom() and rect.left() <= self.mouse_pos.x() <= rect.right() - RangeSize:
            self.main_window._resize_direction = 'bottom'  # 在底边界
            # print("bottom")
            return True

        elif rect.right() - RangeSize <= self.mouse_pos.x() <= rect.right() and rect.bottom() - RangeSize <= self.mouse_pos.y() <= rect.bottom():
            self.main_window._resize_direction = 'bottom-right'  # 在右下角
            # print("bottom-right")
            return True
        # else:
        #     self.main_window._resize_direction = None

        return False

    # def eventFilter(self, obj, event):
    #     if event.type() == QEvent.MouseMove:
    #         # print(f"鼠标移动到: {event.globalX()}, {event.globalY()}")  # 获取全局坐标
    #         # return True
    #         pass
    #     return super().eventFilter(obj, event)


class Window(QWidget):
    def __init__(self):
        super().__init__()

        # 设置窗口初始大小
        self.resize(400, 300)

        # 设置无边框窗口
        self.setWindowFlags(Qt.FramelessWindowHint)

        # 创建一个简单的标题栏
        self.title_bar = QLabel("自定义标题栏", self)
        self.title_bar.setAlignment(Qt.AlignCenter)

        # 布局
        layout = QVBoxLayout(self)
        layout.addWidget(self.title_bar)
        content_button = QPushButton("这是一个按钮", self)
        layout.addWidget(content_button)

        resize_function = ResizableWindow(self)


if __name__ == '__main__':
    # 运行应用程序
    app = QApplication([])
    window = Window()
    window.show()
    app.exec()
