# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main_window.ui'
##
## Created by: Qt User Interface Compiler version 6.8.3
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QFrame, QHBoxLayout, QHeaderView,
    QLabel, QMainWindow, QPushButton, QSizePolicy,
    QSlider, QSpacerItem, QStackedWidget, QToolButton,
    QTreeWidget, QTreeWidgetItem, QVBoxLayout, QWidget)
import icon_rc

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1006, 559)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setMinimumSize(QSize(0, 0))
        MainWindow.setMaximumSize(QSize(16777215, 16777215))
        MainWindow.setCursor(QCursor(Qt.CursorShape.ArrowCursor))
        MainWindow.setStyleSheet(u"*{\n"
"	border:none;\n"
"	padding:0;\n"
"	margin:0;\n"
"	color:#fff;\n"
"	background-color:transparent;\n"
"	background:none;\n"
"	\n"
"}\n"
"#centerMenuContainer{\n"
"	background-color:#1f232a;\n"
"}\n"
"#leftMenuSubContainer{\n"
"	background-color:#191621;\n"
"}\n"
"#MainWindow{\n"
"	background-color:#1f232a;\n"
"}\n"
"QPushButton{\n"
"	text-align:left;\n"
"	padding:2px 5px;\n"
"}\n"
"#head,#frame_4{\n"
"	background-color:#1f232a;\n"
"}\n"
"\n"
"\n"
"\n"
"\n"
"")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.centralwidget.setMinimumSize(QSize(0, 0))
        self.centralwidget.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.centralwidget.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.centralwidget.setStyleSheet(u"#centralwidget{\n"
"background:transparent;\n"
"}")
        self.horizontalLayout = QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_15 = QVBoxLayout()
        self.verticalLayout_15.setObjectName(u"verticalLayout_15")
        self.verticalLayout_15.setContentsMargins(-1, 0, -1, -1)
        self.headContainer = QWidget(self.centralwidget)
        self.headContainer.setObjectName(u"headContainer")
        self.headContainer.setMinimumSize(QSize(0, 30))
        self.headContainer.setMaximumSize(QSize(16777215, 16777215))
        self.headContainer.setStyleSheet(u"\n"
"background-color:#16191d;\n"
"\n"
"")
        self.horizontalLayout_6 = QHBoxLayout(self.headContainer)
        self.horizontalLayout_6.setSpacing(0)
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.horizontalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.menu = QHBoxLayout()
        self.menu.setSpacing(0)
        self.menu.setObjectName(u"menu")
        self.menu.setContentsMargins(6, 0, 0, -1)
        self.menu_show = QPushButton(self.headContainer)
        self.menu_show.setObjectName(u"menu_show")
        self.menu_show.setMaximumSize(QSize(16777215, 16777215))
        font = QFont()
        font.setPointSize(10)
        self.menu_show.setFont(font)
        self.menu_show.setStyleSheet(u"QPushButton {\n"
"    border-radius: 10px;\n"
"    padding: 5px;  /* \u6dfb\u52a0\u4e00\u4e9b\u5185\u8fb9\u8ddd\uff0c\u8ba9\u6309\u94ae\u66f4\u7f8e\u89c2 */\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: #015371;\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    padding-left: 3px;\n"
"    padding-top: 3px;\n"
"}")
        icon = QIcon()
        icon.addFile(u":/icon/icon/menu.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.menu_show.setIcon(icon)
        self.menu_show.setIconSize(QSize(25, 25))

        self.menu.addWidget(self.menu_show)

        self.file = QToolButton(self.headContainer)
        self.file.setObjectName(u"file")
        self.file.setFont(font)
        self.file.setStyleSheet(u"QToolButton {\n"
"    border-radius: 10px;\n"
"    padding: 5px;  /* \u6dfb\u52a0\u4e00\u4e9b\u5185\u8fb9\u8ddd\uff0c\u8ba9\u6309\u94ae\u66f4\u7f8e\u89c2 */\n"
"}\n"
"\n"
"QToolButton:hover {\n"
"    background-color: #015371;\n"
"}\n"
"\n"
"QToolButton:pressed {\n"
"    padding-left: 3px;\n"
"    padding-top: 3px;\n"
"	background-color: #015371;\n"
"}\n"
"QToolButton::menu-indicator {\n"
"                                image: none;\n"
"}")

        self.menu.addWidget(self.file)

        self.processing = QToolButton(self.headContainer)
        self.processing.setObjectName(u"processing")
        self.processing.setFont(font)
        self.processing.setStyleSheet(u"QToolButton {\n"
"    border-radius: 10px;\n"
"    padding: 5px;  /* \u6dfb\u52a0\u4e00\u4e9b\u5185\u8fb9\u8ddd\uff0c\u8ba9\u6309\u94ae\u66f4\u7f8e\u89c2 */\n"
"}\n"
"\n"
"QToolButton:hover {\n"
"    background-color: #015371;\n"
"}\n"
"\n"
"QToolButton:pressed {\n"
"    padding-left: 3px;\n"
"    padding-top: 3px;\n"
"	background-color: #015371;\n"
"}\n"
"QToolButton::menu-indicator {\n"
"                                image: none;\n"
"}")

        self.menu.addWidget(self.processing)

        self.forestry_parameter_extraction = QToolButton(self.headContainer)
        self.forestry_parameter_extraction.setObjectName(u"forestry_parameter_extraction")
        self.forestry_parameter_extraction.setFont(font)
        self.forestry_parameter_extraction.setStyleSheet(u"QToolButton {\n"
"    border-radius: 10px;\n"
"    padding: 5px;  /* \u6dfb\u52a0\u4e00\u4e9b\u5185\u8fb9\u8ddd\uff0c\u8ba9\u6309\u94ae\u66f4\u7f8e\u89c2 */\n"
"}\n"
"\n"
"QToolButton:hover {\n"
"    background-color: #015371;\n"
"}\n"
"\n"
"QToolButton:pressed {\n"
"    padding-left: 3px;\n"
"    padding-top: 3px;\n"
"	background-color: #015371;\n"
"}\n"
"QToolButton::menu-indicator {\n"
"                                image: none;\n"
"}")

        self.menu.addWidget(self.forestry_parameter_extraction)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.menu.addItem(self.horizontalSpacer)


        self.horizontalLayout_6.addLayout(self.menu)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setSpacing(10)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.minimize_window_button = QPushButton(self.headContainer)
        self.minimize_window_button.setObjectName(u"minimize_window_button")
        self.minimize_window_button.setMaximumSize(QSize(16777215, 30))
        self.minimize_window_button.setStyleSheet(u"QPushButton {\n"
"    border-radius: 10px;\n"
"    padding: 5px;  /* \u6dfb\u52a0\u4e00\u4e9b\u5185\u8fb9\u8ddd\uff0c\u8ba9\u6309\u94ae\u66f4\u7f8e\u89c2 */\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: #015371;\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    padding-left: 3px;\n"
"    padding-top: 3px;\n"
"}")
        icon1 = QIcon()
        icon1.addFile(u":/icon/icon/minus.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.minimize_window_button.setIcon(icon1)
        self.minimize_window_button.setIconSize(QSize(20, 20))

        self.horizontalLayout_5.addWidget(self.minimize_window_button)

        self.maximize_window_button = QPushButton(self.headContainer)
        self.maximize_window_button.setObjectName(u"maximize_window_button")
        self.maximize_window_button.setMaximumSize(QSize(16777215, 30))
        self.maximize_window_button.setStyleSheet(u"QPushButton {\n"
"    border-radius: 10px;\n"
"    padding: 5px;  /* \u6dfb\u52a0\u4e00\u4e9b\u5185\u8fb9\u8ddd\uff0c\u8ba9\u6309\u94ae\u66f4\u7f8e\u89c2 */\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: #015371;\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    padding-left: 3px;\n"
"    padding-top: 3px;\n"
"}")
        icon2 = QIcon()
        icon2.addFile(u":/icon/icon/square.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.maximize_window_button.setIcon(icon2)
        self.maximize_window_button.setIconSize(QSize(20, 20))

        self.horizontalLayout_5.addWidget(self.maximize_window_button)

        self.close_window_button = QPushButton(self.headContainer)
        self.close_window_button.setObjectName(u"close_window_button")
        self.close_window_button.setMaximumSize(QSize(16777215, 30))
        self.close_window_button.setStyleSheet(u"QPushButton {\n"
"    border-radius: 10px;\n"
"    padding: 5px;  /* \u6dfb\u52a0\u4e00\u4e9b\u5185\u8fb9\u8ddd\uff0c\u8ba9\u6309\u94ae\u66f4\u7f8e\u89c2 */\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: #015371;\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    padding-left: 3px;\n"
"    padding-top: 3px;\n"
"}")
        icon3 = QIcon()
        icon3.addFile(u":/icon/icon/x.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.close_window_button.setIcon(icon3)
        self.close_window_button.setIconSize(QSize(20, 20))

        self.horizontalLayout_5.addWidget(self.close_window_button)


        self.horizontalLayout_6.addLayout(self.horizontalLayout_5)


        self.verticalLayout_15.addWidget(self.headContainer)

        self.main_body = QHBoxLayout()
        self.main_body.setObjectName(u"main_body")
        self.leftMenuContainer = QWidget(self.centralwidget)
        self.leftMenuContainer.setObjectName(u"leftMenuContainer")
        self.leftMenuContainer.setEnabled(True)
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.leftMenuContainer.sizePolicy().hasHeightForWidth())
        self.leftMenuContainer.setSizePolicy(sizePolicy1)
        self.leftMenuContainer.setMinimumSize(QSize(0, 0))
        self.leftMenuContainer.setMaximumSize(QSize(16777215, 16777215))
        self.leftMenuContainer.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.leftMenuContainer.setStyleSheet(u"background-color:#16191d;\n"
"")
        self.horizontalLayout_3 = QHBoxLayout(self.leftMenuContainer)
        self.horizontalLayout_3.setSpacing(0)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.leftMenuSubContainer = QWidget(self.leftMenuContainer)
        self.leftMenuSubContainer.setObjectName(u"leftMenuSubContainer")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Preferred)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.leftMenuSubContainer.sizePolicy().hasHeightForWidth())
        self.leftMenuSubContainer.setSizePolicy(sizePolicy2)
        self.leftMenuSubContainer.setMinimumSize(QSize(60, 0))
        self.leftMenuSubContainer.setStyleSheet(u"")
        self.verticalLayout_2 = QVBoxLayout(self.leftMenuSubContainer)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.frame_2 = QFrame(self.leftMenuSubContainer)
        self.frame_2.setObjectName(u"frame_2")
        sizePolicy3 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Maximum)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.frame_2.sizePolicy().hasHeightForWidth())
        self.frame_2.setSizePolicy(sizePolicy3)
        self.frame_2.setStyleSheet(u"")
        self.frame_2.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_2.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_4 = QVBoxLayout(self.frame_2)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(5, 5, 6, 6)
        self.open = QPushButton(self.frame_2)
        self.open.setObjectName(u"open")
        self.open.setMaximumSize(QSize(16777215, 16777215))
        self.open.setFont(font)
        self.open.setStyleSheet(u"QPushButton {\n"
"    border-radius: 10px;\n"
"    padding: 5px;  /* \u6dfb\u52a0\u4e00\u4e9b\u5185\u8fb9\u8ddd\uff0c\u8ba9\u6309\u94ae\u66f4\u7f8e\u89c2 */\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: #015371;\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    padding-left: 3px;\n"
"    padding-top: 3px;\n"
"}")
        icon4 = QIcon()
        icon4.addFile(u":/icon/icon/folder.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.open.setIcon(icon4)
        self.open.setIconSize(QSize(25, 25))

        self.verticalLayout_4.addWidget(self.open)

        self.save = QPushButton(self.frame_2)
        self.save.setObjectName(u"save")
        self.save.setMaximumSize(QSize(999999, 16777215))
        self.save.setFont(font)
        self.save.setStyleSheet(u"QPushButton {\n"
"    border-radius: 10px;\n"
"    padding: 5px;  /* \u6dfb\u52a0\u4e00\u4e9b\u5185\u8fb9\u8ddd\uff0c\u8ba9\u6309\u94ae\u66f4\u7f8e\u89c2 */\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: #015371;\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    padding-left: 3px;\n"
"    padding-top: 3px;\n"
"}")
        icon5 = QIcon()
        icon5.addFile(u":/icon/icon/save.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.save.setIcon(icon5)
        self.save.setIconSize(QSize(25, 25))

        self.verticalLayout_4.addWidget(self.save)

        self.remove = QPushButton(self.frame_2)
        self.remove.setObjectName(u"remove")
        self.remove.setMaximumSize(QSize(16777215, 16777215))
        self.remove.setFont(font)
        self.remove.setStyleSheet(u"QPushButton {\n"
"    border-radius: 10px;\n"
"    padding: 5px;  /* \u6dfb\u52a0\u4e00\u4e9b\u5185\u8fb9\u8ddd\uff0c\u8ba9\u6309\u94ae\u66f4\u7f8e\u89c2 */\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: #015371;\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    padding-left: 3px;\n"
"    padding-top: 3px;\n"
"}")
        icon6 = QIcon()
        icon6.addFile(u":/icon/icon/trash-2.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.remove.setIcon(icon6)
        self.remove.setIconSize(QSize(25, 25))

        self.verticalLayout_4.addWidget(self.remove)

        self.attribute_show = QPushButton(self.frame_2)
        self.attribute_show.setObjectName(u"attribute_show")
        self.attribute_show.setMaximumSize(QSize(16777215, 16777215))
        self.attribute_show.setFont(font)
        self.attribute_show.setStyleSheet(u"QPushButton {\n"
"    border-radius: 10px;\n"
"    padding: 5px;  /* \u6dfb\u52a0\u4e00\u4e9b\u5185\u8fb9\u8ddd\uff0c\u8ba9\u6309\u94ae\u66f4\u7f8e\u89c2 */\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: #015371;\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    padding-left: 3px;\n"
"    padding-top: 3px;\n"
"}")
        icon7 = QIcon()
        icon7.addFile(u":/icon/icon/box.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.attribute_show.setIcon(icon7)
        self.attribute_show.setIconSize(QSize(25, 25))

        self.verticalLayout_4.addWidget(self.attribute_show)


        self.verticalLayout_2.addWidget(self.frame_2, 0, Qt.AlignmentFlag.AlignTop)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_2.addItem(self.verticalSpacer)

        self.frame_3 = QFrame(self.leftMenuSubContainer)
        self.frame_3.setObjectName(u"frame_3")
        self.frame_3.setStyleSheet(u"QPushButton:hover{\n"
"	background-color:#015371;\n"
"	border-radius: 10px;\n"
"	\n"
"	\n"
"}\n"
"QPushButton:pressed\n"
"{\n"
"    /*\u5de6\u5185\u8fb9\u8ddd\u4e3a3\u50cf\u7d20\uff0c\u8ba9\u6309\u4e0b\u65f6\u5b57\u5411\u53f3\u79fb\u52a83\u50cf\u7d20*/  \n"
"    padding-left:3px;\n"
"    /*\u4e0a\u5185\u8fb9\u8ddd\u4e3a3\u50cf\u7d20\uff0c\u8ba9\u6309\u4e0b\u65f6\u5b57\u5411\u4e0b\u79fb\u52a83\u50cf\u7d20*/  \n"
"    padding-top:3px;\n"
"}")
        self.frame_3.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_3.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_5 = QVBoxLayout(self.frame_3)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.verticalLayout_5.setContentsMargins(5, 0, 5, 8)
        self.pointCloudCover = QPushButton(self.frame_3)
        self.pointCloudCover.setObjectName(u"pointCloudCover")
        self.pointCloudCover.setMaximumSize(QSize(16777215, 16777215))
        self.pointCloudCover.setFont(font)
        self.pointCloudCover.setStyleSheet(u"QPushButton {\n"
"    border-radius: 10px;\n"
"    padding: 5px;  /* \u6dfb\u52a0\u4e00\u4e9b\u5185\u8fb9\u8ddd\uff0c\u8ba9\u6309\u94ae\u66f4\u7f8e\u89c2 */\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: #015371;\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    padding-left: 3px;\n"
"    padding-top: 3px;\n"
"}")
        icon8 = QIcon()
        icon8.addFile(u":/icon/icon/cloud-rain.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.pointCloudCover.setIcon(icon8)
        self.pointCloudCover.setIconSize(QSize(25, 25))

        self.verticalLayout_5.addWidget(self.pointCloudCover)

        self.imageCover = QPushButton(self.frame_3)
        self.imageCover.setObjectName(u"imageCover")
        self.imageCover.setMaximumSize(QSize(16777215, 16777215))
        self.imageCover.setFont(font)
        self.imageCover.setStyleSheet(u"QPushButton {\n"
"    border-radius: 10px;\n"
"    padding: 5px;  /* \u6dfb\u52a0\u4e00\u4e9b\u5185\u8fb9\u8ddd\uff0c\u8ba9\u6309\u94ae\u66f4\u7f8e\u89c2 */\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: #015371;\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    padding-left: 3px;\n"
"    padding-top: 3px;\n"
"}")
        icon9 = QIcon()
        icon9.addFile(u":/icon/icon/image.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.imageCover.setIcon(icon9)
        self.imageCover.setIconSize(QSize(25, 25))

        self.verticalLayout_5.addWidget(self.imageCover)

        self.vectorCover = QPushButton(self.frame_3)
        self.vectorCover.setObjectName(u"vectorCover")
        self.vectorCover.setMaximumSize(QSize(16777215, 16777215))
        self.vectorCover.setFont(font)
        self.vectorCover.setStyleSheet(u"QPushButton {\n"
"    border-radius: 10px;\n"
"    padding: 5px;  /* \u6dfb\u52a0\u4e00\u4e9b\u5185\u8fb9\u8ddd\uff0c\u8ba9\u6309\u94ae\u66f4\u7f8e\u89c2 */\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: #015371;\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    padding-left: 3px;\n"
"    padding-top: 3px;\n"
"}")
        icon10 = QIcon()
        icon10.addFile(u":/icon/icon/git-branch.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.vectorCover.setIcon(icon10)
        self.vectorCover.setIconSize(QSize(25, 25))

        self.verticalLayout_5.addWidget(self.vectorCover)


        self.verticalLayout_2.addWidget(self.frame_3, 0, Qt.AlignmentFlag.AlignBottom)


        self.horizontalLayout_3.addWidget(self.leftMenuSubContainer)


        self.main_body.addWidget(self.leftMenuContainer)

        self.rightBodyContainer = QWidget(self.centralwidget)
        self.rightBodyContainer.setObjectName(u"rightBodyContainer")
        self.verticalLayout_3 = QVBoxLayout(self.rightBodyContainer)
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.bottomBodyContainer = QWidget(self.rightBodyContainer)
        self.bottomBodyContainer.setObjectName(u"bottomBodyContainer")
        self.horizontalLayout_7 = QHBoxLayout(self.bottomBodyContainer)
        self.horizontalLayout_7.setSpacing(0)
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.horizontalLayout_7.setContentsMargins(0, 0, 0, 0)
        self.resourceContainer = QWidget(self.bottomBodyContainer)
        self.resourceContainer.setObjectName(u"resourceContainer")
        sizePolicy1.setHeightForWidth(self.resourceContainer.sizePolicy().hasHeightForWidth())
        self.resourceContainer.setSizePolicy(sizePolicy1)
        self.resourceContainer.setMinimumSize(QSize(0, 0))
        self.resourceContainer.setMaximumSize(QSize(190, 16777215))
        self.resourceContainer.setFocusPolicy(Qt.FocusPolicy.TabFocus)
        self.resourceContainer.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.verticalLayout_6 = QVBoxLayout(self.resourceContainer)
        self.verticalLayout_6.setSpacing(0)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.verticalLayout_6.setContentsMargins(0, 5, 0, 0)
        self.centerMenuSubContainer = QWidget(self.resourceContainer)
        self.centerMenuSubContainer.setObjectName(u"centerMenuSubContainer")
        self.centerMenuSubContainer.setMinimumSize(QSize(0, 0))
        self.verticalLayout = QVBoxLayout(self.centerMenuSubContainer)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.frame_4 = QFrame(self.centerMenuSubContainer)
        self.frame_4.setObjectName(u"frame_4")
        self.frame_4.setMinimumSize(QSize(0, 0))
        self.frame_4.setMaximumSize(QSize(16777215, 40))
        self.frame_4.setStyleSheet(u"QFrame{\n"
"background-color:#16191d;\n"
"border-radius:20px;\n"
"}")
        self.frame_4.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_4.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_4 = QHBoxLayout(self.frame_4)
        self.horizontalLayout_4.setSpacing(0)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalLayout_4.setContentsMargins(11, -1, 5, -1)
        self.label_2 = QLabel(self.frame_4)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setFont(font)

        self.horizontalLayout_4.addWidget(self.label_2)

        self.centerClose = QPushButton(self.frame_4)
        self.centerClose.setObjectName(u"centerClose")
        self.centerClose.setMaximumSize(QSize(30, 30))
        self.centerClose.setStyleSheet(u"QPushButton {\n"
"    border-radius: 10px;\n"
"    padding: 5px;  /* \u6dfb\u52a0\u4e00\u4e9b\u5185\u8fb9\u8ddd\uff0c\u8ba9\u6309\u94ae\u66f4\u7f8e\u89c2 */\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: #015371;\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    padding-left: 3px;\n"
"    padding-top: 3px;\n"
"}")
        icon11 = QIcon()
        icon11.addFile(u":/icon/icon/x-circle.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.centerClose.setIcon(icon11)
        self.centerClose.setIconSize(QSize(25, 25))

        self.horizontalLayout_4.addWidget(self.centerClose)


        self.verticalLayout.addWidget(self.frame_4)

        self.stackedWidget = QStackedWidget(self.centerMenuSubContainer)
        self.stackedWidget.setObjectName(u"stackedWidget")
        sizePolicy1.setHeightForWidth(self.stackedWidget.sizePolicy().hasHeightForWidth())
        self.stackedWidget.setSizePolicy(sizePolicy1)
        self.stackedWidget.setCursor(QCursor(Qt.CursorShape.ArrowCursor))
        self.stackedWidget.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.stackedWidget.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.stackedWidget.setStyleSheet(u"background-color:transparent;")
        self.point_cloud_resource = QWidget()
        self.point_cloud_resource.setObjectName(u"point_cloud_resource")
        self.verticalLayout_7 = QVBoxLayout(self.point_cloud_resource)
        self.verticalLayout_7.setSpacing(9)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.verticalLayout_7.setContentsMargins(9, -1, 9, 9)
        self.point_cloud_tree_widget = QTreeWidget(self.point_cloud_resource)
        self.point_cloud_tree_widget.headerItem().setText(1, "")
        self.point_cloud_tree_widget.setObjectName(u"point_cloud_tree_widget")
        self.point_cloud_tree_widget.setStyleSheet(u"QTreeWidget {\n"
"                        border: 0.2px solid white; /* \u8bbe\u7f6e\u63cf\u8fb9 */\n"
"                        border-radius: 5px; /* \u8bbe\u7f6e\u5706\u89d2 */\n"
"                    }\n"
"\n"
"                    QTreeWidget::item {\n"
"                        padding: 5px;\n"
"            \n"
"                    }")

        self.verticalLayout_7.addWidget(self.point_cloud_tree_widget)

        self.stackedWidget.addWidget(self.point_cloud_resource)
        self.image_resource = QWidget()
        self.image_resource.setObjectName(u"image_resource")
        self.verticalLayout_8 = QVBoxLayout(self.image_resource)
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.image_tree_widget = QTreeWidget(self.image_resource)
        self.image_tree_widget.headerItem().setText(1, "")
        self.image_tree_widget.setObjectName(u"image_tree_widget")
        self.image_tree_widget.setStyleSheet(u"QTreeWidget {\n"
"                        border: 0.2px solid white; /* \u8bbe\u7f6e\u63cf\u8fb9 */\n"
"                        border-radius: 5px; /* \u8bbe\u7f6e\u5706\u89d2 */\n"
"                    }\n"
"\n"
"                    QTreeWidget::item {\n"
"                        padding: 5px;\n"
"            \n"
"                    }")

        self.verticalLayout_8.addWidget(self.image_tree_widget)

        self.stackedWidget.addWidget(self.image_resource)
        self.vector_resource = QWidget()
        self.vector_resource.setObjectName(u"vector_resource")
        self.verticalLayout_9 = QVBoxLayout(self.vector_resource)
        self.verticalLayout_9.setObjectName(u"verticalLayout_9")
        self.vector_tree_widget = QTreeWidget(self.vector_resource)
        self.vector_tree_widget.headerItem().setText(1, "")
        self.vector_tree_widget.setObjectName(u"vector_tree_widget")
        self.vector_tree_widget.setStyleSheet(u"QTreeWidget {\n"
"                        border: 0.2px solid white; /* \u8bbe\u7f6e\u63cf\u8fb9 */\n"
"                        border-radius: 5px; /* \u8bbe\u7f6e\u5706\u89d2 */\n"
"                    }\n"
"\n"
"                    QTreeWidget::item {\n"
"                        padding: 5px;\n"
"            \n"
"                    }")

        self.verticalLayout_9.addWidget(self.vector_tree_widget)

        self.stackedWidget.addWidget(self.vector_resource)

        self.verticalLayout.addWidget(self.stackedWidget)


        self.verticalLayout_6.addWidget(self.centerMenuSubContainer)


        self.horizontalLayout_7.addWidget(self.resourceContainer)

        self.viewContainer = QWidget(self.bottomBodyContainer)
        self.viewContainer.setObjectName(u"viewContainer")
        sizePolicy4 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.viewContainer.sizePolicy().hasHeightForWidth())
        self.viewContainer.setSizePolicy(sizePolicy4)
        self.viewContainer.setMinimumSize(QSize(163, 0))
        self.viewContainer.setStyleSheet(u"background-color:rgb(0, 0, 0);")
        self.horizontalLayout_2 = QHBoxLayout(self.viewContainer)
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, 5, 0, 0)
        self.view_stacked_widget = QStackedWidget(self.viewContainer)
        self.view_stacked_widget.setObjectName(u"view_stacked_widget")
        self.point_cloud_view = QWidget()
        self.point_cloud_view.setObjectName(u"point_cloud_view")
        self.verticalLayout_12 = QVBoxLayout(self.point_cloud_view)
        self.verticalLayout_12.setSpacing(0)
        self.verticalLayout_12.setObjectName(u"verticalLayout_12")
        self.verticalLayout_12.setContentsMargins(0, 0, 0, 0)
        self.widget_2 = QWidget(self.point_cloud_view)
        self.widget_2.setObjectName(u"widget_2")
        self.widget_2.setMaximumSize(QSize(16777215, 30))
        self.horizontalLayout_13 = QHBoxLayout(self.widget_2)
        self.horizontalLayout_13.setObjectName(u"horizontalLayout_13")
        self.horizontalLayout_13.setContentsMargins(-1, 0, -1, -1)
        self.label = QLabel(self.widget_2)
        self.label.setObjectName(u"label")

        self.horizontalLayout_13.addWidget(self.label)

        self.point_size = QSlider(self.widget_2)
        self.point_size.setObjectName(u"point_size")
        sizePolicy5 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy5.setHorizontalStretch(0)
        sizePolicy5.setVerticalStretch(0)
        sizePolicy5.setHeightForWidth(self.point_size.sizePolicy().hasHeightForWidth())
        self.point_size.setSizePolicy(sizePolicy5)
        self.point_size.setMinimumSize(QSize(150, 0))
        self.point_size.setMaximumSize(QSize(100, 16777215))
        self.point_size.setMaximum(10)
        self.point_size.setValue(3)
        self.point_size.setOrientation(Qt.Orientation.Horizontal)

        self.horizontalLayout_13.addWidget(self.point_size)

        self.size_num = QLabel(self.widget_2)
        self.size_num.setObjectName(u"size_num")

        self.horizontalLayout_13.addWidget(self.size_num)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_13.addItem(self.horizontalSpacer_2)

        self.file_name = QLabel(self.widget_2)
        self.file_name.setObjectName(u"file_name")

        self.horizontalLayout_13.addWidget(self.file_name)


        self.verticalLayout_12.addWidget(self.widget_2)

        self.widget_3 = QWidget(self.point_cloud_view)
        self.widget_3.setObjectName(u"widget_3")
        self.verticalLayout_14 = QVBoxLayout(self.widget_3)
        self.verticalLayout_14.setSpacing(0)
        self.verticalLayout_14.setObjectName(u"verticalLayout_14")
        self.verticalLayout_14.setContentsMargins(0, 0, 0, 0)
        self.point_cloud_view_layout = QVBoxLayout()
        self.point_cloud_view_layout.setSpacing(0)
        self.point_cloud_view_layout.setObjectName(u"point_cloud_view_layout")

        self.verticalLayout_14.addLayout(self.point_cloud_view_layout)


        self.verticalLayout_12.addWidget(self.widget_3)

        self.view_stacked_widget.addWidget(self.point_cloud_view)
        self.image_view = QWidget()
        self.image_view.setObjectName(u"image_view")
        self.verticalLayout_13 = QVBoxLayout(self.image_view)
        self.verticalLayout_13.setSpacing(0)
        self.verticalLayout_13.setObjectName(u"verticalLayout_13")
        self.verticalLayout_13.setContentsMargins(0, 0, 0, 0)
        self.image_file_name = QLabel(self.image_view)
        self.image_file_name.setObjectName(u"image_file_name")
        self.image_file_name.setMaximumSize(QSize(16777215, 30))
        self.image_file_name.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_13.addWidget(self.image_file_name)

        self.widget_4 = QWidget(self.image_view)
        self.widget_4.setObjectName(u"widget_4")
        self.widget_4.setMaximumSize(QSize(16777215, 16777215))
        self.verticalLayout_18 = QVBoxLayout(self.widget_4)
        self.verticalLayout_18.setSpacing(0)
        self.verticalLayout_18.setObjectName(u"verticalLayout_18")
        self.verticalLayout_18.setContentsMargins(0, 0, 0, 0)
        self.image_view_layout = QVBoxLayout()
        self.image_view_layout.setSpacing(0)
        self.image_view_layout.setObjectName(u"image_view_layout")

        self.verticalLayout_18.addLayout(self.image_view_layout)


        self.verticalLayout_13.addWidget(self.widget_4)

        self.view_stacked_widget.addWidget(self.image_view)
        self.vector_view = QWidget()
        self.vector_view.setObjectName(u"vector_view")
        self.verticalLayout_10 = QVBoxLayout(self.vector_view)
        self.verticalLayout_10.setSpacing(0)
        self.verticalLayout_10.setObjectName(u"verticalLayout_10")
        self.verticalLayout_10.setContentsMargins(0, 0, 0, 0)
        self.vector_file_name = QLabel(self.vector_view)
        self.vector_file_name.setObjectName(u"vector_file_name")
        self.vector_file_name.setMaximumSize(QSize(16777215, 30))
        self.vector_file_name.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_10.addWidget(self.vector_file_name)

        self.widget_5 = QWidget(self.vector_view)
        self.widget_5.setObjectName(u"widget_5")
        self.verticalLayout_17 = QVBoxLayout(self.widget_5)
        self.verticalLayout_17.setSpacing(0)
        self.verticalLayout_17.setObjectName(u"verticalLayout_17")
        self.verticalLayout_17.setContentsMargins(0, 0, 0, 0)
        self.vector_view_layout = QVBoxLayout()
        self.vector_view_layout.setSpacing(0)
        self.vector_view_layout.setObjectName(u"vector_view_layout")

        self.verticalLayout_17.addLayout(self.vector_view_layout)


        self.verticalLayout_10.addWidget(self.widget_5)

        self.view_stacked_widget.addWidget(self.vector_view)

        self.horizontalLayout_2.addWidget(self.view_stacked_widget)


        self.horizontalLayout_7.addWidget(self.viewContainer)

        self.attributeContainer = QWidget(self.bottomBodyContainer)
        self.attributeContainer.setObjectName(u"attributeContainer")
        self.attributeContainer.setMaximumSize(QSize(200, 16777215))
        self.verticalLayout_11 = QVBoxLayout(self.attributeContainer)
        self.verticalLayout_11.setSpacing(0)
        self.verticalLayout_11.setObjectName(u"verticalLayout_11")
        self.verticalLayout_11.setContentsMargins(0, 5, 0, 0)
        self.frame_5 = QFrame(self.attributeContainer)
        self.frame_5.setObjectName(u"frame_5")
        self.frame_5.setMinimumSize(QSize(0, 0))
        self.frame_5.setMaximumSize(QSize(16777215, 40))
        self.frame_5.setStyleSheet(u"QFrame{\n"
"background-color:#16191d;\n"
"border-radius:20px;\n"
"}")
        self.frame_5.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_5.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_9 = QHBoxLayout(self.frame_5)
        self.horizontalLayout_9.setSpacing(0)
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.horizontalLayout_9.setContentsMargins(11, -1, 5, -1)
        self.label_6 = QLabel(self.frame_5)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setFont(font)

        self.horizontalLayout_9.addWidget(self.label_6)

        self.attribute_close = QPushButton(self.frame_5)
        self.attribute_close.setObjectName(u"attribute_close")
        self.attribute_close.setMaximumSize(QSize(30, 30))
        self.attribute_close.setStyleSheet(u"QPushButton {\n"
"    border-radius: 10px;\n"
"    padding: 5px;  /* \u6dfb\u52a0\u4e00\u4e9b\u5185\u8fb9\u8ddd\uff0c\u8ba9\u6309\u94ae\u66f4\u7f8e\u89c2 */\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: #015371;\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    padding-left: 3px;\n"
"    padding-top: 3px;\n"
"}")
        self.attribute_close.setIcon(icon11)
        self.attribute_close.setIconSize(QSize(25, 25))

        self.horizontalLayout_9.addWidget(self.attribute_close)


        self.verticalLayout_11.addWidget(self.frame_5)

        self.attribute_stacked_widget = QStackedWidget(self.attributeContainer)
        self.attribute_stacked_widget.setObjectName(u"attribute_stacked_widget")
        self.attribute_stacked_widget.setStyleSheet(u"background-color:transparent;")
        self.point_cloud_attribute = QWidget()
        self.point_cloud_attribute.setObjectName(u"point_cloud_attribute")
        self.horizontalLayout_10 = QHBoxLayout(self.point_cloud_attribute)
        self.horizontalLayout_10.setSpacing(0)
        self.horizontalLayout_10.setObjectName(u"horizontalLayout_10")
        self.horizontalLayout_10.setContentsMargins(0, 0, 0, 0)
        self.points_attribute_layout = QVBoxLayout()
        self.points_attribute_layout.setSpacing(0)
        self.points_attribute_layout.setObjectName(u"points_attribute_layout")

        self.horizontalLayout_10.addLayout(self.points_attribute_layout)

        self.attribute_stacked_widget.addWidget(self.point_cloud_attribute)
        self.image_attribute = QWidget()
        self.image_attribute.setObjectName(u"image_attribute")
        self.horizontalLayout_11 = QHBoxLayout(self.image_attribute)
        self.horizontalLayout_11.setSpacing(0)
        self.horizontalLayout_11.setObjectName(u"horizontalLayout_11")
        self.horizontalLayout_11.setContentsMargins(0, 0, 0, 0)
        self.image_attribute_layout = QVBoxLayout()
        self.image_attribute_layout.setSpacing(0)
        self.image_attribute_layout.setObjectName(u"image_attribute_layout")

        self.horizontalLayout_11.addLayout(self.image_attribute_layout)

        self.attribute_stacked_widget.addWidget(self.image_attribute)
        self.vector_attribute = QWidget()
        self.vector_attribute.setObjectName(u"vector_attribute")
        self.horizontalLayout_12 = QHBoxLayout(self.vector_attribute)
        self.horizontalLayout_12.setSpacing(0)
        self.horizontalLayout_12.setObjectName(u"horizontalLayout_12")
        self.horizontalLayout_12.setContentsMargins(0, 0, 0, 0)
        self.vector_attribute_layout = QVBoxLayout()
        self.vector_attribute_layout.setSpacing(0)
        self.vector_attribute_layout.setObjectName(u"vector_attribute_layout")

        self.horizontalLayout_12.addLayout(self.vector_attribute_layout)

        self.attribute_stacked_widget.addWidget(self.vector_attribute)

        self.verticalLayout_11.addWidget(self.attribute_stacked_widget)


        self.horizontalLayout_7.addWidget(self.attributeContainer)


        self.verticalLayout_3.addWidget(self.bottomBodyContainer)


        self.main_body.addWidget(self.rightBodyContainer)


        self.verticalLayout_15.addLayout(self.main_body)


        self.horizontalLayout.addLayout(self.verticalLayout_15)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        self.stackedWidget.setCurrentIndex(1)
        self.view_stacked_widget.setCurrentIndex(1)
        self.attribute_stacked_widget.setCurrentIndex(1)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
#if QT_CONFIG(tooltip)
        self.menu_show.setToolTip("")
#endif // QT_CONFIG(tooltip)
        self.menu_show.setText("")
        self.file.setText(QCoreApplication.translate("MainWindow", u"\u6587\u4ef6", None))
        self.processing.setText(QCoreApplication.translate("MainWindow", u"\u6570\u636e\u5904\u7406", None))
        self.forestry_parameter_extraction.setText(QCoreApplication.translate("MainWindow", u"\u6797\u4e1a\u53c2\u6570", None))
        self.minimize_window_button.setText("")
        self.maximize_window_button.setText("")
        self.close_window_button.setText("")
#if QT_CONFIG(tooltip)
        self.open.setToolTip(QCoreApplication.translate("MainWindow", u"\u6253\u5f00\u6587\u4ef6", None))
#endif // QT_CONFIG(tooltip)
        self.open.setText(QCoreApplication.translate("MainWindow", u"  \u6253\u5f00\u6587\u4ef6", None))
#if QT_CONFIG(tooltip)
        self.save.setToolTip(QCoreApplication.translate("MainWindow", u"\u4fdd\u5b58\u6587\u4ef6", None))
#endif // QT_CONFIG(tooltip)
        self.save.setText(QCoreApplication.translate("MainWindow", u"  \u4fdd\u5b58\u6587\u4ef6", None))
#if QT_CONFIG(tooltip)
        self.remove.setToolTip(QCoreApplication.translate("MainWindow", u"\u79fb\u9664\u6587\u4ef6", None))
#endif // QT_CONFIG(tooltip)
        self.remove.setText(QCoreApplication.translate("MainWindow", u"  \u79fb\u9664\u6587\u4ef6", None))
#if QT_CONFIG(tooltip)
        self.attribute_show.setToolTip(QCoreApplication.translate("MainWindow", u"\u6570\u636e\u663e\u793a", None))
#endif // QT_CONFIG(tooltip)
        self.attribute_show.setText(QCoreApplication.translate("MainWindow", u"  \u5c5e\u6027\u7ba1\u7406", None))
#if QT_CONFIG(tooltip)
        self.pointCloudCover.setToolTip(QCoreApplication.translate("MainWindow", u"\u70b9\u4e91\u5c42", None))
#endif // QT_CONFIG(tooltip)
        self.pointCloudCover.setText(QCoreApplication.translate("MainWindow", u"  \u70b9\u4e91\u5c42", None))
#if QT_CONFIG(tooltip)
        self.imageCover.setToolTip(QCoreApplication.translate("MainWindow", u"\u5f71\u50cf\u5c42", None))
#endif // QT_CONFIG(tooltip)
        self.imageCover.setText(QCoreApplication.translate("MainWindow", u"  \u5f71\u50cf\u5c42", None))
#if QT_CONFIG(tooltip)
        self.vectorCover.setToolTip(QCoreApplication.translate("MainWindow", u"\u77e2\u91cf\u5c42", None))
#endif // QT_CONFIG(tooltip)
        self.vectorCover.setText(QCoreApplication.translate("MainWindow", u"  \u77e2\u91cf\u5c42", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"\u8d44\u6e90\u7ba1\u7406", None))
        self.centerClose.setText("")
        ___qtreewidgetitem = self.point_cloud_tree_widget.headerItem()
        ___qtreewidgetitem.setText(0, QCoreApplication.translate("MainWindow", u"\u70b9\u4e91\u5c42", None));
        ___qtreewidgetitem1 = self.image_tree_widget.headerItem()
        ___qtreewidgetitem1.setText(0, QCoreApplication.translate("MainWindow", u"\u5f71\u50cf\u5c42", None));
        ___qtreewidgetitem2 = self.vector_tree_widget.headerItem()
        ___qtreewidgetitem2.setText(0, QCoreApplication.translate("MainWindow", u"\u77e2\u91cf\u5c42", None));
        self.label.setText(QCoreApplication.translate("MainWindow", u"\u70b9\u4e91\u5927\u5c0f\uff1a", None))
        self.size_num.setText(QCoreApplication.translate("MainWindow", u"3", None))
        self.file_name.setText("")
#if QT_CONFIG(whatsthis)
        self.image_view.setWhatsThis(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><br/></p></body></html>", None))
#endif // QT_CONFIG(whatsthis)
        self.image_file_name.setText("")
        self.vector_file_name.setText("")
        self.label_6.setText(QCoreApplication.translate("MainWindow", u"\u5c5e\u6027\u663e\u793a", None))
        self.attribute_close.setText("")
    # retranslateUi

