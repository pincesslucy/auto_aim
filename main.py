import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import  pyqtSlot
from window import MyWindow

from PyQt5.QtWidgets import QApplication

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWindow()
    ex.show()
    sys.exit(app.exec_())
