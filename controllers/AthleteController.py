from app import AthletesWindow
from engine import db
from models.Athlete import Athlete
from models.Category import Category
from utils.Validations import *
import traceback


class AthletesController:
    def __init__(self, window:AthletesWindow, *args, **kwargs):
        self.window = window
        self.window.btn_add_atlete.clicked.connect(self.create_athlete)
        self.window.btn_add_atlete.clicked.connect(self.get_all_athletes)
        self.category_id_create = {}
        self.load_categories()

    def create_athlete(self):
        try:
            name = self.window.ed_name.text()
            last_name = self.window.ed_lastname.text()
            age = self.window.ed_age.text()
            club = self.window.ed_club.text()
            nit = self.window.ed_nit.text()
            errors = validate_data(name=name, last_name=last_name, age=age, club=club, nit=nit)
            if errors:
                self.show_errors(errors)
            else:
                # if there is not error, the athlete is create
                index_category = self.window.cb_categories.currentIndex()
                category_id = self.category_id_create[index_category]
                athlete = Athlete(name=name, last_name=last_name, age=int(age), club=club, category_id=category_id,
                                  nit=nit)
                db.session.add(athlete)
                db.session.commit()
                self.clear_fields()
                self.clear_fields_errors()
        except Exception as e:
            traceback.print_exc()

    def get_all_athletes(self):
        pass

    def load_categories(self):
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
            traceback.print_exc()

    def show_errors(self, errors):
        if 'name' in errors:
            self.window.lb_name_error.setText(errors['name'])
        else:
            self.window.lb_name_error.setText('')
        if 'last_name' in errors:
            self.window.lb_lastname_error.setText(errors['last_name'])
        else:
            self.window.lb_lastname_error.setText('')
        if 'age' in errors:
            self.window.lb_age_error.setText(errors['age'])
        else:
            self.window.lb_age_error.setText('')
        if 'club' in errors:
            self.window.lb_club_error.setText(errors['club'])
        else:
            self.window.lb_club_error.setText('')
        if 'nit' in errors:
            self.window.lb_nit_error.setText(errors['nit'])
        else:
            self.window.lb_nit_error.setText('')

    def clear_fields(self):
        self.window.ed_name.setText('')
        self.window.ed_lastname.setText('')
        self.window.ed_age.setText('')
        self.window.ed_club.setText('')
        self.window.ed_nit.setText('')

    def clear_fields_errors(self):
        self.window.lb_name_error.setText('')
        self.window.lb_lastname_error.setText('')
        self.window.lb_age_error.setText('')
        self.window.lb_club_error.setText('')
        self.window.lb_nit_error.setText('')


def validate_data(name, last_name, age, club, nit):
    errors = {}
    # validations for field 'name'
    field = 'name'
    validate_min(field, name, 3, errors)
    validate_max(field, name, 40, errors)

    # validations for field 'last_name'
    field = 'last_name'
    validate_min(field, last_name, 3, errors)
    validate_max(field, last_name, 40, errors)

    # validations for field 'club'
    field = 'club'
    validate_min(field, club, 2, errors)
    validate_max(field, club, 20, errors)

    # validations for field 'age'
    field = 'age'
    validate_exists(field, age, errors)
    validate_int(field, age, errors)

    # validations for field 'nit'
    field = 'nit'
    validate_min(field, nit, 5, errors)
    validate_max(field, nit, 20, errors)
    validate_int(field, nit, errors)
    try:
        athlete = db.session.query(Athlete).filter_by(nit=nit).first()
        if athlete:
            errors['nit'] = 'Ya existe esta cedula'
    except Exception as e:
        print('Error validando cedula' + e)

    return errors
