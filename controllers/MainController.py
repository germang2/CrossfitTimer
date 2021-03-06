from app import MainWindow
from app import CategoriesWindow, AthletesWindow, CompetencesWindow
from controllers.AthleteController import AthletesController
from controllers.CategoriesController import CategoryController
from controllers.CompetenceController import CompetenceController


class MainController:
    def __init__(self, window: MainWindow, *args, **kwargs):
        self.window = window
        # categories handler
        self.window.btn_open_categories.clicked.connect(self.open_category_window)
        self.category_window = CategoriesWindow()
        self.categories_controller = None

        # athletes handler
        self.window.btn_open_atletes.clicked.connect(self.open_athletes_window)
        self.athletes_window = AthletesWindow()
        self.athletes_controller = None

        # competences handler
        self.window.btn_open_competences.clicked.connect(self.open_competences_window)
        self.competences_window = CompetencesWindow()
        self.competences_controller = None

    def open_category_window(self):
        self.categories_controller = CategoryController(self.category_window)
        self.category_window.show()

    def open_athletes_window(self):
        self.athletes_controller = AthletesController(self.athletes_window)
        self.athletes_window.show()

    def open_competences_window(self):
        self.competences_controller = CompetenceController(self.competences_window)
        self.competences_window.show()
