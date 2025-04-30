# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'filtering_dialog.ui'
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
from PySide6.QtWidgets import (QAbstractSpinBox, QApplication, QComboBox, QDialog,
    QDoubleSpinBox, QHBoxLayout, QHeaderView, QLabel,
    QPushButton, QSizePolicy, QSpacerItem, QSpinBox,
    QTreeWidget, QTreeWidgetItem, QVBoxLayout, QWidget)
import icon_rc

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(509, 362)
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
        self.verticalLayout.setContentsMargins(6, -1, 6, -1)
        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(6, -1, 6, -1)
        self.file_tree_widget = QTreeWidget(Dialog)
        __qtreewidgetitem = QTreeWidgetItem()
        __qtreewidgetitem.setTextAlignment(1, Qt.AlignCenter);
        __qtreewidgetitem.setTextAlignment(0, Qt.AlignCenter);
        self.file_tree_widget.setHeaderItem(__qtreewidgetitem)
        self.file_tree_widget.setObjectName(u"file_tree_widget")
        self.file_tree_widget.setStyleSheet(u"QTreeWidget {\n"
"                        border: 0.3px solid white; /* \u8bbe\u7f6e\u63cf\u8fb9 */\n"
"                        border-radius: 5px; /* \u8bbe\u7f6e\u5706\u89d2 */\n"
"				\n"
"                    }\n"
"QTreeWidget::item {\n"
"                        padding: 5px;\n"
"            \n"
"                    }")

        self.horizontalLayout_3.addWidget(self.file_tree_widget)

        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label_6 = QLabel(Dialog)
        self.label_6.setObjectName(u"label_6")

        self.horizontalLayout.addWidget(self.label_6)

        self.filter_type = QComboBox(Dialog)
        self.filter_type.addItem("")
        self.filter_type.setObjectName(u"filter_type")

        self.horizontalLayout.addWidget(self.filter_type)


        self.verticalLayout_3.addLayout(self.horizontalLayout)

        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.label_2 = QLabel(Dialog)
        self.label_2.setObjectName(u"label_2")

        self.horizontalLayout_6.addWidget(self.label_2)

        self.grid_size = QDoubleSpinBox(Dialog)
        self.grid_size.setObjectName(u"grid_size")
        self.grid_size.setValue(2.000000000000000)

        self.horizontalLayout_6.addWidget(self.grid_size)


        self.verticalLayout_3.addLayout(self.horizontalLayout_6)

        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.label = QLabel(Dialog)
        self.label.setObjectName(u"label")

        self.horizontalLayout_7.addWidget(self.label)

        self.dh_min = QDoubleSpinBox(Dialog)
        self.dh_min.setObjectName(u"dh_min")
        self.dh_min.setSingleStep(0.100000000000000)
        self.dh_min.setValue(0.300000000000000)

        self.horizontalLayout_7.addWidget(self.dh_min)


        self.verticalLayout_3.addLayout(self.horizontalLayout_7)

        self.horizontalLayout_8 = QHBoxLayout()
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.label_3 = QLabel(Dialog)
        self.label_3.setObjectName(u"label_3")

        self.horizontalLayout_8.addWidget(self.label_3)

        self.dh_max = QDoubleSpinBox(Dialog)
        self.dh_max.setObjectName(u"dh_max")
        self.dh_max.setValue(25.000000000000000)

        self.horizontalLayout_8.addWidget(self.dh_max)


        self.verticalLayout_3.addLayout(self.horizontalLayout_8)

        self.horizontalLayout_10 = QHBoxLayout()
        self.horizontalLayout_10.setObjectName(u"horizontalLayout_10")
        self.label_5 = QLabel(Dialog)
        self.label_5.setObjectName(u"label_5")

        self.horizontalLayout_10.addWidget(self.label_5)

        self.iterations = QSpinBox(Dialog)
        self.iterations.setObjectName(u"iterations")
        self.iterations.setMinimum(1)
        self.iterations.setMaximum(100)
        self.iterations.setSingleStep(1)
        self.iterations.setStepType(QAbstractSpinBox.StepType.DefaultStepType)
        self.iterations.setValue(3)
        self.iterations.setDisplayIntegerBase(10)

        self.horizontalLayout_10.addWidget(self.iterations)


        self.verticalLayout_3.addLayout(self.horizontalLayout_10)

        self.horizontalLayout_12 = QHBoxLayout()
        self.horizontalLayout_12.setObjectName(u"horizontalLayout_12")
        self.label_4 = QLabel(Dialog)
        self.label_4.setObjectName(u"label_4")

        self.horizontalLayout_12.addWidget(self.label_4)

        self.s = QDoubleSpinBox(Dialog)
        self.s.setObjectName(u"s")
        self.s.setMaximum(1.000000000000000)
        self.s.setSingleStep(0.010000000000000)
        self.s.setValue(0.300000000000000)

        self.horizontalLayout_12.addWidget(self.s)


        self.verticalLayout_3.addLayout(self.horizontalLayout_12)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_3.addItem(self.verticalSpacer)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.cls_tree_widget = QTreeWidget(Dialog)
        __qtreewidgetitem1 = QTreeWidgetItem()
        __qtreewidgetitem1.setTextAlignment(1, Qt.AlignCenter);
        __qtreewidgetitem1.setTextAlignment(0, Qt.AlignCenter);
        self.cls_tree_widget.setHeaderItem(__qtreewidgetitem1)
        self.cls_tree_widget.setObjectName(u"cls_tree_widget")
        self.cls_tree_widget.setMaximumSize(QSize(200, 16777215))
        self.cls_tree_widget.setStyleSheet(u"QTreeWidget {\n"
"                        border: 0.3px solid white; /* \u8bbe\u7f6e\u63cf\u8fb9 */\n"
"                        border-radius: 5px; /* \u8bbe\u7f6e\u5706\u89d2 */\n"
"				\n"
"                    }\n"
"QTreeWidget::item {\n"
"                        padding: 5px;\n"
"            \n"
"                    }")

        self.horizontalLayout_5.addWidget(self.cls_tree_widget)


        self.verticalLayout_3.addLayout(self.horizontalLayout_5)


        self.horizontalLayout_3.addLayout(self.verticalLayout_3)

        self.verticalLayout_4 = QVBoxLayout()
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")

        self.horizontalLayout_3.addLayout(self.verticalLayout_4)


        self.verticalLayout.addLayout(self.horizontalLayout_3)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalLayout_4.setContentsMargins(6, -1, 6, -1)

        self.verticalLayout.addLayout(self.horizontalLayout_4)

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
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"\u6ee4\u6ce2", None))
        ___qtreewidgetitem = self.file_tree_widget.headerItem()
        ___qtreewidgetitem.setText(1, QCoreApplication.translate("Dialog", u"\u6587\u4ef6\u540d", None));
        ___qtreewidgetitem.setText(0, QCoreApplication.translate("Dialog", u"\u9009\u4e2d\u72b6\u6001", None));
        self.label_6.setText(QCoreApplication.translate("Dialog", u"\u6ee4\u6ce2\u7b97\u6cd5\uff1a", None))
        self.filter_type.setItemText(0, QCoreApplication.translate("Dialog", u"\u5f62\u6001\u5b66\u6ee4\u6ce2", None))

        self.label_2.setText(QCoreApplication.translate("Dialog", u"\u683c\u7f51\u5927\u5c0f\uff1a", None))
        self.grid_size.setPrefix("")
        self.grid_size.setSuffix(QCoreApplication.translate("Dialog", u"m", None))
        self.label.setText(QCoreApplication.translate("Dialog", u"\u6700\u5c0f\u9ad8\u5dee\uff1a", None))
        self.dh_min.setSuffix(QCoreApplication.translate("Dialog", u"m", None))
        self.label_3.setText(QCoreApplication.translate("Dialog", u"\u6700\u5927\u9ad8\u5dee\uff1a", None))
        self.dh_max.setSuffix(QCoreApplication.translate("Dialog", u"m", None))
        self.label_5.setText(QCoreApplication.translate("Dialog", u"\u8fed\u4ee3\u6b21\u6570\uff1a", None))
        self.iterations.setSuffix("")
        self.label_4.setText(QCoreApplication.translate("Dialog", u"\u5761\u5ea6\uff1a", None))
        ___qtreewidgetitem1 = self.cls_tree_widget.headerItem()
        ___qtreewidgetitem1.setText(1, QCoreApplication.translate("Dialog", u"\u7c7b\u540d", None));
        ___qtreewidgetitem1.setText(0, QCoreApplication.translate("Dialog", u"\u9009\u4e2d\u72b6\u6001", None));
        self.accept.setText(QCoreApplication.translate("Dialog", u"\u786e\u5b9a", None))
        self.reject.setText(QCoreApplication.translate("Dialog", u"\u53d6\u6d88", None))
    # retranslateUi

