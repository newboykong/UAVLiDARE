import sys

from PySide6.QtWidgets import (QDialog, QApplication,
                               QWidget, QPushButton)

from ui.ui_error_message import Ui_Dialog as ErrorMessage
from functools import partial

################自定义的信息报错窗口#####################

class MyMessage(QDialog):
    def __init__(self, parent=None):
        super(MyMessage, self).__init__(parent)
        # 把ui转为py文件在此接入
        self.ui = ErrorMessage()
        self.ui.setupUi(self)

    def message(self, text):
        self.ui.message.setText(text)



#######################测试代码##########################

class MyWidget(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setWindowTitle("QDialog")
        self.resize(600, 400)
        self.setup_ui()

    def setup_ui(self) -> None:
        """设置界面"""

        # 设置对话框
        # dialog = QDialog(self)
        dialog = MyMessage(self)
        dialog.setWindowTitle("这是一个对话框")
        dialog.resize(300, 200)


        # 在主窗口上弹出对话框
        test_btn = QPushButton("弹出对话框", self)
        test_btn.move(200, 200)
        test_btn.clicked.connect(partial(dialog.open) )  # type: ignore

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyWidget()
    window.show()
    sys.exit(app.exec())