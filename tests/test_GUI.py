import GUIPage


def test_GUIPage_UI():
    start_window = GUIPage.test()
    assert start_window.font == 'Microsoft YaHei'
    assert start_window.windowTitle() == 'Start Window'
    assert start_window.label.text() == 'Dangerous Item Auto Detection'
    assert start_window.Startbutton.text() == 'Select Detection Area'
