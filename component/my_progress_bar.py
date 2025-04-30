from PySide6.QtWidgets import (QDialog)
from PySide6.QtCore import Signal
from ui.ui_progress_bar import Ui_Dialog as ProgressBar


class MyProgressBar(QDialog):
    closed = Signal()  # ✅ 自定义的信号，不是 Qt 内置的

    def __init__(self, parent=None):
        super().__init__(parent)
        # 把ui转为py文件在此接入
        self.ui = ProgressBar()
        self.ui.setupUi(self)

    def set_value(self,value):
        self.ui.progressBar.setValue(value)

    def set_window_title(self,title):
        self.setWindowTitle(title)

    def set_label(self,label):
        self.ui.label.setText(label)

    def closeEvent(self, event):
        self.closed.emit()  # 发出信号，让其他模块知道它关闭了
        super().closeEvent(event)

