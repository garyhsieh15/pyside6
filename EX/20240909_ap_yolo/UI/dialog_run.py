# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'dialog_run.ui'
##
## Created by: Qt User Interface Compiler version 6.7.2
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
    QLabel, QPushButton, QSizePolicy, QTreeView,
    QWidget)

class Ui_Dialog_Run(object):
    def setupUi(self, Dialog_Run):
        if not Dialog_Run.objectName():
            Dialog_Run.setObjectName(u"Dialog_Run")
        Dialog_Run.resize(956, 597)
        self.layoutWidget = QWidget(Dialog_Run)
        self.layoutWidget.setObjectName(u"layoutWidget")
        self.layoutWidget.setGeometry(QRect(430, 530, 351, 53))
        self.horizontalLayout = QHBoxLayout(self.layoutWidget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.dialog_btn_ok = QPushButton(self.layoutWidget)
        self.dialog_btn_ok.setObjectName(u"dialog_btn_ok")

        self.horizontalLayout.addWidget(self.dialog_btn_ok)

        self.dialog_btn_close = QPushButton(self.layoutWidget)
        self.dialog_btn_close.setObjectName(u"dialog_btn_close")

        self.horizontalLayout.addWidget(self.dialog_btn_close)

        self.treeView = QTreeView(Dialog_Run)
        self.treeView.setObjectName(u"treeView")
        self.treeView.setGeometry(QRect(40, 200, 311, 291))
        self.label = QLabel(Dialog_Run)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(140, 60, 58, 15))
        self.pushButton = QPushButton(Dialog_Run)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setGeometry(QRect(520, 70, 93, 28))

        self.retranslateUi(Dialog_Run)

        QMetaObject.connectSlotsByName(Dialog_Run)
    # setupUi

    def retranslateUi(self, Dialog_Run):
        Dialog_Run.setWindowTitle(QCoreApplication.translate("Dialog_Run", u"Dialog", None))
        self.dialog_btn_ok.setText(QCoreApplication.translate("Dialog_Run", u"OK", None))
        self.dialog_btn_close.setText(QCoreApplication.translate("Dialog_Run", u"Close", None))
        self.label.setText(QCoreApplication.translate("Dialog_Run", u"src", None))
        self.pushButton.setText(QCoreApplication.translate("Dialog_Run", u"PushButton", None))
    # retranslateUi

