# -*- coding: utf-8 -*-
from PySide6.QtCore import QObject, QDir, QTimer
from PySide6.QtWidgets import QFileDialog, QFileSystemModel


class FileBrowser(QObject):
    def __init__(self, tree_view, status_bar, parent=None):
        super().__init__(parent)
        self.tree_view = tree_view
        self.status_bar = status_bar
        self.fs_model = QFileSystemModel()
        self.fs_model.setRootPath(QDir.currentPath())
        self.tree_view.setModel(self.fs_model)
        self.tree_view.setRootIndex(self.fs_model.index(QDir.currentPath()))
        for col in range(1, self.fs_model.columnCount()):
            self.tree_view.setColumnHidden(col, True)

    def toggle_tree_view(self, action):
        action.setChecked(True)
        QTimer.singleShot(150, lambda: action.setChecked(False))

        if self.tree_view.isVisible():
            self.tree_view.setVisible(False)
            if self.status_bar:
                self.status_bar.showMessage("已隱藏檔案清單", 2000)
            return

        self.tree_view.setVisible(True)
        if self.status_bar:
            self.status_bar.showMessage("已顯示檔案清單", 2000)

    def open_folder(self):
        folder_path = QFileDialog.getExistingDirectory(
            self.tree_view, "選擇資料夾", QDir.currentPath()
        )
        if not folder_path:
            if self.status_bar:
                self.status_bar.showMessage("已取消選擇資料夾", 2000)
            return

        if not self.tree_view.isVisible():
            self.tree_view.setVisible(True)
        self.tree_view.setRootIndex(self.fs_model.index(folder_path))
        if self.status_bar:
            self.status_bar.showMessage(f"已切換資料夾：{folder_path}", 3000)
