from PyQt5 import QtWidgets, QtCore

from sqlalchemy import or_

from app import AthletesGroupsWindow

from engine import db

from models.Athlete import Athlete
from models.Category import Category
from models.Competence import Competence
from models.Group import Group
from models.GroupAthlete import GroupAthlete

from managers.GroupAthleteManager import GroupAthleteManager
from managers.AthleteManager import AthleteManager
from managers.GroupManager import GroupManager

from utils.style_sheet import ButtonStyleSheet
from utils.string_helper import get_edit_box_value


class AthletesGroupsController:
    def __init__(self, window: AthletesGroupsWindow, competence: Competence, group: Group):
        self.window = window
        self.competence = competence
        self.group = group
        self.setup_resizable_layout()
        self.clear_tables()
        self.load_info()
        self.window.ed_filter_athlete.textChanged.connect(self.filter_athletes)
        self.window.btn_load_athletes.clicked.connect(self.load_all_athletes)
        self.window.btn_reload_assigned_athletes.clicked.connect(self.load_athletes_assigned)

    def setup_resizable_layout(self):
        # 1. Main Setup
        # Keep default size as 1300x750 but allow user to reduce it
        self.window.resize(1300, 750)
        self.window.setMinimumSize(QtCore.QSize(500, 400))

        # Wrap everything in a scroll area to allow resizing without breaking layout
        self.scroll_area = QtWidgets.QScrollArea(self.window)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.scroll_area.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)

        self.centralwidget = QtWidgets.QWidget(self.scroll_area)
        self.centralwidget.setObjectName("centralwidget")
        self.centralwidget.setMinimumSize(QtCore.QSize(1300, 750))
        self.main_layout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.main_layout.setContentsMargins(20, 10, 20, 20)
        self.main_layout.setSpacing(10)

        # 2. Top Info Section (Centered)
        self.setup_top_info_section()

        # 3. Grid for Tables and Controls (Aligns rows)
        self.grid_layout = QtWidgets.QGridLayout()
        self.grid_layout.setSpacing(20)
        self.grid_layout.setColumnStretch(0, 1)
        self.grid_layout.setColumnStretch(1, 1)

        # 4. Available Athletes Section (Left)
        # Filters Area container
        self.avail_filters_container = QtWidgets.QWidget()
        self.avail_filters_container.setFixedWidth(500)
        self.avail_vbox = QtWidgets.QVBoxLayout(self.avail_filters_container)
        self.avail_vbox.setContentsMargins(0, 0, 0, 0)
        self.avail_vbox.setSpacing(2)

        self.window.label_3.setParent(self.avail_filters_container)
        self.window.ed_filter_athlete.setParent(self.avail_filters_container)
        self.window.label_4.setParent(self.avail_filters_container)
        self.window.btn_load_athletes.setParent(self.avail_filters_container)
        
        self.avail_vbox.addWidget(self.window.label_3)
        self.avail_vbox.addWidget(self.window.ed_filter_athlete)
        self.avail_vbox.addWidget(self.window.label_4)
        self.avail_actions = QtWidgets.QHBoxLayout()
        self.avail_actions.addStretch()
        self.avail_actions.addWidget(self.window.btn_load_athletes)
        self.avail_vbox.addLayout(self.avail_actions)

        self.grid_layout.addWidget(self.avail_filters_container, 0, 0, QtCore.Qt.AlignLeft | QtCore.Qt.AlignBottom)

        # Left Table
        self.window.athletes_table.setParent(self.centralwidget)
        header_left = self.window.athletes_table.horizontalHeader()
        header_left.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        for col in range(1, 5):
            header_left.setSectionResizeMode(col, QtWidgets.QHeaderView.Interactive)
            if col == 1: # Categoria
                self.window.athletes_table.setColumnWidth(col, 170)
            else:
                self.window.athletes_table.setColumnWidth(col, 100)
        self.grid_layout.addWidget(self.window.athletes_table, 1, 0)

        # Left Error label
        self.window.lb_error_add_athlete.setParent(self.centralwidget)
        self.grid_layout.addWidget(self.window.lb_error_add_athlete, 2, 0)

        # 5. Assigned Athletes Section (Right)
        # Header Area container
        self.assigned_top_container = QtWidgets.QWidget()
        self.assigned_top_container.setFixedWidth(500)
        self.assigned_vbox = QtWidgets.QVBoxLayout(self.assigned_top_container)
        self.assigned_vbox.setContentsMargins(0, 0, 0, 0)
        self.assigned_vbox.setSpacing(10)

        self.assigned_header = QtWidgets.QHBoxLayout()
        self.window.btn_reload_assigned_athletes.setParent(self.assigned_top_container)
        self.window.label_6.setParent(self.assigned_top_container)
        self.window.lb_group_name_2.setParent(self.assigned_top_container)
        
        self.assigned_header.addWidget(self.window.btn_reload_assigned_athletes)
        self.assigned_header.addWidget(self.window.label_6)
        self.assigned_header.addWidget(self.window.lb_group_name_2)
        self.assigned_header.addStretch()
        self.assigned_vbox.addLayout(self.assigned_header)

        self.grid_layout.addWidget(self.assigned_top_container, 0, 1, QtCore.Qt.AlignLeft | QtCore.Qt.AlignBottom)

        # Right Table
        self.window.table_athletes_assigned.setParent(self.centralwidget)
        header_right = self.window.table_athletes_assigned.horizontalHeader()
        header_right.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        for col in range(1, 6):
            header_right.setSectionResizeMode(col, QtWidgets.QHeaderView.Interactive)
            if col == 2: # Categoria
                self.window.table_athletes_assigned.setColumnWidth(col, 170)
            else:
                self.window.table_athletes_assigned.setColumnWidth(col, 90)
        self.grid_layout.addWidget(self.window.table_athletes_assigned, 1, 1)

        # Right Alert label
        self.window.lb_alert.setParent(self.centralwidget)
        self.grid_layout.addWidget(self.window.lb_alert, 2, 1)

        self.main_layout.addLayout(self.grid_layout)
        
        self.scroll_area.setWidget(self.centralwidget)
        self.window.setCentralWidget(self.scroll_area)

    def setup_top_info_section(self):
        self.top_section_layout = QtWidgets.QVBoxLayout()
        
        # Centering Wrapper for Top Header
        self.header_centering = QtWidgets.QHBoxLayout()
        self.window.lb_title.setParent(self.centralwidget)
        self.window.lb_title.setMinimumSize(QtCore.QSize(1000, 40))
        self.header_centering.addStretch()
        self.header_centering.addWidget(self.window.lb_title)
        self.header_centering.addStretch()
        self.top_section_layout.addLayout(self.header_centering)

        # Form-like info Grid (Centered)
        self.info_centering = QtWidgets.QHBoxLayout()
        self.info_container = QtWidgets.QWidget()
        self.info_container.setFixedWidth(600)
        self.info_grid = QtWidgets.QGridLayout(self.info_container)
        self.info_grid.setSpacing(5)

        self.window.label.setParent(self.info_container)
        self.window.lb_competence_name.setParent(self.info_container)
        self.window.label_5.setParent(self.info_container)
        self.window.lb_competence_date.setParent(self.info_container)
        self.window.label_2.setParent(self.info_container)
        self.window.lb_group_name.setParent(self.info_container)

        self.info_grid.addWidget(self.window.label, 0, 0, QtCore.Qt.AlignRight)
        self.info_grid.addWidget(self.window.lb_competence_name, 0, 1, QtCore.Qt.AlignLeft)
        self.info_grid.addWidget(self.window.label_5, 1, 0, QtCore.Qt.AlignRight)
        self.info_grid.addWidget(self.window.lb_competence_date, 1, 1, QtCore.Qt.AlignLeft)
        self.info_grid.addWidget(self.window.label_2, 2, 0, QtCore.Qt.AlignRight)
        self.info_grid.addWidget(self.window.lb_group_name, 2, 1, QtCore.Qt.AlignLeft)

        self.info_centering.addStretch()
        self.info_centering.addWidget(self.info_container)
        self.info_centering.addStretch()
        
        self.top_section_layout.addLayout(self.info_centering)
        self.main_layout.addLayout(self.top_section_layout)

    def load_info(self):
        """ loads the information about the competence and group """
        self.window.lb_competence_name.setText(self.competence.name)
        self.window.lb_competence_date.setText(str(self.competence.date))
        self.window.lb_group_name.setText(self.group.name)
        self.window.lb_group_name_2.setText(self.group.name)
        self.load_athletes_assigned()
        self.set_style_sheet()

    def clear_table(self, table: QtWidgets.QTableWidget):
        """
        Clears the content of the table and remove all the rows
        :param table: QtWidgets.QTableWidget to clear
        """
        table.setRowCount(0)
        table.clearContents()

    def load_athletes_assigned(self):
        """ loads all athletes for the current group """
        try:
            alert_without_dorsal_flag = False
            self.window.lb_error_add_athlete.setText('')

            self.clear_table(self.window.table_athletes_assigned)
            # groups_athletes = db.session.query(GroupAthlete).filter_by(group_id=self.group.id).order_by('dorsal').all()
            filters = {GroupAthlete.group_id == self.group.id}
            groups_athletes = GroupAthleteManager.get_group_athletes_by_filters(filters=filters, join_group=True)

            if groups_athletes:
                self.window.lb_error_add_athlete.setText('')
                for item in groups_athletes:
                    if not item.athlete:
                        continue

                    i = self.window.table_athletes_assigned.rowCount()

                    self.window.table_athletes_assigned.insertRow(i)
                    name = QtWidgets.QTableWidgetItem(item.athlete.full_name)
                    # disable editing in the cell
                    name.setFlags(QtCore.Qt.ItemIsEnabled)
                    self.window.table_athletes_assigned.setItem(i, 0, name)
                    nit = QtWidgets.QTableWidgetItem(item.athlete.nit)
                    nit.setFlags(QtCore.Qt.ItemIsEnabled)
                    self.window.table_athletes_assigned.setItem(i, 1, nit)
                    category_name = QtWidgets.QTableWidgetItem(item.athlete.category.name)
                    category_name.setFlags(QtCore.Qt.ItemIsEnabled)
                    self.window.table_athletes_assigned.setItem(i, 2, category_name)
                    dorsal = QtWidgets.QTableWidgetItem(item.dorsal)
                    self.window.table_athletes_assigned.setItem(i, 3, dorsal)

                    if item.dorsal is None:
                        alert_without_dorsal_flag = True

                    btn_modify = QtWidgets.QPushButton()
                    btn_modify.setText('Modificar')
                    btn_modify.setProperty('group_athlete', item)
                    btn_modify.clicked.connect(self.modify_dorsal)
                    btn_modify.setStyleSheet(ButtonStyleSheet.BUTTON_SUCCESS)
                    self.window.table_athletes_assigned.setCellWidget(i, 4, btn_modify)

                    btn_remove = QtWidgets.QPushButton()
                    btn_remove.setText('Quitar')
                    btn_remove.clicked.connect(self.remove_athlete_from_group)
                    btn_remove.setProperty('group_athlete', item)
                    btn_remove.setStyleSheet(ButtonStyleSheet.BUTTON_ERROR)
                    self.window.table_athletes_assigned.setCellWidget(i, 5, btn_remove)

                if alert_without_dorsal_flag:
                    self.window.lb_alert.setText('Hay atletas sin dorsal')
                else:
                    self.window.lb_alert.setText('')

        except Exception as e:
            print(f'Error loading athletes for group {self.group}')
            print(e)

    def modify_dorsal(self):
        """ modifies the field dorsal for an athlete in this group """
        index_row = self.window.table_athletes_assigned.currentRow()
        index_column = self.window.table_athletes_assigned.currentColumn()
        if index_row >= 0 and index_column >= 0:
            dorsal_cell = self.window.table_athletes_assigned.item(index_row, 3)
            dorsal = get_edit_box_value(dorsal_cell)
            dorsal = dorsal.strip() if dorsal else ""
            if dorsal:
                group_athlete = (
                    self.window.table_athletes_assigned.cellWidget(index_row, index_column).property('group_athlete')
                )
                current_dorsal = group_athlete.dorsal
                if dorsal == current_dorsal:
                    return

                # verify dorsal must be unique in competence
                competence_id = self.competence.id
                dorsal_in_use_by, group_athlete_in_use = GroupAthleteManager.get_athlete_by_dorsal(
                    dorsal=dorsal,
                    competence_id=competence_id,
                )
                if not dorsal_in_use_by:
                    group_athlete.dorsal = dorsal
                    db.session.add(group_athlete)
                    db.session.commit()
                    self.load_athletes_assigned()
                else:
                    # restore previous dorsal to cell in table
                    dorsal_cell.setText(current_dorsal)
                    # display validation error message
                    athlete_name = dorsal_in_use_by.full_name
                    group_name = group_athlete_in_use.group.name
                    self.window.lb_alert.setText(f'Dorsal "{dorsal}" en uso por: {athlete_name} - Tanda: "{group_name}"')

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
            text = get_edit_box_value(self.window.ed_filter_athlete)
            if text and len(text) >= 1:
                athletes = []
                order = 'full_name'
                if text.isnumeric():
                    athletes = db.session.query(Athlete).filter(
                        Athlete.nit.ilike(f'%{text}%')
                    ).order_by(order).all()
                else:
                    athletes = db.session.query(Athlete).join(Category, Category.id == Athlete.category_id).filter(
                        or_(
                            Athlete.full_name.ilike(f'%{text}%'),
                            Category.name.ilike(f'%{text}%')
                        )
                    ).order_by(order).all()
                if athletes:
                    self.show_athletes_table(athletes)
            else:
                self.clear_table_athletes()

        except Exception as e:
            print(f'Error filtering athletes')
            print(e)

    def load_all_athletes(self):
        try:
            athletes = AthleteManager.get_athletes_by_filters(filters={}, order='full_name')
            self.show_athletes_table(athletes)
        except Exception as e:
            print(f'Error loading all athletes')
            print(e)

    def show_athletes_table(self, athletes):
        """ receives an array of athletes and show them in the table """
        if athletes:
            self.window.athletes_table.clearContents()
            self.window.athletes_table.setRowCount(0)

            for i, athlete in enumerate(athletes):
                self.window.athletes_table.insertRow(i)
                name = QtWidgets.QTableWidgetItem(athlete.full_name)
                name.setFlags(QtCore.Qt.ItemIsEnabled)
                self.window.athletes_table.setItem(i, 0, name)
                category = QtWidgets.QTableWidgetItem(athlete.category.name)
                category.setFlags(QtCore.Qt.ItemIsEnabled)
                self.window.athletes_table.setItem(i, 1, category)
                dorsal = QtWidgets.QTableWidgetItem(athlete.dorsal)
                dorsal.setFlags(QtCore.Qt.ItemIsEnabled)
                self.window.athletes_table.setItem(i, 2, dorsal)
                nit = QtWidgets.QTableWidgetItem(athlete.nit)
                nit.setFlags(QtCore.Qt.ItemIsEnabled)
                self.window.athletes_table.setItem(i, 3, nit)
                btn_add = QtWidgets.QPushButton()
                btn_add.setText('Agregar')
                btn_add.setProperty('athlete', athlete)
                btn_add.clicked.connect(self.add_athlete_to_group)
                btn_add.setStyleSheet(ButtonStyleSheet.BUTTON_SUCCESS)
                self.window.athletes_table.setCellWidget(i, 4, btn_add)

    def add_athlete_to_group(self):
        index_row = self.window.athletes_table.currentRow()
        index_column = self.window.athletes_table.currentColumn()
        if index_row >= 0 and index_column >= 0:
            athlete = self.window.athletes_table.cellWidget(index_row, index_column).property('athlete')
            # checks if the athlete is in other group already
            groups = GroupManager.get_groups_by_filters(filters={Group.competence_id == self.competence.id})
            groups_list = [g.id for g in groups]
            filters = {GroupAthlete.group_id.in_(groups_list), GroupAthlete.athlete_id == athlete.id}
            check_exists = GroupAthleteManager.get_group_athletes_by_filters(filters)
            if check_exists:
                group_athlete = check_exists[0]
                group_name = group_athlete.group.name
                self.window.lb_error_add_athlete.setText(f'{athlete.full_name} ya pertence a la tanda {group_name}')
            else:
                group_athlete = GroupAthlete(
                    athlete_id=athlete.id,
                    group_id=self.group.id,
                    dorsal=athlete.dorsal,
                )
                db.session.add(group_athlete)
                db.session.commit()
                self.load_athletes_assigned()

    def clear_tables(self):
        self.clear_table_athletes_assigned()
        self.clear_table_athletes()

    def clear_table_athletes_assigned(self):
        self.window.table_athletes_assigned.clearContents()
        for i in range(self.window.table_athletes_assigned.rowCount()):
            self.window.table_athletes_assigned.removeRow(i)

    def clear_table_athletes(self):
        self.window.athletes_table.clearContents()
        for i in range(self.window.athletes_table.rowCount()):
            self.window.athletes_table.removeRow(i)

    def set_style_sheet(self):
        self.window.lb_title.setStyleSheet(ButtonStyleSheet.BUTTON_SUCCESS)
        self.window.btn_load_athletes.setStyleSheet(ButtonStyleSheet.BUTTON_SUCCESS)
        self.window.btn_reload_assigned_athletes.setStyleSheet(ButtonStyleSheet.BUTTON_SUCCESS)
        ButtonStyleSheet.set_window_icon(self.window)

