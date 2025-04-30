import sys
import os
from PySide6.QtWidgets import (
    QDialog, QApplication,QFileDialog
)

from ui.ui_normalization_dialog import  Ui_Dialog as NormalizationDialog
from PySide6.QtWidgets import QTreeWidgetItem
from PySide6.QtCore import Qt, Slot
from functools import partial



class MyNormalizationDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        # 把ui转为py文件在此接入
        self.ui = NormalizationDialog()
        self.ui.setupUi(self)
        self.params=None
        self.name = None
        self.ui.select_dem.clicked.connect(partial(self.select_dem))
        self.ui.select_save_file.clicked.connect(partial(self.save))

    def add_items(self, params_point_cloud,params_image):
        """加载分类信息，并为每个分类创建对应的控件"""
        self.params_point_cloud = params_point_cloud
        self.params_image = params_image
        # 清空原有数据
        self.ui.file_tree_widget.clear()
        self.ui.dem_tree_widget.clear()
        self.ui.file_path_dem.clear()
        self.ui.file_path_save.clear()

        self.ui.file_tree_widget.blockSignals(True)
        for name in params_point_cloud.keys():
            item = QTreeWidgetItem(self.ui.file_tree_widget)
            item.setText(1, str(name))
            item.setFlags(item.flags() | Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)  # 允许复选
            item.setCheckState(0,  Qt.Unchecked)  # 默认未选中
        self.ui.file_tree_widget.blockSignals(False)

        self.ui.dem_tree_widget.blockSignals(True)
        for name in params_image.keys():
            item = QTreeWidgetItem(self.ui.dem_tree_widget)
            item.setText(1, str(name))
            item.setFlags(item.flags() | Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)  # 允许复选
            item.setCheckState(0, Qt.Unchecked)  # 默认未选中
        self.ui.dem_tree_widget.blockSignals(False)

        self.ui.file_tree_widget.itemChanged.connect(partial(self.on_item_check_state_changed))
        self.ui.dem_tree_widget.itemChanged.connect(partial(self.on_item_check_state_changed_dem))

    def params_get(self):
        params_dic = {'file_path_dem': str(self.ui.file_path_dem.text()),'file_path_save':str(self.ui.file_path_save.text())}

        for i in range(self.ui.file_tree_widget.topLevelItemCount()):
            item = self.ui.file_tree_widget.topLevelItem(i)
            if item.checkState(0) == Qt.Checked:
                params_dic['file_name'] =str(item.text(1))

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

        self.name = item.text(1)

    def on_item_check_state_changed_dem(self,item,column):
        if column != 0:
            return

            # 如果当前项被选中
        if item.checkState(0) == Qt.Checked:
            # 遍历所有项，取消其他项的选中状态
            for i in range(self.ui.dem_tree_widget.topLevelItemCount()):
                other_item = self.ui.dem_tree_widget.topLevelItem(i)
                if other_item is not item:
                    other_item.setCheckState(0, Qt.Unchecked)

        self.name = item.text(1)
        self.ui.file_path_dem.setText(self.params_image[self.name ])

    def select_dem(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "选择 DEM 文件", "", "DEM 文件 (*.tif)")
        if not file_path:
            return
        self.ui.file_path_dem.setText(file_path)


    def save(self):
        # 让用户选择保存路径
        self.name=self.remove_las_tif_suffix(self.name)
        file_path, _ = QFileDialog.getSaveFileName(self, "另存为 las 文件", self.name + "-normalization", "las 文件 (*.las)")
        if not file_path:
            return
        self.ui.file_path_save.setText(file_path)

    @staticmethod
    def remove_las_tif_suffix(filename):
        # 获取不带扩展名的文件名
        base, ext = os.path.splitext(filename)
        if ext.lower() in ['.las', '.tif']:
            return base
        return filename



if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyNormalizationDialog()
    paras={"name":{'1':{'name':"23:地面"}},
           "name2":{'2':{'name':"12:树木"}}}
    window.add_items(paras)
    window.show()
    sys.exit(app.exec())