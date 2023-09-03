from sqlalchemy import or_
from PyQt5 import QtWidgets

from app import AthletesWindow

from models.Athlete import Athlete
from models.Category import Category
from models.GroupAthlete import GroupAthlete

from engine import db

from utils.style_sheet import ButtonStyleSheet
from utils.string_helper import get_edit_box_value
from utils.Validations import *


class AthletesController:
    def __init__(self, window: AthletesWindow):
        self.window = window
        self.window.btn_add_atlete.clicked.connect(self.create_athlete)
        self.window.btn_get_all_athletes.clicked.connect(self.get_all_athletes)
        self.window.ed_filter.textChanged.connect(self.filter_athletes)
        self.category_id_create = {}
        self.category_id_modify = {}
        self.load_categories()
        self.clear_table()
        self.window.athletes_table.setColumnWidth(0, 380)
        self.set_style_sheet()

    def create_athlete(self):
        """ Creates a new athlete with all fields """
        try:
            full_name = get_edit_box_value(self.window.ed_name)
            club = get_edit_box_value(self.window.ed_club)
            nit = get_edit_box_value(self.window.ed_nit)
            dorsal = get_edit_box_value(self.window.ed_dorsal)
            errors = validate_data(
                full_name=full_name,
                club=club,
                nit=nit,
                dorsal=dorsal
            )
            if errors:
                self.show_errors(errors)
            else:
                # if there are not error, the athlete is create
                index_category = self.window.cb_categories.currentIndex()
                category_id = self.category_id_create[index_category]
                athlete = Athlete(
                    full_name=full_name,
                    club=club,
                    category_id=category_id,
                    nit=nit,
                    dorsal=dorsal
                )
                db.session.add(athlete)
                db.session.commit()
                self.clear_fields()
                self.clear_fields_errors()
        except Exception as e:
            print(e)

    def filter_athletes(self):
        text = get_edit_box_value(self.window.ed_filter)
        if text and len(text) >= 2:
            self.get_all_athletes(filter_text=text)
            self.clear_fields_errors()

    def get_all_athletes(self, filter_text=None):
        """ loads in a table the existing/filtered athletes """
        try:
            self.clear_table()
            if filter_text:
                athletes = db.session.query(Athlete).join(Category, Category.id == Athlete.category_id).filter(
                    or_(
                        Athlete.full_name.ilike(f'%{filter_text}%'),
                        Athlete.club.ilike(f'%{filter_text}%'),
                        Category.name.ilike(f'%{filter_text}%'),
                        Athlete.dorsal.ilike(f'{filter_text}%'),
                    )
                ).order_by('full_name').all()
            else:
                self.window.ed_filter.setText('')
                athletes = db.session.query(Athlete).order_by('full_name').all()
            categories = db.session.query(Category).order_by('name').all()
            if athletes:
                self.window.lb_error_delete.setText('')
                for i, athlete in enumerate(athletes):
                    self.window.athletes_table.insertRow(i)
                    name = QtWidgets.QTableWidgetItem(athlete.full_name)
                    self.window.athletes_table.setItem(i, 0, name)
                    nit = QtWidgets.QTableWidgetItem(athlete.nit)
                    self.window.athletes_table.setItem(i, 1, nit)
                    club = QtWidgets.QTableWidgetItem(athlete.club)
                    self.window.athletes_table.setItem(i, 2, club)
                    dorsal = QtWidgets.QTableWidgetItem(athlete.dorsal)
                    self.window.athletes_table.setItem(i, 3, dorsal)
                    """ creates a comboBox for categories, set as default the current one of the athlete """
                    cb_categories = QtWidgets.QComboBox()
                    for j, category in enumerate(categories):
                        cb_categories.addItem(category.name)
                        self.category_id_modify[j] = category.id
                        if category.id == athlete.category_id:
                            cb_categories.setCurrentIndex(j)
                    cb_categories.setStyleSheet(ButtonStyleSheet.BUTTON_SUCCESS)
                    self.window.athletes_table.setCellWidget(i, 4, cb_categories)
                    modify = QtWidgets.QPushButton()
                    modify.setText('Modificar')
                    modify.setProperty('id', athlete.id)
                    modify.setProperty('operation', 'modify')
                    modify.clicked.connect(self.handle_athletes_table)
                    modify.setStyleSheet(ButtonStyleSheet.BUTTON_SUCCESS)
                    self.window.athletes_table.setCellWidget(i, 5, modify)
                    delete = QtWidgets.QPushButton()

                    delete.setText('Eliminar')
                    delete.setProperty('id', athlete.id)
                    delete.setProperty('operation', 'delete')
                    delete.clicked.connect(self.handle_athletes_table)
                    delete.setStyleSheet(ButtonStyleSheet.BUTTON_ERROR)
                    self.window.athletes_table.setCellWidget(i, 6, delete)

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
                    full_name = get_edit_box_value(self.window.athletes_table.item(index_row, 0))
                    nit = get_edit_box_value(self.window.athletes_table.item(index_row, 1))
                    club = get_edit_box_value(self.window.athletes_table.item(index_row, 2))
                    dorsal = get_edit_box_value(self.window.athletes_table.item(index_row, 3))
                    index_category = self.window.athletes_table.cellWidget(index_row, 4).currentIndex()
                    category_id = self.category_id_create[index_category]
                    errors = validate_data(
                        full_name=full_name,
                        club=club,
                        nit=nit,
                        dorsal=dorsal,
                        athlete_id=athlete_id,
                    )
                    if errors:
                        self.show_errors(errors)
                        return

                    athlete.full_name = full_name
                    athlete.club = club
                    athlete.category_id = int(category_id)
                    athlete.nit = nit
                    athlete.dorsal = dorsal
                    db.session.add(athlete)
                    db.session.commit()

                    self.clear_fields_errors()
                    filter_text = get_edit_box_value(self.window.ed_filter)
                    self.get_all_athletes(filter_text=filter_text)

                elif operation == 'delete' and athlete:
                    # checks if the athlete is assign to a group_athlete, that is the same as competition
                    group_athlete = db.session.query(GroupAthlete).filter_by(athlete_id=athlete.id).first()
                    if group_athlete:
                        self.window.lb_error_delete.setText(
                            f'No se puede borrar a {athlete.full_name} mientras pertenezca a una competencia')
                    else:
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
            print(e)

    def show_errors(self, errors):
        """ shows the errors gotten from the validations """
        if 'full_name' in errors:
            self.window.lb_name_error.setText(errors['full_name'])
        else:
            self.window.lb_name_error.setText('')
        if 'club' in errors:
            self.window.lb_club_error.setText(errors['club'])
        else:
            self.window.lb_club_error.setText('')
        if 'nit' in errors:
            self.window.lb_nit_error.setText(errors['nit'])
        else:
            self.window.lb_nit_error.setText('')
        if 'dorsal' in errors:
            self.window.lb_dorsal_error.setText(errors['dorsal'])
        else:
            self.window.lb_dorsal_error.setText('')
        if 'general_error' in errors:
            self.window.lb_general_error.setText(errors['general_error'])
        else:
            self.window.lb_general_error.setText('')

    def clear_fields(self):
        """ clear all editText fields for the user """
        self.window.ed_name.setText('')
        self.window.ed_club.setText('')
        self.window.ed_nit.setText('')
        self.window.ed_dorsal.setText('')

    def clear_fields_errors(self):
        """ clear all the label fields where errors are show """
        self.window.lb_name_error.setText('')
        self.window.lb_club_error.setText('')
        self.window.lb_nit_error.setText('')
        self.window.lb_dorsal_error.setText('')
        self.window.lb_general_error.setText('')

    def clear_table(self):
        for i in range(self.window.athletes_table.rowCount()):
            self.window.athletes_table.removeRow(i)

    def set_style_sheet(self):
        self.window.lb_title.setStyleSheet(ButtonStyleSheet.BUTTON_SUCCESS)
        self.window.btn_get_all_athletes.setStyleSheet(ButtonStyleSheet.BUTTON_SUCCESS)
        self.window.btn_add_atlete.setStyleSheet(ButtonStyleSheet.BUTTON_SUCCESS)
        self.window.cb_categories.setStyleSheet(ButtonStyleSheet.BUTTON_SUCCESS)
        ButtonStyleSheet.set_window_icon(self.window)


