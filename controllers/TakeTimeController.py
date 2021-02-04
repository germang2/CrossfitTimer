from future.backports.email.headerregistry import Group

from engine import db
from app import TakeTimeWindow
from models.Athlete import Athlete
from models.Group import Group
from models.GroupAthlete import GroupAthlete
from models.Competence import Competence
from sqlalchemy import or_, and_
from PyQt5 import QtWidgets, QtCore
from datetime import datetime
from datetime import time


class TakeTimeController:
    def __init__(self, window: TakeTimeWindow, competence: Competence):
        self.window = window
        self.competence = competence
        self.window.ed_filter.setText('')
        self.window.lb_competence_name.setText(self.competence.name)
        self.window.lb_competence_date.setText(self.competence.date.strftime('%H:%M:%S'))
        self.window.ed_filter.textChanged.connect(self.filter_athletes)
        self.window.btn_update_final_time.clicked.connect(self.update_final_time)
        self.load_initial_data()
        self.window.cb_order_table.currentIndexChanged.connect(self.order_table_filter)
        self.window.btn_reset_time.clicked.connect(self.reset_time)

    def load_initial_data(self):
        try:
            groups = db.session.query(Group).filter_by(competence_id=self.competence.id).order_by(Group.order.asc()).all()
            if groups:
                self.clear_table()
                total_list = []
                for group in groups:
                    athletes_groups = db.session.query(GroupAthlete).filter_by(
                        group_id=group.id).all()
                    total_list += athletes_groups
                self.show_athletes_table(total_list)
        except Exception as e:
            print(f'Error loading data of table')
            print(e)

    def filter_athletes(self):
        try:
            filter_text = self.window.ed_filter.text()
            filter_text.strip()
            if filter_text and filter_text[-1] == ',':
                return
            groups = db.session.query(Group).filter_by(competence_id=self.competence.id).order_by(
                Group.order.asc()).all()
            if len(filter_text) >= 2 and groups:
                group_list = [g.id for g in groups]
                filters_list = filter_text.split(',')
                athletes_list = []
                for f in set(filters_list):
                    athletes_groups = db.session.query(GroupAthlete).filter(GroupAthlete.dorsal.ilike(f))\
                        .join(Group).filter(Group.id.in_(group_list)).order_by('dorsal').all()
                    athletes_list += athletes_groups
                if athletes_list:
                    self.show_athletes_table(athletes_list)
            elif len(filter_text) == 0:
                self.load_initial_data()
        except Exception as e:
            print(f'Error filtering athletes')
            print(e)

    def show_athletes_table(self, athletes_groups):
        for i, athlete in enumerate(athletes_groups):
            self.window.table_times.insertRow(i)

            group_item = QtWidgets.QTableWidgetItem(athlete.group.name)
            self.window.table_times.setItem(i, 0, group_item)

            btn_start = QtWidgets.QPushButton()
            btn_start.setText('INICIAR')
            if athlete.initial_time is not None:
                btn_start.setEnabled(False)
            else:
                btn_start.clicked.connect(self.update_initial_time)
                btn_start.setProperty('group', athlete.group)
            self.window.table_times.setCellWidget(i, 1, btn_start)

            athlete_full_name = QtWidgets.QTableWidgetItem(
                f'{athlete.athlete.full_name}')
            # disable editing in the cell
            athlete_full_name.setFlags(QtCore.Qt.ItemIsEnabled)
            self.window.table_times.setItem(i, 2, athlete_full_name)

            category_name = QtWidgets.QTableWidgetItem(athlete.athlete.category.name)
            self.window.table_times.setItem(i, 3, category_name)

            dorsal = QtWidgets.QTableWidgetItem(athlete.dorsal)
            dorsal.setFlags(QtCore.Qt.ItemIsEnabled)
            self.window.table_times.setItem(i, 4, dorsal)

            initial_time_value = '' if athlete.initial_time is None else athlete.initial_time \
                .strftime('%H:%M:%S.%f')[:-3]
            initial_time = QtWidgets.QTableWidgetItem(initial_time_value)
            initial_time.setFlags(QtCore.Qt.ItemIsEnabled)
            self.window.table_times.setItem(i, 5, initial_time)

            final_time_value = '' if athlete.final_time is None else athlete.final_time.\
                strftime('%H:%M:%S.%f')[:-3]
            final_time = QtWidgets.QTableWidgetItem(final_time_value)
            final_time.setFlags(QtCore.Qt.ItemIsEnabled)
            self.window.table_times.setItem(i, 6, final_time)

            total_time_value = '' if athlete.total_time is None else athlete.total_time\
                .strftime('%H:%M:%S.%f')[:-3]
            total_time = QtWidgets.QTableWidgetItem(total_time_value)
            total_time.setFlags(QtCore.Qt.ItemIsEnabled)
            self.window.table_times.setItem(i, 7, total_time)
        while True:
            row_count = self.window.table_times.rowCount()
            if row_count <= len(athletes_groups):
                break
            else:
                self.window.table_times.removeRow(row_count - 1)

    def update_initial_time(self):
        """ updates the initial time of a set of athletes, in the same group """
        try:
            index_row = self.window.table_times.currentRow()
            index_column = self.window.table_times.currentColumn()
            group = self.window.table_times.cellWidget(index_row, index_column).property('group')
            athletes_groups = db.session.query(GroupAthlete).filter_by(group_id=group.id).all()
            initial_time = datetime.now()
            for athlete_group in athletes_groups:
                athlete_group.initial_time = initial_time
                db.session.add(athlete_group)
            db.session.commit()
            self.load_initial_data()

        except Exception as e:
            print(f'Error updating initial time')
            print(e)

    def update_final_time(self):
        """ updates the final time to all the objects inside gotten from the filter """
        try:
            filter_text = self.window.ed_filter.text()
            filter_text.strip()
            athletes_groups_list = []
            if filter_text[-1] == ',':
                filter_text = filter_text[:-1]
            filter_list = filter_text.split(',')
            groups = db.session.query(Group).filter_by(competence_id=self.competence.id).order_by(
                Group.order.asc()).all()
            group_list = [g.id for g in groups]
            for f in set(filter_list):
                athletes_groups = db.session.query(GroupAthlete).filter(GroupAthlete.dorsal.ilike(f)) \
                    .join(Group).filter(Group.id.in_(group_list)).order_by('dorsal').all()
                athletes_groups_list += athletes_groups
            if athletes_groups_list:
                final_time = datetime.now()
                for athlete in athletes_groups_list:
                    if athlete.initial_time is not None and athlete.final_time is None:
                        initial_time = athlete.initial_time
                        total_seconds = final_time - initial_time

                        total_time = datetime.strptime(f'{total_seconds}', '%H:%M:%S.%f')
                        athlete.final_time = final_time
                        athlete.total_time = total_time
                        db.session.add(athlete)
                db.session.commit()
                self.window.ed_filter.setText('')
        except Exception as e:
            print('Error updating final time and total time')
            print(e)
            self.window.ed_filter.setText('')

    def order_table_filter(self):
        try:
            filter_selected = self.window.cb_order_table.currentText()
            self.window.ed_filter.setText('')
            groups = db.session.query(Group).filter_by(competence_id=self.competence.id).order_by(
                Group.order.asc()).all()
            if filter_selected and groups:
                groups_list = [g.id for g in groups]
                # TODO: filter by groups of competition
                if filter_selected == 'Dorsal':
                    athletes_groups = db.session.query(GroupAthlete).join(Group).filter(Group.id.in_(groups_list))\
                        .order_by(GroupAthlete.dorsal.asc()).all()
                elif filter_selected == 'Hora inicio':
                    athletes_groups = db.session.query(GroupAthlete).join(Group).filter(Group.id.in_(groups_list))\
                        .order_by(GroupAthlete.initial_time.asc()).all()
                elif filter_selected == 'Hora fin':
                    athletes_groups = db.session.query(GroupAthlete).join(Group).filter(Group.id.in_(groups_list))\
                        .order_by(GroupAthlete.final_time.asc()).all()
                elif filter_selected == 'Tiempo total':
                    athletes_groups = db.session.query(GroupAthlete).join(Group).filter(Group.id.in_(groups_list))\
                        .order_by(GroupAthlete.total_time.asc()).all()
                elif filter_selected == 'Nombre':
                    athletes_groups = db.session.query(GroupAthlete).join(Athlete)\
                        .join(Group).filter(Group.id.in_(groups_list)).order_by(Athlete.name.asc()).all()
                elif filter_selected == 'Grupo ascendente':
                    athletes_groups = db.session.query(GroupAthlete).join(Group).filter(Group.id.in_(groups_list))\
                        .order_by(Group.order.asc()).all()
                elif filter_selected == 'Grupo descendente':
                    athletes_groups = db.session.query(GroupAthlete).join(Group).filter(Group.id.in_(groups_list))\
                        .order_by(Group.order.desc()).all()
                else:
                    athletes_groups = db.session.query(GroupAthlete).order_by(GroupAthlete.dorsal.asc()).all()
                self.show_athletes_table(athletes_groups=athletes_groups)
        except Exception as e:
            print(f'Error ordering table')
            print(e)

    def clear_table(self):
        for i in range(self.window.table_times.rowCount()):
            self.window.table_times.removeRow(i)

    def reset_time(self):
        try:
            pass
        except Exception as e:
            print('Error reseting time')
            print(e)
