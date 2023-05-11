import mss
import psutil
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtCore import QTimer
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QImage, QFont, QColor
from PyQt5.QtWidgets import QApplication, QWidget, QHBoxLayout, QVBoxLayout, QFrame, QLabel, QProgressBar, QPushButton, \
    QDesktopWidget, QMainWindow, QGraphicsDropShadowEffect

from deploy import load_model, predict


class ImageDetectionThread(QThread):
    result_ready = pyqtSignal(object)

    def __init__(self, region):
        super().__init__()
        self.region = region

    def run(self):
        x, y, width, height = self.region
        with mss.mss() as sct:
            monitor = {"top": y, "left": x, "width": width, "height": height}
            mss_image = sct.grab(monitor)
        Model = load_model()
        detected_image = predict(Model, mss_image)
        self.result_ready.emit(detected_image)


class StartDetect(QMainWindow):
    def __init__(self, x1, y1, x2, y2):
        super().__init__()
        self.main_window = MainWindow(x1, y1, x2, y2)
        self.setCentralWidget(self.main_window)
        desktop = QDesktopWidget()
        screen_width = desktop.screenGeometry().width()
        screen_height = desktop.screenGeometry().height()
        half_width = screen_width / 2
        self.setGeometry(0, 35, half_width, 670)
        self.setWindowTitle("DIAD")
        #
        # # self.setWindowFlags(Qt.FramelessWindowHint)
        # self.setAttribute(Qt.WA_TranslucentBackground,True)
        self.setStyleSheet("background-color: rgba(60, 60, 60)")
        # pal = self.main_window.palette()
        # pal.setColor(QPalette.Background, QColor(255, 255, 255, 128))
        # self.main_window.setPalette(pal)

        # self.setAttribute(Qt.WA_TranslucentBackground)
        #
        # pal = self.main_window.palette()
        # pal.setColor(QPalette.Background, QColor(0, 255, 0, 0))
        # self.main_window.setPalette(pal)

        self.setFixedSize(self.size())


