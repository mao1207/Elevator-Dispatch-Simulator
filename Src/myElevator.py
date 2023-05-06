import sys, threading
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon

from elevatorUI import *
from dispatch import *


class mywindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(mywindow, self).__init__()
        self.setupUi(self)
        self.setWindowTitle('Elevator Dispatch')
        self.setWindowIcon(QIcon('../Resources/Icon/icon.png'))

if __name__ == '__main__':
    app = QApplication(sys.argv)

    window = mywindow()

    window.show()

    sys.exit(app.exec())
