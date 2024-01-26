import cv2
import numpy as np
import mediapipe as mp
import pyautogui as pag
from mss import mss
import keyboard
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import QThread, pyqtSignal
from transparentwindow import TransparentWindow
from test import MyWindow
import time

from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5.QtGui import QPainter, QColor, QPen
from PyQt5.QtCore import Qt, QTimer, QRect, QPoint

#mediapipe
# mp_pose_detection=mp.solutions.pose
# pose = mp_pose_detection.Pose()
screenWidth, screenHeight = pag.size()

#screenshot
# sct = mss()

#transparent window


class Worker(QThread):
    timeout = pyqtSignal(int)
    def __init__(self, screenWidth, screenHeight):
        super().__init__()
        self.mp_pose_detection = mp.solutions.pose
        self.pose = self.mp_pose_detection.Pose()
        self.screenWidth = screenWidth
        self.screenHeight = screenHeight
    def find_body(self, landmarks):
        x = []
        y = []
        for i in range(0, 33):
            x.append(landmarks[i].x)
            y.append(landmarks[i].y)
        return min(x) * self.screenWidth, min(y) * self.screenHeight, (max(x) - min(x)) * self.screenWidth, (max(y) - min(y)) * self.screenHeight

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
                
                self.num = 50
                self.timeout.emit(self.num)

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
        # self.worker.timeout.connect(self.timeout)

    def initUI(self):
            self.setAttribute(Qt.WA_TranslucentBackground, True)  # 배경 투명하게 설정
            self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)  # 창 테두리 없애고 항상 맨 앞에 두기
            self.setGeometry(0, 0, screenWidth, screenHeight)
            
            self.rect = QRect(0, 0, 100, 100)  # 사각형의 초기 위치와 크기 설정
            # self.worker.timeout.connect(self.timeout)
            # self.timer = QTimer()  # 타이머 생성
            # self.timer.setInterval(50)  # 타이머 간격 설정 (50ms)
            # self.timer.timeout.connect(self.update)  # 타이머 시간이 다 되면 update() 메서드 호출
            # self.timer.start()  # 타이머 시작

    # @pyqtSlot(int)
    # def timeout(self, num):
    #     print(num)

    def paintEvent(self, event):
    
        painter = QPainter(self)

        # 테두리 그리기
        pen = QPen(QColor(255, 0, 0), 3)  # 펜 색상과 두께 설정
        painter.setPen(pen)  # 펜 설정
        painter.drawRect(100, 100, 100, 100)

app = QApplication(sys.argv)
window = MyWindow()
window.show()
sys.exit(app.exec_())


