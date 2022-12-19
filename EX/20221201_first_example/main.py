import sys

from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtCore import QFile
#    folder.file     class
from UI.label import UiMainWindow
#     folder    file
#from UI import label

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = UiMainWindow()
        #self.ui = label.UiMainWindow()
        self.ui.setupUi(self)

if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())
