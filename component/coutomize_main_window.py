from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget
from PySide6.QtGui import QMouseEvent
from PySide6.QtCore import Qt
from component.resize_function import ResizableWindow
from functools import partial

GLOBAL_STATE = "normal"

class CustomWindow(object):
    def __init__(self, main_window, min_button, max_button, close_button, title_bar):
        self.main_window = main_window
        self.min_button = min_button
        self.max_button = max_button
        self.close_button = close_button
        self.title_bar = title_bar

        #################绑定三个按钮##########################
        ###########实现最大化、最小化、窗口销毁##################
        # 连接按钮事件
        self.min_button.clicked.connect(partial(self.minimize_window))
        self.max_button.clicked.connect(partial(self.maximize_window))
        self.close_button.clicked.connect(partial(self.restore_window))

        ##################解决标题栏拖动问题#######################
        self.title_bar.setMouseTracking(True)  # 启用鼠标跟踪
        # 重写title_bar的mousePressEvent函数
        self.title_bar.mousePressEvent = self.title_bar_press
        ########################################################

        #################解决主窗口调整大小问题######################
        self.resize_window = ResizableWindow(self.main_window)
        #######################################################

    #####################################################################

    def minimize_window(self):
        # 最小化窗口
        self.main_window.setWindowState(Qt.WindowMinimized)

    def maximize_window(self):
        global GLOBAL_STATE
        status = GLOBAL_STATE
        if status == "normal":
            # 最大化窗口
            self.main_window.setWindowState(Qt.WindowMaximized)
            GLOBAL_STATE = "maximized"
        elif status == "maximized":
            # 恢复窗口正常状态
            self.main_window.setWindowState(Qt.WindowNoState)
            GLOBAL_STATE = "normal"

    def restore_window(self):
        # 恢复窗口正常状态
        self.main_window.close()

    #################################################################

    def title_bar_press(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton:
            self.main_window.windowHandle().startSystemMove()