def validate_data(full_name, club, nit, dorsal, athlete_id=None):
    """ validate each field for an athlete """
    errors = {}
    # validations for field 'name'
    field = 'full_name'
    validate_min(field, full_name, 3, errors)
    validate_max(field, full_name, 100, errors)

    # validations for field 'club'
    field = 'club'
    validate_min(field, club, 2, errors)
    validate_max(field, club, 20, errors)

    # validations for field 'nit'
    field = 'nit'
    validate_min(field, nit, 5, errors)
    validate_max(field, nit, 20, errors)
    validate_int(field, nit, errors)
    try:
        athlete_query = db.session.query(Athlete).filter_by(nit=nit)
        nit_error_label = 'nit'
        nit_error_message = 'Ya existe esta cedula'
        if athlete_id:
            athlete_query = athlete_query.filter(Athlete.id != athlete_id)
            nit_error_label = 'general_error'
            nit_error_message = f'La cedula {nit} ya se encuentra en uso'

        athlete = athlete_query.first()
        if athlete:
            errors[nit_error_label] = nit_error_message

        dorsal_error_label = 'dorsal'
        dorsal_error_message = 'Esta dorsal ya esta en uso'
        dorsal_query = db.session.query(Athlete).filter_by(dorsal=dorsal)
        if athlete_id:
            dorsal_query = dorsal_query.filter(Athlete.id != athlete_id)
            dorsal_error_label = 'general_error'
            dorsal_error_message = f'La dorsal {dorsal} ya se encuentra en uso'

        dorsal = dorsal_query.first()
        if dorsal:
            errors[dorsal_error_label] = dorsal_error_message
    except Exception as e:
        print('Error validando cedula')
        print(e)

    return errors


