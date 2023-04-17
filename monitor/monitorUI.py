import psutil
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import *


class SystemMonitor(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        # 设置窗口大小、标题
        self.setGeometry(200, 200, 450, 200)
        self.setWindowTitle('System Monitor')

        # 创建三个 label 用于显示 CPU、内存、硬盘使用率
        self.cpu_label = QLabel('CPU Usage:', self)
        self.cpu_label.move(40, 40)
        self.memory_label = QLabel('Memory Usage:', self)
        self.memory_label.move(40, 80)
        self.disk_label = QLabel('Disk Usage:', self)
        self.disk_label.move(40, 120)

        # 创建三个 progress bar 用于显示 CPU、内存、硬盘使用率
        self.cpu_pb = QProgressBar(self)
        self.cpu_pb.setGeometry(200, 36, 200, 20)
        self.memory_pb = QProgressBar(self)
        self.memory_pb.setGeometry(200, 76, 200, 20)
        self.disk_pb = QProgressBar(self)
        self.disk_pb.setGeometry(200, 116, 200, 20)

        # 添加一个定时器，每秒钟更新一次三个 progress bar 的值
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_ui)
        self.timer.start(1000)

        # 显示窗口
        self.show()

    def update_ui(self):
        # 读取系统 CPU、内存、硬盘使用情况
        cpu_percent = int(psutil.cpu_percent())
        memory_percent = int(psutil.virtual_memory().percent)
        disk_percent = int(psutil.disk_usage('/').percent)

        # 默认stylesheet
        pb_stylesheet = """
            QProgressBar {
                border: 2px solid grey;
                border-radius: 5px;
                text-align: center;
                background-color: #FFFFFF;
            }

            QProgressBar::chunk {
                background-color: green;
                width: 20px;
                text-align: none;
            }
        """

        # 更新三个 progress bar 的值
        cpu_pb_stylesheet = pb_stylesheet
        if cpu_percent > 90:
            cpu_pb_stylesheet = pb_stylesheet.replace('green', 'red')
        elif cpu_percent > 50:
            cpu_pb_stylesheet = pb_stylesheet.replace('green', 'orange')
        self.cpu_pb.setStyleSheet(cpu_pb_stylesheet)
        self.cpu_pb.setValue(cpu_percent)
        mem_pb_stylesheet = pb_stylesheet
        if memory_percent > 90:
            mem_pb_stylesheet = pb_stylesheet.replace('green', 'red')
        elif memory_percent > 50:
            mem_pb_stylesheet = pb_stylesheet.replace('green', 'orange')
        self.memory_pb.setStyleSheet(mem_pb_stylesheet)
        self.memory_pb.setValue(memory_percent)
        disk_pb_stylesheet = pb_stylesheet
        if disk_percent > 90:
            disk_pb_stylesheet = pb_stylesheet.replace('green', 'red')
        elif disk_percent > 50:
            disk_pb_stylesheet = pb_stylesheet.replace('green', 'orange')
        self.disk_pb.setStyleSheet(disk_pb_stylesheet)
        self.disk_pb.setValue(disk_percent)


# 主函数
if __name__ == '__main__':
    app = QApplication([])
    monitor = SystemMonitor()
    app.exec_()
