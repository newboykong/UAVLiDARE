import sys
from osgeo import gdal

from component.my_extract_tree_parameters_dialog import MyExtractTreeParamDialog

gdal.UseExceptions()
###################################################################
from functools import partial
###################################################################
# import open3d as o3d
# import win32gui
###################################################################
from PySide6.QtCore import Qt, QEvent
from PySide6.QtWidgets import (QMainWindow,QToolButton,
                               QApplication, QTreeWidgetItem,QMenu,
                               QHeaderView)

################################################################
from component.my_denoising_dialog import MyDenoisingDialog
from component.my_filtering_dialog import MyFilteringDialog
from component.my_dem_dialog import MyDemDialog
from component.my_dsm_dialog import MyDsmDialog
from component.my_chm_dialog import MyChmDialog
from component.my_normalization_dialog import MyNormalizationDialog
from component.my_canopy_cover_dialog import MyCanopyCoverDialog
from component.my_gp_and_lai_dialog import MyGpAndLaiDialog
from component.my_single_wood_division_dialog import MySingleWoodDialog
from component.my_extract_tree_parameters_dialog import MyExtractTreeParamDialog

from component.animated_widget import AnimatedWidth
from component.coutomize_main_window import CustomWindow
from component.attribute_display_point_cloud import AttributeDisplayPointCloud
from component.attribute_display_image import  AttributeDisplayImage
from component.attribute_display_vector import  AttributeDisplayVector
from component.my_progress_bar import MyProgressBar
###################################################################
from ui.ui_main_window import Ui_MainWindow as MainWindow
# from open3d_show import Open3dWindow
from pyvista_show import PyvistaWindow
# from image_show import ImageWindow
from image_show_two import ImageWindow
# from vector_show import VectorWindow
from vector_show_two import VectorWindow

from PySide6.QtGui import QAction
from component.show_by_classification import ShowByClassification


