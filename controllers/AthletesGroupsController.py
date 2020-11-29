from engine import db
from app import AthletesGroupsWindow
from models.Athlete import Athlete
from models.Competence import Competence
from models.Group import Group
from models.GroupAthlete import GroupAthlete
from sqlalchemy import or_
from PyQt5 import QtWidgets, QtCore


class AthletesGroupsController:
    def __init__(self, window: AthletesGroupsWindow, competence: Competence, group: Group):
        self.window = window
        self.competence = competence
        self.group = group
        self.load_info()
        self.window.ed_filter_athlete.textChanged.connect(self.filter_athletes)
        self.window.btn_load_athletes.clicked.connect(self.load_all_athletes)
        self.window.btn_reload_assigned_athletes.clicked.connect(self.load_athletes_assigned)

    def load_info(self):
        """ loads the information about the competence and group """
        self.window.lb_competence_name.setText(self.competence.name)
        self.window.lb_competence_date.setText(str(self.competence.date))
        self.window.lb_group_name.setText(self.group.name)
        self.load_athletes_assigned()

    def load_athletes_assigned(self):
        """ loads all athletes for the current group """
        try:
            groups_athletes = db.session.query(GroupAthlete).filter_by(group_id=self.group.id).order_by('dorsal').all()
            if groups_athletes:
                self.window.lb_error_add_athlete.setText('')
                self.window.table_athletes_assigned.clearContents()
                for i in range(self.window.table_athletes_assigned.rowCount()):
                    self.window.table_athletes_assigned.removeRow(i)
                for i, item in enumerate(groups_athletes):
                    self.window.table_athletes_assigned.insertRow(i)
                    name = QtWidgets.QTableWidgetItem(item.athlete.name)
                    # disable editing in the cell
                    name.setFlags(QtCore.Qt.ItemIsEnabled)
                    self.window.table_athletes_assigned.setItem(i, 0, name)
                    lastname = QtWidgets.QTableWidgetItem(item.athlete.last_name)
                    lastname.setFlags(QtCore.Qt.ItemIsEnabled)
                    self.window.table_athletes_assigned.setItem(i, 1, lastname)
                    nit = QtWidgets.QTableWidgetItem(item.athlete.nit)
                    nit.setFlags(QtCore.Qt.ItemIsEnabled)
                    self.window.table_athletes_assigned.setItem(i, 2, nit)
                    dorsal = QtWidgets.QTableWidgetItem(item.dorsal)
                    self.window.table_athletes_assigned.setItem(i, 3, dorsal)

                    btn_modify = QtWidgets.QPushButton()
                    btn_modify.setText('Modificar')
                    btn_modify.setProperty('group_athlete', item)
                    btn_modify.clicked.connect(self.modify_dorsal)
                    self.window.table_athletes_assigned.setCellWidget(i, 4, btn_modify)

                    btn_remove = QtWidgets.QPushButton()
                    btn_remove.setText('Quitar')
                    btn_remove.clicked.connect(self.remove_athlete_from_group)
                    btn_remove.setProperty('group_athlete', item)
                    self.window.table_athletes_assigned.setCellWidget(i, 5, btn_remove)

                while True:
                    row_count = self.window.table_athletes_assigned.rowCount()
                    if row_count <= len(groups_athletes):
                        break
                    else:
                        self.window.table_athletes_assigned.removeRow(row_count - 1)

        except Exception as e:
            print(f'Error loading athletes for group {self.group}')
            print(e)

    def modify_dorsal(self):
        """ modifies the field dorsal for an athlete in this group """
        index_row = self.window.table_athletes_assigned.currentRow()
        index_column = self.window.table_athletes_assigned.currentColumn()
        if index_row >= 0 and index_column >= 0:
            dorsal = self.window.table_athletes_assigned.item(index_row, 3).text()
            if dorsal:
                group_athlete = self.window.table_athletes_assigned.cellWidget(index_row, index_column) \
                    .property('group_athlete')
                group_athlete.dorsal = dorsal
                db.session.add(group_athlete)
                db.session.commit()
                self.load_athletes_assigned()

    def remove_athlete_from_group(self):
        """ removes an athlete from the current group """
        index_row = self.window.table_athletes_assigned.currentRow()
        index_column = self.window.table_athletes_assigned.currentColumn()
        if index_row >= 0 and index_column >= 0:
            group_athlete = self.window.table_athletes_assigned.cellWidget(index_row, index_column)\
                .property('group_athlete')
            db.session.delete(group_athlete)
            db.session.commit()
            self.load_athletes_assigned()

    def filter_athletes(self):
        """ search athletes filtering with the text the user type """
        try:
            text = self.window.ed_filter_athlete.text()
            text.strip()
            athletes = None
            if text and len(text) >= 3:
                if text.isnumeric():
                    athletes = db.session.query(Athlete).filter(Athlete.nit.ilike(f'%{text}%')).order_by('name').all()
                else:
                    athletes = db.session.query(Athlete).filter(
                        or_(Athlete.name.ilike(f'%{text}%'), Athlete.last_name.ilike(f'%{text}%'))) \
                        .order_by('name').all()
            self.show_athletes_table(athletes)

        except Exception as e:
            print(f'Error filtering athletes')
            print(e)

    def load_all_athletes(self):
        try:
            athletes = db.session.query(Athlete).order_by('name').all()
            self.show_athletes_table(athletes)
        except Exception as e:
            print(f'Error loading all athletes')
            print(e)

    def show_athletes_table(self, athletes):
        """ receives an array of athletes and show them in the table """
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

                btn_add = QtWidgets.QPushButton()
                btn_add.setText('Agregar')
                btn_add.setProperty('athlete', athlete)
                btn_add.clicked.connect(self.add_athlete_to_group)
                self.window.athletes_table.setCellWidget(i, 3, btn_add)
            while True:
                row_count = self.window.athletes_table.rowCount()
                if row_count <= len(athletes):
                    break
                else:
                    self.window.athletes_table.removeRow(row_count - 1)

    def add_athlete_to_group(self):
        index_row = self.window.athletes_table.currentRow()
        index_column = self.window.athletes_table.currentColumn()
        if index_row >= 0 and index_column >= 0:
            athlete = self.window.athletes_table.cellWidget(index_row, index_column).property('athlete')
            check_exists = db.session.query(GroupAthlete).filter_by(athlete_id=athlete.id, group_id=self.group.id).first()
            if check_exists:
                self.window.lb_error_add_athlete.setText(f'{athlete.name} {athlete.last_name} ya fue asignado/a a este grupo')
            else:
                group_athlete = GroupAthlete(athlete_id=athlete.id, group_id=self.group.id)
                db.session.add(group_athlete)
                db.session.commit()
                self.load_athletes_assigned()
