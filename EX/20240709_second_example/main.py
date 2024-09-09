import sys

from PySide6.QtWidgets import QApplication, QMainWindow, QDialog
from PySide6.QtCore import QFile
from UI.label import UiMainWindow
from UI.dialog_NEW import Ui_DialogNEW # 確保已經有dialog_NEW.ui轉換成的Python檔案

class DialogNEW(QDialog):
    def __init__(self):
        super(DialogNEW, self).__init__()
        self.ui = Ui_DialogNEW()
        self.ui.setupUi(self)

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = UiMainWindow()
        self.ui.setupUi(self)
        
        # 修改這裡來顯示DialogNEW視窗
        self.ui.pushButton_5.clicked.connect(self.showDialogNEW)

    def showDialogNEW(self):
        self.dialog = DialogNEW()
        self.dialog.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())