from future.backports.email.headerregistry import Group

from engine import db
from app import TakeTimeWindow
from models.Athlete import Athlete
from models.Category import Category
from models.Group import Group
from models.GroupAthlete import GroupAthlete
from models.Competence import Competence
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QLineEdit
from datetime import datetime
from managers.GroupManager import GroupManager
from managers.GroupAthleteManager import GroupAthleteManager
from fpdf import FPDF
from PyQt5.QtWidgets import QMessageBox
from utils.style_sheet import ButtonStyleSheet
from sqlalchemy import or_


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

    def on_key_ed_filter(self, e):
        if e.key() == QtCore.Qt.Key_Return:
            self.filter_athletes(edit_widget=self.window.ed_filter)
        else:
            QLineEdit.keyPressEvent(self.window.ed_filter, e)

    def on_key_ed_filter_2(self, e):
        if e.key() == QtCore.Qt.Key_Return:
            self.filter_athletes(edit_widget=self.window.ed_filter_2)
        else:
            QLineEdit.keyPressEvent(self.window.ed_filter_2, e)

    def on_key_ed_filter_3(self, e):
        if e.key() == QtCore.Qt.Key_Return:
            self.filter_athletes(edit_widget=self.window.ed_filter_3)
        else:
            QLineEdit.keyPressEvent(self.window.ed_filter_3, e)

    def on_key_reset(self, e):
        if e.key() == QtCore.Qt.Key_Return:
            self.filter_athletes(edit_widget=self.window.ed_reset)
        else:
            QLineEdit.keyPressEvent(self.window.ed_reset, e)

    def on_key_ed_group(self, e):
        if e.key() == QtCore.Qt.Key_Return:
            self.filter_by_group()
        else:
            QLineEdit.keyPressEvent(self.window.ed_filter_group, e)

    def load_initial_data(self):
        try:
            groups = GroupManager.get_groups_by_filters({Group.competence_id == self.competence.id}, order=Group.order.asc())
            if groups:
                self.clear_table()
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
            filter_text = edit_widget.text()
            filter_text.strip()
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
            filter_text = self.window.ed_filter_group.text()
            filter_text.strip()
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
            btn_start.setStyleSheet(ButtonStyleSheet.BUTTON_SUCCESS)
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
        while True:
            row_count = self.window.table_times.rowCount()
            if row_count <= len(athletes_groups):
                break
            else:
                self.window.table_times.removeRow(row_count - 1)
        self.clear_pdf_label()

    def update_initial_time(self):
        """ updates the initial time of a set of athletes, in the same group """
        try:
            index_row = self.window.table_times.currentRow()
            index_column = self.window.table_times.currentColumn()
            group = self.window.table_times.cellWidget(index_row, index_column).property('group')
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
            filter_text = edit_widget.text()
            filter_text.strip()
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
                elif filter_selected == 'Grupo ascendente':
                    athletes_groups = db.session.query(GroupAthlete).join(Group).filter(Group.id.in_(groups_list))\
                        .order_by(Group.order.asc()).all()
                elif filter_selected == 'Grupo descendente':
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
        for i in range(self.window.table_times.rowCount()):
            self.window.table_times.removeRow(i)

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
                    pdf = FPDF(format='letter', unit='in', orientation='L')
                    # Effective page width, or just epw
                    epw = pdf.w - 2 * pdf.l_margin
                    # Set column width to 1/4 of effective page width to distribute content
                    # evenly across table and page
                    headers = ['Grupo', 'Identificacion', 'Nombre', 'Categoria', 'Dorsal', 'Hora Inicial',
                               'Hora Final', 'Tiempo total']
                    col_width = epw / 4
                    column_width = {
                        0: col_width * 0.3,
                        1: col_width * 0.5,
                        2: col_width * 1.1,
                        3: col_width * 0.45,
                        4: col_width * 0.3,
                        5: col_width * 0.4,
                        6: col_width * 0.4,
                        7: col_width * 0.4
                    }
                    pdf.set_font('Arial', 'B', 14)
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
                    sorted_list = sorted(list_with_time, key=lambda x: x.total_time)
                    sorted_list = sorted_list + list_no_time

                    for athlete in sorted_list:
                        data = [
                            athlete.group.name[:10],
                            athlete.athlete.nit,
                            athlete.athlete.full_name[:32],
                            athlete.athlete.category.name[:11],

                            athlete.dorsal,
                            '' if athlete.initial_time is None else athlete.initial_time.strftime('%H:%M:%S.%f')[:-3],
                            '' if athlete.final_time is None else athlete.final_time.strftime('%H:%M:%S.%f')[:-3],
                            '' if athlete.total_time is None else athlete.total_time.strftime('%H:%M:%S.%f')[:-3]

                        ]
                        for i, val in enumerate(data):
                            width = column_width[i]
                            #TODO: cut val in base of column size
                            pdf.cell(width, 2 * th, str(val), border=1)

                        pdf.ln(2*th)

                    pdf.output(f'{self.competence.name}_{category_name}.pdf', 'F')
                    self.window.lb_pdf.setText('PDF generados con exito')
        except Exception as e:
            print(e)

    def set_style_sheet(self):
        self.window.lb_title.setStyleSheet(ButtonStyleSheet.BUTTON_SUCCESS)
        self.window.btn_pdf.setStyleSheet(ButtonStyleSheet.BUTTON_SUCCESS)
        self.window.cb_order_table.setStyleSheet(ButtonStyleSheet.BUTTON_SUCCESS)