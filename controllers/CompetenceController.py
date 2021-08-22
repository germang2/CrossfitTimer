from engine import db
from app import CompetencesWindow
from app import TakeTimeWindow
from controllers.GroupsController import GroupController
from controllers.TakeTimeController import TakeTimeController
from models.Competence import Competence
from utils.Validations import *
from PyQt5 import QtWidgets
from utils.style_sheet import ButtonStyleSheet


class CompetenceController:
    def __init__(self, window: CompetencesWindow, *args, **kwargs):
        self.window = window
        self.window.btn_create_competition.clicked.connect(self.create_competence)
        self.window.btn_get_all_competitions.clicked.connect(self.get_all_competences)
        self.groups_controller = None
        self.take_time_window = TakeTimeWindow()
        self.take_time_controller = None
        self.clear_tables()
        self.set_style_sheet()

    def get_all_competences(self):
        """ shows in a table all the competences created """
        try:
            self.clear_competences_table()
            self.window.lb_error_delete.setText('')
            competences = db.session.query(Competence).order_by('date').all()
            if competences:
                for i, competence in enumerate(competences):
                    self.window.competences_table.insertRow(i)
                    name = QtWidgets.QTableWidgetItem(competence.name)
                    self.window.competences_table.setItem(i, 0, name)
                    place = QtWidgets.QTableWidgetItem(competence.place)
                    self.window.competences_table.setItem(i, 1, place)
                    date_competence = QtWidgets.QTableWidgetItem(str(competence.date))
                    self.window.competences_table.setItem(i, 2, date_competence)
                    time = QtWidgets.QTableWidgetItem(competence.time)
                    self.window.competences_table.setItem(i, 3, time)

                    btn_group = QtWidgets.QPushButton()
                    btn_group.setText('Grupos')
                    btn_group.setProperty('competence', competence)
                    btn_group.clicked.connect(self.see_groups)
                    btn_group.setStyleSheet(ButtonStyleSheet.BUTTON_SUCCESS)
                    self.window.competences_table.setCellWidget(i, 4, btn_group)

                    btn_see = QtWidgets.QPushButton()
                    btn_see.setText('Tiempos')
                    btn_see.setProperty('competence', competence)
                    btn_see.clicked.connect(self.see_competence)
                    btn_see.setStyleSheet(ButtonStyleSheet.BUTTON_SUCCESS)
                    self.window.competences_table.setCellWidget(i, 5, btn_see)

                    modify = QtWidgets.QPushButton()
                    modify.setText('Modificar')
                    modify.setProperty('id', competence.id)
                    modify.setProperty('operation', 'modify')
                    modify.clicked.connect(self.handle_competences_table)
                    modify.setStyleSheet(ButtonStyleSheet.BUTTON_SUCCESS)
                    self.window.competences_table.setCellWidget(i, 6, modify)
        except Exception as e:
            print('Error loading all competences')
            print(e)

    def handle_competences_table(self):
        """ handles the clicks over the buttons modify and delete on the table for athletes """
        index_row = self.window.competences_table.currentRow()
        index_column = self.window.competences_table.currentColumn()
        if index_row >= 0 and index_column >= 0:
            competence_id = int(self.window.competences_table.cellWidget(index_row, index_column).property('id'))
            competence = db.session.query(Competence).filter_by(id=competence_id).first()
            operation = self.window.competences_table.cellWidget(index_row, index_column).property('operation')
            try:
                if operation == 'modify' and competence:
                    name = self.window.competences_table.item(index_row, 0).text()
                    place = self.window.competences_table.item(index_row, 1).text()
                    date_competence = self.window.competences_table.item(index_row, 2).text()
                    time_competence = self.window.competences_table.item(index_row, 3).text()
                    errors = validate_data(name=name, place=place, date_competence=date_competence, time=time_competence)
                    if not errors:
                        competence.name = name
                        competence.place = place
                        date_values = date_competence.split('-')
                        val = date(int(date_values[0]), int(date_values[1]), int(date_values[2]))
                        competence.date = val
                        competence.time = time_competence
                        db.session.add(competence)
                        db.session.commit()
                        self.get_all_competences()
                    else:
                        self.window.lb_error_delete.setText('Hay errores en los datos modficados, por favor verifique')

                elif operation == 'delete' and competence:
                    competence = db.session.query(Competence).filter_by(id=competence_id).first()
                    db.session.delete(competence)
                    db.session.commit()
                    self.get_all_competences()
            except Exception as e:
                print(e)

    def see_groups(self):
        """ select a competence and shows the groups """
        index_row = self.window.competences_table.currentRow()
        index_column = self.window.competences_table.currentColumn()
        competence = self.window.competences_table.cellWidget(index_row, index_column).property('competence')
        self.groups_controller = GroupController(self.window, competence)

    def see_competence(self):
        """ opens a window for take the times of the athletes """
        index_row = self.window.competences_table.currentRow()
        index_column = self.window.competences_table.currentColumn()
        competence = self.window.competences_table.cellWidget(index_row, index_column).property('competence')
        self.take_time_controller = TakeTimeController(self.take_time_window, competence)
        self.take_time_window.show()

    def create_competence(self):
        """ Creates a new competence object """
        try:
            name = self.window.ed_name.text()
            place = self.window.ed_place.text()
            date_competence = self.window.ed_date.text()
            time = self.window.ed_time.text()
            errors = validate_data(name=name, place=place, date_competence=date_competence, time=time)
            if errors:
                self.show_errors(errors)
            else:
                # if there are not errors, the competence is create
                date_values = date_competence.split('-')
                val = date(int(date_values[0]), int(date_values[1]), int(date_values[2]))
                competence = Competence(name=name, place=place, date=val, time=time)
                db.session.add(competence)
                db.session.commit()
                self.clear_fields()
                self.clear_fields_errors()
        except Exception as e:
            print(f'Failed creation of competence: {e}')

    def show_errors(self, errors):
        """ shows the errors gotten from the validations """
        msg = errors['name'] if 'name' in errors else ''
        self.window.lb_name_error.setText(msg)

        msg = errors['place'] if 'place' in errors else ''
        self.window.lb_place_error.setText(msg)

        msg = errors['date'] if 'date' in errors else ''
        self.window.lb_date_error.setText(msg)

        msg = errors['time'] if 'time' in errors else ''
        self.window.lb_time_error.setText(msg)

    def clear_fields(self):
        """ clear all editText fields for the user """
        self.window.ed_name.setText('')
        self.window.ed_place.setText('')
        self.window.ed_date.setText('')
        self.window.ed_time.setText('')

    def clear_fields_errors(self):
        """ clear all the label fields where errors are show """
        self.window.lb_name_error.setText('')
        self.window.lb_place_error.setText('')
        self.window.lb_date_error.setText('')
        self.window.lb_time_error.setText('')

    def clear_tables(self):
        self.clear_competences_table()
        self.clear_groups_table()

    def clear_competences_table(self):
        self.window.competences_table.clearContents()
        for i in range(self.window.competences_table.rowCount()):
            self.window.competences_table.removeRow(i)

    def clear_groups_table(self):
        self.window.groups_table.clearContents()
        for i in range(self.window.groups_table.rowCount()):
            self.window.groups_table.removeRow(i)

    def set_style_sheet(self):
        self.window.lb_title.setStyleSheet(ButtonStyleSheet.BUTTON_SUCCESS)
        self.window.lb_subtitle.setStyleSheet(ButtonStyleSheet.BUTTON_SUCCESS)
        self.window.btn_get_all_competitions.setStyleSheet(ButtonStyleSheet.BUTTON_SUCCESS)
        self.window.btn_create_competition.setStyleSheet(ButtonStyleSheet.BUTTON_SUCCESS)
        self.window.btn_create_group.setStyleSheet(ButtonStyleSheet.BUTTON_SUCCESS)
        self.window.btn_see_all_groups.setStyleSheet(ButtonStyleSheet.BUTTON_SUCCESS)
        ButtonStyleSheet.set_window_icon(self.window)


def validate_data(name, place, date_competence, time):
    """ validate each field of the Competence and returns a dict of errors """
    errors = {}

    # validations for field 'name'
    field = 'name'
    validate_min(field, name, 3, errors)
    validate_max(field, name, 30, errors)

    # validations for field 'place'
    field = 'place'
    validate_min(field, place, 3, errors)
    validate_max(field, place, 50, errors)

    # validations for field 'date'
    field = 'date'
    validate_date(field, date_competence, errors)

    # validations for field 'time'
    field = 'time'
    validate_exists(field, time, errors)

    return errors
