import json
import sys
import laspy
import numpy as np
from pyvistaqt import QtInteractor
import pyvista as pv
from PySide6.QtWidgets import QApplication, QVBoxLayout, QWidget, QMainWindow
# from PySide6.QtCore import QTimer
from PySide6.QtCore import QMutex, QObject, Signal
import os

# 解决json文件打包时缺失的问题
def get_resource_path(filename):
    """获取打包后的资源文件的路径"""
    if getattr(sys, 'frozen', False):  # Nuitka 或 PyInstaller 打包的可执行文件
        return os.path.join(sys._MEIPASS, filename)  # 拼接 _MEIPASS 目录
    return os.path.join(os.path.dirname(__file__), filename)  # 源代码运行时拼接当前目录


class FixedQtInteractor(QtInteractor):
    """完全兼容的修复版本"""
    _render_signal = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)  # 只调用QtInteractor的初始化

        # 确保所有必要属性存在
        self._mutex = QMutex()
        self._pyside6_workaround_render = lambda: None

        # 信号连接
        self._render_signal.connect(self._safe_render)

    def _safe_render(self):
        """线程安全的实际渲染"""
        if self._mutex.tryLock(100):
            try:
                if hasattr(self, 'ren_win'):
                    self.ren_win.Render()
                else:
                    self.render()
                QApplication.processEvents()
            finally:
                self._mutex.unlock()

    def request_render(self):
        """外部调用的安全接口"""
        if hasattr(self, '_render_signal'):
            self._render_signal.emit()
        else:
            self._safe_render()




