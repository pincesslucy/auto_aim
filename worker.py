from PyQt5.QtCore import QThread, pyqtSignal
import cv2
import numpy as np
import mediapipe as mp
import pyautogui as pag
from mss import mss
import keyboard


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
        return min(x)*self.screenWidth, min(y)*self.screenHeight-60, (max(x)-min(x))*self.screenWidth, ((max(y)-min(y))*self.screenHeight)+60

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
        
# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     ex = MyWindow()
#     ex.show()
#     sys.exit(app.exec_())
