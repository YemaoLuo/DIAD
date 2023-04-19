import sys
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QLabel, QPushButton, QVBoxLayout, QWidget
from PyQt6.QtCore import Qt
class StartWindow(QWidget):
    def __init__(self):
        super().__init__()

        # Set the window size and title
        self.setGeometry(100, 100,1480, 800)
        self.setWindowTitle('Start Window')

        # Load image and set it as the background
        self.background = QLabel(self)
        # self.background.setPixmap(QPixmap('radar.png'))#backgroudImage
        self.background.setGeometry(0, 0, 400, 400)

        # Create a QVBoxLayout to hold the button
        layout = QVBoxLayout()
        self.label = QLabel('HELLO', self)
        self.label.setStyleSheet(
            'font-size: 48px; color: black; background-color: white; border-radius: 10px; padding: 20px;')
        self.label.setGeometry(0, 0, self.width(), self.height())
        self.label.setAlignment(Qt.AlignCenter)
        # Create a QPushButton and add it to the layout
        self.Startbutton = QPushButton("Start",self)
        # self.Startbutton.setGeometry(0, 0, 200, 50)
        self.Startbutton.move(500,500)
        self.Startbutton.setFixedSize(150, 80)
        self.Startbutton.setStyleSheet(
            "QPushButton {"
            "background-color: #3fa9f5;"
            "border: 2px solid #1a5d99;"
            "border-radius: 25px;"
            "color: #fff;"
            "font-size: 18px;"
            "font-weight: bold;"
            "padding: 8px 16px;"
            "text-align: center;"
            "}"
            "QPushButton:hover {"
            "background-color: #50b8ff;"
            "}"
            "QPushButton:pressed {"
            "background-color: #1a5d99;"
            "border: 2px solid #3fa9f5;"
            "}"
        )
        # layout.addWidget(self.Startbutton)

        # Set the layout for the window
        # self.setLayout(layout)

        # Connect the button to a function that opens a new window
        self.Startbutton.clicked.connect(self.open_new_window)

    def open_new_window(self):
        # Create a new window with a size of 400x400 and a blank background
        new_window = QWidget()
        new_window.setGeometry(100, 100, 400, 400)
        new_window.setStyleSheet('background-color: white;')
        new_window.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = StartWindow()
    window.show()
    sys.exit(app.exec_())