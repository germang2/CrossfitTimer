import sys
from engine import db
from models.Category import Category
from PyQt5 import QtWidgets
from qt.MainWindow import Ui_MainWindow
from PyQt5.QtWidgets import QTableWidgetItem, QPushButton
from controllers.Categories import CategoryController


class CustomQTableWidgetItem(QTableWidgetItem):
    def __init__(self, *args, **kwargs):
        QTableWidgetItem.__init__(self, *args, **kwargs)
        self.custom_params = {}
        for k,v in kwargs.items():
            self.custom_params[k] = v


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, *args, **kwargs):
        QtWidgets.QMainWindow.__init__(self, *args, **kwargs)
        self.setupUi(self)
        self.categories_table.setFixedWidth(600)
        self.categories_table.setColumnWidth(0, 300)
        self.categories_table.setColumnWidth(1, 150)
        self.categories_table.setColumnWidth(2, 150)
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
        categories = db.session.query(Category).order_by('name').all()
        if categories:
            self.categories_table.clearContents()
            for i in range(self.categories_table.rowCount()):
                self.categories_table.removeRow(i)
            for i, category in enumerate(categories):
                self.categories_table.insertRow(i)
                name = QTableWidgetItem(category.name)
                self.categories_table.setItem(i, 0, name)
                modify = QtWidgets.QPushButton()
                modify.setText('Modificar')
                modify.setProperty('id', category.id)
                modify.setProperty('operation', 'modify')
                modify.clicked.connect(self.handle_categories_table)
                self.categories_table.setCellWidget(i, 1, modify)
                delete = QtWidgets.QPushButton()
                delete.setText('Eliminar')
                delete.setProperty('id', category.id)
                delete.setProperty('operation', 'delete')
                delete.clicked.connect(self.handle_categories_table)
                self.categories_table.setCellWidget(i, 2, delete)


    def handle_categories_table(self):
        index_row = self.categories_table.currentRow()
        index_column = self.categories_table.currentColumn()
        if index_row >= 0 and index_column >= 0:
            operation = self.categories_table.cellWidget(index_row, index_column).property('operation')
            if operation == 'modify':
                try:
                    category_id = int(self.categories_table.cellWidget(index_row, index_column).property('id'))
                    new_name = self.categories_table.item(index_row, 0).text()
                    category = db.session.query(Category).filter_by(id=category_id).first()
                    category.name = new_name
                    db.session.add(category)
                    db.session.commit()

                    self.get_all_categories()

                except Exception as e:
                    print(e)
            elif operation == 'delete':
                try:
                    category_id = int(self.categories_table.cellWidget(index_row, index_column).property('id'))
                    category = db.session.query(Category).filter_by(id=category_id).first()
                    db.session.delete(category)
                    db.session.commit()

                    self.get_all_categories()
                except Exception as e:
                    print(e)



if __name__ == '__main__':
    # Initialize database
    db.Base.metadata.create_all(db.engine)

    app = QtWidgets.QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())