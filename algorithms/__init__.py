import sys
import os

# 将包含 icon_rc.py 文件的目录添加到 sys.path
sys.path.append(os.path.dirname(__file__))
from algorithms.denoisisng import statistical_outlier_removal_kd