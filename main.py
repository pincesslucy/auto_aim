import cv2
import numpy as np
import mediapipe as mp
import pyautogui as pag
from mss import mss
import keyboard
import sys
from PyQt5.QtWidgets import QApplication
from transparentwindow import TransparentWindow
import time

#mediapipe
mp_pose_detection=mp.solutions.pose
pose = mp_pose_detection.Pose()
screenWidth, screenHeight = pag.size()

#screenshot
sct = mss()

#transparent window

app = QApplication(sys.argv)

def find_body(landmarks):
    x = []
    y = []
    for i in range(0, 33):
        x.append(landmarks[i].x)
        y.append(landmarks[i].y)
    return min(x) * screenWidth, min(y) * screenHeight, (max(x) - min(x)) * screenWidth, (max(y) - min(y)) * screenHeight

while True:
    screenshot = sct.grab(sct.monitors[0])  # 화면 캡처
    image = np.array(screenshot)

    image_ = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    results = pose.process(image_)

    if results.pose_landmarks:
        mp.solutions.drawing_utils.draw_landmarks(image_, results.pose_landmarks, mp_pose_detection.POSE_CONNECTIONS)
        nose = results.pose_landmarks.landmark[mp_pose_detection.PoseLandmark.NOSE]
        nose_x = int(nose.x * image.shape[1])
        nose_y = int(nose.y * image.shape[0])

        body_x, body_y, body_w, body_h = find_body(results.pose_landmarks.landmark)
        
        pag.moveTo(nose_x, nose_y)

        window = TransparentWindow(screenWidth, screenHeight, body_x, body_y, body_w, body_h)
        window.show()

    #cv2.imshow('MediaPipe Pose', image)
        if keyboard.is_pressed('q'):
            break

sys.exit(app.exec_())