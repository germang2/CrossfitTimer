import sys
from engine import db
from models.Category import Category
from PyQt5 import QtWidgets
from qt.MainWindow import Ui_MainWindow
from PyQt5.QtWidgets import QTableWidgetItem
from controllers.Categories import CategoryController

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, *args, **kwargs):
        QtWidgets.QMainWindow.__init__(self, *args, **kwargs)
        self.setupUi(self)
        self.btn_create_category.clicked.connect(self.create_category)
        self.btn_get_all_categories.clicked.connect(self.get_all_categories)

    def create_category(self):
        text = self.ed_category.text()
        if text:
            category = Category(name=text)
            db.session.add(category)
            db.session.commit()
            self.ed_category.setText('')

    def get_all_categories(self):
        categories = db.session.query(Category).all()
        if categories:
            self.categories_table.clearContents()
            for i in range(self.categories_table.rowCount()):
                self.categories_table.removeRow(i)
            for i, category in enumerate(categories):
                self.categories_table.insertRow(i)
                name = QTableWidgetItem(category.name)
                self.categories_table.setItem(i, 0, name)
                modify = QTableWidgetItem('Modificar')
                self.categories_table.setItem(i, 1, modify)
                delete = QTableWidgetItem('Eliminar')
                self.categories_table.setItem(i, 2, delete)


if __name__ == '__main__':
    # Initialize database
    db.Base.metadata.create_all(db.engine)

    app = QtWidgets.QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())