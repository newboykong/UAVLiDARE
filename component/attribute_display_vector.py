import sys

from PySide6.QtWidgets import (QApplication, QWidget, QTreeWidget, QTreeWidgetItem,
                               QVBoxLayout, QPushButton, QHBoxLayout)


class AttributeDisplayVector(QWidget):
    def __init__(self, dict=None):
        super().__init__()
        self.dict = dict

        self.tree_widget = QTreeWidget(self)
        self.tree_widget.setHeaderLabels(["属性项", "属性值"])
        self.tree_widget.setColumnCount(2)
        self.tree_widget.setStyleSheet("""
            QTreeWidget {
                border: 0.2px solid white;
                border-radius: 5px;
            }
            QTreeWidget::item {
                padding: 5px;
            }
        """)

        # 文件信息
        self.name = QTreeWidgetItem(self.tree_widget)
        self.name.setText(0, "名称")

        self.type = QTreeWidgetItem(self.tree_widget)
        self.type.setText(0, "类型")

        self.path = QTreeWidgetItem(self.tree_widget)
        self.path.setText(0, "路径")

        # 要素信息
        self.feature_count = QTreeWidgetItem(self.tree_widget)
        self.feature_count.setText(0, "要素数量")

        self.geometry_type = QTreeWidgetItem(self.tree_widget)
        self.geometry_type.setText(0, "几何类型")

        self.has_z = QTreeWidgetItem(self.tree_widget)
        self.has_z.setText(0, "是否含Z值")

        # 字段名
        self.fields = QTreeWidgetItem(self.tree_widget)
        self.fields.setText(0, "字段名")

        # 空间范围
        self.box = QTreeWidgetItem(self.tree_widget)
        self.box.setText(0, "包围盒")

        self.min_x = QTreeWidgetItem(self.box)
        self.min_x.setText(0, "最小X")

        self.min_y = QTreeWidgetItem(self.box)
        self.min_y.setText(0, "最小Y")

        self.max_x = QTreeWidgetItem(self.box)
        self.max_x.setText(0, "最大X")

        self.max_y = QTreeWidgetItem(self.box)
        self.max_y.setText(0, "最大Y")

        self.crs = QTreeWidgetItem(self.tree_widget)
        self.crs.setText(0, "坐标参考系")

        self.tree_widget.expandAll()

        layout = QVBoxLayout(self)
        layout.addWidget(self.tree_widget)
        self.setWindowTitle("矢量图层属性")
        self.setGeometry(200, 200, 600, 500)

    def attributes_show(self, attributes=None):
        if attributes is None:
            attributes={}

        self.name.setText(1, attributes.get("file_name", ""))
        self.type.setText(1, attributes.get("file_type", ""))
        self.path.setText(1, attributes.get("file_path", ""))
        self.feature_count.setText(1, str(attributes.get("feature_count", "")))
        self.geometry_type.setText(1, attributes.get("geometry_type", ""))
        self.has_z.setText(1, str(attributes.get("has_z", "")))

        # 字段名显示为逗号分隔
        fields = attributes.get("field_names", [])
        self.fields.setText(1, ", ".join(fields))

        self.min_x.setText(1, attributes.get("min_x", ""))
        self.min_y.setText(1, attributes.get("min_y", ""))
        self.max_x.setText(1, attributes.get("max_x", ""))
        self.max_y.setText(1, attributes.get("max_y", ""))

        self.crs.setText(1, attributes.get("crs", ""))

        # 自动调整列宽以适应内容
        for column in range(self.tree_widget.columnCount()):
            self.tree_widget.resizeColumnToContents(column)



if __name__ == "__main__":
    app = QApplication(sys.argv)
    test_data = {
        "file_name": "example.shp",
        "file_path": "/data/example.shp",
        "file_type": "*.shap",
        "feature_count": 42,
        "geometry_type": "Polygon",
        "has_z": False,
        "field_names": ["ID", "Name", "Type"],
        "min_x": "100.5",
        "min_y": "200.5",
        "max_x": "150.5",
        "max_y": "250.5",
        "crs": "EPSG:4326"
    }
    w = AttributeDisplayVector()
    w.attributes_show(test_data)
    w.show()
    sys.exit(app.exec())

