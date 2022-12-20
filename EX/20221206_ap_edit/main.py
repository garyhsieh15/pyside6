# -*- coding: utf-8 -*-
import sys

from PySide6.QtWidgets import QApplication, QMainWindow

from PySide6 import QtCore
from PySide6.QtCore import Qt, QObject, Signal
from PySide6.QtCore import QFile

#    folder.file     class
from UI.label import Ui_MainWindow
from UI.dialog_run import Ui_Dialog_Run

class MainWindow(QMainWindow):
    #定義訊號
    btn_ok_signal = Signal()
    def __init__(self):
        super(MainWindow, self).__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui_dialog_run = DialogRun()

        self.ui.actionRun.triggered.connect(self.popup)
        self.ui_dialog_run.dialog_run.dialog_btn_close.clicked.connect(self.btn_clicked)
        self.ui_dialog_run.dialog_run.dialog_btn_ok.clicked.connect(self.btn_clicked_ok)
        # 連結信號與槽函示
        self.btn_ok_signal.connect(self.btn_ok_slot)

        # >>> 設定tree的內容
        # setting num of column.
        self.ui.treeWidget.setColumnCount(1)
        # setting title of column.
        self.ui.treeWidget.setHeaderLabels(["File Manager"])

        # <<<

    # comment out @QtCore.Slot() and the code can be run OK.
    #@QtCore.Slot()
    def popup(self):
        ret = self.ui_dialog_run.show()
        #print(ret)

    def btn_clicked(self):
        self.ui_dialog_run.close()
    
    def btn_clicked_ok(self):
        #發射信號
        self.btn_ok_signal.emit()
    
    # 定義槽函式
    def btn_ok_slot(self):
        print(">>> btn ok slot func")

class DialogRun(QMainWindow):
    def __init__(self):
        super(DialogRun, self).__init__()

        self.dialog_run = Ui_Dialog_Run()
        self.dialog_run.setupUi(self)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())
