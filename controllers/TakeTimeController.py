from engine import db
from app import TakeTimeWindow
from models.Group import Group
from models.GroupAthlete import GroupAthlete
from models.Competence import Competence
from sqlalchemy import or_
from PyQt5 import QtWidgets, QtCore
from datetime import datetime
from datetime import time


class TakeTimeController:
    def __init__(self, window: TakeTimeWindow, competence: Competence):
        self.window = window
        self.competence = competence
        self.window.lb_competence_name = self.competence.name
        self.window.lb_competence_date = self.competence.date
        self.window.ed_filter.textChanged.connect(self.filter_athletes)
        self.window.btn_update_final_time.clicked.connect(self.update_final_time)
        self.load_initial_data()

    def load_initial_data(self, order_group='asc'):
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
            if len(filter_text) >= 3:
                athletes_groups = db.session.query(GroupAthlete)\
                    .filter(GroupAthlete.dorsal.ilike(f'{filter_text}%')).order_by('dorsal').all()
                if athletes_groups:
                    self.show_athletes_table(athletes_groups)
            elif len(filter_text) == 0:
                self.load_initial_data()
        except Exception as e:
            print(f'Error filtering athletes')
            print(e)

    def show_athletes_table(self, athletes_groups):
        for i, athlete in enumerate(athletes_groups):
            self.window.table_times.insertRow(i)

            group_item = QtWidgets.QPushButton()
            group_item.setText(athlete.group.name)
            if athlete.initial_time is not None:
                group_item.setEnabled(False)
            else:
                group_item.clicked.connect(self.update_initial_time)
                group_item.setProperty('group', athlete.group)
            self.window.table_times.setCellWidget(i, 0, group_item)

            athlete_full_name = QtWidgets.QTableWidgetItem(
                f'{athlete.athlete.name} {athlete.athlete.last_name}')
            # disable editing in the cell
            athlete_full_name.setFlags(QtCore.Qt.ItemIsEnabled)
            self.window.table_times.setItem(i, 1, athlete_full_name)

            dorsal = QtWidgets.QTableWidgetItem(athlete.dorsal)
            dorsal.setFlags(QtCore.Qt.ItemIsEnabled)
            self.window.table_times.setItem(i, 2, dorsal)

            initial_time_value = '' if athlete.initial_time is None else athlete.initial_time \
                .strftime('%H:%M:%S')
            initial_time = QtWidgets.QTableWidgetItem(initial_time_value)
            initial_time.setFlags(QtCore.Qt.ItemIsEnabled)
            self.window.table_times.setItem(i, 3, initial_time)

            final_time_value = '' if athlete.final_time is None else athlete.final_time.\
                strftime('%H:%M:%S')
            final_time = QtWidgets.QTableWidgetItem(final_time_value)
            final_time.setFlags(QtCore.Qt.ItemIsEnabled)
            self.window.table_times.setItem(i, 4, final_time)

            total_time_value = '' if athlete.total_time is None else athlete.total_time\
                .strftime('%H:%M:%S')
            total_time = QtWidgets.QTableWidgetItem(total_time_value)
            total_time.setFlags(QtCore.Qt.ItemIsEnabled)
            self.window.table_times.setItem(i, 5, total_time)
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
            athletes_groups = db.session.query(GroupAthlete) \
                .filter(GroupAthlete.dorsal.ilike(f'{filter_text}%')).all()
            if athletes_groups:
                final_time = datetime.now()
                for athlete in athletes_groups:
                    if athlete.initial_time is not None:
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

    def clear_table(self):
        for i in range(self.window.table_times.rowCount()):
            self.window.table_times.removeRow(i)
