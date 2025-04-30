

class PointCloudModel:
    def __init__(self):
        # 存储点云数据，key是点云的名字，value是las对象
        self.point_clouds = {}
        self.images = {}
        self.vectors = {}
        # 储存点云数据key是点云的名字
        # value[0]是points对象
        # value[1]是颜色数组
        # value[2]是去噪后点云
        self.point_clouds_denoising = {}
        # 储存open3d点云的相机参数
        self.open3d_camera_params = {}
        # 储存pyvista点云的相机参数
        self.pyvista_camera_params = {}
        self.point_attribute = {}
        self.image_attribute = {}
        self.vector_attribute = {}
        # 储存点云的显示方式
        self.point_show_way = {}

    def add_point_cloud(self, name, point_cloud):
        self.point_clouds[name] = point_cloud

    def remove_point_cloud(self, name):
        if name in self.point_clouds:
            del self.point_clouds[name]

    def remove_by_name(self, name):
        if name in self.point_clouds:
            del self.point_clouds[name]
            if name + "-查看" in self.point_clouds_denoising:
                self.remove_by_name(name + "-查看")
        if name in self.point_show_way:
            del self.point_show_way[name]
        if name in self.point_attribute:
            del self.point_attribute[name]
        if name in self.point_clouds_denoising:
            del self.point_clouds_denoising[name]
        if name in self.pyvista_camera_params:
            del self.pyvista_camera_params[name]
        if name in self.open3d_camera_params:
            del self.open3d_camera_params[name]
