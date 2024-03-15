
import pyautogui as pag
from PyQt5.QtWidgets import  QMainWindow
from PyQt5.QtCore import pyqtSlot
from worker import Worker

from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QPainter, QColor, QPen
from PyQt5.QtCore import Qt, QRect, QPoint
import numpy as np




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
            self.rects = []

    @pyqtSlot(list)
    def timeout(self, boxes):
        self.rects = [QRect(x1, y1, x2-x1, y2-y1) for x1, y1, x2, y2 in boxes]
        self.update()

    def paintEvent(self, event):
    
        painter = QPainter(self)
        pen = QPen(QColor(0, 255, 0), 6)  # 펜 색상과 두께 설정
        painter.setPen(pen)  # 펜 설정
        for rect in self.rects:
            painter.drawRect(rect)  # 리스트에 저장된 모든 사각형 그리기
