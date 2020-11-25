# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main_window.ui'
#
# Created by: PyQt5 UI code generator 5.15.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.tab_panel = QtWidgets.QTabWidget(self.centralwidget)
        self.tab_panel.setGeometry(QtCore.QRect(0, 10, 811, 621))
        font = QtGui.QFont()
        font.setFamily("Verdana")
        font.setPointSize(8)
        self.tab_panel.setFont(font)
        self.tab_panel.setTabShape(QtWidgets.QTabWidget.Triangular)
        self.tab_panel.setObjectName("tab_panel")
        self.tab_start = QtWidgets.QWidget()
        self.tab_start.setObjectName("tab_start")
        self.label = QtWidgets.QLabel(self.tab_start)
        self.label.setGeometry(QtCore.QRect(300, 20, 231, 61))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.tab_start)
        self.label_2.setGeometry(QtCore.QRect(170, 180, 501, 141))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.tab_panel.addTab(self.tab_start, "")
        self.categories = QtWidgets.QWidget()
        self.categories.setObjectName("categories")
        self.label_3 = QtWidgets.QLabel(self.categories)
        self.label_3.setGeometry(QtCore.QRect(300, 30, 191, 51))
        font = QtGui.QFont()
        font.setFamily("Verdana")
        font.setPointSize(15)
        font.setBold(True)
        font.setWeight(75)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.categories_table = QtWidgets.QTableWidget(self.categories)
        self.categories_table.setGeometry(QtCore.QRect(70, 210, 681, 241))
        self.categories_table.setObjectName("categories_table")
        self.categories_table.setColumnCount(3)
        self.categories_table.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.categories_table.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.categories_table.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.categories_table.setHorizontalHeaderItem(2, item)
        self.ed_category = QtWidgets.QLineEdit(self.categories)
        self.ed_category.setGeometry(QtCore.QRect(250, 120, 301, 41))
        self.ed_category.setObjectName("ed_category")
        self.btn_create_category = QtWidgets.QPushButton(self.categories)
        self.btn_create_category.setGeometry(QtCore.QRect(290, 170, 211, 28))
        self.btn_create_category.setObjectName("btn_create_category")
        self.btn_get_all_categories = QtWidgets.QPushButton(self.categories)
        self.btn_get_all_categories.setGeometry(QtCore.QRect(90, 170, 161, 28))
        self.btn_get_all_categories.setObjectName("btn_get_all_categories")
        self.tab_panel.addTab(self.categories, "")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.tab_panel.setCurrentIndex(1)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "CROSSFIT TIMER"))
        self.label_2.setText(_translate("MainWindow", "Programa y toma el tiempo de tus competiciones"))
        self.tab_panel.setTabText(self.tab_panel.indexOf(self.tab_start), _translate("MainWindow", "Inicio"))
        self.label_3.setText(_translate("MainWindow", "CATEGORIAS"))
        item = self.categories_table.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "Nombre"))
        item = self.categories_table.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "Modificar"))
        item = self.categories_table.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "Eliminar"))
        self.btn_create_category.setText(_translate("MainWindow", "Agregar"))
        self.btn_get_all_categories.setText(_translate("MainWindow", "Consultar"))
        self.tab_panel.setTabText(self.tab_panel.indexOf(self.categories), _translate("MainWindow", "Categorias"))
