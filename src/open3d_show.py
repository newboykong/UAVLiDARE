import sys

import laspy
import numpy as np
###################################################################
import open3d as o3d
import win32gui
from PySide6.QtCore import QTimer
from PySide6.QtGui import QWindow
from PySide6.QtWidgets import QVBoxLayout
from PySide6.QtWidgets import (QWidget,
                               QApplication)




class Open3dWindow(QWidget):
    def __init__(self, las_file_path=None):
        super().__init__()

        # 读取 LAS 文件
        self.las_file_path = las_file_path
        if las_file_path:
            self.las = laspy.read(las_file_path)
            self.points = np.vstack((self.las.x, self.las.y, self.las.z)).transpose()
        # self.setWindowFlags(Qt.FramelessWindowHint)  # 无边框窗口


        # 创建窗口
        self.setWindowTitle("Open3d with LiDAR Data")
        self.setGeometry(100, 100, 800, 600)

        # 创建一个 QWidget 用于布局
        self.layout = QVBoxLayout(self)

        # 创建 Open3D 渲染窗口，visible=False 避免窗口闪烁
        self.vis = o3d.visualization.Visualizer()
        self.vis.create_window(window_name="Open3D", width=1024, height=768, visible=False)

        # 获取默认的相机参数
        self.view_control = self.vis.get_view_control()

        # 修改背景颜色（RGB 格式，范围 0.0 到 1.0）
        render_option = self.vis.get_render_option()
        render_option.background_color = [0, 0, 0]  # 深蓝色背景

        # 嵌入 Open3D 窗口
        hwnd = win32gui.FindWindow(None, "Open3D")
        if hwnd == 0:
            print("无法找到 Open3D 渲染窗口")
            return

        class_name = win32gui.GetClassName(hwnd)
        winid = win32gui.FindWindow(class_name, None)
        sub_window = QWindow.fromWinId(winid)
        displayer = QWidget.createWindowContainer(sub_window)
        self.layout.addWidget(displayer)

        if las_file_path:
            self.points_show(self.las)



        # 使用定时器定期刷新窗口，避免必须拖动窗口才更新
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.vis_render)
        self.timer.start(30)  # 30ms 刷新一次



    def points_show(self, las,camera_params=None):
        # 从las文件获取x,y,z坐标
        points = np.vstack((las.x, las.y, las.z)).transpose()
        # 转换为 Open3D 点云对象
        open3d_points = o3d.geometry.PointCloud()
        open3d_points.points = o3d.utility.Vector3dVector(points)
        # 移除之前的点云，添加新点云
        self.vis.clear_geometries()

        self.vis.add_geometry(open3d_points)
        # 设置相机参数
        self.set_camera_view(open3d_points)

        # 恢复相机参数
        if camera_params is not None:
            # 恢复相机参数
            # self.view_control.convert_from_pinhole_camera_parameters(camera_params)
            pass
        else:
            # self.restore_camera_parameters(open3d_points)
            pass
        # 刷新渲染器
        self.vis_render()

    def vis_render(self):
        # 启动渲染循环
        self.vis.poll_events()
        self.vis.update_renderer()

    def closeEvent(self, event):
        # 窗口关闭时销毁 Open3D 渲染窗口
        self.vis.destroy_window()
        event.accept()

    def restore_camera_parameters(self, open3d_points):
        # 创建 Open3D 渲染窗口，visible=False 避免窗口闪烁
        vis = o3d.visualization.Visualizer()
        vis.create_window(window_name="Open3D_1", width=1024, height=768)
        vis.add_geometry(open3d_points)
        # 获取默认的相机参数
        view_control = vis.get_view_control()
        camera_params = view_control.convert_to_pinhole_camera_parameters()
        self.view_control.convert_from_pinhole_camera_parameters(camera_params)
        # vis.destroy_window()
        print("hkhjk")
        return

    def set_camera_view(self, point_cloud):
        # 获取点云的边界框
        bbox = point_cloud.get_axis_aligned_bounding_box()

        # 获取边界框的中心和大小
        center = bbox.get_center()
        extent = bbox.get_extent()

        # 打印调试信息，确认边界框位置
        print(f"Center: {center}, Extent: {extent}")

        # 设置相机视角：稍微远离点云
        camera_params = self.view_control.convert_to_pinhole_camera_parameters()

        # 可以根据需要调整相机位置和朝向
        # 偏移两倍的边界框扩展以确保相机远离点云
        camera_params.extrinsic = np.array([
            [1, 0, 0, center[0] + extent[0] * 3],  # X轴方向上偏移三倍扩展
            [0, 1, 0, center[1] + extent[1] * 3],  # Y轴方向上偏移三倍扩展
            [0, 0, 1, center[2] + extent[2] * 3],  # Z轴方向上偏移三倍扩展
            [0, 0, 0, 1]
        ])

        # 应用新的相机参数
        self.view_control.convert_from_pinhole_camera_parameters(camera_params)

        # 如果这段代码无法正常显示，你可以尝试打开 Open3D 的默认视角：
        self.view_control.set_front([0, 0, -1])  # 设置相机前方向
        self.view_control.set_up([0, 1, 0])     # 设置相机的上方向
        self.view_control.set_lookat(center)     # 设置相机朝向点云的中心



if __name__ == "__main__":
    # 输入 LAS 文件路径
    file_path = "../pointCloudData/测试数据—林业/Forest_test.las"  # 替换为实际的文件路径

    # 启动应用
    app = QApplication(sys.argv)
    window = Open3dWindow(file_path)
    window.show()
    sys.exit(app.exec())
