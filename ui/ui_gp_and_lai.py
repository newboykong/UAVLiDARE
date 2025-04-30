# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'gp_and_lai.ui'
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
from PySide6.QtWidgets import (QAbstractSpinBox, QApplication, QDialog, QHBoxLayout,
    QHeaderView, QLabel, QLineEdit, QPushButton,
    QSizePolicy, QSpacerItem, QSpinBox, QTreeWidget,
    QTreeWidgetItem, QVBoxLayout, QWidget)
import icon_rc

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(514, 347)
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
        self.file_tree_widget = QTreeWidget(Dialog)
        __qtreewidgetitem = QTreeWidgetItem()
        __qtreewidgetitem.setTextAlignment(1, Qt.AlignCenter);
        __qtreewidgetitem.setTextAlignment(0, Qt.AlignCenter);
        self.file_tree_widget.setHeaderItem(__qtreewidgetitem)
        self.file_tree_widget.setObjectName(u"file_tree_widget")
        self.file_tree_widget.setStyleSheet(u"QTreeWidget {\n"
"                        border: 0.2px solid white; /* \u8bbe\u7f6e\u63cf\u8fb9 */\n"
"                        border-radius: 5px; /* \u8bbe\u7f6e\u5706\u89d2 */\n"
"                    }\n"
"\n"
"                    QTreeWidget::item {\n"
"                        padding: 5px;\n"
"            \n"
"                    }")

        self.verticalLayout.addWidget(self.file_tree_widget)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalLayout_4.setContentsMargins(6, -1, 6, -1)
        self.label_5 = QLabel(Dialog)
        self.label_5.setObjectName(u"label_5")

        self.horizontalLayout_4.addWidget(self.label_5)

        self.file_path_gp = QLineEdit(Dialog)
        self.file_path_gp.setObjectName(u"file_path_gp")

        self.horizontalLayout_4.addWidget(self.file_path_gp)

        self.select_file_gp = QPushButton(Dialog)
        self.select_file_gp.setObjectName(u"select_file_gp")

        self.horizontalLayout_4.addWidget(self.select_file_gp)


        self.verticalLayout.addLayout(self.horizontalLayout_4)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(6, -1, 6, -1)
        self.label_4 = QLabel(Dialog)
        self.label_4.setObjectName(u"label_4")

        self.horizontalLayout_3.addWidget(self.label_4)

        self.file_path_lai = QLineEdit(Dialog)
        self.file_path_lai.setObjectName(u"file_path_lai")

        self.horizontalLayout_3.addWidget(self.file_path_lai)

        self.select_file_lai = QPushButton(Dialog)
        self.select_file_lai.setObjectName(u"select_file_lai")

        self.horizontalLayout_3.addWidget(self.select_file_lai)


        self.verticalLayout.addLayout(self.horizontalLayout_3)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(6, 0, 6, 6)
        self.label_2 = QLabel(Dialog)
        self.label_2.setObjectName(u"label_2")

        self.horizontalLayout_2.addWidget(self.label_2)

        self.grid_size = QSpinBox(Dialog)
        self.grid_size.setObjectName(u"grid_size")
        self.grid_size.setMaximum(50)
        self.grid_size.setStepType(QAbstractSpinBox.StepType.DefaultStepType)
        self.grid_size.setValue(1)

        self.horizontalLayout_2.addWidget(self.grid_size)

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
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"\u7a7a\u9699\u7387\u548c\u53f6\u9762\u6307\u6570", None))
        ___qtreewidgetitem = self.file_tree_widget.headerItem()
        ___qtreewidgetitem.setText(1, QCoreApplication.translate("Dialog", u"\u6587\u4ef6\u540d", None));
        ___qtreewidgetitem.setText(0, QCoreApplication.translate("Dialog", u"\u9009\u4e2d\u72b6\u6001", None));
        self.label_5.setText(QCoreApplication.translate("Dialog", u"\u7a7a\u9699\u7387\uff1a", None))
        self.select_file_gp.setText(QCoreApplication.translate("Dialog", u"\u4fdd\u5b58", None))
        self.label_4.setText(QCoreApplication.translate("Dialog", u"\u53f6\u9762\u6307\u6570\uff1a", None))
        self.select_file_lai.setText(QCoreApplication.translate("Dialog", u"\u4fdd\u5b58", None))
        self.label_2.setText(QCoreApplication.translate("Dialog", u"\u7f51\u683c\u5927\u5c0f\uff1a", None))
        self.grid_size.setSuffix(QCoreApplication.translate("Dialog", u"m", None))
        self.grid_size.setPrefix("")
        self.accept.setText(QCoreApplication.translate("Dialog", u"\u786e\u5b9a", None))
        self.reject.setText(QCoreApplication.translate("Dialog", u"\u53d6\u6d88", None))
    # retranslateUi

