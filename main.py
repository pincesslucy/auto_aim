import cv2
import numpy as np
import mediapipe as mp
import pyautogui as pag
from mss import mss
import keyboard
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import QThread, pyqtSignal, pyqtSlot
from test import MyWindow

from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5.QtGui import QPainter, QColor, QPen
from PyQt5.QtCore import Qt, QRect, QPoint

screenWidth, screenHeight = pag.size()


class Worker(QThread):
    timeout = pyqtSignal(list)
    def __init__(self, screenWidth, screenHeight):
        super().__init__()
        self.mp_pose_detection = mp.solutions.pose
        self.pose = self.mp_pose_detection.Pose()
        self.screenWidth = screenWidth
        self.screenHeight = screenHeight
        self.num = 50
    def find_body(self, landmarks):
        x = []
        y = []
        for i in range(0, 33):
            x.append(landmarks[i].x)
            y.append(landmarks[i].y)
        return min(x)*self.screenWidth, min(y)*self.screenHeight-60, (max(x)-min(x))*self.screenWidth, (max(y)-min(y))*self.screenHeight+60

    def run(self):
        while True:

            sct = mss()

            screenshot = sct.grab(sct.monitors[0])  # 화면 캡처
            image = np.array(screenshot)

            image_ = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            results = self.pose.process(image_)

            if results.pose_landmarks:
                mp.solutions.drawing_utils.draw_landmarks(image_, results.pose_landmarks, self.mp_pose_detection.POSE_CONNECTIONS)
                nose = results.pose_landmarks.landmark[self.mp_pose_detection.PoseLandmark.NOSE]

                nose_x = int(nose.x * image.shape[1])
                nose_y = int(nose.y * image.shape[0])

                body_x, body_y, body_w, body_h = self.find_body(results.pose_landmarks.landmark)
                body_pt = [body_x, body_y, body_w, body_h]

                self.timeout.emit(body_pt)

                pag.moveTo(nose_x, nose_y)
                pag.FAILSAFE = False

        #cv2.imshow('MediaPipe Pose', image)
            if keyboard.is_pressed('q'):
                break


class MyWindow(QMainWindow, QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.worker = Worker(screenWidth, screenHeight)
        self.worker.start()
        self.worker.timeout.connect(self.timeout)

    def initUI(self):
            self.setAttribute(Qt.WA_TranslucentBackground, True)  # 배경 투명하게 설정
            self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)  # 창 테두리 없애고 항상 맨 앞에 두기
            self.setGeometry(0, 0, screenWidth, screenHeight)
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
        pen = QPen(QColor(255, 0, 0), 3)  # 펜 색상과 두께 설정
        painter.setPen(pen)  # 펜 설정
        painter.drawRect(self.rect) 

app = QApplication(sys.argv)
window = MyWindow()
window.show()
sys.exit(app.exec_())


