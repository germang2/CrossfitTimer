# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'categoriesView.ui'
#
# Created by: PyQt5 UI code generator 5.15.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_CategoriesView(object):
    def setupUi(self, CategoriesView):
        CategoriesView.setObjectName("CategoriesView")
        CategoriesView.resize(803, 619)
        self.btn_create_category = QtWidgets.QPushButton(CategoriesView)
        self.btn_create_category.setGeometry(QtCore.QRect(610, 200, 121, 28))
        self.btn_create_category.setObjectName("btn_create_category")
        self.categories_table = QtWidgets.QTableWidget(CategoriesView)
        self.categories_table.setGeometry(QtCore.QRect(50, 250, 700, 331))
        self.categories_table.setObjectName("categories_table")
        self.categories_table.setColumnCount(3)
        self.categories_table.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.categories_table.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.categories_table.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.categories_table.setHorizontalHeaderItem(2, item)
        self.btn_get_all_categories = QtWidgets.QPushButton(CategoriesView)
        self.btn_get_all_categories.setGeometry(QtCore.QRect(80, 200, 161, 28))
        self.btn_get_all_categories.setObjectName("btn_get_all_categories")
        self.ed_category = QtWidgets.QLineEdit(CategoriesView)
        self.ed_category.setGeometry(QtCore.QRect(370, 190, 231, 41))
        self.ed_category.setObjectName("ed_category")
        self.lb_title = QtWidgets.QLabel(CategoriesView)
        self.lb_title.setGeometry(QtCore.QRect(0, 60, 801, 51))
        font = QtGui.QFont()
        font.setFamily("Verdana")
        font.setPointSize(15)
        font.setBold(True)
        font.setWeight(75)
        self.lb_title.setFont(font)
        self.lb_title.setAlignment(QtCore.Qt.AlignCenter)
        self.lb_title.setObjectName("lb_title")
        self.lb_error_delete = QtWidgets.QLabel(CategoriesView)
        self.lb_error_delete.setGeometry(QtCore.QRect(50, 490, 701, 20))
        self.lb_error_delete.setStyleSheet("color:red;")
        self.lb_error_delete.setText("")
        self.lb_error_delete.setAlignment(QtCore.Qt.AlignCenter)
        self.lb_error_delete.setObjectName("lb_error_delete")

        self.retranslateUi(CategoriesView)
        QtCore.QMetaObject.connectSlotsByName(CategoriesView)

    def retranslateUi(self, CategoriesView):
        _translate = QtCore.QCoreApplication.translate
        CategoriesView.setWindowTitle(_translate("CategoriesView", "Dialog"))
        self.btn_create_category.setText(_translate("CategoriesView", "Agregar"))
        item = self.categories_table.horizontalHeaderItem(0)
        item.setText(_translate("CategoriesView", "Nombre"))
        item = self.categories_table.horizontalHeaderItem(1)
        item.setText(_translate("CategoriesView", "Modificar"))
        item = self.categories_table.horizontalHeaderItem(2)
        item.setText(_translate("CategoriesView", "Eliminar"))
        self.btn_get_all_categories.setText(_translate("CategoriesView", "Consultar"))
        self.lb_title.setText(_translate("CategoriesView", "CATEGORIAS"))
