# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'show_by_classification.ui'
##
## Created by: Qt User Interface Compiler version 6.8.2
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
    QPushButton, QSizePolicy, QSpacerItem, QTreeWidget,
    QTreeWidgetItem, QVBoxLayout, QWidget)
import icon_rc

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(442, 327)
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
        self.treeWidget = QTreeWidget(Dialog)
        __qtreewidgetitem = QTreeWidgetItem()
        __qtreewidgetitem.setTextAlignment(3, Qt.AlignCenter);
        __qtreewidgetitem.setTextAlignment(2, Qt.AlignCenter);
        __qtreewidgetitem.setTextAlignment(1, Qt.AlignCenter);
        __qtreewidgetitem.setTextAlignment(0, Qt.AlignCenter);
        self.treeWidget.setHeaderItem(__qtreewidgetitem)
        self.treeWidget.setObjectName(u"treeWidget")
        self.treeWidget.setStyleSheet(u"QTreeWidget {\n"
"                        border: 0.2px solid white; /* \u8bbe\u7f6e\u63cf\u8fb9 */\n"
"                        border-radius: 5px; /* \u8bbe\u7f6e\u5706\u89d2 */\n"
"                    }\n"
"\n"
"                    QTreeWidget::item {\n"
"                        padding: 5px;\n"
"            \n"
"                    }")

        self.verticalLayout.addWidget(self.treeWidget)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(-1, 0, -1, 3)
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer)

        self.help = QPushButton(Dialog)
        self.help.setObjectName(u"help")

        self.horizontalLayout_2.addWidget(self.help)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_2)

        self.pushButton_3 = QPushButton(Dialog)
        self.pushButton_3.setObjectName(u"pushButton_3")
        self.pushButton_3.setStyleSheet(u"")

        self.horizontalLayout_2.addWidget(self.pushButton_3)

        self.pushButton_2 = QPushButton(Dialog)
        self.pushButton_2.setObjectName(u"pushButton_2")
        self.pushButton_2.setMaximumSize(QSize(70, 16777215))

        self.horizontalLayout_2.addWidget(self.pushButton_2)


        self.verticalLayout.addLayout(self.horizontalLayout_2)


        self.verticalLayout_2.addLayout(self.verticalLayout)


        self.retranslateUi(Dialog)
        self.pushButton_2.clicked.connect(Dialog.reject)
        self.pushButton_3.clicked.connect(Dialog.accept)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"\u6309\u9ad8\u7a0b\u663e\u793a", None))
        ___qtreewidgetitem = self.treeWidget.headerItem()
        ___qtreewidgetitem.setText(3, QCoreApplication.translate("Dialog", u"\u989c\u8272", None));
        ___qtreewidgetitem.setText(2, QCoreApplication.translate("Dialog", u"\u7c7b\u540d", None));
        ___qtreewidgetitem.setText(1, QCoreApplication.translate("Dialog", u"\u7c7bID", None));
        ___qtreewidgetitem.setText(0, QCoreApplication.translate("Dialog", u"\u9009\u4e2d\u72b6\u6001", None));
        self.help.setText(QCoreApplication.translate("Dialog", u"\u5e2e\u52a9", None))
        self.pushButton_3.setText(QCoreApplication.translate("Dialog", u"\u786e\u5b9a", None))
        self.pushButton_2.setText(QCoreApplication.translate("Dialog", u"\u53d6\u6d88", None))
    # retranslateUi

