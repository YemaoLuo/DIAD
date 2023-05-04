import sys
from time import sleep

from PIL import ImageGrab
from PyQt5.QtWidgets import QApplication, QMainWindow, QAction, QFileDialog, QDesktopWidget, QLabel, QPushButton
from PyQt5.QtGui import QPixmap, QPainter, QPen, QColor
from PyQt5.QtCore import Qt, QPoint, QRect


class FrameRange(QMainWindow):
    def __init__(self):
        super().__init__()
        self.title = 'Dangerous Item Automatically Detection'
        self.left = 10
        self.top = 10
        self.width = screen_w
        self.height = screen_h
        self.begin = QPoint()
        self.end = QPoint()
        self.image_path = 'ScreenShot.jpg'
        self.initUI()

    def initUI(self):
        CurrentImage = ImageGrab.grab()  # 获得当前屏幕
        # screen_w, screen_h = p.size  # 获得当前屏幕的大小
        CurrentImage.save("ScreenShot.jpg")
        self.setWindowTitle(self.title)
        # self.setStyleSheet('background-image: url(ScreenShot.jpg); background-repeat: no-repeat; background-position: center;')
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.center()
        # self.toolbar = self.addToolBar('Tools')
        self.background = QLabel(self)
        # self.background.setPixmap(QPixmap('ScreenShot.jpg'))
        # self.background.setGeometry(0, 0, self.background.pixmap().width(), self.background.pixmap().height())
        self.save_action = QAction('Save', self)
        self.save_action.setShortcut('Ctrl+S')
        self.save_action.triggered.connect(self.confirm)
        # confirmbutton
        self.Confirmbutton = QPushButton(self)
        self.Confirmbutton.move(0,0)
        self.Confirmbutton.setFixedSize(150, 80)
        self.Confirmbutton.clicked.connect(self.confirm)
        self.Confirmbutton.setStyleSheet("""
                          QPushButton {
                              background-image: url(Confirm.svg);
                              color: green;
                              border-style: solid;
                          }
                          QPushButton:hover {
                              background-image: url(Confirm.svg);
                              border-color: green;
                          }
                          QPushButton:pressed {
                              background-color: #2e6b2e;
                              border-color: #2e6b2e;
                          }
                      """)
        #exitbutton
        self.Exitbutton=QPushButton(self)
        self.Exitbutton.move(150,0)
        self.Exitbutton.setFixedSize(150, 80)
        self.Exitbutton.clicked.connect(self.Exit)
        self.Exitbutton.setStyleSheet("""
                    QPushButton {
                        background-image: url(Exit.svg);
                        color: white;
                        border-style: solid;
                    }
                    QPushButton:hover {
                         background-image: url(Exit.svg);
                         border-color: red;
                    }
                    QPushButton:pressed {
                        background-color: red;
                        border-color: red;
                    }
                """)
        self.show()

    def center(self):
        frame_geometry = self.frameGeometry()
        center_position = QDesktopWidget().availableGeometry().center()
        frame_geometry.moveCenter(center_position)
        self.move(frame_geometry.topLeft())

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        # painter.setWindowFlags(Qt.WindowStaysOnTopHint)
        painter.setPen(QPen(QColor(61, 145, 64, 200), 5, Qt.DotLine))
        painter.setBrush(QColor(61, 145, 64, 0))
        painter.drawRect(QRect(self.begin, self.end))
        self.Confirmbutton.move(self.end)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.begin = event.pos()
            self.end = self.begin
            self.update()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            self.end = event.pos()
            self.update()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.end = event.pos()
            self.update()

    def confirm(self):
        x1 = min(self.begin.x(), self.end.x())
        y1 = min(self.begin.y(), self.end.y())
        x2 = max(self.begin.x(), self.end.x())
        y2 = max(self.begin.y(), self.end.y())
        print(f"Selected Range: ({x1}, {y1}), ({x2}, {y2})")
        self.close()
    def Exit(self):
        self.close()

if __name__ == '__main__':
    p = ImageGrab.grab()  # 获得当前屏幕
    screen_w, screen_h = p.size  # 获得当前屏幕的大小
    p.save("ScreenShot.jpg")
    app = QApplication(sys.argv)
    SelectWindow = FrameRange()
    # ex.setStyleSheet('background-image: url(ScreenShot.jpg); background-repeat: no-repeat; background-position: center;')
    SelectWindow.setStyleSheet('background-image: url(ScreenShot.jpg); background-repeat: no-repeat; background-position: center;}')
    sys.exit(app.exec_())