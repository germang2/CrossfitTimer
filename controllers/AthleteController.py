from app import AthletesWindow
from engine import db
from models.Athlete import Athlete
from models.Category import Category
from utils.Validations import *
from PyQt5 import QtWidgets
from sqlalchemy import or_
import traceback


class AthletesController:
    def __init__(self, window: AthletesWindow, *args, **kwargs):
        self.window = window
        self.window.btn_add_atlete.clicked.connect(self.create_athlete)
        self.window.btn_get_all_athletes.clicked.connect(self.get_all_athletes)
        self.window.ed_filter.textChanged.connect(self.filter_athletes)
        self.category_id_create = {}
        self.category_id_modify = {}
        self.load_categories()

    def create_athlete(self):
        """ Creates a new athlete with all fields """
        try:
            name = self.window.ed_name.text()
            last_name = self.window.ed_lastname.text()
            age = self.window.ed_age.text()
            club = self.window.ed_club.text()
            nit = self.window.ed_nit.text()
            errors = validate_data(name=name, last_name=last_name, age=age, club=club, nit=nit)
            if errors:
                self.show_errors(errors)
            else:
                # if there are not error, the athlete is create
                index_category = self.window.cb_categories.currentIndex()
                category_id = self.category_id_create[index_category]
                athlete = Athlete(name=name, last_name=last_name, age=int(age), club=club, category_id=category_id,
                                  nit=nit)
                db.session.add(athlete)
                db.session.commit()
                self.clear_fields()
                self.clear_fields_errors()
        except Exception as e:
            print(e)

    def filter_athletes(self):
        text = self.window.ed_filter.text()
        if text and len(text) >= 3:
            self.get_all_athletes(filter_text=text)

    def get_all_athletes(self, filter_text=None):
        """ loads in a table all the existing athletes """
        try:
            if filter_text:
                filter_text.strip()
                athletes = db.session.query(Athlete).filter(
                    or_(Athlete.name.ilike(f'%{filter_text}%'), Athlete.last_name.ilike(f'%{filter_text}%')))\
                    .order_by('name').all()
            else:
                athletes = db.session.query(Athlete).order_by('name').all()
            categories = db.session.query(Category).order_by('name').all()
            if athletes:
                self.window.athletes_table.clearContents()
                for i in range(self.window.athletes_table.rowCount()):
                    self.window.athletes_table.removeRow(i)
                for i, athlete in enumerate(athletes):
                    self.window.athletes_table.insertRow(i)
                    name = QtWidgets.QTableWidgetItem(athlete.name)
                    self.window.athletes_table.setItem(i, 0, name)
                    lastname = QtWidgets.QTableWidgetItem(athlete.last_name)
                    self.window.athletes_table.setItem(i, 1, lastname)
                    nit = QtWidgets.QTableWidgetItem(athlete.nit)
                    self.window.athletes_table.setItem(i, 2, nit)
                    age = QtWidgets.QTableWidgetItem(str(athlete.age))
                    self.window.athletes_table.setItem(i, 3, age)
                    club = QtWidgets.QTableWidgetItem(athlete.club)
                    self.window.athletes_table.setItem(i, 4, club)
                    """ creates a comboBox for categories, set as default the current one of the athlete """
                    cb_categories = QtWidgets.QComboBox()
                    for j, category in enumerate(categories):
                        cb_categories.addItem(category.name)
                        self.category_id_modify[j] = category.id
                        if category.id == athlete.category_id:
                            cb_categories.setCurrentIndex(j)
                    self.window.athletes_table.setCellWidget(i, 5, cb_categories)
                    modify = QtWidgets.QPushButton()
                    modify.setText('Modificar')
                    modify.setProperty('id', athlete.id)
                    modify.setProperty('operation', 'modify')
                    modify.clicked.connect(self.handle_athletes_table)
                    self.window.athletes_table.setCellWidget(i, 6, modify)
                    delete = QtWidgets.QPushButton()
                    delete.setText('Eliminar')
                    delete.setProperty('id', athlete.id)
                    delete.setProperty('operation', 'delete')
                    delete.clicked.connect(self.handle_athletes_table)
                    self.window.athletes_table.setCellWidget(i, 7, delete)

            while True:
                row_count = self.window.athletes_table.rowCount()
                if row_count <= len(athletes):
                    break
                else:
                    self.window.athletes_table.removeRow(row_count - 1)

        except Exception as e:
            print(e)
            print('Could not load all the athletes')

    def handle_athletes_table(self):
        """ handles the clicks over the buttons modify and delete on the table for athletes """
        index_row = self.window.athletes_table.currentRow()
        index_column = self.window.athletes_table.currentColumn()
        if index_row >= 0 and index_column >= 0:
            athlete_id = int(self.window.athletes_table.cellWidget(index_row, index_column).property('id'))
            athlete = db.session.query(Athlete).filter_by(id=athlete_id).first()
            operation = self.window.athletes_table.cellWidget(index_row, index_column).property('operation')
            try:
                if operation == 'modify' and athlete:
                    name = self.window.athletes_table.item(index_row, 0).text()
                    lastname = self.window.athletes_table.item(index_row, 1).text()
                    nit = self.window.athletes_table.item(index_row, 2).text()
                    age = self.window.athletes_table.item(index_row, 3).text()
                    club = self.window.athletes_table.item(index_row, 4).text()
                    index_category = self.window.athletes_table.cellWidget(index_row, 5).currentIndex()
                    category_id = self.category_id_create[index_category]
                    athlete.name = name
                    athlete.last_name = lastname
                    athlete.age = int(age)
                    athlete.club = club
                    athlete.category_id = int(category_id)
                    db.session.add(athlete)
                    db.session.commit()

                elif operation == 'delete' and athlete:
                    db.session.delete(athlete)
                    db.session.commit()
                self.get_all_athletes()

            except Exception as e:
                print(e)

    def load_categories(self):
        """ loads in a comboBox all the existing categories """
        try:
            self.window.cb_categories.clear()
            categories = db.session.query(Category).order_by('name').all()
            if categories:
                self.category_id_create.clear()
                for i, category in enumerate(categories):
                    self.window.cb_categories.addItem(category.name, userData=category.id)
                    # it adds a relation between the index of the comboBox and the category.id
                    self.category_id_create[i] = category.id
        except Exception as e:
            traceback.print_exc()

    def show_errors(self, errors):
        """ shows the errors gotten from the validations """
        if 'name' in errors:
            self.window.lb_name_error.setText(errors['name'])
        else:
            self.window.lb_name_error.setText('')
        if 'last_name' in errors:
            self.window.lb_lastname_error.setText(errors['last_name'])
        else:
            self.window.lb_lastname_error.setText('')
        if 'age' in errors:
            self.window.lb_age_error.setText(errors['age'])
        else:
            self.window.lb_age_error.setText('')
        if 'club' in errors:
            self.window.lb_club_error.setText(errors['club'])
        else:
            self.window.lb_club_error.setText('')
        if 'nit' in errors:
            self.window.lb_nit_error.setText(errors['nit'])
        else:
            self.window.lb_nit_error.setText('')

    def clear_fields(self):
        """ clear all editText fields for the user """
        self.window.ed_name.setText('')
        self.window.ed_lastname.setText('')
        self.window.ed_age.setText('')
        self.window.ed_club.setText('')
        self.window.ed_nit.setText('')

    def clear_fields_errors(self):
        """ clear all the label fields where errors are show """
        self.window.lb_name_error.setText('')
        self.window.lb_lastname_error.setText('')
        self.window.lb_age_error.setText('')
        self.window.lb_club_error.setText('')
        self.window.lb_nit_error.setText('')


def validate_data(name, last_name, age, club, nit):
    """ validate each field for an athlete """
    errors = {}
    # validations for field 'name'
    field = 'name'
    validate_min(field, name, 3, errors)
    validate_max(field, name, 40, errors)

    # validations for field 'last_name'
    field = 'last_name'
    validate_min(field, last_name, 3, errors)
    validate_max(field, last_name, 40, errors)

    # validations for field 'club'
    field = 'club'
    validate_min(field, club, 2, errors)
    validate_max(field, club, 20, errors)

    # validations for field 'age'
    field = 'age'
    validate_exists(field, age, errors)
    validate_int(field, age, errors)

    # validations for field 'nit'
    field = 'nit'
    validate_min(field, nit, 5, errors)
    validate_max(field, nit, 20, errors)
    validate_int(field, nit, errors)
    try:
        athlete = db.session.query(Athlete).filter_by(nit=nit).first()
        if athlete:
            errors['nit'] = 'Ya existe esta cedula'
    except Exception as e:
        print('Error validando cedula')
        print(e)

    return errors
