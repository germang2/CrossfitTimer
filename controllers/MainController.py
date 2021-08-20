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

        self.set_style_sheet()

    def open_category_window(self):
        self.categories_controller = CategoryController(self.category_window)
        self.category_window.show()

    def open_athletes_window(self):
        self.athletes_controller = AthletesController(self.athletes_window)
        self.athletes_window.show()

    def open_competences_window(self):
        self.competences_controller = CompetenceController(self.competences_window)
        self.competences_window.show()

    def set_style_sheet(self):
        self.window.setFixedSize(self.window.geometry().width(), self.window.geometry().height())
        style_sheet = f"""
            border-image: url("resources/img/background.jpg");
        """
        self.window.background_image.setStyleSheet(style_sheet)
        button_style_sheet = """
            background-color: rgba(0,23,39,240);
            color: #f7f7f7;
        """
        self.window.btn_open_categories.setStyleSheet(button_style_sheet)
        self.window.btn_open_atletes.setStyleSheet(button_style_sheet)
        self.window.btn_open_competences.setStyleSheet(button_style_sheet)
        self.window.label.setStyleSheet(button_style_sheet)
