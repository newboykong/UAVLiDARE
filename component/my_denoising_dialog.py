import sys
import os
from PySide6.QtWidgets import (QDialog, QApplication,
                               QTreeWidget, QHeaderView)

from component.my_erro_message import MyMessage
from ui.ui_denoising_dialog import Ui_Dialog as DenoisingDialog
from functools import partial

class MyDenoisingDialog(QDialog):
    def __init__(self, parent=None):
        super(MyDenoisingDialog, self).__init__(parent)
        # 把ui转为py文件在此接入
        self.ui = DenoisingDialog()
        self.ui.setupUi(self)
        self.height()
        # self.setWindowFlags(Qt.FramelessWindowHint)  # 无边框窗口
        # self.ui.treeWidget.setHeaderLabels(["", "", ""])  # 设置列头
        self.ui.treeWidget.setColumnCount(2)  # 设置列数为2
        self.ui.treeWidget.setSelectionMode(QTreeWidget.ExtendedSelection)
        self.ui.help.clicked.connect(partial(self.help))
        # 设置列宽
        header = self.ui.treeWidget.header()
        # # 设置列宽模式为固定宽度（如果需要）
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)  # 设置第一列为固定宽度
        # header.setSectionResizeMode(1, QHeaderView.ResizeToContents)  # 设置第二列为固定宽度
        header.resizeSection(0, 60)  # 设置第一列宽度为 200 像素

    def params_get(self):
        denoising_type=self.ui.type.currentText()
        k_neighbors=self.ui.k_neighbors.text()
        std_ratio=self.ui.std_ratio.text()
        # params_dict={"k_neighbors":k_neighbors,"std_ratio":std_ratio}
        name=self.get_selected_item_info()

        return name,denoising_type,int(k_neighbors),int(std_ratio)

    def get_selected_item_info(self):
        self.ui.treeWidget.repaint()
        selected_items = self.ui.treeWidget.selectedItems()
        if selected_items:
            item = selected_items[0]  # 这里只获取第一项（如果允许多选，需要遍历）
            text_1 = item.text(1)  # 第二列文本
            # check_state = item.checkState(0)  # 获取复选框状态
            # check_state_str = "Checked" if check_state == Qt.Checked else "Unchecked"
            return text_1

    def help(self):
        message_box = MyMessage(self)
        message_box.message("""鼠标单击 → 选中一行（高亮）。
        按住 Ctrl + 点击 → 选择多个行（高亮）。
        按住 Shift + 点击 → 选中连续的多行（高亮）。""")
        message_box.setWindowTitle("帮助")
        message_box.open()

    @staticmethod
    def remove_las_tif_suffix(filename):
        # 获取不带扩展名的文件名
        base, ext = os.path.splitext(filename)
        if ext.lower() in ['.las', '.tif']:
            return base
        return filename

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyDenoisingDialog()
    window.show()
    sys.exit(app.exec())