# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'error_message.ui'
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
from PySide6.QtWidgets import (QApplication, QDialog, QLabel, QSizePolicy,
    QVBoxLayout, QWidget)
import icon_rc

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(361, 242)
        Dialog.setStyleSheet(u"QDialog{\n"
"	background-color:#1f232a;\n"
"}\n"
"QPushButton:hover{\n"
"	background-color:#015371;\n"
"	border-radius: 10px;\n"
"	\n"
"}\n"
"QPushButton:pressed\n"
"{\n"
"    /*\u5de6\u5185\u8fb9\u8ddd\u4e3a3\u50cf\u7d20\uff0c\u8ba9\u6309\u4e0b\u65f6\u5b57\u5411\u53f3\u79fb\u52a83\u50cf\u7d20*/  \n"
"    padding-left:3px;\n"
"    /*\u4e0a\u5185\u8fb9\u8ddd\u4e3a3\u50cf\u7d20\uff0c\u8ba9\u6309\u4e0b\u65f6\u5b57\u5411\u4e0b\u79fb\u52a83\u50cf\u7d20*/  \n"
"    padding-top:3px;\n"
"}\n"
"\n"
"QPushButton\n"
"{\n"
"	color:#fff;\n"
"	background-color:#1f232a;\n"
"	border:1px solid;\n"
"     border-radius: 10px;\n"
"	border-color:#fff;\n"
"}")
        self.verticalLayout = QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.message = QLabel(Dialog)
        self.message.setObjectName(u"message")
        font = QFont()
        font.setPointSize(12)
        self.message.setFont(font)
        self.message.setStyleSheet(u"QLabel\n"
"{\n"
"	color:#fff;\n"
"	background-color:transparent;\n"
"	border:0px solid;\n"
"     border-radius: 10px;\n"
"	border-color:#fff;\n"
"}")
        self.message.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout.addWidget(self.message)


        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Dialog", None))
        self.message.setText(QCoreApplication.translate("Dialog", u"\u6587\u4ef6\u76ee\u5f55\u4e0d\u80fd\u4e3a\u7a7a!", None))
    # retranslateUi

