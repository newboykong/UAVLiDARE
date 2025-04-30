import sys

from PySide6.QtWidgets import (QApplication, QWidget, QTreeWidget, QTreeWidgetItem,
                               QVBoxLayout, QPushButton, QHBoxLayout)


class AttributeDisplayPointCloud(QWidget):
    def __init__(self,dict=None):
        super().__init__()
        self.current_cls = None
        self.dict=dict
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
        self.number = QTreeWidgetItem(self.tree_widget)
        self.number.setText(0, "点数量")  # 第一列
        self.number.setText(1, "")  # 第二列

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

        # 添加根节点
        self.center = QTreeWidgetItem(self.tree_widget)
        self.center.setText(0, "几何中心")  # 第一列

        self.center_x = QTreeWidgetItem(self.center)
        self.center_x.setText(0, "中心点-x")  # 第一列
        self.center_x.setText(1, "")  # 第二列

        self.center_y = QTreeWidgetItem(self.center)
        self.center_y.setText(0, "中心点-y")  # 第一列
        self.center_y.setText(1, "")  # 第二列

        self.center_z = QTreeWidgetItem(self.center)
        self.center_z.setText(0, "中心点-z")  # 第一列
        self.center_z.setText(1, "")  # 第二列

        # 添加根节点
        self.point_show_way = QTreeWidgetItem(self.tree_widget)
        self.point_show_way.setText(0, "渲染方式")  # 第一列

        # 添加根节点
        self.point_size = QTreeWidgetItem(self.tree_widget)
        self.point_size.setText(0, "点云尺寸")  # 第一列

        # 添加根节点
        self.classification = QTreeWidgetItem(self.tree_widget)
        self.classification.setText(0, "分类信息")  # 第一列

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
            attributes = {"file_name": "", "file_type": "", "file_path": "", "num_points": "", "min_x": "",
                          "min_y": "", "min_z": "", "max_x": "", "max_y": "", "max_z": "", "center_x": "",
                          "center_y": "", "center_z": "", "classification": {},"point_show_way": "","point_size": ""}
        self.name.setText(1,attributes.get("file_name"))
        self.type.setText(1,attributes.get("file_type"))
        self.file.setText(1,attributes.get("file_path"))
        self.number.setText(1,attributes.get("num_points"))
        self.min_x.setText(1,attributes.get("min_x"))
        self.min_y.setText(1,attributes.get("min_y"))
        self.min_z.setText(1,attributes.get("min_z"))
        self.max_x.setText(1,attributes.get("max_x"))
        self.max_y.setText(1,attributes.get("max_y"))
        self.max_z.setText(1,attributes.get("max_z"))
        self.center_x.setText(1,attributes.get("center_x"))
        self.center_y.setText(1,attributes.get("center_y"))
        self.center_z.setText(1,attributes.get("center_z"))
        self.point_show_way.setText(1,attributes.get("point_show_way"))
        self.point_size.setText(1,str(attributes.get("point_size")))

        # 删除上一次的分类的所有根节点
        self.classification.takeChildren()
        # 获取分类信息
        cls=attributes["classification"]
        if len(cls)>=1:
            for color_id,color_dict in cls.items():
                self.current_cls=QTreeWidgetItem(self.classification)

                # 创建按钮
                button = QPushButton(f"{color_dict['num']}")
                button.setStyleSheet(f"background-color: {color_dict['color']};")
                # 创建一个 QWidget 容器
                widget = QWidget()
                widget.setMinimumWidth(70)
                layout = QHBoxLayout(widget)
                layout.addWidget(button)
                layout.setContentsMargins(0, 0, 0, 0)  # 去掉边距
                widget.setLayout(layout)
                # 在第二列设置按钮
                self.tree_widget.setItemWidget(self.current_cls,1, widget)
                self.current_cls.setText(0,f"{color_id}: "+color_dict["name"])

        # 自动调整列宽以适应内容
        for column in range(self.tree_widget.columnCount()):
            self.tree_widget.resizeColumnToContents(column)




if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = AttributeDisplayPointCloud()
    window.show()
    sys.exit(app.exec())