class MyMainWindow(QMainWindow):
    def __init__(self):
        super(MyMainWindow, self).__init__()

        ############################一些基础配置设置ui,窗口位置大小等############################
        self.ui = MainWindow()
        self.ui.setupUi(self)
        # 设置窗口初始状态：无边框窗口
        self.setWindowFlags(Qt.FramelessWindowHint)  # 无边框窗口
        # self.setWindowFlags(Qt.WindowStaysOnTopHint)  # 始终在最前面显示（可以选择注释掉切换）
        self.resize(1100, 750)
        self.move(190, 20)
        ##################################################################################


        ##################################################################################
        ################################为窗口添加动画效果和标题栏的拖动#########################
        ##################################################################################

        # 侧边栏动画
        self.sidebar_animator = AnimatedWidth(
            self.ui.leftMenuContainer,
            43, 110, 500,
            self.ui.menu_show
        )

        # 资源管理栏动画
        self.sidebar_animator1 = AnimatedWidth(
            self.ui.resourceContainer,
            0, 200, 400,
            self.ui.centerClose,
            self.ui.pointCloudCover,
            self.ui.imageCover,
            self.ui.vectorCover,
        )

        # 属性显示栏动画
        self.sidebar_animator2 = AnimatedWidth(
            self.ui.attributeContainer,
            0, 220, 400,
            self.ui.attribute_close,
            self.ui.attribute_show,
        )


        ############################################################################
        #############################切换资源管理界面的控件##############################
        ############################################################################

        self.ui.pointCloudCover.clicked.connect(partial(self.switch_point))
        self.ui.imageCover.clicked.connect(partial(self.switch_image))
        self.ui.vectorCover.clicked.connect(partial(self.switch_vector))
        self.view_state=""

        ##################################################################################
        ##########################将显示点云的窗口嵌入到pyside6上###############################
        ##################################################################################
        self.pyvista_view = PyvistaWindow(self)
        self.ui.point_cloud_view_layout.addWidget(self.pyvista_view)

        self.image_view = ImageWindow(self)
        self.ui.image_view_layout.addWidget(self.image_view)

        self.vector_view = VectorWindow(self)
        self.ui.vector_view_layout.addWidget(self.vector_view)
        ######################## 弃用 #######################################
        # self.open3d_view = Open3dWindow("../pointCloudData/测试数据—林业/Forest_test.las")
        # self.open3d_view = Open3dWindow()
        # self.ui.point_view_layout.addWidget(self.open3d_view)
        #######################################################################

        ########################################################################
        #################################添加对话框###############################
        ########################################################################

        self.denoising_dialog=MyDenoisingDialog()
        self.filtering_dialog=MyFilteringDialog()
        self.dem_dialog=MyDemDialog()
        self.dsm_dialog=MyDsmDialog()
        self.chm_dialog=MyChmDialog()
        self.normalization_dialog=MyNormalizationDialog()
        self.canopy_cover_dialog=MyCanopyCoverDialog()
        self.gp_and_lai_dialog=MyGpAndLaiDialog()
        self.single_wood_dialog=MySingleWoodDialog()
        self.extract_tree_param_dialog=MyExtractTreeParamDialog()

        self.progress_bar_denoising = MyProgressBar(self)
        self.progress_bar_filter = MyProgressBar(self)
        self.progress_bar_normalization = MyProgressBar(self)
        self.progress_bar_dem = MyProgressBar(self)
        self.progress_bar_dsm = MyProgressBar(self)
        self.progress_bar_chm = MyProgressBar(self)
        self.progress_bar_canopy = MyProgressBar(self)
        self.progress_bar_gp_and_lai = MyProgressBar(self)
        self.progress_bar_single = MyProgressBar(self)
        self.progress_bar_extract = MyProgressBar(self)

        self.show_by_cls_dialog = ShowByClassification()

        #########################自定义主窗口的基本问题###########################
        ###########################################################################
        self.custom_window = CustomWindow(self, self.ui.minimize_window_button, self.ui.maximize_window_button,
                                          self.ui.close_window_button, self.ui.headContainer)

        ################################属性显示窗口#####################################
        ##################################################################################
        self.attribute_display_point_cloud = AttributeDisplayPointCloud(self)
        self.attribute_display_point_cloud.show()
        self.ui.points_attribute_layout.addWidget(self.attribute_display_point_cloud)

        self.attribute_display_image = AttributeDisplayImage(self)
        self.attribute_display_image.show()
        self.ui.image_attribute_layout.addWidget(self.attribute_display_image)

        self.attribute_display_vector = AttributeDisplayVector(self)
        self.attribute_display_vector.show()
        self.ui.vector_attribute_layout.addWidget(self.attribute_display_vector)
        #####################################################################################
        self.add_action()
        ###############################################################################

        point_header = self.ui.point_cloud_tree_widget.header()
        # # 设置列宽模式为固定宽度（如果需要）
        point_header.setSectionResizeMode(0, QHeaderView.ResizeToContents)  # 设置第一列为固定宽度
        point_header.setSectionResizeMode(1, QHeaderView.ResizeToContents)  # 设置第二列为固定宽度

        image_header = self.ui.image_tree_widget.header()
        # # 设置列宽模式为固定宽度（如果需要）
        image_header.setSectionResizeMode(0, QHeaderView.ResizeToContents)  # 设置第一列为固定宽度
        image_header.setSectionResizeMode(1, QHeaderView.ResizeToContents)  # 设置第二列为固定宽度

        vector_header = self.ui.vector_tree_widget.header()
        # # 设置列宽模式为固定宽度（如果需要）
        vector_header.setSectionResizeMode(0, QHeaderView.ResizeToContents)  # 设置第一列为固定宽度
        vector_header.setSectionResizeMode(1, QHeaderView.ResizeToContents)  # 设置第二列为固定宽度
        #########################################################################

    def switch_point(self):
        try:
            if self.ui.point_cloud_resource and self.ui.stackedWidget.indexOf(self.ui.point_cloud_resource) != -1:
                self.ui.stackedWidget.setCurrentWidget(self.ui.point_cloud_resource)
            if self.ui.point_cloud_view and self.ui.view_stacked_widget.indexOf(self.ui.point_cloud_view) != -1:
                self.ui.view_stacked_widget.setCurrentWidget(self.ui.point_cloud_view)
            if self.ui.point_cloud_attribute and self.ui.attribute_stacked_widget.indexOf(
                    self.ui.point_cloud_attribute) != -1:
                self.ui.attribute_stacked_widget.setCurrentWidget(self.ui.point_cloud_attribute)
        except Exception as e:
            print("切换点云层出错：", e)

        self.ui.pointCloudCover.setStyleSheet("background-color: #015371;border-radius: 10px;padding: 5px")
        self.ui.imageCover.setStyleSheet("background-color:transparent;border-radius: 10px;padding: 5px")
        self.ui.vectorCover.setStyleSheet("background-color: transparent;border-radius: 10px;padding: 5px")
        self.view_state = "点云层"

    def switch_image(self):
        try:
            if self.ui.image_resource and self.ui.stackedWidget.indexOf(self.ui.image_resource) != -1:
                self.ui.stackedWidget.setCurrentWidget(self.ui.image_resource)
            if self.ui.image_view and self.ui.view_stacked_widget.indexOf(self.ui.image_view) != -1:
                self.ui.view_stacked_widget.setCurrentWidget(self.ui.image_view)
            if self.ui.image_attribute and self.ui.attribute_stacked_widget.indexOf(self.ui.image_attribute) != -1:
                self.ui.attribute_stacked_widget.setCurrentWidget(self.ui.image_attribute)
        except Exception as e:
            print("切换影像层出错：", e)

        self.ui.pointCloudCover.setStyleSheet("background-color:transparent;border-radius: 10px;padding: 5px")
        self.ui.imageCover.setStyleSheet("background-color: #015371;border-radius: 10px;padding: 5px")
        self.ui.vectorCover.setStyleSheet("background-color: transparent;border-radius: 10px;padding: 5px")
        self.view_state = "影像层"

    def switch_vector(self):
        try:
            # 注意拼写：原来是 self.ui.vector_rsource，这里更正为 vector_resource
            if self.ui.vector_resource and self.ui.stackedWidget.indexOf(self.ui.vector_resource) != -1:
                self.ui.stackedWidget.setCurrentWidget(self.ui.vector_resource)
            if self.ui.vector_view and self.ui.view_stacked_widget.indexOf(self.ui.vector_view) != -1:
                self.ui.view_stacked_widget.setCurrentWidget(self.ui.vector_view)
            if self.ui.vector_attribute and self.ui.attribute_stacked_widget.indexOf(self.ui.vector_attribute) != -1:
                self.ui.attribute_stacked_widget.setCurrentWidget(self.ui.vector_attribute)
        except Exception as e:
            print("切换矢量层出错：", e)

        self.ui.pointCloudCover.setStyleSheet("background-color:transparent;border-radius: 10px;padding: 5px")
        self.ui.imageCover.setStyleSheet("background-color:transparent;border-radius: 10px;padding: 5px")
        self.ui.vectorCover.setStyleSheet("background-color: #015371;border-radius: 10px;padding: 5px")
        self.view_state = "矢量层"

    def item_creat(self, top, text, tool_tip):
        # 为treewidget创建节点
        item = QTreeWidgetItem(top)
        item.setText(0, text)
        item.setToolTip(0, tool_tip)
        return item

    def add_action(self):
        # 创建多个 QAction，使用 & 来添加下划线
        self.open_action = QAction("打开文件", self)  # &1 让 "1" 下划线
        self.save_action = QAction("另存为", self)  # &2 让 "2" 下划线
        self.remove_action = QAction("移除文件", self)  # &3 让 "3" 下划线
        # self.remove_action.triggered.connect(self.on_action3_triggered)
        # 将多个 QAction 添加到菜单中
        self.data_file_menu = QMenu(self)
        self.data_file_menu.addAction(self.open_action)
        self.data_file_menu.addAction(self.save_action)
        self.data_file_menu.addSeparator()  # 添加横线分隔
        self.data_file_menu.addAction(self.remove_action)
        # 设置为悬浮时弹出菜单
        self.ui.file.setMenu(self.data_file_menu)
        self.ui.file.setPopupMode(QToolButton.InstantPopup)  # 设置为鼠标悬浮时弹出菜单



        # 创建多个 QAction，使用 & 来添加下划线
        self.denoising_action = QAction("点云去噪", self)  # &1 让 "1" 下划线
        self.filtering_action = QAction("点云滤波", self)  # &2 让 "2" 下划线
        self.normalization_action = QAction("点云归一化", self)  # &3 让 "3" 下划线
        self.dem_action = QAction("DEM", self)  # &3 让 "3" 下划线
        self.dsm_action = QAction("DSM", self)  # &3 让 "3" 下划线
        self.chm_action = QAction("CHM", self)  # &3 让 "3" 下划线
        self.tif_to_las_action = QAction("tif转las", self)  # &3 让 "3" 下划线
        # self.remove_action.triggered.connect(self.on_action3_triggered)
        # 将多个 QAction 添加到菜单中
        self.data_processing_menu = QMenu(self)
        self.data_processing_menu.addAction(self.denoising_action)
        self.data_processing_menu.addAction(self.filtering_action)
        self.data_processing_menu.addAction(self.normalization_action)
        self.data_processing_menu.addSeparator()  # 添加横线分隔
        self.data_processing_menu.addAction(self.dem_action)
        self.data_processing_menu.addAction(self.dsm_action)
        self.data_processing_menu.addAction(self.chm_action)
        self.data_processing_menu.addSeparator()  # 添加横线分隔
        self.data_processing_menu.addAction(self.tif_to_las_action)


        # 设置为悬浮时弹出菜单
        self.ui.processing.setMenu(self.data_processing_menu)
        self.ui.processing.setPopupMode(QToolButton.InstantPopup)  # 设置为鼠标悬浮时弹出菜单

        # 创建多个 QAction，使用 & 来添加下划线
        self.canopy_cover_action = QAction("植被覆盖度", self)  # &1 让 "1" 下划线
        self.gp_and_lai_action = QAction("空隙率和叶面积", self)  # &2 让 "2" 下划线
        self.single_wood_division_action = QAction("单木分割", self)  # &3 让 "3" 下划线
        self.extract_tree_param_action = QAction("单木结构参数提取", self)  # &3 让 "3" 下划线
        # 将多个 QAction 添加到菜单中
        self.forestry_parameter_extraction_menu = QMenu(self)
        self.forestry_parameter_extraction_menu.addAction(self.canopy_cover_action)
        self.forestry_parameter_extraction_menu.addAction(self.gp_and_lai_action)
        self.forestry_parameter_extraction_menu.addAction(self.single_wood_division_action)
        self.forestry_parameter_extraction_menu.addAction( self.extract_tree_param_action)
        # 设置为悬浮时弹出菜单
        self.ui.forestry_parameter_extraction.setMenu(self.forestry_parameter_extraction_menu)
        self.ui.forestry_parameter_extraction.setPopupMode(QToolButton.InstantPopup)  # 设置为鼠标悬浮时弹出菜单

    def showEvent(self, event):
        # 强制重新绘制窗口以解决最小化后恢复的延迟
        # self.ui.point_cloud_tree_widget.update()
        if self.windowState() == Qt.WindowFullScreen:
            self.setWindowState(Qt.WindowNoState)
            self.setWindowState(Qt.WindowMaximized)
            return
        self.resize(self.width()-10, self.height()-10)
        self.resize(self.width()+10, self.height()+10)
        print("jkljl")
        super().showEvent(event)



if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyMainWindow()
    window.show()
    sys.exit(app.exec())
