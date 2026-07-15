from sqlalchemy import or_
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QLineEdit

from app import AthletesWindow

from models.Athlete import Athlete
from models.Category import Category
from models.GroupAthlete import GroupAthlete

from engine import db

from utils.style_sheet import ButtonStyleSheet
from utils.string_helper import get_edit_box_value, allow_only_unicode_chars
from utils.Validations import *
from utils.pagination_helper import PaginationHelper


class AthletesController:
    def __init__(self, window: AthletesWindow):
        self.window = window
        
        # Setup Resizable Layout and Styles
        self.setup_resizable_layout()
        self.set_style_sheet()
        
        # Initialize Controller State
        self.window.btn_add_atlete.clicked.connect(self.create_athlete)
        self.window.btn_get_all_athletes.clicked.connect(self.get_all_athletes)
        self.window.ed_filter.keyPressEvent = self.on_key_search_athlete
        self.category_id_create = {}
        self.category_id_modify = {}
        self.load_categories()
        self.clear_table()
        
        self.pagination_helper = PaginationHelper()
        self.initialize_pagination()

    def setup_resizable_layout(self):
        """
        Organizes the UI components into nested layouts to allow for resizing.
        This version centers the form elements above the table and fixes their width.
        """
        # Keep default size as 1140x764 but allow user to reduce it
        self.window.resize(1140, 764)
        self.window.setMinimumSize(QtCore.QSize(500, 400))
        
        # Wrap everything in a scroll area to allow resizing without breaking layout
        self.scroll_area = QtWidgets.QScrollArea(self.window)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.scroll_area.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)

        self.centralwidget = QtWidgets.QWidget(self.scroll_area)
        self.centralwidget.setObjectName("centralwidget")
        self.centralwidget.setMinimumSize(QtCore.QSize(1140, 764))
        self.main_layout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.main_layout.setContentsMargins(50, 20, 50, 20)
        self.main_layout.setSpacing(20)
        self.main_layout.setObjectName("main_layout")

        # --- CENTERING WRAPPER FOR FORM ELEMENTS ---
        self.centering_layout = QtWidgets.QHBoxLayout()
        self.form_vbox = QtWidgets.QVBoxLayout()
        self.form_vbox.setSpacing(15)
        # Fix the width of the form area to match the "small screen" look (~1000px)
        # This will be centered horizontally by the stretches in centering_layout
        self.form_container_widget = QtWidgets.QWidget()
        self.form_container_widget.setFixedWidth(1040)
        self.form_container_layout = QtWidgets.QVBoxLayout(self.form_container_widget)
        self.form_container_layout.setContentsMargins(0, 0, 0, 0)
        self.form_container_layout.setSpacing(15)

        # 1. Title Section
        self.window.lb_title.setParent(self.form_container_widget)
        self.window.lb_title.setMinimumHeight(60)
        self.form_container_layout.addWidget(self.window.lb_title)

        # 2. Name Section
        self.name_section = QtWidgets.QVBoxLayout()
        self.name_section.setSpacing(5)
        self.window.label_2.setParent(self.form_container_widget)
        self.window.ed_name.setParent(self.form_container_widget)
        self.window.lb_name_error.setParent(self.form_container_widget)
        self.name_section.addWidget(self.window.label_2)
        self.name_section.addWidget(self.window.ed_name)
        self.name_section.addWidget(self.window.lb_name_error)
        self.form_container_layout.addLayout(self.name_section)

        # 3. Details Section (Cedula, Club, Dorsal, Categoria)
        self.details_row = QtWidgets.QHBoxLayout()
        self.details_row.setSpacing(20)

        # Cedula
        self.cedula_vbox = QtWidgets.QVBoxLayout()
        self.window.label_8.setParent(self.form_container_widget)
        self.window.ed_nit.setParent(self.form_container_widget)
        self.window.lb_nit_error.setParent(self.form_container_widget)
        self.cedula_vbox.addWidget(self.window.label_8)
        self.cedula_vbox.addWidget(self.window.ed_nit)
        self.cedula_vbox.addWidget(self.window.lb_nit_error)
        self.details_row.addLayout(self.cedula_vbox)

        # Club
        self.club_vbox = QtWidgets.QVBoxLayout()
        self.window.label_5.setParent(self.form_container_widget)
        self.window.ed_club.setParent(self.form_container_widget)
        self.window.lb_club_error.setParent(self.form_container_widget)
        self.club_vbox.addWidget(self.window.label_5)
        self.club_vbox.addWidget(self.window.ed_club)
        self.club_vbox.addWidget(self.window.lb_club_error)
        self.details_row.addLayout(self.club_vbox)

        # Dorsal
        self.dorsal_vbox = QtWidgets.QVBoxLayout()
        self.window.label_11.setParent(self.form_container_widget)
        self.window.ed_dorsal.setParent(self.form_container_widget)
        self.window.lb_dorsal_error.setParent(self.form_container_widget)
        self.dorsal_vbox.addWidget(self.window.label_11)
        self.dorsal_vbox.addWidget(self.window.ed_dorsal)
        self.dorsal_vbox.addWidget(self.window.lb_dorsal_error)
        self.details_row.addLayout(self.dorsal_vbox)

        # Categoria
        self.cat_vbox = QtWidgets.QVBoxLayout()
        self.window.label_6.setParent(self.form_container_widget)
        self.window.cb_categories.setParent(self.form_container_widget)
        self.cat_vbox.addWidget(self.window.label_6)
        self.cat_vbox.addWidget(self.window.cb_categories)
        self.cat_vbox.addStretch()
        self.details_row.addLayout(self.cat_vbox)

        self.form_container_layout.addLayout(self.details_row)

        # 4. Agregar Button (Centered within form area)
        self.btn_add_layout = QtWidgets.QHBoxLayout()
        self.window.btn_add_atlete.setParent(self.form_container_widget)
        self.window.btn_add_atlete.setMinimumSize(QtCore.QSize(181, 41))
        self.btn_add_layout.addStretch()
        self.btn_add_layout.addWidget(self.window.btn_add_atlete)
        self.btn_add_layout.addStretch()
        self.form_container_layout.addLayout(self.btn_add_layout)

        # 5. Search and Filter Area
        self.search_area = QtWidgets.QHBoxLayout()
        
        # Left: Consultar and Pagination
        self.search_left = QtWidgets.QVBoxLayout()
        self.window.btn_get_all_athletes.setParent(self.form_container_widget)
        self.window.btn_get_all_athletes.setMinimumSize(QtCore.QSize(121, 41))
        self.search_left.addWidget(self.window.btn_get_all_athletes)
        
        self.pagination_layout = QtWidgets.QHBoxLayout()
        self.window.lb_pagination.setParent(self.form_container_widget)
        self.window.cb_pagination.setParent(self.form_container_widget)
        self.pagination_layout.addWidget(self.window.lb_pagination)
        self.pagination_layout.addWidget(self.window.cb_pagination)
        self.pagination_layout.addStretch()
        self.search_left.addLayout(self.pagination_layout)
        self.search_area.addLayout(self.search_left)

        self.search_area.addStretch()

        # Right: Filtrar
        self.search_right = QtWidgets.QVBoxLayout()
        self.search_right.setSpacing(2)
        self.window.label_7.setParent(self.form_container_widget)
        self.window.ed_filter.setParent(self.form_container_widget)
        self.window.label_9.setParent(self.form_container_widget)
        self.window.label_10.setParent(self.form_container_widget)
        self.search_right.addWidget(self.window.label_7)
        self.search_right.addWidget(self.window.ed_filter)
        self.search_right.addWidget(self.window.label_9)
        self.search_right.addWidget(self.window.label_10)
        self.search_area.addLayout(self.search_right)
        
        self.form_container_layout.addLayout(self.search_area)

        # Finalize and center the form container
        self.centering_layout.addStretch()
        self.centering_layout.addWidget(self.form_container_widget)
        self.centering_layout.addStretch()
        self.main_layout.addLayout(self.centering_layout)

        # 6. Table Section (Full width below form)
        self.window.athletes_table.setParent(self.centralwidget)
        header = self.window.athletes_table.horizontalHeader()
        # Set Nombres to stretch and others to interactive for a balanced, adjustable layout
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        for col in range(1, 7):
            header.setSectionResizeMode(col, QtWidgets.QHeaderView.Interactive)
            self.window.athletes_table.setColumnWidth(col, 120)
        
        # Increase width for Club column
        self.window.athletes_table.setColumnWidth(2, 150)
        self.main_layout.addWidget(self.window.athletes_table)

        # 7. Footer
        self.footer_layout = QtWidgets.QVBoxLayout()
        self.window.lb_general_error.setParent(self.centralwidget)
        self.window.lb_error_delete.setParent(self.centralwidget)
        self.footer_layout.addWidget(self.window.lb_general_error)
        self.footer_layout.addWidget(self.window.lb_error_delete)
        self.main_layout.addLayout(self.footer_layout)

        self.scroll_area.setWidget(self.centralwidget)
        self.window.setCentralWidget(self.scroll_area)

    def handle_pagination(self):
        index = self.window.cb_pagination.currentIndex()
        if index >= 0:
            current_page = index + 1
            self.pagination_helper.set_config({"current_page": current_page})
            self.filter_athletes()

    def initialize_pagination(self):
        self.pagination_helper.set_cb_pagination(
            ui_element=self.window.cb_pagination,
            handle_cb_pagination_method=self.handle_pagination,
        )
        self.pagination_helper.set_lb_pagination(ui_element=self.window.lb_pagination)
        self.pagination_helper.hide_ui_elements()
        self.pagination_helper.set_config(config={"order_by": "full_name"})

    def create_athlete(self):
        """ Creates a new athlete with all fields """
        try:
            full_name = allow_only_unicode_chars(get_edit_box_value(self.window.ed_name))
            club = allow_only_unicode_chars(get_edit_box_value(self.window.ed_club))
            nit = allow_only_unicode_chars(get_edit_box_value(self.window.ed_nit))
            dorsal = allow_only_unicode_chars(get_edit_box_value(self.window.ed_dorsal, return_none=True))
            errors = validate_data(
                full_name=full_name,
                club=club,
                nit=nit,
                dorsal=dorsal
            )
            if errors:
                self.show_errors(errors)
            else:
                # if there are not error, the athlete is create
                index_category = self.window.cb_categories.currentIndex()
                category_id = self.category_id_create[index_category]
                athlete = Athlete(
                    full_name=full_name,
                    club=club,
                    category_id=category_id,
                    nit=nit,
                    dorsal=dorsal
                )
                db.session.add(athlete)
                db.session.commit()
                self.clear_fields()
                self.clear_fields_errors()
        except Exception as e:
            print(e)

    def filter_athletes(self):
        text = allow_only_unicode_chars(get_edit_box_value(self.window.ed_filter))
        if text and len(text) >= 2:
            self.get_all_athletes(filter_text=text)
            self.clear_fields_errors()
        else:
            self.get_all_athletes()

    def on_key_search_athlete(self, e):
        """
        Verifies the key pressed in ed field to filter athletes
        :param e: event object
        """
        if e.key() == QtCore.Qt.Key_Return or e.key() == QtCore.Qt.Key_Enter:
            self.pagination_helper.set_config({"current_page": 1})
            self.filter_athletes()
        else:
            QLineEdit.keyPressEvent(self.window.ed_filter, e)

    def get_all_athletes(self, filter_text=None):
        """ loads in a table the existing/filtered athletes """
        try:
            self.clear_table()
            if filter_text:
                athletes_query = db.session.query(Athlete).join(Category, Category.id == Athlete.category_id).filter(
                    or_(
                        Athlete.full_name.ilike(f'%{filter_text}%'),
                        Athlete.club.ilike(f'%{filter_text}%'),
                        Category.name.ilike(f'%{filter_text}%'),
                        Athlete.dorsal.ilike(f'{filter_text}%'),
                        Athlete.nit.like(f'%{filter_text}%'),
                    )
                )
            else:
                self.window.ed_filter.setText('')
                athletes_query = db.session.query(Athlete)

            athletes = self.pagination_helper.get_page_result(query=athletes_query)
            categories = db.session.query(Category).order_by('name').all()
            if athletes:
                self.window.lb_error_delete.setText('')
                for i, athlete in enumerate(athletes):
                    self.window.athletes_table.insertRow(i)
                    name = QtWidgets.QTableWidgetItem(athlete.full_name)
                    self.window.athletes_table.setItem(i, 0, name)
                    nit = QtWidgets.QTableWidgetItem(athlete.nit)
                    self.window.athletes_table.setItem(i, 1, nit)
                    club = QtWidgets.QTableWidgetItem(athlete.club)
                    self.window.athletes_table.setItem(i, 2, club)
                    dorsal = QtWidgets.QTableWidgetItem(athlete.dorsal)
                    self.window.athletes_table.setItem(i, 3, dorsal)
                    """ creates a comboBox for categories, set as default the current one of the athlete """
                    cb_categories = QtWidgets.QComboBox()
                    for j, category in enumerate(categories):
                        cb_categories.addItem(category.name)
                        self.category_id_modify[j] = category.id
                        if category.id == athlete.category_id:
                            cb_categories.setCurrentIndex(j)
                    cb_categories.setStyleSheet(ButtonStyleSheet.BUTTON_SUCCESS)
                    self.window.athletes_table.setCellWidget(i, 4, cb_categories)
                    modify = QtWidgets.QPushButton()
                    modify.setText('Modificar')
                    modify.setProperty('id', athlete.id)
                    modify.setProperty('operation', 'modify')
                    modify.clicked.connect(self.handle_athletes_table)
                    modify.setStyleSheet(ButtonStyleSheet.BUTTON_SUCCESS)
                    self.window.athletes_table.setCellWidget(i, 5, modify)
                    delete = QtWidgets.QPushButton()

                    delete.setText('Eliminar')
                    delete.setProperty('id', athlete.id)
                    delete.setProperty('operation', 'delete')
                    delete.clicked.connect(self.handle_athletes_table)
                    delete.setStyleSheet(ButtonStyleSheet.BUTTON_ERROR)
                    self.window.athletes_table.setCellWidget(i, 6, delete)

            while True:
                row_count = self.window.athletes_table.rowCount()
                if row_count <= len(athletes):
                    break
                else:
                    self.window.athletes_table.removeRow(row_count - 1)

        except Exception as e:
            print(e)
            print('Could not load all the athletes: Error detail: {}'.format(e))

    def handle_athletes_table(self):
        """ handles the clicks over the buttons modify and delete on the table for athletes """
        index_row = self.window.athletes_table.currentRow()
        index_column = self.window.athletes_table.currentColumn()
        if index_row >= 0 and index_column >= 0:
            athlete_id = int(self.window.athletes_table.cellWidget(index_row, index_column).property('id'))
            athlete = db.session.query(Athlete).filter_by(id=athlete_id).first()
            operation = self.window.athletes_table.cellWidget(index_row, index_column).property('operation')
            try:
                if operation == 'modify' and athlete:
                    full_name = allow_only_unicode_chars(get_edit_box_value(self.window.athletes_table.item(index_row, 0)))
                    nit = allow_only_unicode_chars(get_edit_box_value(self.window.athletes_table.item(index_row, 1)))
                    club = allow_only_unicode_chars(get_edit_box_value(self.window.athletes_table.item(index_row, 2)))
                    dorsal = allow_only_unicode_chars(get_edit_box_value(self.window.athletes_table.item(index_row, 3)))
                    index_category = self.window.athletes_table.cellWidget(index_row, 4).currentIndex()
                    category_id = self.category_id_create[index_category]
                    errors = validate_data(
                        full_name=full_name,
                        club=club,
                        nit=nit,
                        dorsal=dorsal,
                        athlete_id=athlete_id,
                    )
                    if errors:
                        self.show_errors(errors)
                        return

                    if full_name:
                        athlete.full_name = full_name

                    if club:
                        athlete.club = club

                    if category_id:
                        athlete.category_id = int(category_id)

                    if nit:
                        athlete.nit = nit

                    if dorsal:
                        athlete.dorsal = dorsal

                    db.session.add(athlete)
                    db.session.commit()

                    self.clear_fields_errors()
                    filter_text = get_edit_box_value(self.window.ed_filter)
                    self.get_all_athletes(filter_text=filter_text)

                elif operation == 'delete' and athlete:
                    # checks if the athlete is assign to a group_athlete, that is the same as competition
                    group_athlete = db.session.query(GroupAthlete).filter_by(athlete_id=athlete.id).first()
                    if group_athlete:
                        db.session.delete(group_athlete)

                    db.session.delete(athlete)
                    db.session.commit()

                    self.clear_fields_errors()
                    filter_text = get_edit_box_value(self.window.ed_filter)
                    self.get_all_athletes(filter_text=filter_text)
            except Exception as e:
                print(e)

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

    def show_errors(self, errors):
        """ shows the errors gotten from the validations """
        if 'full_name' in errors:
            self.window.lb_name_error.setText(errors['full_name'])
        else:
            self.window.lb_name_error.setText('')
        if 'club' in errors:
            self.window.lb_club_error.setText(errors['club'])
        else:
            self.window.lb_club_error.setText('')
        if 'nit' in errors:
            self.window.lb_nit_error.setText(errors['nit'])
        else:
            self.window.lb_nit_error.setText('')
        if 'dorsal' in errors:
            self.window.lb_dorsal_error.setText(errors['dorsal'])
        else:
            self.window.lb_dorsal_error.setText('')
        if 'general_error' in errors:
            self.window.lb_general_error.setText(errors['general_error'])
        else:
            self.window.lb_general_error.setText('')

    def clear_fields(self):
        """ clear all editText fields for the user """
        self.window.ed_name.setText('')
        self.window.ed_club.setText('')
        self.window.ed_nit.setText('')
        self.window.ed_dorsal.setText('')

    def clear_fields_errors(self):
        """ clear all the label fields where errors are show """
        self.window.lb_name_error.setText('')
        self.window.lb_club_error.setText('')
        self.window.lb_nit_error.setText('')
        self.window.lb_dorsal_error.setText('')
        self.window.lb_general_error.setText('')

    def clear_table(self):
        for i in range(self.window.athletes_table.rowCount()):
            self.window.athletes_table.removeRow(i)

    def set_style_sheet(self):
        self.window.lb_title.setStyleSheet(ButtonStyleSheet.BUTTON_SUCCESS)
        self.window.btn_get_all_athletes.setStyleSheet(ButtonStyleSheet.BUTTON_SUCCESS)
        self.window.btn_add_atlete.setStyleSheet(ButtonStyleSheet.BUTTON_SUCCESS)
        self.window.cb_categories.setStyleSheet(ButtonStyleSheet.BUTTON_SUCCESS)
        ButtonStyleSheet.set_window_icon(self.window)


