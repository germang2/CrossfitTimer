from qt.MainWindow import Ui_MainWindow
from qt.CategoriesView import Ui_CategoriesView
from PyQt5 import QtWidgets


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, *args, **kwargs):
        QtWidgets.QMainWindow.__init__(self, *args, **kwargs)
        self.setupUi(self)


class CategoriesWindow(QtWidgets.QMainWindow, Ui_CategoriesView):
    def __init__(self, *args, **kwargs):
        QtWidgets.QMainWindow.__init__(self, *args, **kwargs)
        self.setupUi(self)

