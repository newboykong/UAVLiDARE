# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'single_wood_division_dialog.ui'
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
from PySide6.QtWidgets import (QApplication, QDialog, QHBoxLayout, QHeaderView,
    QLabel, QLineEdit, QPushButton, QSizePolicy,
    QSpacerItem, QTreeWidget, QTreeWidgetItem, QVBoxLayout,
    QWidget)
import icon_rc

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(512, 342)
        Dialog.setStyleSheet(u"QDialog{\n"
"	background-color:#1f232a;\n"
"}\n"
"\n"
"\n"
"\n"
"")
        self.verticalLayout_2 = QVBoxLayout(Dialog)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setSpacing(6)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.chm_file_tree_widget = QTreeWidget(Dialog)
        __qtreewidgetitem = QTreeWidgetItem()
        __qtreewidgetitem.setTextAlignment(1, Qt.AlignCenter);
        __qtreewidgetitem.setTextAlignment(0, Qt.AlignCenter);
        self.chm_file_tree_widget.setHeaderItem(__qtreewidgetitem)
        self.chm_file_tree_widget.setObjectName(u"chm_file_tree_widget")
        self.chm_file_tree_widget.setStyleSheet(u"QTreeWidget {\n"
"                        border: 0.2px solid white; /* \u8bbe\u7f6e\u63cf\u8fb9 */\n"
"                        border-radius: 5px; /* \u8bbe\u7f6e\u5706\u89d2 */\n"
"                    }\n"
"\n"
"                    QTreeWidget::item {\n"
"                        padding: 5px;\n"
"            \n"
"                    }")

        self.verticalLayout.addWidget(self.chm_file_tree_widget)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalLayout_4.setContentsMargins(6, -1, 6, -1)
        self.label_3 = QLabel(Dialog)
        self.label_3.setObjectName(u"label_3")

        self.horizontalLayout_4.addWidget(self.label_3)

        self.chm_file_path = QLineEdit(Dialog)
        self.chm_file_path.setObjectName(u"chm_file_path")

        self.horizontalLayout_4.addWidget(self.chm_file_path)

        self.select_file_chm = QPushButton(Dialog)
        self.select_file_chm.setObjectName(u"select_file_chm")

        self.horizontalLayout_4.addWidget(self.select_file_chm)


        self.verticalLayout.addLayout(self.horizontalLayout_4)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(6, -1, 6, -1)
        self.label_2 = QLabel(Dialog)
        self.label_2.setObjectName(u"label_2")

        self.horizontalLayout_3.addWidget(self.label_2)

        self.save_file_path_tif = QLineEdit(Dialog)
        self.save_file_path_tif.setObjectName(u"save_file_path_tif")

        self.horizontalLayout_3.addWidget(self.save_file_path_tif)

        self.select_file_tif = QPushButton(Dialog)
        self.select_file_tif.setObjectName(u"select_file_tif")

        self.horizontalLayout_3.addWidget(self.select_file_tif)


        self.verticalLayout.addLayout(self.horizontalLayout_3)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.horizontalLayout_5.setContentsMargins(6, -1, 6, -1)
        self.label_4 = QLabel(Dialog)
        self.label_4.setObjectName(u"label_4")

        self.horizontalLayout_5.addWidget(self.label_4)

        self.save_file_path_shp = QLineEdit(Dialog)
        self.save_file_path_shp.setObjectName(u"save_file_path_shp")

        self.horizontalLayout_5.addWidget(self.save_file_path_shp)

        self.select_file_shp = QPushButton(Dialog)
        self.select_file_shp.setObjectName(u"select_file_shp")

        self.horizontalLayout_5.addWidget(self.select_file_shp)


        self.verticalLayout.addLayout(self.horizontalLayout_5)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(-1, 0, -1, 3)
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_2)

        self.accept = QPushButton(Dialog)
        self.accept.setObjectName(u"accept")
        self.accept.setStyleSheet(u"")

        self.horizontalLayout_2.addWidget(self.accept)

        self.reject = QPushButton(Dialog)
        self.reject.setObjectName(u"reject")
        self.reject.setMaximumSize(QSize(70, 16777215))

        self.horizontalLayout_2.addWidget(self.reject)


        self.verticalLayout.addLayout(self.horizontalLayout_2)


        self.verticalLayout_2.addLayout(self.verticalLayout)


        self.retranslateUi(Dialog)
        self.reject.clicked.connect(Dialog.reject)
        self.accept.clicked.connect(Dialog.accept)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"\u5355\u6728\u5206\u5272", None))
        ___qtreewidgetitem = self.chm_file_tree_widget.headerItem()
        ___qtreewidgetitem.setText(1, QCoreApplication.translate("Dialog", u"\u6587\u4ef6\u540d", None));
        ___qtreewidgetitem.setText(0, QCoreApplication.translate("Dialog", u"\u9009\u4e2d\u72b6\u6001", None));
        self.label_3.setText(QCoreApplication.translate("Dialog", u"\u9009\u62e9CHM\u6587\u4ef6\uff1a", None))
        self.select_file_chm.setText(QCoreApplication.translate("Dialog", u"\u9009\u62e9", None))
        self.label_2.setText(QCoreApplication.translate("Dialog", u"\u4fdd\u5b58\u4e3a.tif\uff1a", None))
        self.select_file_tif.setText(QCoreApplication.translate("Dialog", u"\u4fdd\u5b58", None))
        self.label_4.setText(QCoreApplication.translate("Dialog", u"\u4fdd\u5b58\u4e3a.shp\uff1a", None))
        self.select_file_shp.setText(QCoreApplication.translate("Dialog", u"\u4fdd\u5b58", None))
        self.accept.setText(QCoreApplication.translate("Dialog", u"\u786e\u5b9a", None))
        self.reject.setText(QCoreApplication.translate("Dialog", u"\u53d6\u6d88", None))
    # retranslateUi

