from app import MainWindow
from controllers.Categories import CategoryController
from app import CategoriesWindow


class MainController:
    def __init__(self, window: MainWindow, *args, **kwargs):
        self.window = window
        self.window.btn_open_categories.clicked.connect(self.open_category_window)
        self.category_window = None
        self.categories_controller = None

    def open_category_window(self):
        self.category_window = CategoriesWindow()
        self.categories_controller = CategoryController(self.category_window)
        self.category_window.show()

