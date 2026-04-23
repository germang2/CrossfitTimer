# -*- coding: utf-8 -*-

import math
from datetime import datetime
from sqlalchemy import or_

from fpdf import FPDF
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QLineEdit

from engine import db
from app import TakeTimeWindow
from models.Athlete import Athlete
from models.Category import Category
from models.Group import Group
from models.GroupAthlete import GroupAthlete
from models.Competence import Competence
from managers.GroupManager import GroupManager
from managers.GroupAthleteManager import GroupAthleteManager

from utils.style_sheet import ButtonStyleSheet
from utils.string_helper import (
    get_edit_box_value,
    remove_inner_new_lines,
    allow_only_unicode_chars,
)
from utils.Validations import is_positive_number
from utils.logger_helper import logger


class TakeTimeController:
    def __init__(self, window: TakeTimeWindow, competence: Competence):
        self.window = window
        self.competence = competence
        self.window.ed_filter.setText('')
        self.window.lb_competence_name.setText(self.competence.name)
        self.window.lb_competence_date.setText(self.competence.date.strftime('%d-%m-%Y'))
        self.window.ed_filter.keyPressEvent = self.on_key_ed_filter
        self.window.ed_filter_2.keyPressEvent = self.on_key_ed_filter_2
        self.window.ed_filter_3.keyPressEvent = self.on_key_ed_filter_3
        self.window.btn_update_final_time.clicked.connect(self.update_final_time_ed)
        self.window.btn_update_final_time_2.clicked.connect(self.update_final_time_ed_2)
        self.window.btn_update_final_time_3.clicked.connect(self.update_final_time_ed_3)
        self.window.ed_reset.keyPressEvent = self.on_key_reset
        self.window.ed_filter_group.keyPressEvent = self.on_key_ed_group
        self.load_initial_data()
        self.window.cb_order_table.currentIndexChanged.connect(self.order_table_filter)
        self.window.btn_reset_time.clicked.connect(self.reset_time)
        self.window.btn_pdf.clicked.connect(self.generate_pdf)
        self.set_style_sheet()
        self.message_box = None
        self.btn_yes = None
        self.btn_no = None
        self.window.table_times.keyReleaseEvent = self.handle_table_event
        self.built_message_box()
        self.pdf_configuration = {
            "name_max_length": 24
        }

    def built_message_box(self):
        self.message_box = QtWidgets.QMessageBox(self.window)
        self.message_box.setWindowTitle('Confirmar accion')
        self.message_box.setIcon(QtWidgets.QMessageBox.Question)
        self.message_box.setText('Desea iniciar el tiempo de la oleada')

        self.btn_yes = self.message_box.addButton('Aceptar', QtWidgets.QMessageBox.YesRole)
        self.btn_no = self.message_box.addButton('Cancelar', QtWidgets.QMessageBox.NoRole)
        self.message_box.setDefaultButton(self.btn_no)

    def ask_confirmation(self, group_name):
        index_row = self.window.table_times.currentRow()
        index_column = self.window.table_times.currentColumn()
        if index_row >= 0 and index_column >= 0:
            self.message_box.setText(f"Desea iniciar el tiempo de la oleada '{group_name}'?")
            self.message_box.exec_()

            if self.message_box.clickedButton() == self.btn_yes:
                return True
        return False

    def handle_table_event(self, e):
        if e.key() == QtCore.Qt.Key_Return or e.key() == QtCore.Qt.Key_Enter:
            index_row = self.window.table_times.currentRow()
            index_column = self.window.table_times.currentColumn()
            if index_row >= 0 and index_column in [8, 9]:
                _id = self.window.table_times.cellWidget(index_row, 1).property("group_athlete_id")
                value_text = self.window.table_times.item(index_row, index_column).text()

                # Get current record to have the old value for reverting if needed
                filters = {
                    GroupAthlete.id == _id
                }
                group_athletes = GroupAthleteManager.get_group_athletes_by_filters(
                    filters=filters
                )
                if group_athletes:
                    group_athlete = group_athletes[0]
                    # Determine old value based on column
                    old_value = group_athlete.tasks_completed if index_column == 8 else group_athlete.penalty
                    old_value_str = str(old_value) if old_value is not None else "0"

                    # Validate new value
                    is_valid = is_positive_number(value_text)
                    if is_valid:
                        value_int = int(value_text)
                        # Specific validation for penalty column
                        if index_column == 9 and value_int > 1000:
                            is_valid = False

                    if is_valid:
                        if index_column == 8:
                            group_athlete.tasks_completed = int(value_text)
                        elif index_column == 9:
                            group_athlete.penalty = int(value_text)
                        db.session.add(group_athlete)
                        db.session.commit()
                    else:
                        # Revert the value in the table cell
                        self.window.table_times.item(index_row, index_column).setText(old_value_str)
        else:
            pass

    def handle_status_change(self, checkbox):
        group_athlete_id = checkbox.property('group_athlete_id')
        is_checked = checkbox.isChecked()
        filters = {
            GroupAthlete.id == group_athlete_id
        }
        group_athlete = GroupAthleteManager.get_group_athletes_by_filters(
            filters=filters
        )
        if group_athlete:
            group_athlete = group_athlete[0]
            group_athlete.status = is_checked
            db.session.add(group_athlete)
            db.session.commit()

    def clear_table_input(self, table: QtWidgets.QTableWidget, index_row: int, index_column: int):
        """
        Clears the table input with an empty value
        :param table: QtWidgets.QTableWidget, table that contains the cells
        :param index_row: int, row to apply the clear format
        :param index_column: int, column to apply the clear format
        """
        try:
            table.item(index_row, index_column).setText("")
        except Exception as e:
            logger.error(f"Error cleaning cell: {index_row}, {index_column}. Error details: {e}")

    def on_key_ed_filter(self, e):
        if e.key() == QtCore.Qt.Key_Return or e.key() == QtCore.Qt.Key_Enter:
            self.filter_athletes(edit_widget=self.window.ed_filter)
        else:
            QLineEdit.keyPressEvent(self.window.ed_filter, e)

    def on_key_ed_filter_2(self, e):
        if e.key() == QtCore.Qt.Key_Return or e.key() == QtCore.Qt.Key_Enter:
            self.filter_athletes(edit_widget=self.window.ed_filter_2)
        else:
            QLineEdit.keyPressEvent(self.window.ed_filter_2, e)

    def on_key_ed_filter_3(self, e):
        if e.key() == QtCore.Qt.Key_Return or e.key() == QtCore.Qt.Key_Enter:
            self.filter_athletes(edit_widget=self.window.ed_filter_3)
        else:
            QLineEdit.keyPressEvent(self.window.ed_filter_3, e)

    def on_key_reset(self, e):
        if e.key() == QtCore.Qt.Key_Return or e.key() == QtCore.Qt.Key_Enter:
            self.filter_athletes(edit_widget=self.window.ed_reset)
        else:
            QLineEdit.keyPressEvent(self.window.ed_reset, e)

    def on_key_ed_group(self, e):
        if e.key() == QtCore.Qt.Key_Return or e.key() == QtCore.Qt.Key_Enter:
            self.filter_by_group()
        else:
            QLineEdit.keyPressEvent(self.window.ed_filter_group, e)

    def load_initial_data(self):
        try:
            filter_text = get_edit_box_value(self.window.ed_filter_group)
            if filter_text:
                self.filter_by_group()
                return

            groups = GroupManager.get_groups_by_filters({Group.competence_id == self.competence.id}, order=Group.order.asc())
            if groups:
                total_list = []
                for group in groups:
                    athletes_groups = GroupAthleteManager.get_group_athletes_by_filters({GroupAthlete.group_id == group.id})
                    total_list += athletes_groups
                self.show_athletes_table(total_list)
        except Exception as e:
            print(f'Error loading data of table')
            print(e)

    def filter_athletes(self, edit_widget):
        try:
            filter_text = allow_only_unicode_chars(get_edit_box_value(edit_widget))
            if filter_text and filter_text[-1] == ',':
                return
            groups = GroupManager.get_groups_by_filters(
                filters={Group.competence_id == self.competence.id},
                order=Group.order.asc()
            )
            if len(filter_text) >= 2 and groups:
                group_list = [g.id for g in groups]
                filters_list = filter_text.split(',')
                athletes_list = []
                for f in set(filters_list):
                    athletes_groups = GroupAthleteManager.filter_athletes_by_dorsal(
                        filters={GroupAthlete.dorsal.ilike(f), Group.id.in_(group_list)},
                    )
                    athletes_list += athletes_groups
                if athletes_list:
                    self.show_athletes_table(athletes_list)
            elif len(filter_text) == 0:
                self.load_initial_data()
        except Exception as e:
            print(f'Error filtering athletes')
            print(e)
        self.clear_pdf_label()

    def filter_by_group(self):
        try:
            filter_text = allow_only_unicode_chars(get_edit_box_value(self.window.ed_filter_group))
            if filter_text and filter_text[-1] == ',':
                return
            groups = GroupManager.get_groups_by_filters(
                filters={Group.competence_id == self.competence.id},
                order=Group.order.asc()
            )
            if len(filter_text) >= 2 and groups:
                group_list = [g.id for g in groups]
                filters_list = filter_text.split(',')
                athletes_list = []

                for f in set(filters_list):
                    param_to_filter = f'%{f}%'
                    category_list = db.session.query(Category).filter(Category.name.ilike(param_to_filter)).all()
                    category_id_list = [cat.id for cat in category_list]
                    athletes_groups = GroupAthleteManager.filter_athletes_by_dorsal(
                        filters={
                            or_(
                                Group.name.ilike(param_to_filter),
                                Athlete.full_name.ilike(param_to_filter),
                                Athlete.category_id.in_(category_id_list)
                            ),
                            Group.id.in_(group_list)
                        },
                    )
                    athletes_list += athletes_groups
                if athletes_list:
                    self.show_athletes_table(athletes_list)
            elif len(filter_text) == 0:
                self.load_initial_data()
        except Exception as e:
            print(f'Error filtering athletes')
            print(e)
        self.clear_pdf_label()

    def show_athletes_table(self, athletes_groups):
        self.clear_table()
        for athlete in athletes_groups:
            if not athlete.athlete:
                continue

            i = self.window.table_times.rowCount()

            self.window.table_times.insertRow(i)

            group_item = QtWidgets.QTableWidgetItem(athlete.group.name)
            self.window.table_times.setItem(i, 0, group_item)

            btn_start = QtWidgets.QPushButton()
            btn_start.setText('INICIAR')
            if athlete.initial_time is not None:
                btn_start.setEnabled(False)
                btn_start.setStyleSheet(ButtonStyleSheet.BUTTON_DISABLED)
            else:
                btn_start.clicked.connect(self.update_initial_time)
                btn_start.setProperty('group', athlete.group)
                btn_start.setStyleSheet(ButtonStyleSheet.BUTTON_SUCCESS)
            btn_start.setProperty('group_athlete_id', athlete.id)
            self.window.table_times.setCellWidget(i, 1, btn_start)

            athlete_full_name = QtWidgets.QTableWidgetItem(
                f'{athlete.athlete.full_name}')
            # disable editing in the cell
            athlete_full_name.setFlags(QtCore.Qt.ItemIsEnabled)
            self.window.table_times.setItem(i, 2, athlete_full_name)

            category_name = QtWidgets.QTableWidgetItem(athlete.athlete.category.name)
            category_name.setFlags(QtCore.Qt.ItemIsEnabled)
            self.window.table_times.setItem(i, 3, category_name)

            dorsal = QtWidgets.QTableWidgetItem(athlete.dorsal)
            dorsal.setFlags(QtCore.Qt.ItemIsEnabled)
            self.window.table_times.setItem(i, 4, dorsal)

            initial_time_value = '' if athlete.initial_time is None else athlete.initial_time \
                .strftime('%H:%M:%S.%f')[:-3]
            initial_time = QtWidgets.QTableWidgetItem(initial_time_value)
            initial_time.setFlags(QtCore.Qt.ItemIsEnabled)
            self.window.table_times.setItem(i, 5, initial_time)

            final_time_value = '' if athlete.final_time is None else athlete.final_time \
                .strftime('%H:%M:%S.%f')[:-3]
            final_time = QtWidgets.QTableWidgetItem(final_time_value)
            final_time.setFlags(QtCore.Qt.ItemIsEnabled)
            self.window.table_times.setItem(i, 6, final_time)

            total_time_value = '' if athlete.total_time is None else athlete.total_time\
                .strftime('%H:%M:%S.%f')[:-3]
            total_time = QtWidgets.QTableWidgetItem(total_time_value)
            total_time.setFlags(QtCore.Qt.ItemIsEnabled)
            self.window.table_times.setItem(i, 7, total_time)

            tasks_completed_value = str(athlete.tasks_completed) if athlete.tasks_completed else ""
            tasks_completed = QtWidgets.QTableWidgetItem(tasks_completed_value)
            self.window.table_times.setItem(i, 8, tasks_completed)

            penalty_value = str(athlete.penalty) if athlete.penalty is not None else "0"
            penalty = QtWidgets.QTableWidgetItem(penalty_value)
            self.window.table_times.setItem(i, 9, penalty)

            # status column with widget-level styling (reverted)
            container = QtWidgets.QWidget()
            layout = QtWidgets.QHBoxLayout(container)
            cb_status = QtWidgets.QCheckBox()
            cb_status.setProperty('group_athlete_id', athlete.id)
            cb_status.stateChanged.connect(lambda state, cb=cb_status: self.handle_status_change(cb))
            cb_status.setChecked(athlete.status if athlete.status is not None else True)
            cb_status.setStyleSheet(ButtonStyleSheet.CHECKBOX_STYLE) # Reverted to widget level
            layout.addWidget(cb_status)
            layout.setAlignment(QtCore.Qt.AlignCenter)
            layout.setContentsMargins(0, 0, 0, 0)
            self.window.table_times.setCellWidget(i, 10, container)

        self.clear_pdf_label()

    def update_initial_time(self):
        """ updates the initial time of a set of athletes, in the same group """
        try:
            index_row = self.window.table_times.currentRow()
            index_column = self.window.table_times.currentColumn()
            group = self.window.table_times.cellWidget(index_row, index_column).property('group')
            confirm_start_time = self.ask_confirmation(group.name)
            if confirm_start_time:
                # athletes_groups = db.session.query(GroupAthlete).filter_by(group_id=group.id).all()
                athletes_groups = GroupAthleteManager.get_group_athletes_by_filters({GroupAthlete.group_id == group.id})
                initial_time = datetime.now()
                for athlete_group in athletes_groups:
                    athlete_group.initial_time = initial_time
                    db.session.add(athlete_group)
                db.session.commit()
                self.load_initial_data()

        except Exception as e:
            print(f'Error updating initial time')
            print(e)
        self.clear_pdf_label()

    def filter_athletes_by_dorsal(self, edit_widget):
        """
        Filter athletes using the text inserted by the user, with the field 'dorsal'
        :param edit_widget: Widget, edit text where take text
        :return: Array of GroupAthlete
        """
        try:
            filter_text = allow_only_unicode_chars(get_edit_box_value(edit_widget))
            athletes_groups_list = []
            if filter_text and filter_text[-1] == ',':
                filter_text = filter_text[:-1]
            filter_list = filter_text.split(',')
            groups = db.session.query(Group).filter_by(competence_id=self.competence.id).order_by(
                Group.order.asc()).all()
            group_list = [g.id for g in groups]
            for f in set(filter_list):
                athletes_groups = db.session.query(GroupAthlete).filter(GroupAthlete.dorsal.ilike(f)) \
                    .join(Group).filter(Group.id.in_(group_list)).order_by('dorsal').all()
                athletes_groups_list += athletes_groups
            return athletes_groups_list
        except Exception as e:
            print(e)
            return []

    def update_final_time_ed(self):
        self.update_final_time(edit_widget=self.window.ed_filter)

    def update_final_time_ed_2(self):
        self.update_final_time(edit_widget=self.window.ed_filter_2)

    def update_final_time_ed_3(self):
        self.update_final_time(edit_widget=self.window.ed_filter_3)

    def update_final_time(self, edit_widget):
        """ updates the final time to all the objects inside gotten from the filter """
        try:
            athletes_groups_list = self.filter_athletes_by_dorsal(edit_widget=edit_widget)
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
                self.filter_athletes(edit_widget=edit_widget)
                edit_widget.setText('')
        except Exception as e:
            print('Error updating final time and total time')
            print(e)
        self.clear_pdf_label()

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
                        .join(Group).filter(Group.id.in_(groups_list)).order_by(Athlete.full_name.asc()).all()
                elif filter_selected == 'Tanda ascendente':
                    athletes_groups = db.session.query(GroupAthlete).join(Group).filter(Group.id.in_(groups_list))\
                        .order_by(Group.order.asc()).all()
                elif filter_selected == 'Tanda descendente':
                    athletes_groups = db.session.query(GroupAthlete).join(Group).filter(Group.id.in_(groups_list))\
                        .order_by(Group.order.desc()).all()
                else:
                    athletes_groups = db.session.query(GroupAthlete).join(Group).filter(Group.id.in_(groups_list))\
                        .order_by(GroupAthlete.dorsal.asc()).all()
                self.show_athletes_table(athletes_groups=athletes_groups)
        except Exception as e:
            print(f'Error ordering table')
            print(e)
        self.clear_pdf_label()

    def clear_table(self):
        # for i in range(self.window.table_times.rowCount()):
        #     self.window.table_times.removeRow(i)
        self.window.table_times.clearContents()
        self.window.table_times.setRowCount(0)

    def reset_time(self):
        try:
            athletes_groups_list = self.filter_athletes_by_dorsal(edit_widget=self.window.ed_reset)
            if athletes_groups_list:
                for athlete in athletes_groups_list:
                    athlete.final_time = None
                    athlete.total_time = None
                    db.session.add(athlete)
                db.session.commit()
                self.filter_athletes(edit_widget=self.window.ed_reset)
                self.window.ed_reset.setText('')
        except Exception as e:
            print('Error reseting time')
            print(e)
        self.clear_pdf_label()

    def clear_pdf_label(self):
        self.window.lb_pdf.setText('')

    def generate_pdf(self):

        try:
            groups = GroupManager.get_groups_by_filters({Group.competence_id == self.competence.id},
                                                        order=Group.order.asc())
            if groups:
                athletes_dict = {}
                for group in groups:
                    athletes_groups = GroupAthleteManager.get_group_athletes_by_filters(
                        filters={GroupAthlete.group_id == group.id},
                        order='total_time'
                    )
                    for athlete in athletes_groups:
                        category_name = athlete.athlete.category.name
                        if category_name in athletes_dict:
                            athletes_dict[category_name].append(athlete)
                        else:
                            athletes_dict[category_name] = [athlete]

                for category_name, athlete_list in athletes_dict.items():
                    category_name = remove_inner_new_lines(category_name).strip()
                    pdf = FPDF(format='letter', unit='in', orientation='L')
                    # Effective page width, or just epw
                    epw = pdf.w - 2 * pdf.l_margin
                    # Set column width to 1/4 of effective page width to distribute content
                    # evenly across table and page
                    headers = [
                        'Tanda',
                        'Posición',
                        'Nombre',
                        'Club',
                        'Dorsal',
                        'Hora Inicial',
                        'Hora Final',
                        'Tiempo total',
                        "# Manillas",
                    ]
                    col_width = epw / 4
                    column_width = {
                        # Group
                        0: col_width * 0.3,
                        # Position
                        1: col_width * 0.3,
                        # Name
                        2: col_width * 1.2,
                        # Club
                        3: col_width * 0.45,
                        # Dorsal
                        4: col_width * 0.3,
                        # Initial time
                        5: col_width * 0.4,
                        # Final time
                        6: col_width * 0.4,
                        # Total time
                        7: col_width * 0.4,
                        # Tasks_completed
                        8: col_width * 0.3
                    }
                    pdf.set_font('Arial', 'B', 12)
                    pdf.add_page()
                    pdf.cell(epw, 0.0, f'{self.competence.name} - Categoria: {category_name}', align='C')

                    pdf.ln(0.5)
                    # Text height is the same as current font size
                    th = pdf.font_size

                    pdf.set_font('Arial', 'B', 9.0)
                    for i, header in enumerate(headers):
                        width = column_width[i]
                        # TODO: cut val in base of column size
                        pdf.cell(width, 2 * th, header, border=1)

                    pdf.set_font('Arial', '', 9.0)
                    pdf.ln(2 * th)

                    list_with_time = [a for a in athlete_list if a.total_time]
                    list_no_time = [a for a in athlete_list if a.total_time is None]
                    # sorted_list = sorted(list_with_time, key=lambda x: x.total_time)
                    sorted_list = sorted(list_with_time, key=self.none_safe_key, reverse=False)
                    sorted_list = sorted_list + list_no_time

                    for position, athlete in enumerate(sorted_list):
                        if not athlete:
                            continue
                        data = [
                            athlete.group.name[:10],
                            # index + 1 = position
                            position + 1,
                            allow_only_unicode_chars(athlete.athlete.full_name),
                            allow_only_unicode_chars(athlete.athlete.club[:11]),

                            athlete.dorsal,
                            '' if athlete.initial_time is None else athlete.initial_time.strftime('%H:%M:%S.%f')[:-3],
                            '' if athlete.final_time is None else athlete.final_time.strftime('%H:%M:%S.%f')[:-3],
                            '' if athlete.total_time is None else athlete.total_time.strftime('%H:%M:%S.%f')[:-3],
                            athlete.tasks_completed if athlete.tasks_completed else 0,
                        ]
                        # Calculate row height based on Name wrapping
                        name_text = str(data[2])
                        name_w = column_width[2]
                        # Rough estimate of lines needed
                        lines = math.ceil(pdf.get_string_width(name_text) / (name_w - 0.1))
                        lines = max(lines, 1)
                        row_h = max(2 * th, lines * th)

                        if pdf.get_y() + row_h > pdf.page_break_trigger:
                            pdf.add_page()

                        x_start = pdf.get_x()
                        y_start = pdf.get_y()

                        for i, val in enumerate(data):
                            width = column_width[i]
                            if i == 2:
                                # Nombre column with wrapping
                                x = pdf.get_x()
                                y = pdf.get_y()
                                pdf.multi_cell(width, row_h / lines, str(val), border=1)
                                pdf.set_xy(x + width, y)
                            else:
                                pdf.cell(width, row_h, str(val), border=1)

                        pdf.set_y(y_start + row_h)

                    pdf.output(f'{self.competence.name}_{category_name}.pdf', 'F')
                    self.window.lb_pdf.setText('PDF generados con exito')
        except Exception as e:
            print(e)

    def none_safe_key(self, obj):
        return (
            -(int(obj.tasks_completed) if obj.tasks_completed is not None else 0),
            obj.total_time if obj.total_time is not None else None
        )

    def set_style_sheet(self):
        self.window.lb_title.setStyleSheet(ButtonStyleSheet.BUTTON_SUCCESS)
        self.window.btn_pdf.setStyleSheet(ButtonStyleSheet.BUTTON_SUCCESS)
        self.window.cb_order_table.setStyleSheet(ButtonStyleSheet.BUTTON_SUCCESS)

        self.window.table_times.setColumnWidth(2, 200)
        self.window.table_times.setColumnWidth(4, 100)
        ButtonStyleSheet.set_window_icon(self.window)
