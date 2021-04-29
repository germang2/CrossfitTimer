from engine import db
from app import CompetencesWindow
from app import AthletesGroupsWindow
from models.Competence import Competence
from models.Group import Group
from utils.Validations import *
from utils.Colors import ColorPicker
from PyQt5 import QtWidgets
from controllers.AthletesGroupsController import AthletesGroupsController


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
        self.built_style()

    def built_style(self):
        pass

    def create_group(self):
        """ validate data and creates a new Group """
        name = self.window.ed_group_name.text()
        order = self.window.ed_group_order.text()
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
                    btn_see.setStyleSheet(ColorPicker.BUTTON_TABLE_COLOR)
                    self.window.groups_table.setCellWidget(i, 2, btn_see)

                    btn_modify = QtWidgets.QPushButton()
                    btn_modify.setText('Modificar')
                    btn_modify.clicked.connect(self.modify_group)
                    btn_modify.setProperty('id', group.id)
                    btn_modify.setStyleSheet(ColorPicker.BUTTON_TABLE_COLOR)
                    self.window.groups_table.setCellWidget(i, 3, btn_modify)

                    btn_delete = QtWidgets.QPushButton()
                    btn_delete.setText('Eliminar')
                    btn_delete.clicked.connect(self.delete_group)
                    btn_delete.setProperty('id', group.id)
                    btn_delete.setStyleSheet(ColorPicker.BUTTON_TABLE_COLOR)
                    self.window.groups_table.setCellWidget(i, 4, btn_delete)
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
            name = self.window.groups_table.item(index_row, 0).text()
            order = self.window.groups_table.item(index_row, 1).text()
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
