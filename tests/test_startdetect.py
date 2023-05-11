from PyQt5.QtWidgets import QApplication

import GUIPage


def test():
    app = QApplication([])
    x1, y1, x2, y2 = 900, 20, 1800, 820  # Define your region here
    window = GUIPage.StartDetect(x1, y1, x2, y2)
    assert window.windowTitle().title() == 'DIAD'
    window.show()
    app.exec_()
