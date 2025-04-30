import sys
import os
from PySide6.QtWidgets import (
    QDialog, QApplication,QFileDialog
)

from ui.ui_ectract_tree_parameters import Ui_Dialog as ExtractTreeParamDialog
from PySide6.QtWidgets import QTreeWidgetItem
from PySide6.QtCore import Qt, Slot
from functools import partial


class MyExtractTreeParamDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        # 把ui转为py文件在此接入
        self.ui = ExtractTreeParamDialog()
        self.ui.setupUi(self)
        self.params=None
        self.name= None
        self.ui.select_file_csv.clicked.connect(partial(self.file_save_csv))
        self.ui.select_file_chm.clicked.connect(partial(self.file_chm_clicked))

    def add_items(self, params_dic):
        """加载分类信息，并为每个分类创建对应的控件"""
        self.params = params_dic
        # 清空原有数据
        self.ui.chm_file_tree_widget.clear()
        self.ui.chm_file_path.clear()
        self.ui.save_file_path_csv.clear()

        self.ui.chm_file_tree_widget.blockSignals(True)
        for name in params_dic.keys():
            item = QTreeWidgetItem(self.ui.chm_file_tree_widget)
            item.setText(1, str(name))
            item.setFlags(item.flags() | Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)  # 允许复选
            item.setCheckState(0,  Qt.Unchecked)  # 默认未选中
        self.ui.chm_file_tree_widget.blockSignals(False)

        self.ui.chm_file_tree_widget.itemChanged.connect(partial(self.on_item_check_state_changed))

    def params_get(self):
        params_dic = {'chm_file_path': str(self.ui.chm_file_path.text()),
                      'save_file_path_csv':str(self.ui.save_file_path_csv.text())}

        return params_dic

    @Slot(QTreeWidgetItem, int)
    def on_item_check_state_changed(self, item, column):
        if column != 0:
            return

            # 如果当前项被选中
        if item.checkState(0) == Qt.Checked:
            # 遍历所有项，取消其他项的选中状态
            for i in range(self.ui.chm_file_tree_widget.topLevelItemCount()):
                other_item = self.ui.chm_file_tree_widget.topLevelItem(i)
                if other_item is not item:
                    other_item.setCheckState(0, Qt.Unchecked)

        self.ui.chm_file_path.setText(self.params[item.text(1)])
        self.name = item.text(1)


    def file_save_csv(self):
        # 让用户选择保存路径
        self.name=self.remove_las_tif_suffix(self.name)
        file_path, _ = QFileDialog.getSaveFileName(self, "另存为 CSV 文件", self.name + "-CSV",
                                                   "CSV 文件 (*.csv)")
        if not file_path:
            return
        self.ui.save_file_path_csv.setText(file_path)

    def file_chm_clicked(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "选择 CHM 文件", "", "CHM 文件 (*.tif)")
        if not file_path:
            return
        self.ui.chm_file_path.setText(file_path)
        self.name = os.path.basename(file_path)

    @staticmethod
    def remove_las_tif_suffix(filename):
        # 获取不带扩展名的文件名
        base, ext = os.path.splitext(filename)
        if ext.lower() in ['.las', '.tif']:
            return base
        return filename

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyExtractTreeParamDialog()
    paras={"name":{'1':{'name':"23:地面"}},
           "name2":{'2':{'name':"12:树木"}}}
    window.add_items(paras)
    window.show()
    sys.exit(app.exec())
