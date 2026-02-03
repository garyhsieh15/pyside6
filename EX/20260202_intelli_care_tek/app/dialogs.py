# -*- coding: utf-8 -*-
from PySide6.QtCore import QDir
from PySide6.QtWidgets import QFileDialog, QFileSystemModel, QMainWindow

from ui.generated.dialog_run import Ui_Dialog_Run


class DialogRun(QMainWindow):
    def __init__(self):
        super(DialogRun, self).__init__()

        self.dialog_run = Ui_Dialog_Run()
        self.dialog_run.setupUi(self)

        self.model = QFileSystemModel()
        self.model.setRootPath(QDir.currentPath())
        self.dialog_run.treeView.setModel(self.model)
        self.dialog_run.treeView.setRootIndex(self.model.index(""))

        self.dialog_run.pushButton.clicked.connect(self.open_folder_dialog)

    def open_folder_dialog(self):
        folder_path = QFileDialog.getExistingDirectory(
            self, "選擇資料夾", QDir.currentPath()
        )
        if folder_path:
            self.dialog_run.treeView.setRootIndex(self.model.index(folder_path))
