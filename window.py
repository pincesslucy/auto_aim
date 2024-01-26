
import pyautogui as pag
from PyQt5.QtWidgets import  QMainWindow
from PyQt5.QtCore import pyqtSlot
from worker import Worker

from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QPainter, QColor, QPen
from PyQt5.QtCore import Qt, QRect, QPoint



class MyWindow(QMainWindow, QWidget):
    
    def __init__(self):
        super().__init__()
        self.initUI()
        self.worker = Worker(self.screenWidth, self.screenHeight)
        self.worker.start()
        self.worker.timeout.connect(self.timeout)

    def initUI(self):
            self.screenWidth, self.screenHeight = pag.size()
            self.setAttribute(Qt.WA_TranslucentBackground, True)  # 배경 투명하게 설정
            self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)  # 창 테두리 없애고 항상 맨 앞에 두기
            self.setGeometry(0, 0, self.screenWidth, self.screenHeight)
            self.rect = QRect(0, 0, 100, 100)  # 사각형의 초기 위치와 크기 설정

    @pyqtSlot(list)
    def timeout(self, body_pt):
        self.rect.moveTopLeft(QPoint(int(body_pt[0]), int(body_pt[1])))

        self.rect.setWidth(int(body_pt[2]))
        self.rect.setHeight(int(body_pt[3]))
        super().update()

    def paintEvent(self, event):
    
        painter = QPainter(self)
        # 테두리 그리기
        pen = QPen(QColor(0, 255, 0), 6)  # 펜 색상과 두께 설정
        painter.setPen(pen)  # 펜 설정
        painter.drawRect(self.rect) 
