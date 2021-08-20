from models.Athlete import Athlete

from app import CategoriesWindow

from engine import db

from PyQt5 import QtWidgets

from models.Category import Category

from utils.style_sheet import ButtonStyleSheet


class CategoryController:
    def __init__(self, main_window: CategoriesWindow, *args, **kwargs):
        self.window = main_window
        self.window.categories_table.setFixedWidth(720)
        self.window.categories_table.setColumnWidth(0, 380)
        self.window.categories_table.setColumnWidth(1, 150)
        self.window.categories_table.setColumnWidth(2, 150)
        self.window.btn_create_category.clicked.connect(self.create_category)
        self.window.btn_get_all_categories.clicked.connect(self.get_all_categories)
        self.clear_table()
        self.set_style_sheet()

    def create_category(self):
        text = self.window.ed_category.text()
        if text:
            category = Category(name=text)
            db.session.add(category)
            db.session.commit()
            self.window.ed_category.setText('')
            self.get_all_categories()

    def get_all_categories(self):
        self.window.lb_error_delete.setText('')
        self.clear_table()
        categories = db.session.query(Category).order_by('name').all()
        if categories:
            for i, category in enumerate(categories):
                self.window.categories_table.insertRow(i)
                name = QtWidgets.QTableWidgetItem(category.name)
                self.window.categories_table.setItem(i, 0, name)
                modify = QtWidgets.QPushButton()
                modify.setText('Modificar')
                modify.setProperty('id', category.id)
                modify.setProperty('operation', 'modify')
                modify.clicked.connect(self.handle_categories_table)
                modify.setStyleSheet(ButtonStyleSheet.BUTTON_SUCCESS)
                self.window.categories_table.setCellWidget(i, 1, modify)
                delete = QtWidgets.QPushButton()
                delete.setText('Eliminar')
                delete.setProperty('id', category.id)
                delete.setProperty('operation', 'delete')
                delete.clicked.connect(self.handle_categories_table)
                delete.setStyleSheet(ButtonStyleSheet.BUTTON_ERROR)
                self.window.categories_table.setCellWidget(i, 2, delete)
            while True:
                row_count = self.window.categories_table.rowCount()
                if row_count <= len(categories):
                    break
                else:
                    self.window.categories_table.removeRow(row_count - 1)

    def handle_categories_table(self):
        index_row = self.window.categories_table.currentRow()
        index_column = self.window.categories_table.currentColumn()
        if index_row >= 0 and index_column >= 0:
            operation = self.window.categories_table.cellWidget(index_row, index_column).property('operation')
            if operation == 'modify':
                try:
                    category_id = int(self.window.categories_table.cellWidget(index_row, index_column).property('id'))
                    category = db.session.query(Category).filter_by(id=category_id).first()
                    new_name = self.window.categories_table.item(index_row, 0).text()
                    category.name = new_name
                    db.session.add(category)
                    db.session.commit()

                    self.get_all_categories()

                except Exception as e:
                    print(e)
            elif operation == 'delete':
                try:
                    category_id = int(self.window.categories_table.cellWidget(index_row, index_column).property('id'))
                    category = db.session.query(Category).filter_by(id=category_id).first()
                    # checks if the category is assigned to at least on athlete
                    athlete = db.session.query(Athlete).filter_by(category_id=category_id).first()
                    if athlete:
                        self.window.lb_error_delete.setText(
                            f'No se puede borrar {category.name}, hay atletas que la tienen asignada')
                    else:
                        db.session.delete(category)
                        db.session.commit()
                        self.get_all_categories()
                except Exception as e:
                    print(e)

    def clear_table(self):
        for i in range(self.window.categories_table.rowCount()):
            self.window.categories_table.removeRow(i)

    def set_style_sheet(self):
        self.window.setFixedWidth(self.window.geometry().width())
        self.window.lb_title.setStyleSheet(ButtonStyleSheet.BUTTON_SUCCESS)
        self.window.btn_get_all_categories.setStyleSheet(ButtonStyleSheet.BUTTON_SUCCESS)
        self.window.btn_create_category.setStyleSheet(ButtonStyleSheet.BUTTON_SUCCESS)
