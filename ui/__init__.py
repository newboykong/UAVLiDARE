
import sys
import os

# 将包含 icon_rc.py 文件的目录添加到 sys.path
sys.path.append(os.path.dirname(__file__))

# 现在可以导入 icon_rc
import icon_rc

from ui.ui_main_window import Ui_MainWindow as MainWindow

