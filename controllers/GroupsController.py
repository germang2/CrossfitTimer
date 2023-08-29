from PyQt5.QtWidgets import QMessageBox
from PyQt5 import QtWidgets

from engine import db

from app import CompetencesWindow
from app import AthletesGroupsWindow

from controllers.AthletesGroupsController import AthletesGroupsController

from models.Competence import Competence
from models.Group import Group

from utils.Validations import *
from utils.style_sheet import ButtonStyleSheet
from utils.string_helper import get_edit_box_value


class GroupController:
    def __init__(self, window: CompetencesWindow, competence: Competence):
        self.window = window
        self.competence = competence
        self.window.btn_create_group.clicked.connect(self.create_group)
        self.window.btn_see_all_groups.clicked.connect(self.load_groups_competence)
        if self.competence is None:
            raise ValueError('competence instance must not be None')
        self.window.lb_competence_selected.setText(f'COMPETENCIA: {self.competence.name}')
        self.show_group_items()
        self.load_groups_competence()

        self.athletes_groups_window = AthletesGroupsWindow()
        self.athletes_groups_controller = None
        self.message_box = None
        self.btn_yes = None
        self.btn_no = None
        self.built_message_box()

    def built_message_box(self):
        self.message_box = QMessageBox(self.window)
        self.message_box.setWindowTitle('Confirmar accion')
        self.message_box.setIcon(QMessageBox.Question)
        self.message_box.setText('Desea borrar la oleada?')

        self.btn_yes = self.message_box.addButton('Aceptar', QMessageBox.YesRole)
        self.btn_no = self.message_box.addButton('Cancelar', QMessageBox.NoRole)
        self.message_box.setDefaultButton(self.btn_no)

    def create_group(self):
        """ validate data and creates a new Group """
        name = get_edit_box_value(self.window.ed_group_name)
        order = get_edit_box_value(self.window.ed_group_order)
        errors = validate_data(name=name, order=order)
        if errors:
            self.show_errors(errors)
        else:
            # there are no errors, then the group is create
            try:
                group = Group(name=name, order=order, competence_id=self.competence.id)
                db.session.add(group)
                db.session.commit()
                self.clear_fields()
                self.clear_errors()
                self.load_groups_competence()
            except Exception as e:
                print(f'Error creating group')
                print(e)

    def show_errors(self, errors):
        """ shows all errors after validate data """
        msg = errors['name'] if 'name' in errors else ''
        self.window.lb_group_name_error.setText(msg)
        msg = errors['order'] if 'order' in errors else ''
        self.window.lb_group_order_error.setText(msg)

    def clear_fields(self):
        self.window.ed_group_name.setText('')
        self.window.ed_group_order.setText('')

    def clear_errors(self):
        self.window.lb_group_name_error.setText('')
        self.window.lb_group_order_error.setText('')

    def show_group_items(self):
        self.window.lb_competence_selected.setHidden(False)
        # TODO: Complete method

    def load_groups_competence(self):
        try:
            for i in range(self.window.groups_table.rowCount()):
                self.window.groups_table.removeRow(i)
            groups = db.session.query(Group).filter_by(competence_id=self.competence.id).order_by('order').all()
            if groups:
                for i, group in enumerate(groups):
                    self.window.groups_table.insertRow(i)
                    name = QtWidgets.QTableWidgetItem(group.name)
                    self.window.groups_table.setItem(i, 0, name)
                    order = QtWidgets.QTableWidgetItem(str(group.order))
                    self.window.groups_table.setItem(i, 1, order)

                    btn_see = QtWidgets.QPushButton()
                    btn_see.setText('Ver')
                    btn_see.clicked.connect(self.open_assign_athlete)
                    btn_see.setProperty('competence', self.competence)
                    btn_see.setProperty('group', group)
                    btn_see.setStyleSheet(ButtonStyleSheet.BUTTON_SUCCESS)
                    self.window.groups_table.setCellWidget(i, 2, btn_see)

                    modify = QtWidgets.QPushButton()
                    modify.setText('Modificar')
                    modify.clicked.connect(self.modify_group)
                    modify.setProperty('id', group.id)
                    modify.setStyleSheet(ButtonStyleSheet.BUTTON_SUCCESS)
                    self.window.groups_table.setCellWidget(i, 3, modify)

                    delete = QtWidgets.QPushButton()
                    delete.setText('Eliminar')
                    delete.clicked.connect(self.ask_confirmation)
                    delete.setProperty('id', group.id)
                    delete.setStyleSheet(ButtonStyleSheet.BUTTON_ERROR)
                    self.window.groups_table.setCellWidget(i, 4, delete)
                while True:
                    row_count = self.window.groups_table.rowCount()
                    if row_count <= len(groups):
                        break
                    else:
                        self.window.groups_table.removeRow(row_count - 1)
            else:
                while True:
                    row_count = self.window.groups_table.rowCount()
                    if row_count <= len(groups):
                        break
                    else:
                        self.window.groups_table.removeRow(row_count - 1)

        except Exception as e:
            print(f'Error loading groups of competence: {self.competence}')
            print(e)

    def modify_group(self):
        index_row = self.window.groups_table.currentRow()
        index_column = self.window.groups_table.currentColumn()
        if index_row >= 0 and index_column >= 0:
            name = get_edit_box_value(self.window.groups_table.item(index_row, 0))
            order = get_edit_box_value(self.window.groups_table.item(index_row, 1))
            errors = validate_data(name, order)
            if not errors:
                group_id = int(self.window.groups_table.cellWidget(index_row, index_column).property('id'))
                group = db.session.query(Group).filter_by(id=group_id).first()
                group.name = name
                group.order = order
                db.session.add(group)
                db.session.commit()
            self.load_groups_competence()

    def delete_group(self):
        index_row = self.window.groups_table.currentRow()
        index_column = self.window.groups_table.currentColumn()
        if index_row >= 0 and index_column >= 0:
            group_id = int(self.window.groups_table.cellWidget(index_row, index_column).property('id'))
            group = db.session.query(Group).filter_by(id=group_id).first()
            db.session.delete(group)
            db.session.commit()
        self.load_groups_competence()

    def open_assign_athlete(self):
        """ opens the view that allows assign athletes to the selected group """
        index_row = self.window.groups_table.currentRow()
        index_column = self.window.groups_table.currentColumn()
        item = self.window.groups_table.cellWidget(index_row, index_column)
        competence = item.property('competence')
        group = item.property('group')
        self.athletes_groups_controller = AthletesGroupsController(window=self.athletes_groups_window,
                                                                   competence=competence,
                                                                   group=group)
        self.athletes_groups_window.show()

    def ask_confirmation(self):
        index_row = self.window.groups_table.currentRow()
        index_column = self.window.groups_table.currentColumn()
        if index_row >= 0 and index_column >= 0:
            group_id = int(self.window.groups_table.cellWidget(index_row, index_column).property('id'))
            group = db.session.query(Group).filter_by(id=group_id).first()
            self.message_box.setText(f"Desea borrar la oleada '{group.name}'?")
            self.message_box.exec_()

            if self.message_box.clickedButton() == self.btn_yes:
                self.delete_group()


def validate_data(name, order):
    """ validate each field of a Group """
    errors = {}
    field = 'name'
    validate_min(field, name, 1, errors)
    validate_max(field, name, 20, errors)

    field = 'order'
    validate_exists(field, order, errors)
    if 'order' not in errors:
        validate_int(field, order, errors)
    return errors
