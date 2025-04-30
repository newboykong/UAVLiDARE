@echo off
:: 激活 Anaconda 环境
call D:\anaconda\Scripts\activate.bat pointCloud

:: 进入项目目录
cd /d D:\pointCloud\

:: 创建必要的 Qt 配置
echo [Paths] > qt.conf
echo Prefix = . >> qt.conf
echo Plugins = PySide6/plugins >> qt.conf

:: 执行 Nuitka 打包命令（兼容旧版本）
python -m nuitka --standalone --onefile ^
    --enable-plugin=pyside6 ^
    --include-qt-plugins=sensible ^
    --include-package=pyvista ^
    --include-package=pyvistaqt ^
    --include-package=algorithms ^
    --include-package=ui ^
    --include-package=component ^
    --include-package=matplotlib ^
    --include-module=vtk ^
    --include-module=vtkmodules.qt.QVTKRenderWindowInteractor ^
    --include-module=vtkmodules.util.numpy_support ^
    --include-module=PySide6.QtOpenGL ^
    --include-module=PySide6.QtOpenGLWidgets ^
    --include-data-files=./src/classification_mapping.json=classification_mapping.json ^
    --include-data-files=./src/color_mapping.json=color_mapping.json ^
    --include-data-files=./ui/icon_rc.py=icon_rc.py ^
    --include-qt-plugins=platforms,styles ^
    --output-dir=dist ^
    --output-filename=myapp.exe ^
    --remove-output ^
    --follow-imports ^
    --windows-console-mode=disable ^
    --assume-yes-for-downloads ^
    ./src/main.py

:: 打开日志查看（可选）
rem notepad log.txt

:: 等待查看输出
pause

::    --windows-console-mode=disable ^
::    --include-data-files=./src/proj.db=./proj.db ^


