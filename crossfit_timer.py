from engine import db
from models.Category import Category
from models.Athlete import Athlete
from models.Competence import Competence
from models.CompetenceAthlete import CompetenceAthlete
from models.Group import Group
from PyQt5 import QtWidgets
from qt.MainWindow import Ui_MainWindow
import sys


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, *args, **kwargs):
        QtWidgets.QMainWindow.__init__(self, *args, **kwargs)
        self.setupUi(self)


if __name__ == '__main__':
    # Initialize database
    db.Base.metadata.create_all(db.engine)

    app = QtWidgets.QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())