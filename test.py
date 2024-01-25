import sys
from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5.QtGui import QPainter, QColor, QPen
from PyQt5.QtCore import Qt, QTimer, QRect

class MyWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setAttribute(Qt.WA_TranslucentBackground, True)  # 배경 투명하게 설정
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)  # 창 테두리 없애고 항상 맨 앞에 두기
        self.setGeometry(300, 300, 500, 500)  # 창 크기 및 위치 설정

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
        self.rect.moveTop(self.rect.y() + 5)  # 사각형의 y 좌표를 5 증가
        if self.rect.y() > self.height():  # 사각형이 창 밖으로 나가면
            self.rect.moveTop(0)  # 사각형의 y 좌표를 0으로 설정
        super().update()  # 화면 갱신

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWindow()
    ex.show()
    sys.exit(app.exec_())
