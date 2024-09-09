# -*- coding: utf-8 -*-
import sys

from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtWidgets import QFileSystemModel

from PySide6.QtGui import QStandardItemModel, QStandardItem

from PySide6 import QtCore
from PySide6.QtCore import Signal
from PySide6.QtCore import QFile, QDir

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

        # >>> 設定treeView的內容
        #model_00 = QFileSystemModel()
        #model_00.setRootPath(QDir.currentPath())
        #self.ui.treeView.setModel(model_00)
        
        model = QStandardItemModel(self.ui.treeView)
        model.setHorizontalHeaderLabels(["class", "NP"])
        #model.invisibleRootItem()
        for row in range(4):
            item = QStandardItem("row- "+str(row))
            for column in range(2):
                item2 = QStandardItem("column: "+str(column))
                # 讓欄位點兩下後，不可編輯
                item2.setEditable(False)
                item.appendRow(item2)
            model.appendRow(item)
        
        self.ui.treeView.setModel(model)
        # 全部展開
        self.ui.treeView.expandAll()
        self.ui.treeView.doubleClicked.connect(self.get_value)
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

    
    def get_value(self, val):
        print(">>> show val.data: ", val.data())
        print(">>> show val.row: ", val.row())
        print(">>> show val.column: ", val.column())

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
