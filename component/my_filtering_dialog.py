import sys
import os
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QDialog, QApplication, QTreeWidgetItem
)

from ui.ui_filtering_dialog import Ui_Dialog as FilteringDialog
from PySide6.QtWidgets import QTreeWidgetItem
from PySide6.QtCore import Qt, Slot
from functools import partial
import re


class MyFilteringDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        # 把ui转为py文件在此接入
        self.ui = FilteringDialog()
        self.ui.setupUi(self)
        self.params=None

    def add_items(self, params_dic):
        """加载分类信息，并为每个分类创建对应的控件"""
        self.params = params_dic
        # 清空原有数据
        self.ui.file_tree_widget.clear()
        self.ui.cls_tree_widget.clear()
        self.ui.grid_size.setValue(2)
        self.ui.dh_min.setValue(0.30)
        self.ui.dh_max.setValue(25.00)
        self.ui.iterations.setValue(3)
        self.ui.s.setValue(0.30)

        self.ui.file_tree_widget.blockSignals(True)
        for name in params_dic.keys():
            item = QTreeWidgetItem(self.ui.file_tree_widget)
            item.setText(1, str(name))
            item.setFlags(item.flags() | Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)  # 允许复选
            item.setCheckState(0,  Qt.Unchecked)  # 默认未选中
        self.ui.file_tree_widget.blockSignals(False)

        self.ui.file_tree_widget.itemChanged.connect(partial(self.on_item_check_state_changed))

    def params_get(self):
        params_dic = {'filter_type': str(self.ui.filter_type.currentText()), 'grid_size': float(self.ui.grid_size.value()),
                      'dh_min': float(self.ui.dh_min.value()), 'dh_max': float(self.ui.dh_max.value()),
                      'iterations': int(self.ui.iterations.value()), 's': float(self.ui.s.value())}

        for i in range(self.ui.file_tree_widget.topLevelItemCount()):
            item = self.ui.file_tree_widget.topLevelItem(i)
            if item.checkState(0) == Qt.Checked:
                params_dic['file_name'] =str(item.text(1))

        cls_id=[]
        for i in range(self.ui.cls_tree_widget.topLevelItemCount()):
            item = self.ui.cls_tree_widget.topLevelItem(i)
            if item.checkState(0) == Qt.Checked:
                text=item.text(1)
                match = re.match(r"(\d+)", text)  # \d+ 匹配数字
                if match:
                    number = int(match.group(1))
                    cls_id.append(number)

        params_dic['cls_id']=cls_id
        return params_dic

    @Slot(QTreeWidgetItem, int)
    def on_item_check_state_changed(self, item, column):
        if column != 0:
            return

            # 如果当前项被选中
        if item.checkState(0) == Qt.Checked:
            # 遍历所有项，取消其他项的选中状态
            for i in range(self.ui.file_tree_widget.topLevelItemCount()):
                other_item = self.ui.file_tree_widget.topLevelItem(i)
                if other_item is not item:
                    other_item.setCheckState(0, Qt.Unchecked)

        self.ui.cls_tree_widget.clear()
        name=item.text(1)
        for cls_id,cls_dic in self.params[name].items():
            item = QTreeWidgetItem(self.ui.cls_tree_widget)
            item.setText(1, str(cls_id)+":"+str(cls_dic['name']))
            item.setFlags(item.flags() | Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)  # 允许复选
            item.setCheckState(0, Qt.Unchecked)  # 默认选中

    @staticmethod
    def remove_las_tif_suffix(filename):
        # 获取不带扩展名的文件名
        base, ext = os.path.splitext(filename)
        if ext.lower() in ['.las', '.tif']:
            return base
        return filename

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyFilteringDialog()
    paras={"name":{'1':{'name':"23:地面"}},
           "name2":{'2':{'name':"12:树木"}}}
    window.add_items(paras)
    window.show()
    sys.exit(app.exec())
