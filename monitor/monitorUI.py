import psutil
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import *


class SystemMonitor(QWidget):
    def __init__(self):
        super().__init__()
        self.setGeometry(200, 200, 450, 200)
        self.setWindowTitle('System Monitor')

        self.widgets = {}
        self.widgets['CPU'] = self.createProgressBar('CPU Usage:', 40)
        self.widgets['Memory'] = self.createProgressBar('Memory Usage:', 80)
        self.widgets['Disk'] = self.createProgressBar('Disk Usage:', 120)

        self.timer = QTimer(timeout=self.update_ui)
        self.timer.start(1000)

        self.show()

    def createProgressBar(self, label, y):
        pb = QProgressBar(self)
        pb.setGeometry(200, y - 4, 200, 20)
        self.widgets[label] = pb
        QLabel(label, self).move(40, y)
        return pb

    def updateProgressBar(self, pb, value):
        pb.setValue(int(value))
        stylesheet = f"""
            QProgressBar {{
                border: 2px solid grey;
                border-radius: 5px;
                text-align: center;
                background-color: #FFFFFF;
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

        self.updateProgressBar(self.widgets['CPU'], cpu_percent)
        self.updateProgressBar(self.widgets['Memory'], memory_percent)
        self.updateProgressBar(self.widgets['Disk'], disk_percent)


if __name__ == '__main__':
    app = QApplication([])
    monitor = SystemMonitor()
    app.exec_()
