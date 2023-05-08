from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QImage, QFont
from PyQt5.QtWidgets import QApplication, QWidget, QHBoxLayout, QVBoxLayout, QFrame, QLabel, QProgressBar, QPushButton, \
    QDesktopWidget
import psutil
from PyQt5.QtCore import QTimer
import mss
from deploy import load_model, predict, plot_result
from PyQt5.QtCore import QThread, pyqtSignal

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


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        desktop = QDesktopWidget()
        screen_width = desktop.screenGeometry().width()
        screen_height= desktop.screenGeometry().height()

        rightFrame = QFrame(self)

        
        mainLayout = QVBoxLayout(self)
        topLayout = QHBoxLayout()
        bottomLayout = QHBoxLayout()

        
        rightFrame.setFixedWidth(250)

        
        self.screenshot_label = QLabel(self)
        self.screenshot_label.setMinimumSize(screen_width/2-250, screen_height-500)
        self.screenshot_label.setAlignment(Qt.AlignCenter)
        self.region=(900,20,900,800)

        self.screenshot(self.region)
        
        self.screenshot_label.setStyleSheet("border: 2px solid black;")


        leftLayout = QVBoxLayout(self.screenshot_label)
        leftLayout.addWidget(self.screenshot_label)

        self.image_detection_thread = ImageDetectionThread(self.region)
        self.image_detection_thread.result_ready.connect(self.handle_detection_result)

        progressWrapper = QWidget(self)
        progressWrapperLayout = QVBoxLayout(progressWrapper)

        label1 = QLabel("CPU")
        label1.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        label2 = QLabel("Memory")
        label2.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        label3 = QLabel("Disk")
        label3.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

        self.progressBar1 = QProgressBar(self)
        self.progressBar1.setFixedWidth(150)
        self.progressBar1.setObjectName("progressBar1")
        self.progressBar2 = QProgressBar(self)
        self.progressBar2.setFixedWidth(150)
        self.progressBar2.setObjectName("progressBar2")
        self.progressBar3 = QProgressBar(self)
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

        
        rightLayout = QVBoxLayout(rightFrame)
        rightLayout.addWidget(progressWrapper)

        self.monitor()

        rightLayout.addStretch()

        
        topLayout.addWidget(self.screenshot_label)
        topLayout.addWidget(rightFrame)

        
        self.button = QPushButton("开始检测", self)
        self.button.setFixedSize(100, 50)
        bottomLayout.addWidget(self.button, alignment=Qt.AlignCenter)
        
        
        self.button.clicked.connect(self.toggle_timer)

        
        self.timer = QTimer(self)
        # self.timer.timeout.connect(lambda: self.screendetect(self.region))
        self.timer.timeout.connect(self.start_detection)

        mainLayout.addLayout(topLayout)
        mainLayout.addLayout(bottomLayout)

        
        half_width = screen_width / 2
        self.setGeometry(0, 35, half_width, 600)
        self.setWindowTitle("DIAD")
        
        self.setFixedSize(self.size())


    def toggle_timer(self):
        if self.timer.isActive():
            self.timer.stop()
            self.button.setText("开始检测")
        else:
            self.timer.start(100)
            self.button.setText("停止检测")

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

    
    def screenshot(self, region):
        
        x, y, width, height = region
        with mss.mss() as sct:
            monitor = {"top": y, "left": x, "width": width, "height": height}
            mss_image = sct.grab(monitor)
        qim = QImage(mss_image.rgb, mss_image.width, mss_image.height, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(qim)
        self.screenshot_label.setFixedSize(self.screenshot_label.width(), self.screenshot_label.height())
        scale_mode = Qt.KeepAspectRatio
        self.screenshot_label.setPixmap(pixmap.scaled(self.screenshot_label.size(),
                                                      scale_mode,
                                                      Qt.SmoothTransformation))

    def start_detection(self):
        self.image_detection_thread.start()


    def handle_detection_result(self, detected_image):
        self.display_result(detected_image)


    def display_result(self, cv2_image):
        height, width, channels = cv2_image.shape
        bytes_per_line = channels * width
        qimage = QImage(cv2_image.data, width, height, bytes_per_line, QImage.Format_RGB888).rgbSwapped()
        pixmap = QPixmap.fromImage(qimage)
        scale_mode = Qt.KeepAspectRatio
        self.screenshot_label.setPixmap(pixmap.scaled(self.screenshot_label.size(),
                                                      scale_mode,
                                                      Qt.SmoothTransformation))


if __name__ == '__main__':
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()