def validate_data(full_name, club, nit, dorsal, athlete_id=None):
    """ validate each field for an athlete """
    errors = {}
    # validations for field 'name'
    field = 'full_name'
    validate_min(field, full_name, 3, errors)
    validate_max(field, full_name, 100, errors)

    # validations for field 'club'
    field = 'club'
    validate_min(field, club, 2, errors)
    validate_max(field, club, 20, errors)

    # validations for field 'nit'
    field = 'nit'
    validate_min(field, nit, 5, errors)
    validate_max(field, nit, 20, errors)
    validate_int(field, nit, errors)
    try:
        athlete_query = db.session.query(Athlete).filter_by(nit=nit)
        nit_error_label = 'nit'
        nit_error_message = 'Ya existe esta cedula'
        if athlete_id:
            athlete_query = athlete_query.filter(Athlete.id != athlete_id)
            nit_error_label = 'general_error'
            nit_error_message = f'La cedula {nit} ya se encuentra en uso'

        athlete = athlete_query.first()
        if athlete:
            errors[nit_error_label] = nit_error_message

        if dorsal:
            dorsal_error_label = 'dorsal'
            dorsal_error_message = 'Esta dorsal ya esta en uso'
            dorsal_query = db.session.query(Athlete).filter_by(dorsal=dorsal)
            if athlete_id:
                dorsal_query = dorsal_query.filter(Athlete.id != athlete_id)
                dorsal_error_label = 'general_error'
                dorsal_error_message = f'La dorsal {dorsal} ya se encuentra en uso'

            dorsal = dorsal_query.first()
            if dorsal:
                errors[dorsal_error_label] = dorsal_error_message
    except Exception as e:
        print('Error validando cedula')
        print(e)

    return errors


