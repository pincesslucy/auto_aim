from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtGui import QPainter, QColor, QPen
from PyQt5.QtCore import Qt
import sys

class TransparentWindow(QWidget):
    def __init__(self,screenW, screenH, x, y, w, h):
        super().__init__()

        # 창 설정
        self.setAttribute(Qt.WA_TranslucentBackground, True)  # 배경 투명하게
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)  # 창 테두리 없애고 항상 위에 띄우기
        self.setGeometry(0, 0, screenW, screenH)
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        

    def paintEvent(self, event):
        
        painter = QPainter(self)

        # 테두리 그리기
        pen = QPen(QColor(255, 0, 0), 3)  # 펜 색상과 두께 설정
        painter.setPen(pen)  # 펜 설정
        painter.drawRect(self.x, self.y, self.w, self.h)

# if __name__ == "__main__":
#     app = QApplication(sys.argv)

#     window = TransparentWindow(1920, 1080, 100, 100, 200, 200)
#     window.show()

#     sys.exit(app.exec_())
