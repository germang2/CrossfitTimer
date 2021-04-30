from future.backports.email.headerregistry import Group
from datetime import datetime
from engine import db
from app import TakeTimeWindow
from utils.Colors import ColorPicker

from models.Athlete import Athlete
from models.Category import Category
from models.Competence import Competence
from models.Group import Group
from models.GroupAthlete import GroupAthlete


from managers.GroupAthleteManager import GroupAthleteManager
from managers.GroupManager import GroupManager

from fpdf import FPDF
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QMessageBox


class TakeTimeController:
    def __init__(self, window: TakeTimeWindow, competence: Competence):
        self.window = window
        self.competence = competence
        self.category_id_create = {}
        self.window.ed_filter.setText('')
        self.window.lb_competence_name.setText(self.competence.name)
        self.window.lb_competence_date.setText(self.competence.date.strftime('%Y-%m-%d'))
        self.window.ed_filter.textChanged.connect(self.filter_athletes)
        self.window.btn_update_final_time.clicked.connect(self.update_final_time)
        self.window.btn_reset_time.clicked.connect(self.ask_confirmation_reset_time)
        self.load_initial_data()
        self.window.cb_order_table.currentIndexChanged.connect(self.order_table_filter)
        self.window.btn_generate_pdf.clicked.connect(self.generate_pdf)
        self.load_categories()
        self.message_box = None
        self.btn_yes = None
        self.btn_no = None
        self.built_message_box()
        self.built_style()

    def built_style(self):
        self.window.setStyleSheet(ColorPicker.BACKGROUND_GRADIENT_COLOR)
        self.window.label_2.setStyleSheet(ColorPicker.LABEL_COLOR)
        self.window.label_3.setStyleSheet(ColorPicker.LABEL_COLOR)
        self.window.label_5.setStyleSheet(ColorPicker.LABEL_COLOR)
        self.window.label_7.setStyleSheet(ColorPicker.LABEL_COLOR)
        self.window.label_8.setStyleSheet(ColorPicker.LABEL_COLOR)
        self.window.lb_msg.setStyleSheet(ColorPicker.LABEL_COLOR)
        self.window.groupBox.setStyleSheet(ColorPicker.LABEL_COLOR)
        self.window.groupBox_2.setStyleSheet(ColorPicker.LABEL_COLOR)
        self.window.lb_competence_name.setStyleSheet(ColorPicker.LABEL_COLOR)
        self.window.lb_competence_date.setStyleSheet(ColorPicker.LABEL_COLOR)
        self.window.table_times.horizontalHeader().setStyleSheet(ColorPicker.TABLE_HORIZONTAL_HEADER_COLOR)
        self.window.table_times.verticalHeader().setStyleSheet(ColorPicker.TABLE_VERTICAL_HEADER_COLOR)

    def built_message_box(self):
        self.message_box = QMessageBox(self.window)
        self.message_box.setWindowTitle('Confirmar accion')
        self.message_box.setIcon(QMessageBox.Question)
        self.message_box.setText('Desea resetear el tiempo final?')

        self.btn_yes = self.message_box.addButton('Aceptar', QMessageBox.YesRole)
        self.btn_no = self.message_box.addButton('Cancelar', QMessageBox.NoRole)
        self.message_box.setDefaultButton(self.btn_no)
        self.btn_yes.setStyleSheet(f'color: {ColorPicker.SHADOW_OF_LIGHT_BLUE}')
        self.btn_no.setStyleSheet(f'color: {ColorPicker.SHADOW_OF_LIGHT_BLUE}')
        self.message_box.setStyleSheet(f'color: {ColorPicker.SHADOW_OF_LIGHT_BLUE}')

    def ask_confirmation_reset_time(self):
        self.message_box.setText(f"Confirmar accion")
        self.message_box.exec_()
        if self.message_box.clickedButton() == self.btn_yes:
            self.reset_time()

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
            btn_start.setStyleSheet(ColorPicker.BUTTON_TABLE_COLOR)
            self.window.table_times.setCellWidget(i, 1, btn_start)

            athlete_full_name = QtWidgets.QTableWidgetItem(
                f'{athlete.athlete.name} {athlete.athlete.last_name}')
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
        self.window.lb_msg.setText('')

    def update_initial_time(self):
        """ updates the initial time of a set of athletes, in the same group """
        try:
            index_row = self.window.table_times.currentRow()
            index_column = self.window.table_times.currentColumn()
            group = self.window.table_times.cellWidget(index_row, index_column).property('group')
            athletes_groups = db.session.query(GroupAthlete)\
                .filter(GroupAthlete.initial_time.is_(None))\
                .filter_by(group_id=group.id).all()
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

    def reset_time(self):
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
                for athlete in athletes_groups_list:
                    athlete.final_time = None
                    athlete.total_time = None
                    db.session.add(athlete)
                db.session.commit()
                self.window.ed_filter.setText('')
        except Exception as e:
            print('Error reseting time')
            print(e)

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

    def load_categories(self):
        """ loads in a comboBox all the existing categories """
        try:
            self.window.cb_categories.clear()
            categories = db.session.query(Category).order_by('name').all()
            if categories:
                self.category_id_create.clear()
                for i, category in enumerate(categories):
                    self.window.cb_categories.addItem(category.name, userData=category.id)
                    # it adds a relation between the index of the comboBox and the category.id
                    self.category_id_create[i] = category.id
        except Exception as e:
            print(e)

    def generate_pdf(self):
        # TODO add column club next to category
        index_category = self.window.cb_categories.currentIndex()
        category_id = self.category_id_create[index_category]

        try:
            groups = GroupManager.get_groups_by_filters(
                filters={
                    Group.competence_id == self.competence.id
                }
            )
            groups_id_list = [g.id for g in groups]

            athletes_groups = GroupAthleteManager.get_group_athletes_by_filters(
                filters={
                    Group.id.in_(groups_id_list),
                    Athlete.category_id == category_id
                },
                order='total_time'
            )

            if athletes_groups:
                athletes_dict = {}

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
                    headers = ['Grupo', 'Identificacion', 'Nombre', 'Categoria', 'Club', 'Dorsal', 'Hora Inicial',
                               'Hora Final', 'Tiempo total']
                    col_width = epw / 4
                    column_width = {
                        0: col_width * 0.3,
                        1: col_width * 0.38,
                        2: col_width * 1.1,
                        3: col_width * 0.38,
                        4: col_width * 0.38,
                        5: col_width * 0.3,
                        6: col_width * 0.4,
                        7: col_width * 0.4,
                        8: col_width * 0.4
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
                            f'{athlete.athlete.name} {athlete.athlete.last_name}'[:32],
                            athlete.athlete.category.name[:11],
                            athlete.athlete.club[:11],
                            athlete.dorsal,
                            '' if athlete.initial_time is None else athlete.initial_time.strftime('%H:%M:%S.%f')[:-3],
                            '' if athlete.final_time is None else athlete.final_time.strftime('%H:%M:%S.%f')[:-3],
                            '' if athlete.total_time is None else athlete.total_time.strftime('%H:%M:%S.%f')[:-3]

                        ]
                        for i, val in enumerate(data):
                            width = column_width[i]
                            # TODO: cut val in base of column size
                            pdf.cell(width, 2 * th, str(val), border=1)

                        pdf.ln(2 * th)

                    pdf.output(f'{self.competence.name}_{category_name}.pdf', 'F')
                    self.window.lb_msg.setStyleSheet("color: green;")
                    self.window.lb_msg.setText(f'PDF para categoria {category_name} generado con exito')
            else:
                category_name = db.session.query(Category).filter(Category.id == category_id).first().name
                self.window.lb_msg.setStyleSheet("color: red;")
                self.window.lb_msg.setText(f'No hay atletas de la categoria {category_name} para esta competencia')
        except Exception as e:
            print(e)