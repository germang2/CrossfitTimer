import sys
from engine import db
from PyQt5 import QtWidgets
from app import MainWindow
from controllers.MainController import MainController


if __name__ == '__main__':
    # Initialize database
    db.Base.metadata.create_all(db.engine)
    app = QtWidgets.QApplication(sys.argv)
    main_window = MainWindow()
    main_controller = MainController(main_window)
    main_window.show()
    sys.exit(app.exec_())
