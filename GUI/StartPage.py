import sys
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QLabel, QPushButton, QVBoxLayout, QWidget, QHBoxLayout
from PyQt5.QtCore import Qt
class StartWindow(QWidget):
    def __init__(self):
        super().__init__()

        # Set the window size and title
        self.setGeometry(100, 100,880, 560)
        self.setWindowTitle('Start Window')

        # Load image and set it as the background
        self.background = QLabel(self)
        # self.background.setPixmap(QPixmap('radar.png'))#backgroudImage
        self.background.setGeometry(0, 0, 400, 400)

        # Create a QVBoxLayout to hold the button
        layout = QVBoxLayout()
        self.label = QLabel('Dangerous Item Auto Detection', self)
        self.label.setStyleSheet(
            'font-size: 48px; color: black')
        self.label.setGeometry(0, 0, self.width(), self.height())
        self.label.setAlignment(Qt.AlignCenter)
        # Create a QPushButton and add it to the layout
        self.Startbutton = QPushButton("Select Detection Area",self)
        # self.Startbutton.setGeometry(0, 0, 200, 50)
        # self.Startbutton.setAlignment(Qt.AlignCenter)
        self.Startbutton.setFixedSize(300, 80)
        self.Startbutton.setStyleSheet(
            "QPushButton {"
            "background-color: #2e6b2e;"
            "border: 5px soild #90EE90;"
            "border-radius: 25px;"
            "color:white;"
            "font-size: 18px;"
            "font-weight: bold;"
            "padding: 8px 16px;"
            "text-align: center;"
            "}"
            "QPushButton:hover {"
            "background-color: green;"
            "}"
            "QPushButton:pressed {"
            "background-color: #2e6b2e;"
            "border: 2px solid #2e6b2e;"
            "}"
        )
        # Create vertical layout and add label and button to it
        vlayout = QVBoxLayout()
        vlayout.addWidget(self.label)
        vlayout.addWidget(self.Startbutton)

        # Set label and button to center horizontally
        self.label.setAlignment(Qt.AlignHCenter)
        # self.Startbutton.setAlignment(Qt.AlignHCenter)

        # Create horizontal layout and add vertical layout to it
        hlayout = QHBoxLayout()
        hlayout.addStretch()
        hlayout.addLayout(vlayout)
        hlayout.addStretch()

        # Set layout to center horizontally
        hlayout.setAlignment(Qt.AlignCenter)
        vlayout.setAlignment(Qt.AlignCenter)
        # Set window layout
        self.setLayout(hlayout)

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