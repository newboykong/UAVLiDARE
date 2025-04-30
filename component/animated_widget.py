from PySide6.QtCore import Qt, QTimer, QObject
from PySide6.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QFrame
import sys
from PySide6.QtCore import QObject, QPropertyAnimation, QEasingCurve
from functools import partial

class AnimatedWidth(QObject):
    def __init__(self, widget, min_width, max_width, duration, button, *args):
        super().__init__()

        self.widget = widget  # 需要动画效果的控件
        self.buttons = args  # 额外按钮控件，用来启动动画
        self.button = button
        self.min_width = min_width  # 控件最小宽度
        self.max_width = max_width  # 控件最大宽度
        self.duration = duration  # 动画持续时间（毫秒）
        self.is_collapsed = True  # 默认是折叠状态

        # 设置控件的初始宽度为最小宽度（折叠状态）
        self.widget.setMinimumWidth(self.min_width)
        self.widget.setMaximumWidth(self.min_width)

        # 创建 QPropertyAnimation 动画
        self.animation = QPropertyAnimation(self.widget, b"minimumWidth")  # 动画目标是控件的 minimumWidth
        self.animation.setDuration(self.duration)  # 设置动画的持续时间
        self.animation.setStartValue(self.min_width)  # 动画开始时控件的宽度
        self.animation.setEndValue(self.max_width)  # 动画结束时控件的宽度
        self.animation.setEasingCurve(QEasingCurve.InOutQuad)  # 设置动画曲线，使动画更加平滑

        # 使用 partial 绑定按钮的点击事件
        self.button.clicked.connect(partial(self.start_animation))
        for button in self.buttons:
            button.clicked.connect(partial(self.expend))

    def start_animation(self, checked=False):
        """启动动画，切换展开与折叠状态"""
        if self.animation.state() == QPropertyAnimation.Running:
            return  # 如果动画正在运行，不再启动新动画

        # 根据折叠状态来确定目标宽度
        target_width = self.max_width if self.is_collapsed else self.min_width

        # 设置动画的起始和结束宽度
        self.animation.setStartValue(self.widget.width())  # 动画从当前控件的宽度开始
        self.animation.setEndValue(target_width)  # 动画结束时到目标宽度

        # 启动动画
        self.animation.start()

        # 切换折叠状态
        self.is_collapsed = not self.is_collapsed

    def expend(self, checked=False):
        """当按钮点击时，展开控件"""
        if self.is_collapsed:
            self.start_animation()
