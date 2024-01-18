import sys

from PyQt5.QtWidgets import *


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Student management system')

        file_menu_item = self.menuBar().addMenu('&File')
        help_menu_item = self.menuBar().addMenu('&Help')


app = QApplication(sys.argv)
main_page = MainWindow()
main_page.show()
sys.exit(app.exec())
