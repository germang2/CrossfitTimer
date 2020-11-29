from app import CompetencesWindow
from controllers.GroupsController import GroupController
from engine import db
from models.Competence import Competence
from utils.Validations import *
from PyQt5 import QtWidgets


class CompetenceController:
    def __init__(self, window: CompetencesWindow, *args, **kwargs):
        self.window = window
        self.window.btn_create_competition.clicked.connect(self.create_competence)
        self.window.btn_get_all_competitions.clicked.connect(self.get_all_competences)
        self.window.competences_table.clicked.connect(self.handle_competences_table)
        self.groups_controller = None


    def get_all_competences(self):
        """ shows in a table all the competences created """
        try:
            competences = db.session.query(Competence).order_by('date').all()
            if competences:
                self.window.competences_table.clearContents()
                for i in range(self.window.competences_table.rowCount()):
                    self.window.competences_table.removeRow(i)
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
                    reward = QtWidgets.QTableWidgetItem(competence.reward)
                    self.window.competences_table.setItem(i, 4, reward)

                    btn_see = QtWidgets.QPushButton()
                    btn_see.setText('Ver')
                    btn_see.setProperty('competence', competence)
                    btn_see.clicked.connect(self.see_competence)
                    self.window.competences_table.setCellWidget(i, 5, btn_see)

                    modify = QtWidgets.QPushButton()
                    modify.setText('Modificar')
                    modify.setProperty('id', competence.id)
                    modify.setProperty('operation', 'modify')
                    modify.clicked.connect(self.handle_competences_table)
                    self.window.competences_table.setCellWidget(i, 6, modify)
        except Exception as e:
            print('Error loading all competences')
            print(e)

    def handle_competences_table(self):
        pass

    def see_competence(self):
        index_row = self.window.competences_table.currentRow()
        index_column = self.window.competences_table.currentColumn()
        competence = self.window.competences_table.cellWidget(index_row, index_column).property('competence')
        self.groups_controller = GroupController(self.window, competence)

    def create_competence(self):
        """ Creates a new competence object """
        try:
            name = self.window.ed_name.text()
            place = self.window.ed_place.text()
            date_competence = self.window.ed_date.text()
            time = self.window.ed_time.text()
            reward = self.window.ed_reward.text()
            errors = validate_data(name=name, place=place, date_competence=date_competence, time=time, reward=reward)
            if errors:
                self.show_errors(errors)
            else:
                # if there are not errors, the competence is create
                date_values = date_competence.split('-')
                val = date(int(date_values[0]), int(date_values[1]), int(date_values[2]))
                competence = Competence(name=name, place=place, date=val, time=time, reward=reward)
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

        msg = errors['reward'] if 'reward' in errors else ''
        self.window.lb_reward_error.setText(msg)

    def clear_fields(self):
        """ clear all editText fields for the user """
        self.window.ed_name.setText('')
        self.window.ed_place.setText('')
        self.window.ed_date.setText('')
        self.window.ed_time.setText('')
        self.window.ed_reward.setText('')

    def clear_fields_errors(self):
        """ clear all the label fields where errors are show """
        self.window.lb_name_error.setText('')
        self.window.lb_place_error.setText('')
        self.window.lb_date_error.setText('')
        self.window.lb_time_error.setText('')
        self.window.lb_reward_error.setText('')


def validate_data(name, place, date_competence, time, reward):
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

    # validations for field 'reward'
    field = 'reward'
    if reward and len(reward) > 0:
        validate_max(field, reward, 50, errors)
    return errors
