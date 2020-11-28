from qt.MainWindow import Ui_MainWindow
from qt.CategoriesView import Ui_CategoriesView
from qt.AthletesView import Ui_AthletesView
from qt.CompetenciasView import Ui_CompetencesView
from PyQt5 import QtWidgets


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, *args, **kwargs):
        QtWidgets.QMainWindow.__init__(self, *args, **kwargs)
        self.setupUi(self)


class CategoriesWindow(QtWidgets.QMainWindow, Ui_CategoriesView):
    def __init__(self, *args, **kwargs):
        QtWidgets.QMainWindow.__init__(self, *args, **kwargs)
        self.setupUi(self)


class AthletesWindow(QtWidgets.QMainWindow, Ui_AthletesView):
    def __init__(self, *args, **kwargs):
        QtWidgets.QMainWindow.__init__(self, *args, **kwargs)
        self.setupUi(self)


class CompetencesWindow(QtWidgets.QMainWindow, Ui_CompetencesView):
    def __init__(self, *args, **kwargs):
        QtWidgets.QMainWindow.__init__(self, *args, **kwargs)
        self.setupUi(self)