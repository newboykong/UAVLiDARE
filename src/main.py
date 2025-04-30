import os
import sys
import platform
import subprocess

os.environ["QT_API"] = "pyside6"
os.environ["VTK_QTDIR"] = os.path.dirname(__file__)


# def resource_path(relative_path):
#     """
#     获取资源文件路径。适配源码运行与 Nuitka 打包环境。
#     """
#     if getattr(sys, 'frozen', False):
#         # Nuitka 打包后：资源文件通常与可执行文件放在同一目录
#         return os.path.join(os.path.dirname(sys.executable), relative_path)
#     else:
#         # 源码运行时
#         return os.path.join(os.path.abspath("."), relative_path)
#
# # 获取 proj.db 的路径
# proj_path = resource_path("proj.db")

# 设置 PROJ 数据路径环境变量
# os.environ["PROJ_DATA"] = os.path.dirname(proj_path)
# os.environ['PROJ_LIB'] = os.path.dirname(proj_path)





# 解决PySide6 6.8+的OpenGL问题
from PySide6 import QtCore

QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_UseDesktopOpenGL)
QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_ShareOpenGLContexts)


# 手动添加项目目录
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'ui')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'algorithms')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
# 现在可以导入 icon_rc
from osgeo import ogr
import json
import laspy
import numpy as np
from PySide6.QtCore import Qt, QPoint
from PySide6.QtWidgets import QApplication, QFileDialog, QTreeWidgetItem, QTreeWidget, QMenu
from data_processing import DenoisingPointCloud, FilterPointCloud, DemGet, DsmGet, ChmGet, Normalization, CanopyCover, \
    GapAndLAL, SingleWoodDivision,ExtractTreeParameters
from my_main_window import MyMainWindow
from point_cloud_model import PointCloudModel
from component.my_erro_message import MyMessage
from functools import partial
from osgeo import gdal
gdal.UseExceptions()
from PySide6.QtCore import QTimer, QCoreApplication


# 设置Qt平台插件路径
os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = os.path.join(os.path.dirname(sys.executable), 'platforms')


# 解决json文件打包时缺失的问题
def get_resource_path(filename):
    """获取打包后的资源文件的路径"""
    if getattr(sys, 'frozen', False):  # Nuitka 或 PyInstaller 打包的可执行文件
        return os.path.join(sys._MEIPASS, filename)  # 拼接 _MEIPASS 目录
    return os.path.join(os.path.dirname(__file__), filename)  # 源代码运行时拼接当前目录


