from PyQt5.QtWidgets import QApplication

import GUIPage
import startdetect


def test():
    app = QApplication([])
    x1, y1, x2, y2 = 900, 20, 1800, 820
    window = GUIPage.StartDetect(x1, y1, x2, y2)
    assert window.windowTitle().title() == 'DIAD'
    assert window.styleSheet().title() == 'Background-Color: Rgba(60, 60, 60)'
    main_window = startdetect.MainWindow(x1, y1, x2, y2)
    height = main_window.rightFrame.height()
    width = main_window.rightFrame.width()
    assert height / width == 0.8
