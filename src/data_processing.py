import numpy as np
from PySide6.QtCore import QThread, Signal

from algorithms.canopy_cover import canopy_cover
from algorithms.chm import chm_get
from algorithms.dem import dem_get
from algorithms.denoisisng import statistical_outlier_removal_kd
from algorithms.dsm import dsm_get
from algorithms.filtering import pmf_filter
from algorithms.gp_and_lai import gp_and_lai
from algorithms.normalization import normalization
from algorithms.single_wood_division import single_wood_division
from algorithms.extract_tree_parameters import extract_tree_parameters

"""去噪"""


class DenoisingPointCloud(QThread):
    progress_updated = Signal(int)  # 进度信号
    finished_signal = Signal()  # 计算完成信号
    result_signal = Signal(np.ndarray, np.ndarray)  # 结果信号，传递 `filtered_points` 和 `filtered_points_index`



    def __init__(self, denoising_type, params: dict):
        super().__init__()
        self.denoising_type = denoising_type
        self.params = params
        self.stopped = False

    def run(self):
        if self.denoising_type == '统计去噪':
            points = self.params["points"]
            k_neighbors = self.params["k_neighbors"]
            std_ratio = self.params["std_ratio"]
            filter_points, filter_points_index = statistical_outlier_removal_kd(points,
                                                                            k_neighbors,
                                                                            std_ratio,
                                                                            self.progress_updated,self.should_stop)

            self.result_signal.emit(filter_points, filter_points_index)
            self.finished_signal.emit()  # 计算完成信号

    def should_stop(self):
        return self.stopped


"""滤波"""


class FilterPointCloud(QThread):
    progress_updated = Signal(int)  # 进度信号
    finished_signal = Signal()  # 计算完成信号
    result_signal = Signal(str, object)  # 结果信号，传递 `filtered_points` 和 `filtered_points_index`


    def __init__(self, params: dict):
        super().__init__()
        self.params = params
        self.filter_type = self.params["filter_type"]
        self.stopped = False


    def run(self):
        if self.filter_type == '形态学滤波':
            las = self.params["las"]
            grid_size = float(self.params["grid_size"])
            dh_min = float(self.params["dh_min"])
            dh_max = float(self.params["dh_max"])
            s = float(self.params["s"])
            iterations = int(self.params["iterations"])
            cls_id = self.params["cls_id"]
            las = pmf_filter(las, grid_size=(grid_size, -grid_size), dh_min=dh_min, dh_max=dh_max, s=s,
                                     iterations=iterations,
                                     progress_updated=self.progress_updated, cls_id=cls_id,stop_callback=self.should_stop)


            if self.stopped:
                self.result_signal.emit(None,None)
            else:
                self.result_signal.emit(self.params['file_name'], las)
            self.finished_signal.emit()  # 计算完成信号
            self.stopped = False

    def should_stop(self):
        return self.stopped


"""DEM"""


class DemGet(QThread):
    progress_updated = Signal(int)  # 进度信号
    finished_signal = Signal()  # 计算完成信号
    result_signal = Signal(object)  # 结果信号，传递 `filtered_points` 和 `filtered_points_index`

    def __init__(self, params: dict):
        super().__init__()
        self.params = params
        self.stopped = False

    def run(self):
        las = self.params["las"]
        grid_size = float(self.params["grid_size"])
        file_path = str(self.params["file_path"])
        z_min_tmp = dem_get(las, grid_size=(grid_size, -grid_size), file_path=file_path,
                            progress_updated=self.progress_updated,stop_callback=self.should_stop)
        if self.stopped:
            self.result_signal.emit(None)
        else:
            self.result_signal.emit(file_path)
        self.finished_signal.emit()  # 计算完成信号
        self.stopped = False

    def should_stop(self):
        return self.stopped
"""DSM"""


class DsmGet(QThread):
    progress_updated = Signal(int)  # 进度信号
    finished_signal = Signal()  # 计算完成信号
    result_signal = Signal(object)  # 结果信号，传递 `filtered_points` 和 `filtered_points_index`

    def __init__(self, params: dict):
        super().__init__()
        self.params = params
        self.stopped = False

    def run(self):
        las = self.params["las"]
        grid_size = float(self.params["grid_size"])
        file_path = str(self.params["file_path"])
        z_max_tmp = dsm_get(las, grid_size=(grid_size, -grid_size), file_path=file_path,
                            progress_updated=self.progress_updated,stop_callback=self.should_stop)
        if self.stopped:
            self.result_signal.emit(None)
        else:
            self.result_signal.emit(file_path)
        self.finished_signal.emit()  # 计算完成信号
        self.stopped = False

    def should_stop(self):
        return self.stopped

"""CHM"""


