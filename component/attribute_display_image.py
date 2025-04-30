import sys

from PySide6.QtWidgets import (QApplication, QWidget, QTreeWidget, QTreeWidgetItem,
                               QVBoxLayout, QPushButton, QHBoxLayout)


class AttributeDisplayImage(QWidget):
    def __init__(self, dict=None):
        super().__init__()
        self.current_cls = None
        self.dict = dict
        # 创建 QTreeWidget 控件
        self.tree_widget = QTreeWidget(self)
        # self.tree_widget.setHeaderHidden(True)
        self.tree_widget.setHeaderLabels(["属性项", "属性值"])
        self.tree_widget.setColumnCount(2)  # 设置列数为2

        # 设置 QTreeWidget 样式，添加描边和边框
        self.tree_widget.setStyleSheet("""
                    QTreeWidget {
                        border: 0.2px solid white; /* 设置描边 */
                        border-radius: 5px; /* 设置圆角 */
                    }

                    QTreeWidget::item {
                        padding: 5px;

                    }

                """)

        # 添加根节点
        self.name = QTreeWidgetItem(self.tree_widget)
        self.name.setText(0, "名称")  # 第一列
        self.name.setText(1, "")  # 第二列

        # 添加根节点
        self.type = QTreeWidgetItem(self.tree_widget)
        self.type.setText(0, "类型")  # 第一列
        self.type.setText(1, "")  # 第二列

        # 添加根节点
        self.file = QTreeWidgetItem(self.tree_widget)
        self.file.setText(0, "文件")  # 第一列
        self.file.setText(1, "")  # 第二列

        # 添加根节点
        self.bands = QTreeWidgetItem(self.tree_widget)
        self.bands.setText(0, "波段数")  # 第一列
        self.bands.setText(1, "")  # 第二列

        # 添加根节点
        self.rows = QTreeWidgetItem(self.tree_widget)
        self.rows.setText(0, "行数")  # 第一列
        self.rows.setText(1, "")  # 第二列

        # 添加根节点
        self.cols = QTreeWidgetItem(self.tree_widget)
        self.cols.setText(0, "列数")  # 第一列
        self.cols.setText(1, "")  # 第二列

        # 添加根节点
        self.origin_x = QTreeWidgetItem(self.tree_widget)
        self.origin_x.setText(0, "x-源点")  # 第一列
        self.origin_x.setText(1, "")  # 第二列

        # 添加根节点
        self.origin_y = QTreeWidgetItem(self.tree_widget)
        self.origin_y.setText(0, "y-源点")  # 第一列
        self.origin_y.setText(1, "")  # 第二列

        # 添加根节点
        self.pixel_width = QTreeWidgetItem(self.tree_widget)
        self.pixel_width.setText(0, "像素宽")  # 第一列
        self.pixel_width.setText(1, "")  # 第二列

        # 添加根节点
        self.pixel_height = QTreeWidgetItem(self.tree_widget)
        self.pixel_height.setText(0, "像素高")  # 第一列
        self.pixel_height.setText(1, "")  # 第二列

        # 添加根节点
        self.box = QTreeWidgetItem(self.tree_widget)
        self.box.setText(0, "包围盒大小")  # 第一列

        # 添加子节点
        self.min_x = QTreeWidgetItem(self.box)
        self.min_x.setText(0, "最小值-x")  # 第一列
        self.min_x.setText(1, "")  # 第二列

        # 添加子节点
        self.min_y = QTreeWidgetItem(self.box)
        self.min_y.setText(0, "最小值-y")  # 第一列
        self.min_y.setText(1, "")  # 第二列

        # 添加子节点
        self.min_z = QTreeWidgetItem(self.box)
        self.min_z.setText(0, "最小值-z")  # 第一列
        self.min_z.setText(1, "")  # 第二列

        # 添加子节点
        self.max_x = QTreeWidgetItem(self.box)
        self.max_x.setText(0, "最大值-x")  # 第一列
        self.max_x.setText(1, "")  # 第二列

        # 添加子节点
        self.max_y = QTreeWidgetItem(self.box)
        self.max_y.setText(0, "最大值-y")  # 第一列
        self.max_y.setText(1, "")  # 第二列

        # 添加子节点
        self.max_z = QTreeWidgetItem(self.box)
        self.max_z.setText(0, "最大值-z")  # 第一列
        self.max_z.setText(1, "")  # 第二列

        # 展开所有节点
        self.tree_widget.expandAll()

        # 设置列宽
        # header = self.tree_widget.header()
        # # 设置列宽模式为固定宽度（如果需要）
        # header.setSectionResizeMode(0, QHeaderView.ResizeToContents)  # 设置第一列为固定宽度
        # header.setSectionResizeMode(1, QHeaderView.ResizeToContents)  # 设置第一列为固定宽度

        # 创建布局并将 QTreeWidget 添加到布局
        layout = QVBoxLayout(self)
        layout.addWidget(self.tree_widget)  # 将 self.tree_widget 添加到布局中

        # 设置窗口尺寸
        self.setWindowTitle("QTreeWidget with Multiple Columns")
        self.setGeometry(100, 100, 700, 500)

    def attributes_show(self, attributes=None):
        if attributes is None:
            attributes = {"file_name": "", "file_type": "", "file_path": "", "bands": "", "rows": "",
                          "cols": "", "origin_x":"","origin_y":"","pixel_width":"","pixel_height":"","min_x": "",
                          "min_y": "", "min_z": "", "max_x": "", "max_y": "", "max_z": ""}
        self.name.setText(1, attributes.get("file_name"))
        self.type.setText(1, attributes.get("file_type"))
        self.file.setText(1, attributes.get("file_path"))
        self.bands.setText(1, attributes.get("bands"))
        self.rows.setText(1, attributes.get("rows"))
        self.cols.setText(1, attributes.get("cols"))
        self.origin_x.setText(1, attributes.get("origin_x"))
        self.origin_y.setText(1, attributes.get("origin_y"))
        self.pixel_width.setText(1, attributes.get("pixel_width"))
        self.pixel_height.setText(1, attributes.get("pixel_height"))
        self.min_x.setText(1, attributes.get("min_x"))
        self.min_y.setText(1, attributes.get("min_y"))
        self.min_z.setText(1, attributes.get("min_z"))
        self.max_x.setText(1, attributes.get("max_x"))
        self.max_y.setText(1, attributes.get("max_y"))
        self.max_z.setText(1, attributes.get("max_z"))

        # 自动调整列宽以适应内容
        for column in range(self.tree_widget.columnCount()):
            self.tree_widget.resizeColumnToContents(column)



if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = AttributeDisplayImage()
    window.show()
    sys.exit(app.exec())
