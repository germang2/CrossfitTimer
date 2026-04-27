from engine import db
from app import CompetencesWindow
from app import TakeTimeWindow
from controllers.GroupsController import GroupController
from controllers.TakeTimeController import TakeTimeController
from managers.GroupManager import GroupManager
from managers.GroupAthleteManager import GroupAthleteManager
from models.Competence import Competence
from models.Group import Group
from utils.Validations import *
from PyQt5 import QtWidgets, QtCore
from utils.style_sheet import ButtonStyleSheet


class CompetenceController:
    def __init__(self, window: CompetencesWindow, *args, **kwargs):
        self.window = window
        self.window.btn_create_competition.clicked.connect(self.create_competence)
        self.window.btn_get_all_competitions.clicked.connect(self.get_all_competences)
        self.groups_controller = None
        self.take_time_window = TakeTimeWindow()
        self.take_time_controller = None
        self.setup_resizable_layout()
        self.clear_tables()
        self.set_style_sheet()
        self.message_box = None
        self.built_message_box()

    def setup_resizable_layout(self):
        # 1. Main Setup
        self.centralwidget = QtWidgets.QWidget(self.window)
        self.main_layout = QtWidgets.QHBoxLayout(self.centralwidget) # Horizontal split
        self.main_layout.setContentsMargins(20, 20, 20, 20)
        self.main_layout.setSpacing(30)

        # 2. Competence Column (Left)
        self.setup_competence_column()

        # 3. Tandas Column (Right)
        self.setup_tandas_column()

        self.window.setCentralWidget(self.centralwidget)
        self.window.setMinimumSize(QtCore.QSize(1300, 750))

    def setup_competence_column(self):
        self.left_column = QtWidgets.QVBoxLayout()
        self.left_column.setSpacing(10)

        # Centering Wrapper for the Form
        self.comp_centering_layout = QtWidgets.QHBoxLayout()
        
        # Form Container (Fixed width to match original design)
        self.comp_form_container = QtWidgets.QWidget()
        self.comp_form_container.setFixedWidth(740)
        self.comp_form_layout = QtWidgets.QVBoxLayout(self.comp_form_container)
        self.comp_form_layout.setContentsMargins(0, 0, 0, 0)
        self.comp_form_layout.setSpacing(5)

        # Header
        self.window.lb_title.setParent(self.comp_form_container)
        self.window.lb_title.setMinimumSize(QtCore.QSize(700, 40))
        self.comp_form_layout.addWidget(self.window.lb_title)

        # Inputs Grid
        self.comp_inputs_grid = QtWidgets.QGridLayout()
        self.comp_inputs_grid.setSpacing(10)
        
        # Row 1: Nombre & Lugar
        self.window.label_2.setParent(self.comp_form_container)
        self.window.label_3.setParent(self.comp_form_container)
        self.window.ed_name.setParent(self.comp_form_container)
        self.window.ed_place.setParent(self.comp_form_container)
        
        self.comp_inputs_grid.addWidget(self.window.label_2, 0, 0, QtCore.Qt.AlignCenter)
        self.comp_inputs_grid.addWidget(self.window.label_3, 0, 1, QtCore.Qt.AlignCenter)
        self.comp_inputs_grid.addWidget(self.window.ed_name, 1, 0)
        self.comp_inputs_grid.addWidget(self.window.ed_place, 1, 1)

        # Errors Row 1
        self.window.lb_name_error.setParent(self.comp_form_container)
        self.window.lb_place_error.setParent(self.comp_form_container)
        self.comp_inputs_grid.addWidget(self.window.lb_name_error, 2, 0)
        self.comp_inputs_grid.addWidget(self.window.lb_place_error, 2, 1)

        # Row 2: Fecha & Hora
        self.window.label_4.setParent(self.comp_form_container)
        self.window.label_5.setParent(self.comp_form_container)
        self.window.ed_date.setParent(self.comp_form_container)
        self.window.ed_time.setParent(self.comp_form_container)
        self.comp_inputs_grid.addWidget(self.window.label_4, 3, 0, QtCore.Qt.AlignCenter)
        self.comp_inputs_grid.addWidget(self.window.label_5, 3, 1, QtCore.Qt.AlignCenter)
        self.comp_inputs_grid.addWidget(self.window.ed_date, 4, 0)
        self.comp_inputs_grid.addWidget(self.window.ed_time, 4, 1)

        # Errors Row 2 & Label 6 (año-mes-dia)
        self.window.lb_date_error.setParent(self.comp_form_container)
        self.window.lb_time_error.setParent(self.comp_form_container)
        self.window.label_6.setParent(self.comp_form_container)
        self.comp_inputs_grid.addWidget(self.window.lb_date_error, 5, 0)
        self.comp_inputs_grid.addWidget(self.window.label_6, 6, 0, QtCore.Qt.AlignCenter)
        self.comp_inputs_grid.addWidget(self.window.lb_time_error, 5, 1)
        
        self.comp_form_layout.addLayout(self.comp_inputs_grid)

        # Buttons Area
        self.comp_btns_layout = QtWidgets.QHBoxLayout()
        self.window.btn_create_competition.setParent(self.comp_form_container)
        self.window.btn_get_all_competitions.setParent(self.comp_form_container)
        self.window.btn_create_competition.setMinimumSize(QtCore.QSize(170, 40))
        self.window.btn_get_all_competitions.setMinimumSize(QtCore.QSize(160, 40))
        self.comp_btns_layout.addStretch()
        self.comp_btns_layout.addWidget(self.window.btn_create_competition)
        self.comp_btns_layout.addStretch()
        self.comp_btns_layout.addWidget(self.window.btn_get_all_competitions)
        self.comp_btns_layout.addStretch()
        self.comp_form_layout.addLayout(self.comp_btns_layout)

        # Finalize Form centering
        self.comp_centering_layout.addStretch()
        self.comp_centering_layout.addWidget(self.comp_form_container)
        self.comp_centering_layout.addStretch()
        self.left_column.addLayout(self.comp_centering_layout)

        # Table
        self.window.competences_table.setParent(self.centralwidget)
        header = self.window.competences_table.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch) # Nombre
        for col in range(1, 8):
            header.setSectionResizeMode(col, QtWidgets.QHeaderView.Interactive)
            self.window.competences_table.setColumnWidth(col, 100)
        self.left_column.addWidget(self.window.competences_table)
        
        # Bottom error label
        self.window.lb_error_delete.setParent(self.centralwidget)
        self.left_column.addWidget(self.window.lb_error_delete)

        self.main_layout.addLayout(self.left_column)

    def setup_tandas_column(self):
        self.right_column = QtWidgets.QVBoxLayout()
        self.right_column.setSpacing(10)

        # Centering Wrapper for Tandas Form
        self.tan_centering_layout = QtWidgets.QHBoxLayout()
        self.tan_form_container = QtWidgets.QWidget()
        self.tan_form_container.setFixedWidth(500)
        self.tan_form_layout = QtWidgets.QVBoxLayout(self.tan_form_container)
        self.tan_form_layout.setContentsMargins(0, 0, 0, 0)
        self.tan_form_layout.setSpacing(10)

        # Header & Subtitle
        self.window.lb_subtitle.setParent(self.tan_form_container)
        self.window.lb_competence_selected.setParent(self.tan_form_container)
        self.tan_form_layout.addWidget(self.window.lb_subtitle)
        self.tan_form_layout.addWidget(self.window.lb_competence_selected)

        # Inputs Grid
        self.tan_grid = QtWidgets.QGridLayout()
        self.window.label_8.setParent(self.tan_form_container)
        self.window.label_9.setParent(self.tan_form_container)
        self.window.ed_group_name.setParent(self.tan_form_container)
        self.window.ed_group_order.setParent(self.tan_form_container)
        self.window.btn_create_group.setParent(self.tan_form_container)
        
        self.tan_grid.addWidget(self.window.label_8, 0, 0, QtCore.Qt.AlignCenter)
        self.tan_grid.addWidget(self.window.label_9, 0, 1, QtCore.Qt.AlignCenter)
        self.tan_grid.addWidget(self.window.ed_group_name, 1, 0)
        self.tan_grid.addWidget(self.window.ed_group_order, 1, 1)
        self.tan_grid.addWidget(self.window.btn_create_group, 1, 2)
        
        # Errors
        self.window.lb_group_name_error.setParent(self.tan_form_container)
        self.window.lb_group_order_error.setParent(self.tan_form_container)
        self.tan_grid.addWidget(self.window.lb_group_name_error, 2, 0)
        self.tan_grid.addWidget(self.window.lb_group_order_error, 2, 1)
        
        self.tan_form_layout.addLayout(self.tan_grid)

        # Actions
        self.tan_actions = QtWidgets.QHBoxLayout()
        self.window.btn_see_all_groups.setParent(self.tan_form_container)
        self.tan_actions.addWidget(self.window.btn_see_all_groups)
        self.tan_actions.addStretch()
        self.tan_form_layout.addLayout(self.tan_actions)

        # Finalize Tandas Form centering
        self.tan_centering_layout.addStretch()
        self.tan_centering_layout.addWidget(self.tan_form_container)
        self.tan_centering_layout.addStretch()
        self.right_column.addLayout(self.tan_centering_layout)

        # Table
        self.window.groups_table.setParent(self.centralwidget)
        header = self.window.groups_table.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch) # Nombre
        for col in range(1, 5):
            header.setSectionResizeMode(col, QtWidgets.QHeaderView.Interactive)
            self.window.groups_table.setColumnWidth(col, 80)
        self.right_column.addWidget(self.window.groups_table)

        self.main_layout.addLayout(self.right_column)

    def built_message_box(self):
        self.message_box = QtWidgets.QMessageBox(self.window)
        self.message_box.setWindowTitle('Confirmar accion')
        self.message_box.setIcon(QtWidgets.QMessageBox.Question)
        self.message_box.setText('Desea borrar la competencia?')

        self.btn_yes = self.message_box.addButton('Aceptar', QtWidgets.QMessageBox.YesRole)
        self.btn_no = self.message_box.addButton('Cancelar', QtWidgets.QMessageBox.NoRole)
        self.message_box.setDefaultButton(self.btn_no)

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
                    btn_group.setText('Tandas')
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

                    delete = QtWidgets.QPushButton()
                    delete.setText('Eliminar')
                    delete.setProperty('id', competence.id)
                    delete.setProperty('operation', 'delete')
                    delete.clicked.connect(self.ask_confirmation)
                    delete.setStyleSheet(ButtonStyleSheet.BUTTON_ERROR)
                    self.window.competences_table.setCellWidget(i, 7, delete)
        except Exception as e:
            print('Error loading all competences')
            print(e)

    def ask_confirmation(self):
        index_row = self.window.competences_table.currentRow()
        index_column = self.window.competences_table.currentColumn()
        if index_row >= 0 and index_column >= 0:
            competence_id = int(self.window.competences_table.cellWidget(index_row, index_column).property('id'))
            competence = db.session.query(Competence).filter_by(id=competence_id).first()
            self.message_box.setText(f"Desea borrar la competencia '{competence.name}'?")
            self.message_box.exec_()

            if self.message_box.clickedButton() == self.btn_yes:
                self.delete_competence()

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

    def delete_competence(self):
        index_row = self.window.competences_table.currentRow()
        index_column = self.window.competences_table.currentColumn()
        if index_row >= 0 and index_column >= 0:
            competence_id = int(self.window.competences_table.cellWidget(index_row, index_column).property('id'))
            competence = db.session.query(Competence).filter_by(id=competence_id).first()
            competence_groups = GroupManager.get_groups_by_filters(filters={Group.competence_id == competence_id})

            for group in competence_groups:
                group_athletes_filters = {
                    "group_id": group.id
                }
                group_athletes = GroupAthleteManager.get_by_filters(
                    filters=group_athletes_filters,
                )
                for group_athlete in group_athletes:
                    db.session.delete(group_athlete)

                db.session.delete(group)
            db.session.delete(competence)
            db.session.commit()

            self.clear_groups_table()
        self.get_all_competences()

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
