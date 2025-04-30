@echo off
:: 激活 Anaconda 环境
call D:\anaconda\Scripts\activate.bat pointCloud

:: 进入项目目录
cd /d D:\pointCloud\src\

python main.py

:: 等待查看输出
pause