class PyvistaWindow(QWidget):
    def __init__(self, parent=None,las_file_path=None):
        super().__init__(parent)

        # 读取 LAS 文件
        if las_file_path:
            self.las = laspy.read(las_file_path)
            self.points = np.vstack((self.las.x, self.las.y, self.las.z)).transpose()
        # self.setWindowFlags(Qt.FramelessWindowHint)  # 无边框窗口

        # 创建窗口
        self.setWindowTitle("PyVista with LiDAR Data")
        self.setGeometry(100, 100, 800, 600)

        # 创建一个 QWidget 用于布局
        self.layout = QVBoxLayout(self)

        # 正确初始化交互器（关键修改）
        self.plotter = FixedQtInteractor(None)  # 不直接传递parent
        self.plotter.interactor.setParent(self)  # 后设置parent
        self.layout.addWidget(self.plotter.interactor)
        self.layout.setContentsMargins(0, 0, 0, 0)

        # 添加以下设置
        self.plotter.enable_anti_aliasing('fxaa')  # 使用性能更好的抗锯齿
        # self.plotter.set_use_parallel_projection(True)  # 平行投影性能更好
        self.plotter.set_background('black')

        # 添加坐标轴
        self.axes_actor=self.plotter.add_axes(color="white")  # 在左下角添加坐标轴

        # 将点云数据添加到 PyVista
        if las_file_path:
            self.points_show_by_elevation(self.las)

        # # 定时刷新
        # self.render_timer = QTimer()
        # self.render_timer.timeout.connect(self.force_render)
        # self.render_timer.start(100)

    def points_show_by_classification(self, las, camera_params=None,color_dict=None,point_size=3):
        # 获取las文件的x,y,z坐标
        points = np.vstack((las.x, las.y, las.z)).T

        # 清除之前的点云数据
        self.plotter.clear()

        # 创建一个 PyVista 点云对象
        point_cloud = pv.PolyData(points)
        self.plotter.enable_anti_aliasing("fxaa")  # 禁用抗锯齿
        # 总结：
        # FXAA：快速且性能友好，但效果稍差。
        # SSAA：效果最佳，但需要较高的性能开销。
        # MSAA：在性能和效果之间做出了平衡，适用于大部分场景。
        # 你可以根据需求选择不同的抗锯齿方法。如果想禁用抗锯齿，可以使用
        # None。

        # 存储图例项
        legend_entries = []

        # 获取las的分类信息
        classification = las.classification
        classification = np.atleast_1d(classification)  # 确保是 1D 数组

        # 设置点云颜色（根据分类信息）
        point_cloud["Classification"] = classification

        # 加载配置文件，获取类别序号和类别名的对应关系
        classification_path = get_resource_path("classification_mapping.json")
        with open(classification_path, "r", encoding="utf-8") as f:
            classification_mapping = json.load(f)

        # 加载配置文件，获取序号与颜色之间的对应关系
        color_path = get_resource_path("color_mapping.json")
        with open(color_path, "r", encoding="utf-8") as f:
            color_mapping = json.load(f)

        if color_dict is None:
            # 根据标签为点云着色
            for i in np.unique(classification):
                mask = np.where(classification == i)[0]  # 获取索引
                sub_cloud = point_cloud.extract_points(mask)
                try:
                    color = color_mapping[f"{i}"]
                    classification_name = classification_mapping[f"{i}"]["english_name"]
                except KeyError:
                    color = color_mapping["21-255"]
                    classification_name = classification_mapping["21-255"]["name"]
                self.plotter.add_mesh(sub_cloud, color=color, point_size=int(point_size))
                legend_entries.append([f'Class {i}: {classification_name}', color])  # 手动存储图例项
        else:
            for cls_id,paras in color_dict.items():
                if paras["state"]=='选中':
                    classification_name = classification_mapping[f"{cls_id}"]["english_name"]
                    mask = np.where(classification == int(cls_id))[0]  # 获取索引
                    sub_cloud = point_cloud.extract_points(mask)
                    self.plotter.add_mesh(sub_cloud, color=paras["color"], point_size=int(point_size))
                    legend_entries.append([f"Class {cls_id}: {classification_name}", paras['color']])  # 手动存储图例项

        # 添加图例
        # self.plotter.add_legend(legend_entries)

        self.plotter.add_legend(
            legend_entries,  # 图例项
            # size=(0.5, 0.05),  # (宽度, 高度) 0~1
            # bcolor="white",  # 背景颜色
            # border=True  # 是否显示边框
        )

        if camera_params:
            self.plotter.camera_position = camera_params
        else:
            # 如果需要恢复到默认相机位置
            self.plotter.reset_camera()
        # 添加坐标轴
        self.axes_actor = self.plotter.add_axes(color="white")  # 在左下角添加坐标轴
        # 强制渲染
        self.force_render()

    def points_show_by_elevation(self,las_or_points,camera_params=None,point_size=3):
        try:
            # 假设加载的是las数据
            las = las_or_points
            # 获取las文件的x,y,z坐标
            points = np.vstack((las.x, las.y, las.z)).T
        except Exception as e:
            # 假设加载的是points数据
            points = las_or_points

        # 清除之前的点云数据
        self.plotter.clear()
        """
        将点云数据添加到 PyVista Plotter 中，并根据高程设置颜色
        """
        # 创建一个 PyVista 点云对象
        point_cloud = pv.PolyData(points)

        self.plotter.enable_anti_aliasing("fxaa")  # 禁用抗锯齿
        # 总结：
        # FXAA：快速且性能友好，但效果稍差。
        # SSAA：效果最佳，但需要较高的性能开销。
        # MSAA：在性能和效果之间做出了平衡，适用于大部分场景。
        # 你可以根据需求选择不同的抗锯齿方法。如果想禁用抗锯齿，可以使用
        # None。

        # 通过 Z 值来着色（使用点的 Z 坐标作为颜色映射的依据）
        point_cloud.point_data['高程'] = points[:, 2]  # 将 Z 值作为高程字段
        # point_cloud.set_active_scalars(None)
        # 使用高程值来着色，设置颜色映射
        self.plotter.add_mesh(point_cloud, scalars="高程", cmap="viridis", point_size=int(point_size),
                              render_points_as_spheres=True, show_scalar_bar=False)
        # 添加颜色条，并设置字体大小和标签颜色
        self.plotter.add_scalar_bar(
            title="elevation",
            color='white',
            vertical=False,
            title_font_size=20,
            label_font_size=18,
        )
        if camera_params:
            self.plotter.camera_position = camera_params
        else:
            # 如果需要恢复到默认相机位置
            self.plotter.reset_camera()


        # 添加坐标轴
        self.axes_actor=self.plotter.add_axes(color="white")  # 在左下角添加坐标轴
        # 强制渲染
        self.force_render()

    def points_show_by_colors(self,las_or_points,camera_params=None,colors=None,point_size=3):
        if colors is None:
            return

        try:
            # 假设加载的是las数据
            las = las_or_points
            # 获取las文件的x,y,z坐标
            points = np.vstack((las.x, las.y, las.z)).T
        except Exception as e:
            # 假设加载的是points数据
            points = las_or_points

        # 清除之前的点云数据
        self.plotter.clear()
        """
        将点云数据添加到 PyVista Plotter 中，并根据高程设置颜色
        """
        # 创建一个 PyVista 点云对象
        point_cloud = pv.PolyData(points)

        self.plotter.enable_anti_aliasing("fxaa")  # 禁用抗锯齿
        # 总结：
        # FXAA：快速且性能友好，但效果稍差。
        # SSAA：效果最佳，但需要较高的性能开销。
        # MSAA：在性能和效果之间做出了平衡，适用于大部分场景。
        # 你可以根据需求选择不同的抗锯齿方法。如果想禁用抗锯齿，可以使用
        # None。

        # 创建 PyVista 点云对象并着色
        point_cloud.point_data['colors'] = colors
        self.plotter.add_mesh(point_cloud, scalars="colors", rgb=True, point_size=int(point_size), render_points_as_spheres=True,
                              show_scalar_bar=False)
        # 添加颜色条，并设置字体大小和标签颜色
        self.plotter.add_scalar_bar(
            title="denoising",
            color='white',
            background_color='white',
            vertical=False,
            label_font_size=18,
        )
        if camera_params:
            self.plotter.camera_position = camera_params
        else:
            # 如果需要恢复到默认相机位置
            self.plotter.reset_camera()
        # 添加坐标轴
        self.axes_actor = self.plotter.add_axes(color="white")  # 在左下角添加坐标轴
        # 强制渲染
        self.force_render()

    # 替换原来的force_render实现
    def force_render(self):
        if hasattr(self, 'plotter'):
            self.plotter.request_render()



if __name__ == "__main__":
    # 输入 LAS 文件路径
    file_path = "../pointCloudData/测试数据—林业/Forest_test.las"  # 替换为实际的文件路径

    # 启动应用
    app = QApplication(sys.argv)
    window = PyvistaWindow(las_file_path=file_path)
    window.show()
    sys.exit(app.exec())
