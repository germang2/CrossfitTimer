import math

from typing import (
    Callable,
    Optional,
)

from PyQt5.QtWidgets import (
    QComboBox,
    QLabel,
)

from utils.style_sheet import ButtonStyleSheet


class PaginationHelper:
    def __init__(self):
        self.cb_pagination: Optional[QComboBox] = None
        self.lb_pagination: Optional[QLabel] = None
        # default pagination limit
        self.limit = 30
        self.current_page = 1
        self.order_by = None
        self.total_results = 0
        self.total_pages = 0
        self.handle_cb_pagination_method = None

    def set_cb_pagination(
        self,
        ui_element: QComboBox,
        handle_cb_pagination_method: Callable,
    ):
        """
        Store the Qt Widget that contains the combo box for display the pages
        :param ui_element: QComboBox
        :param handle_cb_pagination_method: Callable method to connect with combo box and handle the event of index change
        """
        self.cb_pagination = ui_element
        self.handle_cb_pagination_method = handle_cb_pagination_method
        self.cb_pagination.setStyleSheet(ButtonStyleSheet.BUTTON_SUCCESS)
        self.cb_pagination.currentIndexChanged.connect(handle_cb_pagination_method)

    def set_lb_pagination(self, ui_element: QLabel):
        """
        Store the Qt Widget that contains the label for pagination
        :param ui_element: QLabel
        """
        self.lb_pagination = ui_element

    def set_config(self, config: dict):
        """
        Configure the pagination params
        :param config: dict, with pagination values to configure. Ie,
        {
          "limit": 25,
          "current_page": 2,
          "order_by": "name"
        }
        """
        for key, value in config.items():
            if hasattr(self, key):
                setattr(self, key, value)

    def hide_ui_elements(self):
        """
        hide the ui elements related to pagination
        """
        self.cb_pagination.hide()
        self.lb_pagination.hide()

    def update_ui_elements(self):
        """
        Updates the ui elements related to pagination with options and values
        """
        if self.total_results > self.limit:
            self.lb_pagination.setHidden(False)
            self.cb_pagination.setHidden(False)

            self.cb_pagination.clear()
            # disconnect event handler to avoid trigger event on index change
            self.cb_pagination.currentIndexChanged.disconnect()
            # total_pages + 1 to include the last page
            pagination_pages = list(range(1, self.total_pages + 1))
            pagination_pages = list(map(lambda x: str(x), pagination_pages))
            self.cb_pagination.addItems(pagination_pages)
            # index starts with zero
            self.cb_pagination.setCurrentIndex(self.current_page - 1)

            # re connects event handler to handle index change
            self.cb_pagination.currentIndexChanged.connect(self.handle_cb_pagination_method)
        else:
            self.hide_ui_elements()

    def get_page_result(self, query):
        """
        Receives an SQL Alchemy orm query and builds the pagination with it
        :param query: SQL Alchemy ORM instance
        :return: dict, with results and pagination data
        """
        offset_value = (self.current_page - 1) * self.limit
        self.total_results = query.count()
        self.total_pages = math.ceil(self.total_results / self.limit)

        self.update_ui_elements()

        query = (
            query.order_by(self.order_by)
            .offset(offset_value)
            .limit(self.limit)
        )
        return query.all()
