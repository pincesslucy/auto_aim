from PyQt5.QtCore import QThread, pyqtSignal
import cv2
import numpy as np
import pyautogui as pag
from mss import mss
import keyboard
from ultralytics import YOLO
import torch


class Worker(QThread):
    timeout = pyqtSignal(list)
   
    def __init__(self, screenWidth, screenHeight):
        super().__init__()
        self.screenWidth = screenWidth
        self.screenHeight = screenHeight
        self.num = 50
        self.model = YOLO("yolov8m-pose.pt")

    def predict(self, frame, iou=0.7, conf=0.25):
        results = self.model(
            source=frame,
            device= "cuda:0" if torch.cuda.is_available() else "cpu",
            iou=iou,
            conf=conf,
            verbose=False,
        )
        result = results[0]
        return result

    def get_boxes(self, frame, result):
        bboxes = []
        for boxes in result.boxes:
            x1, y1, x2, y2, score, classes = boxes.data.squeeze().cpu().numpy()
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
            bboxes.append((x1, y1, x2, y2))
        return bboxes

    def run(self):
        while True:

            sct = mss()

            screenshot = sct.grab(sct.monitors[0])  # 화면 캡처
            image = np.array(screenshot)
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            result = self.predict(image)
            bbox = self.get_boxes(image, result)
            self.timeout.emit(bbox)

        #cv2.imshow('MediaPipe Pose', image)
            if keyboard.is_pressed('q'):
                break
        
# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     ex = MyWindow()
#     ex.show()
#     sys.exit(app.exec_())
