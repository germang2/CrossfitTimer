from PyQt5 import QtGui


class ButtonStyleSheet(object):
    """
    Contains methods and variables related to set style sheet fot buttons
    """

    BUTTON_SUCCESS = """
        background-color: rgba(0,23,39,240);
        color: #f7f7f7;
    """

    BUTTON_ERROR = """
        background-color: rgba(64,107,3,255);
        color: #f7f7f7;
    """

    WINDOW_ICON_PATH = 'resources/img/belicos-icon.ico'

    @staticmethod
    def set_window_icon(window):
        window.setWindowIcon(QtGui.QIcon(ButtonStyleSheet.WINDOW_ICON_PATH))