class PointCloudController:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        """为view组件的按钮添加事件"""
        self.view.ui.open.clicked.connect(partial(self.get_file))
        self.view.ui.point_cloud_tree_widget.itemClicked.connect(partial(self.point_tree_item_clicked))
        self.view.ui.image_tree_widget.itemClicked.connect(partial(self.image_tree_item_clicked))
        self.view.ui.vector_tree_widget.itemClicked.connect(partial(self.vector_tree_item_clicked))
        self.view.ui.remove.clicked.connect(partial(self.remove_data))
        self.view.ui.save.clicked.connect(partial(self.save_data))

        """为文件菜单栏添加事件"""
        self.view.open_action.triggered.connect(partial(self.get_file))
        self.view.remove_action.triggered.connect(partial(self.remove_data))
        self.view.save_action.triggered.connect(partial(self.save_data))

        """添加节点右击菜单"""
        self.view.ui.point_cloud_tree_widget.setContextMenuPolicy(Qt.CustomContextMenu)  # 允许自定义右键菜单
        self.view.ui.point_cloud_tree_widget.customContextMenuRequested.connect(partial(self.show_context_menu))  # 绑定菜单事件
        self.view.show_by_cls_dialog.accepted.connect(partial(self.show_by_cls_accepted))

        """点云去噪"""
        self.view.denoising_action.triggered.connect(partial(self.denoising_point_cloud))
        self.view.denoising_dialog.accepted.connect(partial(self.denoising_accepted))

        """点云滤波"""
        self.view.filtering_action.triggered.connect(partial(self.filter_point_cloud))
        self.view.filtering_dialog.accepted.connect(partial(self.filter_accepted))

        """点云归一化"""
        self.view.normalization_action.triggered.connect(partial(self.normalize_points))
        self.view.normalization_dialog.accepted.connect(partial(self.normalize_accepted))

        """DEM"""
        self.view.dem_action.triggered.connect(partial(self.dem_get))
        self.view.dem_dialog.accepted.connect(partial(self.dem_accepted))

        """DSM"""
        self.view.dsm_action.triggered.connect(partial(self.dsm_get))
        self.view.dsm_dialog.accepted.connect(partial(self.dsm_accepted))

        """CHM"""
        self.view.chm_action.triggered.connect(partial(self.chm_get))
        self.view.chm_dialog.accepted.connect(partial(self.chm_accepted))

        """tif转las"""
        self.view.tif_to_las_action.triggered.connect(partial(self.save_tif_to_lsa))

        """植被覆盖程度"""
        self.view.canopy_cover_action.triggered.connect(partial(self.canopy_cover_apply))
        self.view.canopy_cover_dialog.accepted.connect(partial(self.canopy_cover_accepted))

        """空隙率和叶面指数"""
        self.view.gp_and_lai_action.triggered.connect(partial(self.gp_and_lai_apply))
        self.view.gp_and_lai_dialog.accepted.connect(partial(self.gp_and_lai_accepted))

        """单木分割"""
        self.view.single_wood_division_action.triggered.connect(partial(self.single_wood_division_apply))
        self.view.single_wood_dialog.accepted.connect(partial(self.single_wood_division_accepted))

        """单木结构参数提取"""
        self.view.extract_tree_param_action.triggered.connect(partial(self.extract_tree_param_apply))
        self.view.extract_tree_param_dialog.accepted.connect(partial(self.extract_tree_param_accepted))


        """数据处理线程类"""
        self.denoising = None
        self.filtering = None
        self.dem = None
        self.dsm = None
        self.chm = None
        self.normalization = None
        self.canopy_cover = None
        self.gp_and_lai = None
        self.single_wood_division = None
        self.extract_tree_param= None

        """设置点云大小"""
        self.view.ui.point_size.valueChanged.connect(partial(self.point_size_change))

    """从文件加载数据"""

    def load_point_cloud(self,file_path=None):
        # 加载新的文件之前储存当前显示点云的相机参数
        currNode = self.view.ui.file_name.text()
        if currNode and currNode != "":
            self.save_camera_params(currNode)

        file=[]
        # 获取文件
        file.append(file_path)
        file.append(os.path.basename(file_path))

        if file:
            if file[1] not in self.model.point_clouds:
                las = laspy.read(file[0])
            else:
                error_message = MyMessage(self.view)
                error_message.message("文件名重复！")
                error_message.open()
                return
        else:
            return
        # 初始化显示方式、相机参数
        self.model.point_show_way[file[1]] = "elevation"
        self.model.pyvista_camera_params[file[1]] = None
        # 添加点云数据到model层
        self.model.add_point_cloud(file[1], las)
        # 将点云属性添加到mode层
        self.point_attribute_get(las=self.model.point_clouds[file[1]]
                                 , file_path=file[0])
        # 点云数据可视化
        try:
            self.view.open3d_view.points_show(las)
        except Exception as e:
            # self.view.pyvista_view.points_show(las)
            self.points_show(file[1])
        # 在视图层的资源管理添加节点
        self.add_items_point_cloud(file[1])
        self.view.switch_point()
        self.view.view_state="点云层"

    def load_image(self,file_path=None):
        file = []
        # 获取文件
        file.append(file_path)
        file.append(os.path.basename(file_path))

        if file:
            if file[1] not in self.model.images:
                image = gdal.Open(file[0])
            else:
                error_message = MyMessage(self.view)
                error_message.message("文件名重复！")
                error_message.open()
                return
        else:
            return

        # 添加影像数据到model层
        self.model.images[file[1]] = file[0]
        # 将点云属性添加到mode层
        self.image_attribute_get(image=image
                                 , file_path=file[0])
        # 影像数据可视化
        self.image_show(file[1])

        # 在视图层的资源管理添加节点
        self.add_items_image(file[1])

        self.view.view_state="影像层"

    def load_vector(self,file_path=None):
        file = []
        # 获取文件
        file.append(file_path)
        file.append(os.path.basename(file_path))

        if file:
            if file[1] not in self.model.vectors:
                driver = ogr.GetDriverByName("ESRI Shapefile")
                vector = driver.Open(file[0], 0)
            else:
                error_message = MyMessage(self.view)
                error_message.message("文件名重复！")
                error_message.open()
                return
        else:
            return

        # 添加影像数据到model层
        self.model.vectors[file[1]] = file[0]
        # 将点云属性添加到mode层
        self.vector_attribute_get(vector=vector
                                 , file_path=file[0])
        # 影像数据可视化
        self.vector_show(file[1])

        # 在视图层的资源管理添加节点
        self.add_items_vector(file[1])

        self.view.view_state = "矢量层"

    """封装在资源管理栏添加节点的功能"""

    def add_items_point_cloud(self, name):
        # 在视图层的资源管理添加节点
        item = self.view.item_creat(self.view.ui.point_cloud_tree_widget, name, name)
        self.view.ui.point_cloud_tree_widget.setCurrentItem(item)

    def add_items_image(self, name):
        # 在视图层的资源管理添加节点
        item = self.view.item_creat(self.view.ui.image_tree_widget, name, name)
        self.view.ui.image_tree_widget.setCurrentItem(item)

    def add_items_vector(self, name):
        # 在视图层的资源管理添加节点
        item = self.view.item_creat(self.view.ui.vector_tree_widget, name, name)
        self.view.ui.vector_tree_widget.setCurrentItem(item)

    """改变渲染时的点云大小"""

    def point_size_change(self, value):
        # 获取当前高亮相
        name = self.view.ui.file_name.text()
        self.save_camera_params(name)
        size = self.view.ui.point_size.value()
        if name == "":
            self.view.ui.point_size.setValue(3)
            return
        self.model.point_attribute[name]['point_size'] = size
        self.points_show(name)

    def update_slider(self, value):
        """避免在 setValue() 期间触发 valueChanged 事件"""
        self.view.ui.point_size.blockSignals(True)  # 暂时阻止信号
        self.view.ui.point_size.setValue(value)
        self.view.ui.point_size.blockSignals(False)  # 恢复信号

    """根据model储存的信息灵活显示点云数据按（高程/分类信息/颜色）"""
    """点云可视化也伴随着属性栏的显示，标题的显示"""

    def points_show(self, name, colors=None):
        cls_params = None
        try:
            las = self.model.point_clouds[name]
            show_way = self.model.point_show_way[name]
            camera_params = self.model.pyvista_camera_params[name]
            cls_params = self.model.point_attribute[name]['classification']
            point_size = self.model.point_attribute[name]['point_size']
        except KeyError as e:
            las = self.model.point_clouds_denoising[name][0]
            show_way = "colors"
            camera_params = self.model.pyvista_camera_params[name]
            colors = self.model.point_clouds_denoising[name][1]
            point_size = self.model.point_attribute[name]['point_size']
            self.show_message("这是一个结果查看数据"
                              "不能改变渲染方式"
                              "查看完可直接移除！")

        if show_way == "elevation":
            self.view.pyvista_view.points_show_by_elevation(las, camera_params, point_size=point_size)
        elif show_way == "classification":
            self.view.pyvista_view.points_show_by_classification(las, camera_params, color_dict=cls_params,
                                                                 point_size=point_size)
        elif show_way == "colors":
            self.view.pyvista_view.points_show_by_colors(las, camera_params, colors, point_size=point_size)
        else:
            self.show_message("显示点云失败！")

        # 显示点云属性
        self.model.point_attribute[name]['point_show_way']=show_way
        point_attributes = self.model.point_attribute[name]
        self.view.attribute_display_point_cloud.attributes_show(point_attributes)

        # 显示标题
        self.view.ui.file_name.setText(name)
        self.view.ui.size_num.setText(str(point_size))
        self.update_slider(int(point_size))

        self.view.view_state="点云层"

    def image_show(self, name,title=None):
        tif_file=self.model.images[name]
        self.view.image_view.image_show(tif_file,title=title)
        self.view.ui.image_file_name.setText(name)
        self.view.switch_image()

        image_attributes = self.model.image_attribute[name]
        self.view.attribute_display_image.attributes_show(image_attributes)

        self.view.view_state="影像层"

    def vector_show(self, name,title=None):
        vector_file=self.model.vectors[name]
        self.view.vector_view.vector_show(vector_file,title=title)
        self.view.ui.vector_file_name.setText(name)
        self.view.switch_vector()

        vector_attributes = self.model.vector_attribute[name]
        self.view.attribute_display_vector.attributes_show(vector_attributes)

        self.view.view_state="矢量层"

    """通过pyside6组件获取文件路径和文件名"""

    def get_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self.view,
            "选择 LAS 或 TIF 文件",
            "",
            "LAS/TIF/SHP 文件 (*.las *.tif *.shp);;LAS 文件 (*.las);;TIF 文件 (*.tif);;SHP 文件 (*.shp);;所有文件 (*.*)"
        )
        if file_path:
            file_ext = os.path.splitext(file_path)[1].lower()

            if file_ext == ".las":
                self.load_point_cloud(file_path)

            elif file_ext == ".tif":
                self.load_image(file_path)

            elif file_ext == ".shp":
                self.load_vector(file_path)

            else:
                self.show_message("不支持的文件类型")
                return None

    """从模型中删除点云"""

    def remove_data(self):
        if self.view.view_state=="点云层":
            # 若没有数据可以删除直接返回
            currNode = self.view.ui.point_cloud_tree_widget.currentItem()
            if not currNode:
                return
            # 从point_cloud_tree_widget删除节点
            self.remove_node_by_text(currNode.text(0))
            # 从点云数据字典删除该项
            self.model.remove_by_name(currNode.text(0))
            self.update_ui()  # 更新UI
        elif self.view.view_state=="影像层":
            # 若没有数据可以删除直接返回
            currNode = self.view.ui.image_tree_widget.currentItem()
            if not currNode:
                return
            # 从point_cloud_tree_widget删除节点
            self.remove_node_by_text(currNode.text(0))
            # 从点云数据字典删除该项
            del self.model.images[currNode.text(0)]
            del self.model.image_attribute[currNode.text(0)]
            self.update_ui()  # 更新UI
        elif self.view.view_state=="矢量层":
            # 若没有数据可以删除直接返回
            currNode = self.view.ui.vector_tree_widget.currentItem()
            if not currNode:
                return
            # 从point_cloud_tree_widget删除节点
            self.remove_node_by_text(currNode.text(0))
            # 从点云数据字典删除该项
            del self.model.vectors[currNode.text(0)]
            del self.model.vector_attribute[currNode.text(0)]
            self.update_ui()  # 更新UI

    def remove_node_by_text(self, text):
        items=None

        if self.view.view_state=="点云层":
            items = self.view.ui.point_cloud_tree_widget.findItems(text, Qt.MatchRecursive)  # 递归查找匹配的文本
            for item in items:
                parent = item.parent()
                if parent:
                    parent.removeChild(item)  # 如果有父节点，则从父节点移除
                else:
                    index = self.view.ui.point_cloud_tree_widget.indexOfTopLevelItem(item)
                    self.view.ui.point_cloud_tree_widget.takeTopLevelItem(index)  # 如果是顶层节点，直接移除
        elif self.view.view_state=="影像层":
            items = self.view.ui.image_tree_widget.findItems(text, Qt.MatchRecursive)
            for item in items:
                parent = item.parent()
                if parent:
                    parent.removeChild(item)  # 如果有父节点，则从父节点移除
                else:
                    index = self.view.ui.image_tree_widget.indexOfTopLevelItem(item)
                    self.view.ui.image_tree_widget.takeTopLevelItem(index)  # 如果是顶层节点，直接移除
        elif self.view.view_state=="矢量层":
            items = self.view.ui.vector_tree_widget.findItems(text, Qt.MatchRecursive)
            for item in items:
                parent = item.parent()
                if parent:
                    parent.removeChild(item)  # 如果有父节点，则从父节点移除
                else:
                    index = self.view.ui.vector_tree_widget.indexOfTopLevelItem(item)
                    self.view.ui.vector_tree_widget.takeTopLevelItem(index)  # 如果是顶层节点，直接移除

    """另存点云数据"""

    def save_data(self):
        if self.view.view_state=="点云层":
            # 若没有选择数据，直接返回
            currNode = self.view.ui.point_cloud_tree_widget.currentItem()
            if not currNode:
                self.show_message("你没有选择数据！")
                return
            name = currNode.text(0)

            # 让用户选择保存路径
            file_path, _ = QFileDialog.getSaveFileName(self.view, "另存为 LAS 文件", name, "LAS 文件 (*.las)")
            if not file_path:
                return

            # 从 model 加载数据
            try:
                las_or_points = self.model.point_clouds[name]
            except KeyError:
                self.show_message("这是结果查看数据不能保存！")
                return

            self.points_save(las_or_points, file_path)

        elif self.view.view_state=="影像层":
            # 若没有选择数据，直接返回
            currNode = self.view.ui.image_tree_widget.currentItem()
            if not currNode:
                self.show_message("你没有选择数据！")
                return
            name = currNode.text(0)

            # 从模型层加载 gdal 读取后的 tif 数据
            tif_path = self.model.images[name]
            tif_file = gdal.Open(tif_path)
            # 让用户选择保存路径
            file_path, _ = QFileDialog.getSaveFileName(self.view, "另存为 tif 文件", name, "tif 文件 (*.tif)")
            if not file_path:
                return

            if not tif_file:
                return

            self.image_save(tif_file, file_path)

        elif self.view.view_state == "矢量层":
            # 若没有选择数据，直接返回
            currNode = self.view.ui.vector_tree_widget.currentItem()
            if not currNode:
                self.show_message("你没有选择数据！")
                return
            name = currNode.text(0)

            # 从模型层加载 gdal 读取后的 tif 数据
            vector_path = self.model.vectors[name]
            driver = ogr.GetDriverByName("ESRI Shapefile")
            vector_file = driver.Open(vector_path, 0)

            # 让用户选择保存路径
            file_path, _ = QFileDialog.getSaveFileName(self.view, "另存为 shp 文件", name, "shp 文件 (*.shp)")
            if not file_path:
                return

            if not vector_file:
                return

            self.vector_save(vector_file, file_path)

    def points_save(self,las_or_points,file_path):
        try:
            # 判断是否是 laspy.LasData 类型
            if isinstance(las_or_points, laspy.LasData):
                las = las_or_points
            else:
                points = las_or_points  # 确保是 NumPy 数组
                x, y, z = points[:, 0], points[:, 1], points[:, 2]

                # 创建 LAS 头部信息
                header = laspy.LasHeader(point_format=3, version="1.4")
                header.scales = [0.01, 0.01, 0.01]  # 设置比例因子
                header.offsets = [np.min(x), np.min(y), np.min(z)]  # 以最小值作为偏移量

                # 创建 LasData
                las = laspy.LasData(header)

                # 转换坐标为存储格式
                las.x = x
                las.y = y
                las.z = z

            las.write(file_path)

            self.show_message("文件已成功保存！")
        except Exception as e:
            self.show_message(f"文件保存失败: {str(e)}")

    def image_save(self,tif_file,file_path):
        try:
            # 获取数据的驱动程序类型，默认为 GeoTIFF
            driver = gdal.GetDriverByName('GTiff')
            if not driver:
                self.show_message("无法获取 TIF 文件驱动")
                return

            # 创建新的 TIF 文件并保存
            out_tif_file = driver.Create(file_path, tif_file.RasterXSize, tif_file.RasterYSize, tif_file.RasterCount,
                                         tif_file.GetRasterBand(1).DataType)

            # 设置仿射变换和投影信息
            out_tif_file.SetGeoTransform(tif_file.GetGeoTransform())
            out_tif_file.SetProjection(tif_file.GetProjection())

            # 逐波段复制数据
            for band_idx in range(1, tif_file.RasterCount + 1):
                band = tif_file.GetRasterBand(band_idx)
                out_band = out_tif_file.GetRasterBand(band_idx)
                out_band.WriteArray(band.ReadAsArray())

            # 完成保存
            out_tif_file.FlushCache()  # 确保数据被写入磁盘
            del out_tif_file  # 关闭文件
            self.show_message("文件已成功保存！")
        except Exception as e:
            self.show_message(f"文件保存失败: {str(e)}")

    def vector_save(self, vector_file, file_path):
        try:
            # 如果目标路径已存在，先删除
            if os.path.exists(file_path):
                ogr.GetDriverByName("ESRI Shapefile").DeleteDataSource(file_path)

            # 获取源图层
            in_layer = vector_file.GetLayer()

            # 获取驱动
            driver = ogr.GetDriverByName("ESRI Shapefile")
            out_ds = driver.CreateDataSource(file_path)

            # 拷贝坐标参考系
            spatial_ref = in_layer.GetSpatialRef()

            # 创建输出图层（与输入图层同类型）
            out_layer = out_ds.CreateLayer(in_layer.GetName(), srs=spatial_ref, geom_type=in_layer.GetGeomType())

            # 拷贝字段结构
            in_layer_defn = in_layer.GetLayerDefn()
            for i in range(in_layer_defn.GetFieldCount()):
                field_defn = in_layer_defn.GetFieldDefn(i)
                out_layer.CreateField(field_defn)

            # 添加要素
            for feature in in_layer:
                out_feature = ogr.Feature(out_layer.GetLayerDefn())
                out_feature.SetGeometry(feature.GetGeometryRef().Clone())
                for i in range(out_feature.GetFieldCount()):
                    out_feature.SetField(i, feature.GetField(i))
                out_layer.CreateFeature(out_feature)
                out_feature = None  # 清除以释放内存

            out_ds.FlushCache()
            out_ds = None  # 保存文件
            self.show_message("文件已成功保存！")
        except Exception as e:
            self.show_message(f"文件保存失败: {str(e)}")

    def save_tif_to_lsa(self):
        if self.view.view_state == "影像层":
            currNode = self.view.ui.image_tree_widget.currentItem()
            if not currNode:
                self.show_message("你没有选择数据！")
                return
            name = currNode.text(0)

            tif_path = self.model.images.get(name)
            tif_file = gdal.Open(tif_path)
            if tif_file is None:
                self.show_message(fr"[{name}]数据丢失！")
                return

            name = self.remove_las_tif_suffix(name)
            file_path, _ = QFileDialog.getSaveFileName(self.view, "另存为 las 文件", name + ".las", "las 文件 (*.las)")
            if not file_path:
                return

            band = tif_file.GetRasterBand(1)
            data = band.ReadAsArray()
            nodata = band.GetNoDataValue()

            # 创建有效数据掩码
            if nodata is not None:
                mask = data != nodata
            else:
                mask = np.ones_like(data, dtype=bool)

            rows, cols = np.where(mask)
            if rows.size == 0 or cols.size == 0:
                self.show_message("该影像没有有效的数据点！")
                return

            zs = data[rows, cols]

            # 获取地理变换
            transform = tif_file.GetGeoTransform()
            origin_x, pixel_width, _, origin_y, _, pixel_height = transform

            # 计算坐标
            xs = origin_x + cols * pixel_width
            ys = origin_y + rows * pixel_height

            # 转换为 numpy 数组并清洗无效值
            xs = np.array(xs, dtype=np.float64)
            ys = np.array(ys, dtype=np.float64)
            zs = np.array(zs, dtype=np.float64)

            # 移除包含 NaN 或 inf 的点
            valid_mask = np.isfinite(xs) & np.isfinite(ys) & np.isfinite(zs)
            xs = xs[valid_mask]
            ys = ys[valid_mask]
            zs = zs[valid_mask]

            if xs.size == 0:
                self.show_message("有效点全为 NaN，无法保存 las 文件！")
                return

            # 创建 LAS 头
            header = laspy.LasHeader(point_format=3, version="1.4")
            header.scales = [0.01, 0.01, 0.01]
            header.offsets = [np.min(xs), np.min(ys), np.min(zs)]

            # 写入 las 文件
            las = laspy.LasData(header)
            las.x = xs
            las.y = ys
            las.z = zs

            try:
                las.write(file_path)
                self.show_message("文件已成功保存！")
                self.load_point_cloud(file_path)
            except Exception as e:
                self.show_message(f"保存失败：{str(e)}")

    """封装常用的代码：弹出信息框"""

    def show_message(self, message, title="错误提示"):
        error_message = MyMessage(self.view)
        error_message.message(message)
        error_message.setWindowTitle(title)
        error_message.open()

    """删除点云后刷新UI"""

    def update_ui(self):
        if self.view.view_state=="点云层":
            # 获取当前高光项
            currNode = self.view.ui.point_cloud_tree_widget.currentItem()
            # 如果没有项清除点云可视化窗口
            if not currNode:
                try:
                    self.view.open3d_view.vis.clear_geometries()
                except Exception as e:
                    self.view.pyvista_view.plotter.clear()
                    self.view.pyvista_view.force_render()
                # 初始化文件名标签和属性显示窗口
                self.view.ui.file_name.setText("")
                self.view.attribute_display_point_cloud.attributes_show(None)
                self.view.ui.point_size.setValue(3)
                return
            # 如果还有选项，当前高亮项点云可视化
            self.points_show(currNode.text(0))
        elif self.view.view_state=="影像层":
            # 获取当前高光项
            currNode = self.view.ui.image_tree_widget.currentItem()
            # 如果没有项清除点云可视化窗口
            if not currNode:
                self.view.image_view.clear()
                # self.view.image_view.canvas.draw()
                self.view.ui.image_file_name.setText("")
                self.view.attribute_display_image.attributes_show(None)
                return
            # 如果还有选项，当前高亮项点云可视化
            self.image_show(currNode.text(0))
        elif self.view.view_state=="矢量层":
            # 获取当前高光项
            currNode = self.view.ui.vector_tree_widget.currentItem()
            # 如果没有项清除点云可视化窗口
            if not currNode:
                self.view.vector_view.clear()
                # self.view.vector_view.canvas.draw()
                self.view.ui.vector_file_name.setText("")
                self.view.attribute_display_vector.attributes_show(None)
                return
            # 如果还有选项，当前高亮项点云可视化
            self.vector_show(currNode.text(0))

    """解决point_cloud_tree_widget和点云显示窗口的交互问题"""

    def point_tree_item_clicked(self, item, column):
        # 在点云数据字典中查找
        for i in self.model.point_clouds:
            if i == item.text(0):
                # 保存之前的相机参数
                self.save_camera_params(self.view.ui.file_name.text())
                # 尝试open3d显示点云
                try:
                    self.view.open3d_view.points_show(self.model.point_clouds[i], self.model.open3d_camera_params[i])
                except Exception as e:
                    self.points_show(i)

        # 在点云去噪字典中查找
        for i in self.model.point_clouds_denoising:
            if i == item.text(0):
                # 保存之前的相机参数
                self.save_camera_params(self.view.ui.file_name.text())
                # 显示去噪后的数据
                self.points_show(i)

    def image_tree_item_clicked(self, item, column):
        # 在点影像字典字典中查找
        for i in self.model.images:
            if i == item.text(0):
                # 显示去噪后的数据
                self.image_show(i)

    def vector_tree_item_clicked(self, item, column):
        # 在点影像字典字典中查找
        for i in self.model.vectors:
            if i == item.text(0):
                # 显示去噪后的数据
                self.vector_show(i)

    """切换视图时保存相机参数"""

    def save_camera_params(self, name):
        # 尝试open3d的相机参数储存
        try:
            # 获取当前视图控制器
            view_control = self.view.open3d_view.vis.get_view_control()
            # 获取相机参数，包括相机位置、方向、视角等
            camera_params = view_control.convert_to_pinhole_camera_parameters()
            self.model.open3d_camera_params[name] = camera_params
        except Exception as e:
            # 尝试pyvista的相机参数储存
            camera_params = self.view.pyvista_view.plotter.camera_position
            self.model.pyvista_camera_params[name] = camera_params

    """获取点云属性"""

    def point_attribute_get(self, las=None, file_path=None, name=None):
        if las is None:
            las = self.model.point_clouds[name]
        # 获取las文件的x,y,z坐标
        points = np.vstack((las.x, las.y, las.z)).T
        # 创建字典储存返回的结果
        result_dic = {}
        # 获取las的分类信息
        # 创建储存分类信息的数组
        cls = las.classification
        # 创建字典储存分类信息
        cls_dic = {}
        # 加载配置文件，获取类别序号和类别名的对应关系
        classification_path = get_resource_path("classification_mapping.json")
        with open(classification_path, "r", encoding="utf-8") as f:
            class_mapping = json.load(f)

        # 加载配置文件，获取序号与颜色之间的对应关系
        color_path = get_resource_path("color_mapping.json")
        with open(color_path, "r", encoding="utf-8") as f:
            color_mapping = json.load(f)

        for i in np.unique(cls):
            current_cls = np.where(cls == i)[0]
            current_length = str(len(current_cls))
            try:
                cls_name = class_mapping[f"{i}"]["name"]
                color = color_mapping[f"{i}"]
            except Exception as e:
                cls_name = f"未知类别"
                color = color_mapping["21-255"]
            cls_dic[f'{i}'] = {"name": cls_name, "num": current_length, "color": color, "state": "选中"}

        if file_path:
            # 获取文件名和文件类型
            name = os.path.basename(file_path)
            file_type = "*.las"  # LAS 文件类型
        else:
            # 获取文件名和文件类型
            file_type = "LAS"  # LAS 文件类型
            file_path = "内存中"  # 文件路径

        # 计算点云的数量
        num_points = len(points)

        # 计算最小值和最大值
        min_vals = points.min(axis=0)
        max_vals = points.max(axis=0)

        # 计算中心点
        center = points.mean(axis=0)

        # 获取渲染方式
        point_show_way = self.model.point_show_way[name]
        result_dic["file_name"] = name
        result_dic["file_type"] = file_type
        result_dic["file_path"] = file_path
        result_dic["num_points"] = str(num_points)
        result_dic["min_x"] = str(round(min_vals[0], 3))
        result_dic["min_y"] = str(round(min_vals[1], 3))
        result_dic["min_z"] = str(round(min_vals[2], 3))
        result_dic["max_x"] = str(round(max_vals[0], 3))
        result_dic["max_y"] = str(round(max_vals[1], 3))
        result_dic["max_z"] = str(round(max_vals[2], 3))
        result_dic["center_x"] = str(round(center[0], 3))
        result_dic["center_y"] = str(round(center[1], 3))
        result_dic["center_z"] = str(round(center[2], 3))
        result_dic["classification"] = cls_dic
        result_dic["point_show_way"] = point_show_way
        result_dic["point_size"] = "3"

        # 在model层更新数据
        self.model.point_attribute[name] = result_dic

    def image_attribute_get(self, image=None, file_path=None, name=None):
        image_file=None
        file_directory=None
        file_name=None
        params_dict={}

        if image is not None:
            image_file = image

        if file_path is not None:
            file_name = os.path.basename(file_path)
        else:
            file_directory="内存中"

        file_type="*.tif"

        if name is not None:
            file_name = name

        band = image_file.GetRasterBand(1)
        bands = image_file.RasterCount
        data = band.ReadAsArray()

        nodata = band.GetNoDataValue()

        # 获取地理变换参数
        transform = image_file.GetGeoTransform()  # [originX, pixelWidth, 0, originY, 0, -pixelHeight]
        origin_x, pixel_width, _, origin_y, _, pixel_height = transform

        # 获取行列索引
        rows, cols = np.where(data != nodata)
        zs = data[rows, cols]

        # 计算 x, y 坐标
        xs = origin_x + cols * pixel_width
        ys = origin_y + rows * pixel_height  # 注意：GDAL 的 Y 是从上到下，所以一般是减去

        # 转换为 numpy 数组
        xs = np.array(xs)
        ys = np.array(ys)
        zs = np.array(zs)

        min_x = np.min(xs)
        min_y = np.min(ys)
        min_z = np.min(zs)
        max_x = np.max(xs)
        max_y = np.max(ys)
        max_z = np.max(zs)

        rows = image_file.RasterYSize
        cols = image_file.RasterXSize

        # 如果是标准的 DEM 数据，通常是单波段（灰度图，bands = 1）
        bands = image.RasterCount

        params_dict["min_x"] = str(round(min_x, 3))
        params_dict["min_y"] = str(round(min_y, 3))
        params_dict["min_z"] = str(round(min_z, 3))
        params_dict["max_x"] = str(round(max_x, 3))
        params_dict["max_y"] = str(round(max_y, 3))
        params_dict["max_z"] = str(round(max_z, 3))
        params_dict["file_name"]= str(file_name)
        params_dict["file_type"] = file_type
        params_dict["file_path"] = str(file_path)
        params_dict["bands"] = str(bands)
        params_dict["rows"] = str(rows)
        params_dict["cols"] = str(cols)
        params_dict["origin_x"] = str(round(origin_x,3))
        params_dict["origin_y"] = str(round(origin_y,3))
        params_dict["pixel_width"] = str(round(pixel_width,3))
        params_dict["pixel_height"] = str(round(pixel_height,3))

        self.model.image_attribute[file_name] = params_dict

        return params_dict

    def vector_attribute_get(self, vector=None, file_path=None, name=None):
        layer = None
        file_directory = None
        file_name = None
        params_dict = {}

        if vector is not None:
            layer = vector.GetLayer()

        if file_path is not None:
            file_name = os.path.basename(file_path)
        else:
            file_directory = "内存中"

        file_type = "*.shp"

        if name is not None:
            file_name = name

        # 初始边界
        min_x, max_x, min_y, max_y = float('inf'), float('-inf'), float('inf'), float('-inf')

        feature_count = 0
        geometry_type = None
        has_z = False
        field_names = []

        for feature in layer:
            feature_count += 1
            geom = feature.GetGeometryRef()
            if geom is None:
                continue

            # 几何类型
            if geometry_type is None:
                geometry_type = geom.GetGeometryName()

            # 检查是否是三维
            if geom.GetCoordinateDimension() == 3:
                has_z = True

            # 计算范围
            env = geom.GetEnvelope()  # (minX, maxX, minY, maxY)
            min_x = min(min_x, env[0])
            max_x = max(max_x, env[1])
            min_y = min(min_y, env[2])
            max_y = max(max_y, env[3])

        # 提取字段名
        layer_defn = layer.GetLayerDefn()
        for i in range(layer_defn.GetFieldCount()):
            field_defn = layer_defn.GetFieldDefn(i)
            field_names.append(field_defn.GetName())

        # 坐标系信息
        spatial_ref = layer.GetSpatialRef()
        crs = spatial_ref.ExportToWkt() if spatial_ref else "Unknown"

        # 写入信息
        params_dict["file_name"] = str(file_name)
        params_dict["file_path"] = str(file_path)
        params_dict["file_type"] = file_type
        params_dict["feature_count"] = feature_count
        params_dict["geometry_type"] = geometry_type
        params_dict["has_z"] = has_z
        params_dict["field_names"] = field_names
        params_dict["min_x"] = str(round(min_x, 3))
        params_dict["min_y"] = str(round(min_y, 3))
        params_dict["max_x"] = str(round(max_x, 3))
        params_dict["max_y"] = str(round(max_y, 3))
        params_dict["extent"] = (min_x, min_y, max_x, max_y)
        params_dict["crs"] = crs

        self.model.vector_attribute[file_name] = params_dict
        return params_dict

    """为节点添加事件"""

    def show_context_menu(self, pos: QPoint):
        """ 右键菜单 """
        item = self.view.ui.point_cloud_tree_widget.itemAt(pos)  # 获取当前鼠标位置的节点
        if item is None:
            return  # 空白区域不显示菜单

        # 创建菜单添加删除和文件另存
        menu = QMenu(self.view.ui.point_cloud_tree_widget)
        menu.setStyleSheet("""
                   QMenu {
                       background-color:#16191d;  /* 菜单背景色 */
                       border: 1px solid #222222;
                   }
                   QMenu::item {
                       background-color: transparent;
                       color: #FFFFFF;  /* 文字颜色 */
                       padding: 8px 20px;
                   }
                   QMenu::item:selected { 
                       background-color: #015371;  /* 选中项颜色 */
                   }
                   QMenu::item:disabled {
                       color: #777777;  /* 禁用项颜色 */
                   }
                   QMenu::separator {
                       height: 1px;
                       background: #444444;  /* 分割线颜色 */
                       margin: 4px 8px;
                   }
               """)
        remove_file = menu.addAction("删除")
        save_file = menu.addAction("文件另存")

        # 添加渲染方式子菜单
        point_show_way_menu = QMenu("渲染方式", self.view.ui.point_cloud_tree_widget)
        # 设置暗黑主题的菜单样式
        point_show_way_menu.setStyleSheet("""
             QMenu {
                       background-color:#16191d;  /* 菜单背景色 */
                       border: 1px solid #222222;
                   }
                   QMenu::item {
                       background-color: transparent;
                       color: #FFFFFF;  /* 文字颜色 */
                       padding: 8px 20px;
                   }
                   QMenu::item:selected { 
                       background-color: #015371;  /* 选中项颜色 */
                   }
                   QMenu::item:disabled {
                       color: #777777;  /* 禁用项颜色 */
                   }
                   QMenu::separator {
                       height: 1px;
                       background: #444444;  /* 分割线颜色 */
                       margin: 4px 8px;
                   }
        """)
        elevation = point_show_way_menu.addAction("按高程渲染")
        classification = point_show_way_menu.addAction("按分类渲染")

        # 将子菜单添加到主菜单
        menu.addMenu(point_show_way_menu)

        # # 添加渲染方式子菜单
        # data_processing = QMenu("数据处理", self.view.ui.point_cloud_tree_widget)
        # data_processing.setStyleSheet("""
        #                    QMenu {
        #                background-color:#16191d;  /* 菜单背景色 */
        #                border: 1px solid #222222;
        #            }
        #            QMenu::item {
        #                background-color: transparent;
        #                color: #FFFFFF;  /* 文字颜色 */
        #                padding: 8px 20px;
        #            }
        #            QMenu::item:selected {
        #                background-color: #015371;  /* 选中项颜色 */
        #            }
        #            QMenu::item:disabled {
        #                color: #777777;  /* 禁用项颜色 */
        #            }
        #            QMenu::separator {
        #                height: 1px;
        #                background: #444444;  /* 分割线颜色 */
        #                margin: 4px 8px;
        #            }
        #                """)
        # denoising = data_processing.addAction("去噪")
        # filtering = data_processing.addAction("滤波")
        # dem = data_processing.addAction("生成DEM")
        #
        # # 将子菜单添加到主菜单
        # menu.addMenu(data_processing)

        # 运行菜单，并获取用户选择的操作
        action = menu.exec(self.view.ui.point_cloud_tree_widget.mapToGlobal(pos))

        # 获取当前项名字
        name = item.text(0)
        # 处理菜单点击
        if action == remove_file:
            self.remove_data()
        elif action == save_file:
            self.save_data()
        elif action == elevation:
            self.model.point_show_way[name] = "elevation"
            self.save_camera_params(self.view.ui.file_name.text())
            self.points_show(name)
        elif action == classification:
            self.model.point_show_way[name] = "classification"
            self.save_camera_params(self.view.ui.file_name.text())
            cls_dic = self.model.point_attribute[name]["classification"]
            self.view.show_by_cls_dialog.add_items(cls_dic)
            self.view.show_by_cls_dialog.open()
        # elif action == denoising:
        #     self.denoising_point_cloud()

    def show_by_cls_accepted(self):
        name = self.view.ui.point_cloud_tree_widget.currentItem().text(0)
        cls_dic = self.view.show_by_cls_dialog.paras_get()
        model_cls_dic = self.model.point_attribute[name]["classification"]
        for cls_id in cls_dic.keys():
            for key, value in cls_dic[cls_id].items():
                model_cls_dic[cls_id][key] = value

        self.model.point_attribute[name]["classification"] = model_cls_dic
        self.points_show(name)

    @staticmethod
    def remain_data(in_las, mask):

        # 根据需要选择点格式和版本
        header = laspy.LasHeader(point_format=3, version="1.4")
        # 创建 LasData 对象，并添加点数据
        new_las = laspy.LasData(header)
        # 只保存选中的点
        new_las.x = in_las.x[mask]
        new_las.y = in_las.y[mask]
        new_las.z = in_las.z[mask]
        new_las.classification = in_las.classification[mask]  # 复制分类信息
        new_las.intensity = in_las.intensity[mask]  # 复制强度
        new_las.return_number = in_las.return_number[mask]  # 复制回波编号
        new_las.number_of_returns = in_las.number_of_returns[mask]  # 复制总回波数
        new_las.scan_angle_rank = in_las.scan_angle_rank[mask]  # 复制扫描角度
        if hasattr(in_las, "gps_time"):
            new_las.gps_time = in_las.gps_time[mask]  # 复制GPS时间（如果有）

        return new_las



    """----------------------数据处理----------------------"""

    """应用去噪"""

    def denoising_point_cloud(self):
        # 打开对话框
        self.view.denoising_dialog.open()
        # 每次运行去噪是清除treeWidget上次留下的节点防止重复
        self.view.denoising_dialog.ui.treeWidget.clear()
        # 记录文件序号
        num = 1
        # 给文件选择框添加文件选项
        for key, value in self.model.point_clouds.items():
            # 添加根节点
            child_item = QTreeWidgetItem(self.view.denoising_dialog.ui.treeWidget)
            child_item.setText(1, str(key))  # 第二列
            child_item.setText(0, str(num))  # 第二列
            num += 1
        # 设置treeWidget中的选项是可多选的
        self.view.denoising_dialog.ui.treeWidget.setSelectionMode(QTreeWidget.ExtendedSelection)

    # 点击去噪按钮后执行的函数
    def denoising_accepted(self):
        # 从对话框获取（文件名，滤波类型，领域点数，方差倍数）
        name, filter_type, k_neighbors, std_ratio = self.view.denoising_dialog.params_get()
        if name == None:
            self.show_message("没有选择文件！")
            return
        # 如过内存中已有该去噪文件弹出错误信息
        real_name = self.remove_las_tif_suffix(name)
        for key in self.model.point_clouds.keys():
            if key == real_name + "-去噪":
                error_message = MyMessage(self.view)
                error_message.message("该数据已去过噪！")
                error_message.setWindowTitle("错误提示")
                error_message.open()
                return
        # 如果没选中文件弹出错误信息
        if name is None:
            error_message = MyMessage(self.view)
            error_message.message("你未选择文件！")
            error_message.setWindowTitle("错误提示")
            error_message.open()
            return
        # 进度条窗口显示
        self.view.progress_bar_denoising.set_value(0)
        self.view.progress_bar_denoising.set_window_title("点云去噪")
        self.view.progress_bar_denoising.open()
        self.view.progress_bar_denoising.closed.connect(partial(self.denoising_stopped))
        # 获取文件的points信息
        points = self.model.point_clouds[name]
        # 应用模型的滤波功能，返回正常点云，和去噪后的点云索引
        params_dict = {"points": points, "k_neighbors": k_neighbors, "std_ratio": std_ratio}
        self.denoising = DenoisingPointCloud(filter_type, params_dict)
        # filtered_points, filtered_points_index=denoising.statistical_denoising(type,params_dict)
        """点击按钮，启动多线程计算"""
        self.denoising.progress_updated.connect(partial(self.denoising_update_progress))  # 连接进度信号
        self.denoising.result_signal.connect(partial(self.denoising_result_get))  # 参数发送
        self.denoising.finished_signal.connect(partial(self.calculation_finished))  # 计算完成信号
        self.denoising.start()

    def denoising_update_progress(self, value):
        self.view.progress_bar_denoising.set_value(value)

    def denoising_result_get(self, filtered_points, filtered_points_index):
        if filtered_points is None or filtered_points_index is None:
            return
        # 从对话框获取（文件名，滤波类型，领域点数，方差倍数）
        name, filter_type, k_neighbors, std_ratio = self.view.denoising_dialog.params_get()
        # 获取文件的points信息
        las = self.model.point_clouds[name]
        # 创建颜色数组（绿色为正常点，红色为噪声点）
        colors = np.zeros((filtered_points_index.shape[0], 3))
        colors[~filtered_points_index] = [1, 0, 0]  # 红色代表噪声点
        colors[filtered_points_index] = [0, 1, 0]  # 绿色代表正常点
        # 在model层的point_clouds储存去噪后的数据
        new_las = self.remain_data(las, filtered_points_index)
        name=self.remove_las_tif_suffix(name)
        self.model.point_clouds[name + "-去噪"] = new_las
        # 在model层的point_clouds_denoising储存points数据，颜色数据和去噪后点云数据
        self.model.point_clouds_denoising[name + "-去噪查看"] = [las, colors, filtered_points]
        # 初始化当前加载点云的相机参数和显示方式
        self.model.pyvista_camera_params[name + "-去噪"] = None
        self.model.pyvista_camera_params[name + "-去噪查看"] = None
        self.model.point_show_way[name + "-去噪查看"] = "colors"
        self.model.point_show_way[name + "-去噪"] = "elevation"
        # 在model存储去噪后的点云属性
        self.point_attribute_get(las=new_las, name=name + "-去噪")
        # 存储去噪查看的点云属性
        self.point_attribute_get(las=las, name=name + "-去噪查看")
        # 显示去除噪点后的点云数据
        self.points_show(name + "-去噪")
        self.add_items_point_cloud(name + "-去噪")
        # 显示点云，按colors显示，便于查看噪点和正常点

        self.points_show(name + "-去噪查看")
        self.add_items_point_cloud(name + "-去噪查看")

    def calculation_finished(self):
        self.view.progress_bar_denoising.set_label("已完成！")
        self.view.progress_bar_denoising.close()

    def denoising_stopped(self):
        self.denoising.stopped=True


    """应用滤波"""

    def filter_point_cloud(self):
        # 打开对话框
        self.view.filtering_dialog.open()
        # 创建字典储存文件名和对应的类别信息
        params = {}
        for file_name in self.model.point_clouds.keys():
            params[file_name] = self.model.point_attribute[file_name]['classification']
        # 在滤波窗口添加信息
        self.view.filtering_dialog.add_items(params)

    def filter_accepted(self):
        # 从对话框获取参数
        params = self.view.filtering_dialog.params_get()
        # 如果没有选中文件直接返回
        if params.get('file_name') is None:
            self.show_message("没有选择文件！")
            return
        # 进度条窗口显示
        self.view.progress_bar_filter.set_value(0)
        self.view.progress_bar_filter.set_window_title(params['filter_type'] + "滤波")
        self.view.progress_bar_filter.open()
        self.view.progress_bar_filter.closed.connect(partial(self.filter_stopped))
        # 获取参数
        name = params['file_name']
        las = self.model.point_clouds[name]
        params['las'] = las
        """点击按钮，启动多线程计算"""
        self.filtering = FilterPointCloud(params)
        self.filtering.progress_updated.connect(partial(self.filter_update_progress))  # 连接进度信号
        self.filtering.result_signal.connect(partial(self.filter_result_get))  # 参数发送
        self.filtering.finished_signal.connect(partial(self.filter_finished))  # 计算完成信号
        self.filtering.start()

    def filter_update_progress(self, value):
        self.view.progress_bar_filter.set_value(value)

    def filter_result_get(self, name, las):
        if not las :
            return
        # 更新las数据
        # self.model.point_clouds[name]=las
        # 初始化当前加载点云的相机参数和显示方式
        self.model.point_show_way[name] = "classification"
        # 更新属性信息
        self.point_attribute_get(las=las, name=name)
        # 点云显示
        self.points_show(name)

    def filter_finished(self):
        self.view.progress_bar_filter.set_label("已完成！")
        self.view.progress_bar_filter.close()

    def filter_stopped(self):
         self.filtering.stopped=True

    """生成DEM"""

    def dem_get(self):
        # 打开对话框
        self.view.dem_dialog.open()
        # 创建字典储存文件名和对应的类别信息
        params = {}
        for file_name in self.model.point_clouds.keys():
            params[file_name] = None
        # 在滤波窗口添加信息
        self.view.dem_dialog.add_items(params)


    def dem_accepted(self):
        # 从对话框获取参数
        params = self.view.dem_dialog.params_get()
        # 如果没有选中文件直接返回
        if params.get('file_name') is None:
            self.show_message("没有选择文件！")
            return
        if not params['file_path'] :
            self.show_message("没有选择保存路径！")
            return
        # 进度条窗口显示
        self.view.progress_bar_dem.set_value(0)
        self.view.progress_bar_dem.set_window_title("DEM")
        self.view.progress_bar_dem.open()
        self.view.progress_bar_dem.closed.connect(partial(self.dem_stopped))
        # 获取参数
        name = params['file_name']
        las = self.model.point_clouds[name]
        params['las'] = las
        """点击按钮，启动多线程计算"""
        self.dem = DemGet(params)
        self.dem.progress_updated.connect(partial(self.dem_update_progress))  # 连接进度信号
        self.dem.result_signal.connect(partial(self.dem_result_get))  # 参数发送
        self.dem.finished_signal.connect(partial(self.dem_finished))  # 计算完成信号
        self.dem.start()

    def dem_update_progress(self,value):
        self.view.progress_bar_dem.set_value(value)

    def dem_result_get(self,file_path):
        if not file_path:
            return
        self.load_image(file_path)

    def dem_finished(self):
        self.view.progress_bar_dem.set_label("已完成！")
        self.view.progress_bar_dem.close()

    def dem_stopped(self):
        self.dem.stopped=True


    """生成DSM"""

    def dsm_get(self):
        # 打开对话框
        self.view.dsm_dialog.open()
        # 创建字典储存文件名和对应的类别信息
        params = {}
        for file_name in self.model.point_clouds.keys():
            params[file_name] = None
        # 在滤波窗口添加信息
        self.view.dsm_dialog.add_items(params)

    def dsm_accepted(self):
        # 从对话框获取参数
        params = self.view.dsm_dialog.params_get()
        # 如果没有选中文件直接返回
        if params.get('file_name') is None:
            self.show_message("没有选择文件！")
            return
        if not params['file_path']:
            self.show_message("没有选择保存路径！")
            return
        # 进度条窗口显示
        self.view.progress_bar_dsm.set_value(0)
        self.view.progress_bar_dsm.set_window_title("DSM")
        self.view.progress_bar_dsm.open()
        self.view.progress_bar_dsm.closed.connect(partial(self.dsm_stopped))
        # 获取参数
        name = params['file_name']
        las = self.model.point_clouds[name]
        params['las'] = las
        """点击按钮，启动多线程计算"""
        self.dsm = DsmGet(params)
        self.dsm.progress_updated.connect(partial(self.dsm_update_progress))  # 连接进度信号
        self.dsm.result_signal.connect(partial(self.dsm_result_get))  # 参数发送
        self.dsm.finished_signal.connect(partial(self.dsm_finished))  # 计算完成信号
        self.dsm.start()

    def dsm_update_progress(self,value):
        self.view.progress_bar_dsm.set_value(value)

    def dsm_result_get(self,file_path):
        if not file_path:
            return
        self.load_image(file_path)

    def dsm_finished(self):
        self.view.progress_bar_dsm.set_label("已完成！")
        self.view.progress_bar_dsm.close()

    def dsm_stopped(self):
        self.dsm.stopped=True

    """生成CHM"""

    def chm_get(self):
        # 打开对话框
        self.view.chm_dialog.open()
        # 创建字典储存文件名和对应的类别信息
        params = {}
        for file_name in self.model.point_clouds.keys():
            params[file_name] = None
        # 在滤波窗口添加信息
        self.view.chm_dialog.add_items(params)

    def chm_accepted(self):
        # 从对话框获取参数
        params = self.view.chm_dialog.params_get()
        # 如果没有选中文件直接返回
        if params.get('file_name') is None:
            self.show_message("没有选择文件！")
            return
        if not params['file_path'] :
            self.show_message("没有选择文件路径！")
            return
        # 进度条窗口显示
        self.view.progress_bar_chm.set_value(0)
        self.view.progress_bar_chm.set_window_title("CHM")
        self.view.progress_bar_chm.open()
        self.view.progress_bar_chm.closed.connect(partial(self.chm_stopped))
        # 获取参数
        name = params['file_name']
        las = self.model.point_clouds[name]
        params['las'] = las
        """点击按钮，启动多线程计算"""
        self.chm = ChmGet(params)
        self.chm.progress_updated.connect(partial(self.chm_update_progress))  # 连接进度信号
        self.chm.result_signal.connect(partial(self.chm_result_get))  # 参数发送
        self.chm.finished_signal.connect(partial(self.chm_finished))  # 计算完成信号
        self.chm.start()

    def chm_update_progress(self,value):
        self.view.progress_bar_chm.set_value(value)

    def chm_result_get(self,file_path):
        if not file_path:
            return
        self.load_image(file_path)

    def chm_finished(self):
        self.view.progress_bar_chm.set_label("已完成！")
        self.view.progress_bar_chm.close()

    def chm_stopped(self):
        self.chm.stopped=True

    """点云归一化"""

    def normalize_points(self):
        # 打开对话框
        self.view.normalization_dialog.open()
        # 创建字典储存文件名和对应的类别信息
        params_point_cloud = {}
        params_image={}
        for file_name in self.model.point_clouds.keys():
            params_point_cloud[file_name] = None
        for file_name in self.model.images.keys():
            params_image[file_name] = self.model.image_attribute[file_name]["file_path"]
        # 在滤波窗口添加信息
        self.view.normalization_dialog.add_items(params_point_cloud=params_point_cloud, params_image=params_image)

    def normalize_accepted(self):
        # 从对话框获取参数
        params = self.view.normalization_dialog.params_get()
        # 如果没有选中文件直接返回
        if params.get('file_name') is None:
            self.show_message("没有选择文件！")
            return
        if not params['file_path_dem']:
            self.show_message("没有选择DEM文件！")
            return
        if not params['file_path_save']:
            self.show_message("没有选择保存路径！")
            return
        # 获取参数
        name = params['file_name']
        las = self.model.point_clouds[name]
        params['las'] = las
        # 进度条窗口显示
        self.view.progress_bar_normalization.set_value(0)
        self.view.progress_bar_normalization.set_window_title("点云归一化")
        self.view.progress_bar_normalization.open()
        self.view.progress_bar_normalization.closed.connect(partial(self.normalize_stopped))
        """点击按钮，启动多线程计算"""
        self.normalization =Normalization(params)
        self.normalization.progress_updated.connect(partial(self.normalize_update_progress))  # 连接进度信号
        self.normalization.result_signal.connect(partial(self.normalize_result_get))  # 参数发送
        self.normalization.finished_signal.connect(partial(self.normalize_finished))  # 计算完成信号
        self.normalization.start()

    def normalize_update_progress(self,value):
        self.view.progress_bar_normalization.set_value(value)

    def normalize_result_get(self,file_path):
        if not file_path:
            return
        self.load_point_cloud(file_path=file_path)

    def normalize_finished(self):
        self.view.progress_bar_normalization.set_label("已完成！")
        self.view.progress_bar_normalization.close()

    def normalize_stopped(self):
        self.normalization.stopped=True

    """植被覆盖度"""

    def canopy_cover_apply(self):
        # 打开对话框
        self.view.canopy_cover_dialog.open()
        # 创建字典储存文件名和对应的类别信息
        params = {}
        for file_name in self.model.point_clouds.keys():
            params[file_name] = None
        # 在滤波窗口添加信息
        self.view.canopy_cover_dialog.add_items(params)

    def canopy_cover_accepted(self):
        # 从对话框获取参数
        params = self.view.canopy_cover_dialog.params_get()
        # 如果没有选中文件直接返回
        if params.get('file_name') is None:
            self.show_message("没有选择文件！")
            return
        if not params['file_path'] :
            self.show_message("没有选择保存路径！")
            return
        # 获取参数
        name = params['file_name']
        las = self.model.point_clouds[name]
        params['las'] = las
        # 进度条窗口显示
        self.view.progress_bar_canopy.set_value(0)
        self.view.progress_bar_canopy.set_window_title("植被覆盖程度")
        self.view.progress_bar_canopy.open()
        self.view.progress_bar_canopy.closed.connect(partial(self.canopy_stopped))
        """点击按钮，启动多线程计算"""
        self.canopy_cover = CanopyCover(params)
        self.canopy_cover.progress_updated.connect(partial(self.canopy_cover_update_progress))  # 连接进度信号
        self.canopy_cover.result_signal.connect(partial(self.canopy_cover_result_get))  # 参数发送
        self.canopy_cover.finished_signal.connect(partial(self.canopy_cover_finished))  # 计算完成信号
        self.canopy_cover.start()

    def canopy_cover_update_progress(self,value):
        self.view.progress_bar_canopy.set_value(value)

    def canopy_cover_result_get(self,file_path):
        if not file_path:
            return
        self.load_image(file_path)

    def canopy_cover_finished(self):
        self.view.progress_bar_canopy.set_label("已完成！")
        self.view.progress_bar_canopy.close()

    def canopy_stopped(self):
        self.canopy_cover.stopped=True

    """空隙率和叶面积"""

    def gp_and_lai_apply(self):
        # 打开对话框
        self.view.gp_and_lai_dialog.open()
        # 创建字典储存文件名和对应的类别信息
        params = {}
        for file_name in self.model.point_clouds.keys():
            params[file_name] = None
        # 在滤波窗口添加信息
        self.view.gp_and_lai_dialog.add_items(params)

    def gp_and_lai_accepted(self):
        # 从对话框获取参数
        params = self.view.gp_and_lai_dialog.params_get()
        # 如果没有选中文件直接返回
        if params.get('file_name') is None:
            self.show_message("没有选择文件！")
            return
        if not params['file_path'] :
            self.show_message("没有选择保存路径！")
            return
        # 获取参数
        name = params['file_name']
        las = self.model.point_clouds[name]
        params['las'] = las
        # 进度条窗口显示
        self.view.progress_bar_gp_and_lai.set_value(0)
        self.view.progress_bar_gp_and_lai.set_window_title("空隙率和叶面指数")
        self.view.progress_bar_gp_and_lai.open()
        self.view.progress_bar_gp_and_lai.closed.connect(partial(self.gp_and_lai_stopped))
        """点击按钮，启动多线程计算"""
        self.gp_and_lai = GapAndLAL(params)
        self.gp_and_lai.progress_updated.connect(partial(self.gp_and_lai_update_progress))  # 连接进度信号
        self.gp_and_lai.result_signal.connect(partial(self.gp_and_lai_result_get))  # 参数发送
        self.gp_and_lai.finished_signal.connect(partial(self.gp_and_lai_finished))  # 计算完成信号
        self.gp_and_lai.start()

    def gp_and_lai_update_progress(self,value):
        self.view.progress_bar_gp_and_lai.set_value(value)

    def gp_and_lai_result_get(self,file_path):
        if not file_path:
            return
        self.load_image(file_path['gp'])
        self.load_image(file_path['lai'])

    def gp_and_lai_finished(self):
        self.view.progress_bar_gp_and_lai.set_label("已完成！")
        self.view.progress_bar_gp_and_lai.close()

    def gp_and_lai_stopped(self):
        self.gp_and_lai.stopped=True

    """单木分割"""

    def single_wood_division_apply(self):
        # 打开对话框
        self.view.single_wood_dialog.open()
        # 创建字典储存文件名和对应的类别信息
        params = {}
        for file_name in self.model.images.keys():
            params[file_name] = self.model.image_attribute[file_name]['file_path']
        # 在滤波窗口添加信息
        self.view.single_wood_dialog.add_items(params)

    def single_wood_division_accepted(self):
        # 从对话框获取参数
        params = self.view.single_wood_dialog.params_get()
        # 如果没有选中文件直接返回
        if not params['chm_file_path'] :
            self.show_message("没有选择CHM文件！")
            return
        if not params['save_file_path_tif']:
            self.show_message("没有选择保存路径！")
            return
        if not params['save_file_path_shp']:
            self.show_message("没有选择保存路径！")
            return
        # 获取参数
        # name = params['file_name']
        # las = self.model.point_clouds[name]
        # params['las'] = las
        # 进度条窗口显示
        self.view.progress_bar_single.set_value(0)
        self.view.progress_bar_single.set_window_title("单木分割")
        self.view.progress_bar_single.open()
        self.view.progress_bar_single.closed.connect(partial(self.single_stopped))
        """点击按钮，启动多线程计算"""
        self.single_wood_division = SingleWoodDivision(params)
        self.single_wood_division.progress_updated.connect(partial(self.single_wood_division_update_progress))  # 连接进度信号
        self.single_wood_division.result_signal.connect(partial(self.single_wood_division_result_get))  # 参数发送
        self.single_wood_division.finished_signal.connect(partial(self.single_wood_division_finished))  # 计算完成信号
        self.single_wood_division.start()

    def single_wood_division_update_progress(self,value):
        self.view.progress_bar_single.set_value(value)

    def single_wood_division_result_get(self,file_path):
        if not file_path:
            return
        self.load_image(file_path[0])
        self.load_vector(file_path[1])

    def single_wood_division_finished(self):
        self.view.progress_bar_single.set_label("已完成！")
        self.view.progress_bar_single.close()

    def single_stopped(self):
        self.single_wood_division.stopped=True

    """弹木结构参数提取"""

    def extract_tree_param_apply(self):
        # 打开对话框
        self.view.extract_tree_param_dialog.open()
        # 创建字典储存文件名和对应的类别信息
        params = {}
        for file_name in self.model.images.keys():
            params[file_name] = self.model.image_attribute[file_name]['file_path']
        # 在滤波窗口添加信息
        self.view.extract_tree_param_dialog.add_items(params)

    def extract_tree_param_accepted(self):
        # 从对话框获取参数
        params = self.view.extract_tree_param_dialog.params_get()
        # 如果没有选中文件直接返回
        if not params['chm_file_path']:
            self.show_message("没有选择CHM文件！")
            return
        if not params['save_file_path_csv']:
            self.show_message("没有选择保存路径！")
            return
        # 获取参数
        # name = params['file_name']
        # las = self.model.point_clouds[name]
        # params['las'] = las
        # 进度条窗口显示
        self.view.progress_bar_extract.set_value(0)
        self.view.progress_bar_extract.set_window_title("弹木结构参数提取")
        self.view.progress_bar_extract.open()
        self.view.progress_bar_extract.closed.connect(partial(self.extract_stopped))
        """点击按钮，启动多线程计算"""
        self.extract_tree_param = ExtractTreeParameters(params)
        self.extract_tree_param.progress_updated.connect(partial(self.extract_tree_param_update_progress))  # 连接进度信号
        self.extract_tree_param.result_signal.connect(partial(self.extract_tree_param_result_get))  # 参数发送
        self.extract_tree_param.finished_signal.connect(partial(self.extract_tree_param_finished))  # 计算完成信号
        self.extract_tree_param.start()

    def extract_tree_param_update_progress(self, value):
        self.view.progress_bar_extract.set_value(value)

    def extract_tree_param_result_get(self, file_path):
        if not file_path or not os.path.exists(file_path):
            return

        system_platform = platform.system()

        try:
            if system_platform == "Windows":
                os.startfile(file_path)
            elif system_platform == "Darwin":  # macOS
                subprocess.call(["open", file_path])
            else:  # Linux and other
                subprocess.call(["xdg-open", file_path])
            self.show_message(f"已使用系统默认软件打开文件：\n"
                              f"{file_path}","提示")
        except Exception as e:
            self.show_message(f"打开文件失败：\n{e}")


    def extract_tree_param_finished(self):
        self.view.progress_bar_extract.set_label("已完成！")
        self.view.progress_bar_extract.close()

    def extract_stopped(self):
        self.extract_tree_param.stopped = True

    """"保存文件时去除后缀"""
    @staticmethod
    def remove_las_tif_suffix(filename):
        # 获取不带扩展名的文件名
        base, ext = os.path.splitext(filename)
        if ext.lower() in ['.las', '.tif']:
            return base
        return filename


if __name__ == "__main__":
    app = QApplication(sys.argv)
    model = PointCloudModel()
    view = MyMainWindow()
    controller = PointCloudController(model, view)
    view.show()
    sys.exit(app.exec())

    # 在主线程中持续渲染
    # while True:
    #     view.vis_render()
    #     QCoreApplication.processEvents()  # 处理 Qt 的事件循环
