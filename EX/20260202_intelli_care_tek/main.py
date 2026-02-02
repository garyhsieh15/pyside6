# -*- coding: utf-8 -*-
import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QFileSystemModel, QFileDialog
from PySide6.QtGui import QStandardItemModel, QStandardItem
from PySide6.QtCore import Signal, QDir

#    folder.file     class
from UI.label import Ui_MainWindow
from UI.dialog_run import Ui_Dialog_Run

class MainWindow(QMainWindow):
    # 定義訊號
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

    # comment out @QtCore.Slot() and the code can be run OK.
    # @QtCore.Slot()
    def popup(self):
        ret = self.ui_dialog_run.show()
        # print(ret)

    def btn_clicked(self):
        self.ui_dialog_run.close()
    
    def btn_clicked_ok(self):
        # 發射信號
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

        # 設定dialog_run中的treeView的內容
        self.model = QFileSystemModel()
        self.model.setRootPath(QDir.currentPath())
        self.dialog_run.treeView.setModel(self.model)
        self.dialog_run.treeView.setRootIndex(self.model.index(""))  # 設置為空白

        # 連結pushButton的點擊事件
        self.dialog_run.pushButton.clicked.connect(self.open_folder_dialog)

    def open_folder_dialog(self):
        folder_path = QFileDialog.getExistingDirectory(self, "選擇資料夾", QDir.currentPath())
        if folder_path:
            self.dialog_run.treeView.setRootIndex(self.model.index(folder_path))

if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())