class MainWindow(QWidget):
    def __init__(self, x1, y1, x2, y2):
        super().__init__()

        self.region = (x1, y1, x2 - x1, y2 - y1)

        self.image_detection_thread = ImageDetectionThread(self.region)
        self.image_detection_thread.result_ready.connect(self.display_result)

        self.font = QFont()
        self.font.setFamily("Microsoft YaHei")
        # self.font.setWeight(10)
        self.font.setBold(True)

        desktop = QDesktopWidget()
        screen_width = desktop.screenGeometry().width()
        screen_height = desktop.screenGeometry().height()

        self.rightFrame = QFrame(self)
        self.rightFrame.setStyleSheet("""
            QFrame {
                background-color: rgba(255, 255, 255, 255);
                border-top-right-radius: 20px;
                border-bottom-right-radius: 20px;
            }
        """)
        # self.rightFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.add_shadow(self.rightFrame)

        mainLayout = QVBoxLayout(self)
        topLayout = QHBoxLayout()
        bottomLayout = QHBoxLayout()

        self.rightFrame.setFixedWidth(245)
        self.rightFrame.setFixedHeight(screen_height - 500)

        self.screenshot_label = QLabel(self)
        self.screenshot_label.setMinimumSize(screen_width / 2 - 250, screen_height - 500)
        pixmap = QPixmap('cat.png')
        self.screenshot_label.setPixmap(pixmap)
        self.screenshot_label.setStyleSheet(
            "background-color: rgba(255, 255, 255);border-top-left-radius: 20px;border-bottom-left-radius: 20px;")

        self.screenshot_label.setAlignment(Qt.AlignCenter)
        self.add_shadow(self.screenshot_label)
        self.screenshot_label.lower()
        # self.region=(900,20,900,800)
        self.region = (x1, y1, x2 - x1, y2 - y1)
        # self.screenshot(self.region)

        # self.screenshot_label.setStyleSheet("border: 2px solid black;")

        leftLayout = QVBoxLayout(self.screenshot_label)
        leftLayout.addWidget(self.screenshot_label)

        self.progressWrapper = QWidget(self)
        self.progressWrapper.setStyleSheet("background-color: rgba(255, 255, 255);")
        progressWrapperLayout = QVBoxLayout(self.progressWrapper)

        label1 = QLabel("CPU")
        label1.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        label1.setStyleSheet("background-color: rgba(0, 0, 0);border-radius: 4px;color:white")
        label1.setFont(self.font)
        label2 = QLabel("Mem")
        label2.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        label2.setStyleSheet("background-color: rgba(0, 0, 0);border-radius: 4px;color:white")
        label2.setFont(self.font)
        label3 = QLabel("Disk")
        label3.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        label3.setStyleSheet("background-color: rgba(0, 0, 0);border-radius: 4px;color:white")
        label3.setFont(self.font)

        self.progressBar1 = QProgressBar(self)
        self.progressBar1.setFixedWidth(150)
        self.progressBar1.setFont(self.font)
        self.progressBar1.setObjectName("progressBar1")
        self.progressBar2 = QProgressBar(self)
        self.progressBar2.setFixedWidth(150)
        self.progressBar2.setFont(self.font)
        self.progressBar2.setObjectName("progressBar2")
        self.progressBar3 = QProgressBar(self)
        self.progressBar3.setFont(self.font)
        self.progressBar3.setObjectName("progressBar3")
        self.progressBar3.setFixedWidth(150)

        progressBarLayout1 = QHBoxLayout()
        progressBarLayout1.addWidget(label1)
        progressBarLayout1.addWidget(self.progressBar1)

        progressBarLayout2 = QHBoxLayout()
        progressBarLayout2.addWidget(label2)
        progressBarLayout2.addWidget(self.progressBar2)

        progressBarLayout3 = QHBoxLayout()
        progressBarLayout3.addWidget(label3)
        progressBarLayout3.addWidget(self.progressBar3)

        progressWrapperLayout.addLayout(progressBarLayout1)
        progressWrapperLayout.addLayout(progressBarLayout2)
        progressWrapperLayout.addLayout(progressBarLayout3)
        progressWrapperLayout.setAlignment(Qt.AlignRight)

        space = QLabel("      ")
        diad_label = QLabel("DIAD")
        diad_label.setStyleSheet("font-size: 30px;color: gray;")
        diad_label.setFont(self.font)
        # example=QLabel("knife")
        # example.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        # example.setStyleSheet("background-color: rgba(252, 60, 39);border-radius: 4px;color:white;font-size: 20px")
        # example.setFont(self.font)

        rightLayout = QVBoxLayout(self.rightFrame)
        rightLayout.addWidget(self.progressWrapper)
        rightLayout.addWidget(space)

        self.detected_objects_layout = QVBoxLayout()
        rightLayout.addLayout(self.detected_objects_layout)

        # self.detected_objects_layout.addWidget(example)
        # rightLayout.removeWidget(example)

        self.monitor()

        rightLayout.addStretch()
        rightLayout.addWidget(diad_label, alignment=Qt.AlignBottom | Qt.AlignRight)

        topLayout.addWidget(self.screenshot_label)
        topLayout.addWidget(self.rightFrame)

        self.button = QPushButton("Start!", self)
        self.button.setFixedSize(140, 40)
        self.button.setFont(self.font)
        self.add_shadow2(self.button)
        bottomLayout.addWidget(self.button, alignment=Qt.AlignCenter)

        self.startStyle = """
            QPushButton {
                background-color: rgba(34, 221, 122);
                border-radius: 20px;
                font-size: 20px;
                font-weight: bold;
                color:black
            }
            QPushButton:hover {
                background-color: rgba(0, 128, 0);
                box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.5);
            }
        """

        self.stopStyle = """
            QPushButton {
                background-color: rgba(252, 60, 39);
                border-radius: 20px;
                font-size: 20px;
                font-weight: bold;
                color:black
            }
            QPushButton:hover {
                background-color: rgba(128, 0, 0);
                box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.5);
            }
        """

        self.button.setStyleSheet(self.startStyle)

        self.button.clicked.connect(self.toggle_timer)

        self.timer = QTimer(self)
        self.timer.timeout.connect(lambda: self.screendetect(self.region))

        mainLayout.addLayout(topLayout)
        mainLayout.addLayout(bottomLayout)

        # half_width = screen_width / 2
        # self.setGeometry(0, 35, half_width, 600)
        # self.setWindowTitle("DIAD")
        #
        # self.setFixedSize(self.size())

    def add_shadow(self, label):
        # 添加阴影
        self.effect_shadow = QGraphicsDropShadowEffect(self)
        self.effect_shadow.setOffset(0, 0)  # 偏移
        self.effect_shadow.setBlurRadius(30)  # 阴影半径
        self.effect_shadow.setColor(Qt.black)  # 阴影颜色
        label.setGraphicsEffect(self.effect_shadow)  # 将设置套用到label窗口中

    def add_shadow2(self, label):
        # 添加阴影
        self.effect_shadow = QGraphicsDropShadowEffect(self)
        self.effect_shadow.setOffset(0, 3)  # 偏移
        self.effect_shadow.setBlurRadius(30)  # 阴影半径
        self.effect_shadow.setColor(QColor(30, 30, 30))  # 阴影颜色
        label.setGraphicsEffect(self.effect_shadow)  # 将设置套用到label窗口中

    def toggle_timer(self):
        if self.timer.isActive():
            self.timer.stop()
            self.button.setText("Start!")
            self.button.setStyleSheet(self.startStyle)
        else:
            self.timer.start(100)
            self.button.setText("Stop!")
            self.button.setStyleSheet(self.stopStyle)

    def monitor(self):
        self.mtimer = QTimer(timeout=self.update_ui)
        self.mtimer.start(1000)
        self.show()

    def updateProgressBar(self, pb, value):
        pb.setValue(int(value))
        stylesheet = f"""
            QProgressBar {{
                border: 2px solid grey;
                border-radius: 5px;
                text-align: center;
                background-color: 
            }}
            QProgressBar::chunk {{
                background-color: {self.getColor(value)};
                width: 20px;
                text-align: none;
            }}
        """
        pb.setStyleSheet(stylesheet)

    def getColor(self, value):
        if value > 90:
            return 'red'
        elif value > 50:
            return 'orange'
        else:
            return 'green'

    def update_ui(self):
        cpu_percent = psutil.cpu_percent()
        memory_percent = psutil.virtual_memory().percent
        disk_percent = psutil.disk_usage('/').percent

        self.updateProgressBar(self.progressBar1, cpu_percent)
        self.updateProgressBar(self.progressBar2, memory_percent)
        self.updateProgressBar(self.progressBar3, disk_percent)

    # 初始截图展示
    # def screenshot(self, region):
    #
    #     x, y, width, height = region
    #     with mss.mss() as sct:
    #         monitor = {"top": y, "left": x, "width": width, "height": height}
    #         mss_image = sct.grab(monitor)
    #     time.sleep(1)
    #     qim = QImage(mss_image.rgb, mss_image.width, mss_image.height, QImage.Format_RGB888)
    #     pixmap = QPixmap.fromImage(qim)
    #     self.screenshot_label.setFixedSize(self.screenshot_label.width(), self.screenshot_label.height())
    #     scale_mode = Qt.KeepAspectRatio
    #     self.screenshot_label.setPixmap(pixmap.scaled(self.screenshot_label.size(),
    #                                                   scale_mode,
    #                                                   Qt.SmoothTransformation))

    # def screendetect(self, region):
    #
    #     x, y, width, height = region
    #     with mss.mss() as sct:
    #         monitor = {"top": y, "left": x, "width": width, "height": height}
    #         mss_image = sct.grab(monitor)
    #     Model = load_model()
    #     detected_image = predict(Model, mss_image)
    #     self.display_result(detected_image)
    def screendetect(self, region):
        x, y, width, height = region
        with mss.mss() as sct:
            monitor = {"top": y, "left": x, "width": width, "height": height}
            mss_image = sct.grab(monitor)
        Model = load_model()
        detected_image, detected_objects = predict(Model, mss_image)
        self.display_result(detected_image)

        # Update detected objects labels
        self.update_detected_objects_labels(detected_objects)

    def display_result(self, cv2_image):
        height, width, channels = cv2_image.shape
        bytes_per_line = channels * width
        qimage = QImage(cv2_image.data, width, height, bytes_per_line, QImage.Format_RGB888).rgbSwapped()
        pixmap = QPixmap.fromImage(qimage)
        scale_mode = Qt.KeepAspectRatio
        self.screenshot_label.setPixmap(pixmap.scaled(self.screenshot_label.size(),
                                                      scale_mode,

                                                      Qt.SmoothTransformation))

    def start_detection(self):
        self.image_detection_thread.start()

    def handle_detection_result(self, detected_image):
        self.display_result(detected_image)

    def update_detected_objects_labels(self, detected_objects):
        # Delete old labels
        for i in reversed(range(self.detected_objects_layout.count())):
            self.detected_objects_layout.itemAt(i).widget().setParent(None)

        # Create new labels for detected objects
        for obj in detected_objects:
            label = QLabel(obj)
            label.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            label.setStyleSheet("background-color: rgba(252, 60, 39);border-radius: 4px;color:white;font-size: 20px")
            label.setFont(self.font)
            self.detected_objects_layout.addWidget(label)


if __name__ == '__main__':
    app = QApplication([])
    x1, y1, x2, y2 = 900, 20, 1800, 820  # Define your region here
    window = StartDetect(x1, y1, x2, y2)
    window.show()
    app.exec_()
