# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'athletesView.ui'
#
# Created by: PyQt5 UI code generator 5.15.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_AthletesView(object):
    def setupUi(self, AthletesView):
        AthletesView.setObjectName("AthletesView")
        AthletesView.resize(1088, 764)
        self.lb_title = QtWidgets.QLabel(AthletesView)
        self.lb_title.setGeometry(QtCore.QRect(10, 30, 1071, 41))
        font = QtGui.QFont()
        font.setFamily("MS Sans Serif")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.lb_title.setFont(font)
        self.lb_title.setAlignment(QtCore.Qt.AlignCenter)
        self.lb_title.setObjectName("lb_title")
        self.label_2 = QtWidgets.QLabel(AthletesView)
        self.label_2.setGeometry(QtCore.QRect(200, 80, 161, 41))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.label_5 = QtWidgets.QLabel(AthletesView)
        self.label_5.setGeometry(QtCore.QRect(370, 170, 101, 41))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_5.setFont(font)
        self.label_5.setObjectName("label_5")
        self.label_6 = QtWidgets.QLabel(AthletesView)
        self.label_6.setGeometry(QtCore.QRect(750, 180, 101, 41))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_6.setFont(font)
        self.label_6.setObjectName("label_6")
        self.cb_categories = QtWidgets.QComboBox(AthletesView)
        self.cb_categories.setGeometry(QtCore.QRect(740, 220, 211, 31))
        self.cb_categories.setObjectName("cb_categories")
        self.ed_name = QtWidgets.QLineEdit(AthletesView)
        self.ed_name.setGeometry(QtCore.QRect(190, 120, 771, 41))
        self.ed_name.setObjectName("ed_name")
        self.ed_club = QtWidgets.QLineEdit(AthletesView)
        self.ed_club.setGeometry(QtCore.QRect(360, 210, 201, 41))
        self.ed_club.setObjectName("ed_club")
        self.btn_get_all_athletes = QtWidgets.QPushButton(AthletesView)
        self.btn_get_all_athletes.setGeometry(QtCore.QRect(130, 337, 121, 41))
        self.btn_get_all_athletes.setObjectName("btn_get_all_athletes")
        self.btn_add_atlete = QtWidgets.QPushButton(AthletesView)
        self.btn_add_atlete.setGeometry(QtCore.QRect(470, 280, 181, 41))
        self.btn_add_atlete.setObjectName("btn_add_atlete")
        self.ed_filter = QtWidgets.QLineEdit(AthletesView)
        self.ed_filter.setGeometry(QtCore.QRect(710, 330, 191, 41))
        self.ed_filter.setObjectName("ed_filter")
        self.label_7 = QtWidgets.QLabel(AthletesView)
        self.label_7.setGeometry(QtCore.QRect(770, 300, 91, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_7.setFont(font)
        self.label_7.setObjectName("label_7")
        self.athletes_table = QtWidgets.QTableWidget(AthletesView)
        self.athletes_table.setGeometry(QtCore.QRect(70, 410, 951, 291))
        self.athletes_table.setObjectName("athletes_table")
        self.athletes_table.setColumnCount(7)
        self.athletes_table.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.athletes_table.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.athletes_table.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.athletes_table.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.athletes_table.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.athletes_table.setHorizontalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        self.athletes_table.setHorizontalHeaderItem(5, item)
        item = QtWidgets.QTableWidgetItem()
        self.athletes_table.setHorizontalHeaderItem(6, item)
        self.lb_name_error = QtWidgets.QLabel(AthletesView)
        self.lb_name_error.setGeometry(QtCore.QRect(190, 160, 201, 20))
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(255, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(120, 120, 120))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)
        self.lb_name_error.setPalette(palette)
        self.lb_name_error.setText("")
        self.lb_name_error.setObjectName("lb_name_error")
        self.lb_lastname_error = QtWidgets.QLabel(AthletesView)
        self.lb_lastname_error.setGeometry(QtCore.QRect(460, 160, 201, 20))
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(255, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(120, 120, 120))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)
        self.lb_lastname_error.setPalette(palette)
        self.lb_lastname_error.setText("")
        self.lb_lastname_error.setObjectName("lb_lastname_error")
        self.lb_age_error = QtWidgets.QLabel(AthletesView)
        self.lb_age_error.setGeometry(QtCore.QRect(730, 160, 201, 20))
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(255, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(120, 120, 120))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)
        self.lb_age_error.setPalette(palette)
        self.lb_age_error.setText("")
        self.lb_age_error.setObjectName("lb_age_error")
        self.lb_club_error = QtWidgets.QLabel(AthletesView)
        self.lb_club_error.setGeometry(QtCore.QRect(360, 250, 201, 20))
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(255, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(120, 120, 120))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)
        self.lb_club_error.setPalette(palette)
        self.lb_club_error.setText("")
        self.lb_club_error.setObjectName("lb_club_error")
        self.ed_nit = QtWidgets.QLineEdit(AthletesView)
        self.ed_nit.setGeometry(QtCore.QRect(190, 210, 161, 41))
        self.ed_nit.setText("")
        self.ed_nit.setObjectName("ed_nit")
        self.lb_nit_error = QtWidgets.QLabel(AthletesView)
        self.lb_nit_error.setGeometry(QtCore.QRect(190, 250, 161, 20))
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(255, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(120, 120, 120))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)
        self.lb_nit_error.setPalette(palette)
        self.lb_nit_error.setText("")
        self.lb_nit_error.setObjectName("lb_nit_error")
        self.label_8 = QtWidgets.QLabel(AthletesView)
        self.label_8.setGeometry(QtCore.QRect(200, 170, 101, 41))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_8.setFont(font)
        self.label_8.setObjectName("label_8")
        self.label_9 = QtWidgets.QLabel(AthletesView)
        self.label_9.setGeometry(QtCore.QRect(720, 370, 191, 20))
        self.label_9.setObjectName("label_9")
        self.lb_error_delete = QtWidgets.QLabel(AthletesView)
        self.lb_error_delete.setGeometry(QtCore.QRect(70, 720, 951, 20))
        self.lb_error_delete.setStyleSheet("color:red;")
        self.lb_error_delete.setText("")
        self.lb_error_delete.setAlignment(QtCore.Qt.AlignCenter)
        self.lb_error_delete.setObjectName("lb_error_delete")
        self.label_10 = QtWidgets.QLabel(AthletesView)
        self.label_10.setGeometry(QtCore.QRect(690, 389, 261, 21))
        self.label_10.setObjectName("label_10")
        self.ed_dorsal = QtWidgets.QLineEdit(AthletesView)
        self.ed_dorsal.setGeometry(QtCore.QRect(570, 210, 161, 41))
        self.ed_dorsal.setObjectName("ed_dorsal")
        self.label_11 = QtWidgets.QLabel(AthletesView)
        self.label_11.setGeometry(QtCore.QRect(580, 170, 101, 41))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_11.setFont(font)
        self.label_11.setObjectName("label_11")
        self.lb_dorsal_error = QtWidgets.QLabel(AthletesView)
        self.lb_dorsal_error.setGeometry(QtCore.QRect(570, 250, 161, 20))
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(255, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(120, 120, 120))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)
        self.lb_dorsal_error.setPalette(palette)
        self.lb_dorsal_error.setText("")
        self.lb_dorsal_error.setObjectName("lb_dorsal_error")
        self.lb_general_error = QtWidgets.QLabel(AthletesView)
        self.lb_general_error.setGeometry(QtCore.QRect(70, 700, 951, 20))
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(255, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(120, 120, 120))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)
        self.lb_general_error.setPalette(palette)
        self.lb_general_error.setText("")
        self.lb_general_error.setAlignment(QtCore.Qt.AlignCenter)
        self.lb_general_error.setObjectName("lb_general_error")

        self.retranslateUi(AthletesView)
        QtCore.QMetaObject.connectSlotsByName(AthletesView)

    def retranslateUi(self, AthletesView):
        _translate = QtCore.QCoreApplication.translate
        AthletesView.setWindowTitle(_translate("AthletesView", "Dialog"))
        self.lb_title.setText(_translate("AthletesView", "CONFIGURAR ATLETAS"))
        self.label_2.setText(_translate("AthletesView", "Nombres y apellidos"))
        self.label_5.setText(_translate("AthletesView", "Club"))
        self.label_6.setText(_translate("AthletesView", "Categoria"))
        self.btn_get_all_athletes.setText(_translate("AthletesView", "Consultar"))
        self.btn_add_atlete.setText(_translate("AthletesView", "Agregar"))
        self.label_7.setText(_translate("AthletesView", "Filtrar"))
        item = self.athletes_table.horizontalHeaderItem(0)
        item.setText(_translate("AthletesView", "Nombres"))
        item = self.athletes_table.horizontalHeaderItem(1)
        item.setText(_translate("AthletesView", "Cedula"))
        item = self.athletes_table.horizontalHeaderItem(2)
        item.setText(_translate("AthletesView", "Club"))
        item = self.athletes_table.horizontalHeaderItem(3)
        item.setText(_translate("AthletesView", "Dorsal"))
        item = self.athletes_table.horizontalHeaderItem(4)
        item.setText(_translate("AthletesView", "Categoria"))
        item = self.athletes_table.horizontalHeaderItem(5)
        item.setText(_translate("AthletesView", "Modificar"))
        item = self.athletes_table.horizontalHeaderItem(6)
        item.setText(_translate("AthletesView", "Eliminar"))
        self.label_8.setText(_translate("AthletesView", "Cedula"))
        self.label_9.setText(_translate("AthletesView", "Requiere minimo 2 caracteres"))
        self.label_10.setText(_translate("AthletesView", "Busca por nombre, club, categoria y cedula"))
        self.label_11.setText(_translate("AthletesView", "Dorsal"))
