import sys
import re
from functools import partial
from PySide6.QtGui import QCursor
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QDialog, QApplication, QWidget, QPushButton, QTreeWidgetItem,
    QHBoxLayout, QColorDialog
)
from ui.ui_show_by_classification import Ui_Dialog as ShowByCls


class ShowByClassification(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = ShowByCls()
        self.ui.setupUi(self)

    def add_items(self, paras_dic):
        """加载分类信息，并为每个分类创建对应的控件"""
        self.ui.treeWidget.clear()  # 清空原有数据

        for color_id, color_dict in paras_dic.items():
            item = QTreeWidgetItem(self.ui.treeWidget)
            item.setText(1, str(color_id))
            item.setText(2, color_dict["name"])
            item.setFlags(item.flags() | Qt.ItemIsUserCheckable)  # 允许复选
            item.setCheckState(0, Qt.Checked)  # 默认选中

            # 创建颜色按钮
            button = QPushButton()
            button.setMaximumWidth(30)
            button.setStyleSheet(f"background-color: {color_dict['color']};")

            # 绑定颜色选择事件（使用 partial 传递 item）
            button.clicked.connect(partial(self.pick_color, item))

            # 创建 QWidget 容器
            widget = QWidget()
            layout = QHBoxLayout(widget)
            layout.addWidget(button)
            layout.setContentsMargins(0, 0, 0, 0)  # 去掉边距
            widget.setLayout(layout)

            # 在第三列设置按钮
            self.ui.treeWidget.setItemWidget(item, 3, widget)

            # 设置文本对齐方式
            for i in range(4):
                item.setTextAlignment(i, Qt.AlignCenter)

    def paras_get(self):
        """获取分类信息，包括选中状态和颜色"""
        cls_dic = {}

        for i in range(self.ui.treeWidget.topLevelItemCount()):
            item = self.ui.treeWidget.topLevelItem(i)

            # 获取复选框状态
            selected_state = "选中" if item.checkState(0) == Qt.Checked else "未选中"

            # 获取分类 ID 和名称
            cls_id = item.text(1)
            cls_name = item.text(2)

            # 获取颜色按钮控件
            widget = self.ui.treeWidget.itemWidget(item, 3)
            button = widget.layout().itemAt(0).widget()
            color = self.get_button_background_color(button)

            cls_dic[cls_id] = {"name": cls_name, "color": color, "state": selected_state}

        return cls_dic

    def pick_color(self, item):
        """点击颜色按钮时触发颜色选择"""
        widget = self.ui.treeWidget.itemWidget(item, 3)
        button = widget.layout().itemAt(0).widget()

        color = QColorDialog.getColor()
        if color.isValid():
            button.setStyleSheet(f"background-color: {color.name()};")

    @staticmethod
    def get_button_background_color(button: QPushButton):
        """获取按钮背景颜色"""
        style = button.styleSheet()
        match = re.search(r"background-color:\s*([^;]+);", style)
        return match.group(1) if match else "未设置颜色"


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ShowByClassification()
    cls = {
        "1": {"name": "地面点", "color": "red"},
        "2": {"name": "非地面点", "color": "blue"}
    }
    window.show()
    window.add_items(cls)
    window.accepted.connect(window.paras_get)
    sys.exit(app.exec())
