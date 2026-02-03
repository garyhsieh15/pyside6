# -*- coding: utf-8 -*-
from pathlib import Path
import builtins
import sys
from PySide6.QtCore import Signal, Qt
from PySide6.QtWidgets import (
    QMainWindow,
    QMessageBox,
    QSplitter,
    QToolBar,
    QVBoxLayout,
    QWidget,
    QWidgetAction,
    QSizePolicy,
)

from ui.generated.label import Ui_MainWindow
from .dialogs import DialogRun
from .file_browser import FileBrowser
from .preview import PreviewManager


class MainWindow(QMainWindow):
    btn_ok_signal = Signal()

    def __init__(self):
        super(MainWindow, self).__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui_dialog_run = DialogRun()

        self.ui.menuFile_F.setTitle("檔案")
        self.ui.actionOpen.setText("開啟資料夾...")

        self.setUnifiedTitleAndToolBarOnMac(True)

        splitter = QSplitter(self)
        splitter.setOrientation(Qt.Horizontal)

        self.preview_manager = PreviewManager(self.ui.centralwidget)

        splitter.addWidget(self.ui.treeView)
        splitter.addWidget(self.preview_manager.panel_widget())
        splitter.setStretchFactor(0, 0)
        splitter.setStretchFactor(1, 1)
        splitter.setSizes([260, 600])

        central_layout = QVBoxLayout(self.ui.centralwidget)
        central_layout.setContentsMargins(0, 0, 0, 0)
        central_layout.addWidget(splitter)

        self.preview_toolbar = QToolBar(self)
        self.preview_toolbar.setMovable(False)
        self.preview_toolbar.setFloatable(False)
        self.preview_toolbar.setAllowedAreas(Qt.TopToolBarArea)
        self.preview_toolbar.setStyleSheet(
            "QToolBar { background-color: #B5B5B5; border-bottom: 1px solid #8F8F8F; }"
        )

        spacer = QWidget(self.preview_toolbar)
        spacer.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        spacer_action = QWidgetAction(self.preview_toolbar)
        spacer_action.setDefaultWidget(spacer)
        self.preview_toolbar.addAction(spacer_action)

        controls_action = QWidgetAction(self.preview_toolbar)
        controls_action.setDefaultWidget(self.preview_manager.controls_widget())
        self.preview_toolbar.addAction(controls_action)
        self.addToolBar(Qt.TopToolBarArea, self.preview_toolbar)

        self.file_browser = FileBrowser(self.ui.treeView, self.statusBar(), self)
        self.ui.treeView.clicked.connect(
            lambda index: self.preview_manager.handle_tree_click(index, self.file_browser.fs_model)
        )

        self.ui.actionRun.triggered.connect(self.popup)
        self.ui.actionFileManager.triggered.connect(self.file_browser.open_folder)
        self.ui.actionFileManager.setCheckable(True)
        self.ui.actionCallList.triggered.connect(
            lambda: self.file_browser.toggle_tree_view(self.ui.actionCallList)
        )
        self.ui.actionCallList.setCheckable(True)
        self.ui.actionOpen.triggered.connect(self.file_browser.open_folder)
        self.ui_dialog_run.dialog_run.dialog_btn_close.clicked.connect(self.btn_clicked)
        self.ui_dialog_run.dialog_run.dialog_btn_ok.clicked.connect(self.btn_clicked_ok)
        self.btn_ok_signal.connect(self.btn_ok_slot)

        self.ui.toolBar_2.removeAction(self.ui.actionCallList)
        self.ui.toolBar.insertAction(self.ui.actionFileManager, self.ui.actionCallList)
        first_action = self.ui.toolBar.actions()[0] if self.ui.toolBar.actions() else None
        if first_action and first_action is not self.ui.actionFileManager:
            self.ui.toolBar.removeAction(self.ui.actionFileManager)
            self.ui.toolBar.insertAction(first_action, self.ui.actionFileManager)

        self._check_ui_generated_freshness()

    def _check_ui_generated_freshness(self):
        pairs = [
            (Path("ui/main_win.ui"), Path("ui/generated/label.py")),
            (Path("ui/dialog_run.ui"), Path("ui/generated/dialog_run.py")),
        ]
        needs_regen = False
        for ui_path, gen_path in pairs:
            if not gen_path.exists() or (
                ui_path.exists() and ui_path.stat().st_mtime > gen_path.stat().st_mtime
            ):
                needs_regen = True
                break

        is_packaged = getattr(sys, "frozen", False) or getattr(sys, "__compiled__", False)
        is_packaged = is_packaged or getattr(builtins, "__compiled__", False)
        if needs_regen and not is_packaged:
            QMessageBox.information(
                self,
                "需要重新產生 UI",
                "UI 已更新：請執行 scripts/regenerate_ui.sh 重新產生。",
            )

    def popup(self):
        self.ui_dialog_run.show()

    def btn_clicked(self):
        self.ui_dialog_run.close()

    def btn_clicked_ok(self):
        self.btn_ok_signal.emit()

    def btn_ok_slot(self):
        print(">>> btn ok slot func")