class ChmGet(QThread):
    progress_updated = Signal(int)  # 进度信号
    finished_signal = Signal()  # 计算完成信号
    result_signal = Signal(object)  # 结果信号，传递 `filtered_points` 和 `filtered_points_index`

    def __init__(self, params: dict):
        super().__init__()
        self.params = params
        self.stopped = False

    def run(self):
        las = self.params["las"]
        grid_size = float(self.params["grid_size"])
        file_path = str(self.params["file_path"])
        chm_tmp = chm_get(las, grid_size=(grid_size, -grid_size), file_path=file_path,
                          progress_updated=self.progress_updated,stop_callback=self.should_stop)
        if self.stopped:
            self.result_signal.emit(None)
        else:
            self.result_signal.emit(file_path)
        self.finished_signal.emit()  # 计算完成信号
        self.stopped = False

    def should_stop(self):
        return self.stopped
"""点云归一化"""


class Normalization(QThread):
    progress_updated = Signal(int)  # 进度信号
    finished_signal = Signal()  # 计算完成信号
    result_signal = Signal(object)  # 结果信号，传递 `filtered_points` 和 `filtered_points_index`

    def __init__(self, params: dict):
        super().__init__()
        self.params = params
        self.stopped = False

    def run(self):
        las= self.params["las"]
        dem_path = str(self.params["file_path_dem"])
        file_path = str(self.params["file_path_save"])
        chm_tmp = normalization( las,dem_path=dem_path, file_path=file_path,
                                progress_updated=self.progress_updated,stop_callback=self.should_stop)
        if self.stopped:
            self.result_signal.emit(None)
        else:
            self.result_signal.emit(file_path)
        self.finished_signal.emit()  # 计算完成信号
        self.stopped = False

    def should_stop(self):
        return self.stopped
"""植被覆盖程度"""


class CanopyCover(QThread):
    progress_updated = Signal(int)  # 进度信号
    finished_signal = Signal()  # 计算完成信号
    result_signal = Signal(object)  # 结果信号，传递 `filtered_points` 和 `filtered_points_index`

    def __init__(self, params: dict):
        super().__init__()
        self.params = params
        self.stopped = False

    def run(self):
        las = self.params["las"]
        grid_size = float(self.params["grid_size"])
        file_path = str(self.params["file_path"])
        canopy_cover(las, grid_size=(grid_size, -grid_size), file_path=file_path,
                     progress_updated=self.progress_updated,stop_callback=self.should_stop)
        if self.stopped:
            self.result_signal.emit(None)
        else:
            self.result_signal.emit(file_path)
        self.finished_signal.emit()  # 计算完成信号
        self.stopped = False

    def should_stop(self):
        return self.stopped
"""空隙率和叶面指数"""


class GapAndLAL(QThread):
    progress_updated = Signal(int)  # 进度信号
    finished_signal = Signal()  # 计算完成信号
    result_signal = Signal(object)  # 结果信号，传递 `filtered_points` 和 `filtered_points_index`

    def __init__(self, params: dict):
        super().__init__()
        self.params = params
        self.stopped = False

    def run(self):
        las = self.params["las"]
        grid_size = float(self.params["grid_size"])
        file_path = self.params["file_path"]
        gp_and_lai(las,  grid_size=(grid_size, -grid_size),file_path=file_path,
                   progress_updated=self.progress_updated,stop_callback=self.should_stop)
        if self.stopped:
            self.result_signal.emit(None)
        else:
            self.result_signal.emit(file_path)
        self.finished_signal.emit()  # 计算完成信号
        self.stopped = False

    def should_stop(self):
        return self.stopped
"""单木分割"""


class SingleWoodDivision(QThread):
    progress_updated = Signal(int)  # 进度信号
    finished_signal = Signal()  # 计算完成信号
    result_signal = Signal(object)  # 结果信号，传递 `filtered_points` 和 `filtered_points_index`

    def __init__(self, params: dict):
        super().__init__()
        self.params = params
        self.stopped = False

    def run(self):
        chm = self.params["chm_file_path"]
        file_path = self.params["save_file_path_tif"]
        print(file_path)
        file_path_shp = self.params["save_file_path_shp"]
        # file_path = float(self.params["file_path"])
        single_wood_division(chm_file=chm,file_path=file_path, file_path_shp=file_path_shp, progress_updated=self.progress_updated,stop_callback=self.should_stop)
        if self.stopped:
            self.result_signal.emit(None)
        else:
            self.result_signal.emit([file_path,file_path_shp])
        self.finished_signal.emit()  # 计算完成信号
        self.stopped = False

    def should_stop(self):
        return self.stopped


class ExtractTreeParameters(QThread):
    progress_updated = Signal(int)  # 进度信号
    finished_signal = Signal()  # 计算完成信号
    result_signal = Signal(object)  # 结果信号，传递 `filtered_points` 和 `filtered_points_index`

    def __init__(self, params: dict):
        super().__init__()
        self.params = params
        self.stopped = False

    def run(self):
        chm = self.params["chm_file_path"]
        file_path_csv = self.params["save_file_path_csv"]
        # file_path = float(self.params["file_path"])
        extract_tree_parameters(chm_file=chm,csv_path= file_path_csv,  progress_updated=self.progress_updated,stop_callback=self.should_stop)
        if self.stopped:
            self.result_signal.emit(None)
        else:
            self.result_signal.emit(file_path_csv)
        self.finished_signal.emit()  # 计算完成信号
        self.stopped = False

    def should_stop(self):
        return self.stopped