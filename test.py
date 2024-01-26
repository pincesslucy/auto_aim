import sys
from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5.QtGui import QPainter, QColor, QPen
from PyQt5.QtCore import Qt, QTimer, QRect, QPoint

class MyWindow(QWidget):
    def __init__(self, body_pt):
        super().__init__()
        self.initUI()
        self.body_pt = body_pt

    def initUI(self):
        self.setAttribute(Qt.WA_TranslucentBackground, True)  # 배경 투명하게 설정
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)  # 창 테두리 없애고 항상 맨 앞에 두기
        self.setGeometry(0, 0, 1900, 800)
        
        self.rect = QRect(0, 0, 100, 100)  # 사각형의 초기 위치와 크기 설정

        self.timer = QTimer()  # 타이머 생성
        self.timer.setInterval(50)  # 타이머 간격 설정 (50ms)
        self.timer.timeout.connect(self.update)  # 타이머 시간이 다 되면 update() 메서드 호출
        self.timer.start()  # 타이머 시작

    def paintEvent(self, e):
        qp = QPainter()
        qp.begin(self)
        self.drawRectangles(qp)  # 사각형 그리기
        qp.end()

    def drawRectangles(self, qp):
        pen = QPen(QColor(255, 0, 0), 3)  # 펜 색상과 두께 설정
        qp.setPen(pen)
        qp.drawRect(self.rect)  # 사각형 그리기

    def update(self):
        # 사각형의 위치를 코의 위치로 설정
        self.rect.moveCenter(QPoint(int(self.body_pt[0]), int(self.body_pt[1])))

        self.rect.setWidth(int(self.body_pt[2]))
        self.rect.setHeight(int(self.body_pt[3]))
        super().update()  # 화면 갱신
        
# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     ex = MyWindow()
#     ex.show()
#     sys.exit(app.exec_())
