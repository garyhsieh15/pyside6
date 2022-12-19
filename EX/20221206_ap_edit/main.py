import sys

from PySide6.QtWidgets import QApplication, QMainWindow

from PySide6 import QtCore
from PySide6.QtCore import Qt, QObject
from PySide6.QtCore import QFile

#    folder.file     class
from UI.label import Ui_MainWindow
from UI.dialog_run import Ui_Dialog_Run

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui_dialog_run = DialogRun()
        self.ui.actionRun.triggered.connect(self.popup)

    @QtCore.Slot()
    def popup(self):
        ret = self.ui_dialog_run.show()
        #print(ret)

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
