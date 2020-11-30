# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'competenciasView.ui'
#
# Created by: PyQt5 UI code generator 5.15.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_CompetencesView(object):
    def setupUi(self, CompetencesView):
        CompetencesView.setObjectName("CompetencesView")
        CompetencesView.resize(1516, 814)
        self.label = QtWidgets.QLabel(CompetencesView)
        self.label.setGeometry(QtCore.QRect(420, 20, 311, 41))
        font = QtGui.QFont()
        font.setFamily("MS Sans Serif")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(CompetencesView)
        self.label_2.setGeometry(QtCore.QRect(310, 120, 81, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(CompetencesView)
        self.label_3.setGeometry(QtCore.QRect(670, 120, 81, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.ed_name = QtWidgets.QLineEdit(CompetencesView)
        self.ed_name.setGeometry(QtCore.QRect(250, 160, 191, 31))
        self.ed_name.setObjectName("ed_name")
        self.ed_place = QtWidgets.QLineEdit(CompetencesView)
        self.ed_place.setGeometry(QtCore.QRect(600, 160, 191, 31))
        self.ed_place.setObjectName("ed_place")
        self.lb_name_error = QtWidgets.QLabel(CompetencesView)
        self.lb_name_error.setGeometry(QtCore.QRect(250, 190, 191, 20))
        self.lb_name_error.setStyleSheet("color:rgb(255, 0, 0)")
        self.lb_name_error.setText("")
        self.lb_name_error.setAlignment(QtCore.Qt.AlignCenter)
        self.lb_name_error.setObjectName("lb_name_error")
        self.lb_place_error = QtWidgets.QLabel(CompetencesView)
        self.lb_place_error.setGeometry(QtCore.QRect(600, 190, 191, 20))
        self.lb_place_error.setStyleSheet("color:rgb(255, 0, 0)")
        self.lb_place_error.setText("")
        self.lb_place_error.setAlignment(QtCore.Qt.AlignCenter)
        self.lb_place_error.setObjectName("lb_place_error")
        self.ed_date = QtWidgets.QLineEdit(CompetencesView)
        self.ed_date.setGeometry(QtCore.QRect(250, 250, 191, 31))
        self.ed_date.setObjectName("ed_date")
        self.lb_date_error = QtWidgets.QLabel(CompetencesView)
        self.lb_date_error.setGeometry(QtCore.QRect(180, 280, 351, 20))
        self.lb_date_error.setStyleSheet("color:rgb(255, 0, 0)")
        self.lb_date_error.setText("")
        self.lb_date_error.setAlignment(QtCore.Qt.AlignCenter)
        self.lb_date_error.setObjectName("lb_date_error")
        self.label_4 = QtWidgets.QLabel(CompetencesView)
        self.label_4.setGeometry(QtCore.QRect(320, 210, 81, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.label_5 = QtWidgets.QLabel(CompetencesView)
        self.label_5.setGeometry(QtCore.QRect(670, 210, 81, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_5.setFont(font)
        self.label_5.setObjectName("label_5")
        self.ed_time = QtWidgets.QLineEdit(CompetencesView)
        self.ed_time.setGeometry(QtCore.QRect(600, 250, 191, 31))
        self.ed_time.setObjectName("ed_time")
        self.lb_time_error = QtWidgets.QLabel(CompetencesView)
        self.lb_time_error.setGeometry(QtCore.QRect(600, 280, 191, 20))
        self.lb_time_error.setStyleSheet("color:rgb(255, 0, 0)")
        self.lb_time_error.setText("")
        self.lb_time_error.setAlignment(QtCore.Qt.AlignCenter)
        self.lb_time_error.setObjectName("lb_time_error")
        self.label_6 = QtWidgets.QLabel(CompetencesView)
        self.label_6.setGeometry(QtCore.QRect(250, 300, 191, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_6.setFont(font)
        self.label_6.setAlignment(QtCore.Qt.AlignCenter)
        self.label_6.setObjectName("label_6")
        self.ed_reward = QtWidgets.QLineEdit(CompetencesView)
        self.ed_reward.setGeometry(QtCore.QRect(250, 340, 191, 31))
        self.ed_reward.setObjectName("ed_reward")
        self.lb_reward_error = QtWidgets.QLabel(CompetencesView)
        self.lb_reward_error.setGeometry(QtCore.QRect(250, 370, 191, 20))
        self.lb_reward_error.setStyleSheet("color:rgb(255, 0, 0)")
        self.lb_reward_error.setText("")
        self.lb_reward_error.setAlignment(QtCore.Qt.AlignCenter)
        self.lb_reward_error.setObjectName("lb_reward_error")
        self.btn_create_competition = QtWidgets.QPushButton(CompetencesView)
        self.btn_create_competition.setGeometry(QtCore.QRect(430, 390, 231, 41))
        self.btn_create_competition.setObjectName("btn_create_competition")
        self.competences_table = QtWidgets.QTableWidget(CompetencesView)
        self.competences_table.setGeometry(QtCore.QRect(40, 480, 891, 281))
        self.competences_table.setObjectName("competences_table")
        self.competences_table.setColumnCount(8)
        self.competences_table.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.competences_table.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.competences_table.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.competences_table.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.competences_table.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.competences_table.setHorizontalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        self.competences_table.setHorizontalHeaderItem(5, item)
        item = QtWidgets.QTableWidgetItem()
        self.competences_table.setHorizontalHeaderItem(6, item)
        item = QtWidgets.QTableWidgetItem()
        self.competences_table.setHorizontalHeaderItem(7, item)
        self.btn_get_all_competitions = QtWidgets.QPushButton(CompetencesView)
        self.btn_get_all_competitions.setGeometry(QtCore.QRect(60, 430, 161, 41))
        self.btn_get_all_competitions.setObjectName("btn_get_all_competitions")
        self.label_7 = QtWidgets.QLabel(CompetencesView)
        self.label_7.setGeometry(QtCore.QRect(1070, 130, 311, 41))
        font = QtGui.QFont()
        font.setFamily("MS Sans Serif")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_7.setFont(font)
        self.label_7.setAlignment(QtCore.Qt.AlignCenter)
        self.label_7.setObjectName("label_7")
        self.lb_competence_selected = QtWidgets.QLabel(CompetencesView)
        self.lb_competence_selected.setGeometry(QtCore.QRect(1040, 190, 381, 41))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.lb_competence_selected.setFont(font)
        self.lb_competence_selected.setAlignment(QtCore.Qt.AlignCenter)
        self.lb_competence_selected.setObjectName("lb_competence_selected")
        self.label_8 = QtWidgets.QLabel(CompetencesView)
        self.label_8.setGeometry(QtCore.QRect(1130, 240, 81, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_8.setFont(font)
        self.label_8.setObjectName("label_8")
        self.lb_group_name_error = QtWidgets.QLabel(CompetencesView)
        self.lb_group_name_error.setGeometry(QtCore.QRect(1060, 310, 191, 20))
        self.lb_group_name_error.setStyleSheet("color:rgb(255, 0, 0)")
        self.lb_group_name_error.setText("")
        self.lb_group_name_error.setAlignment(QtCore.Qt.AlignCenter)
        self.lb_group_name_error.setObjectName("lb_group_name_error")
        self.ed_group_name = QtWidgets.QLineEdit(CompetencesView)
        self.ed_group_name.setGeometry(QtCore.QRect(1060, 280, 161, 31))
        self.ed_group_name.setObjectName("ed_group_name")
        self.ed_group_order = QtWidgets.QLineEdit(CompetencesView)
        self.ed_group_order.setGeometry(QtCore.QRect(1250, 280, 121, 31))
        self.ed_group_order.setObjectName("ed_group_order")
        self.lb_group_order_error = QtWidgets.QLabel(CompetencesView)
        self.lb_group_order_error.setGeometry(QtCore.QRect(1220, 310, 151, 20))
        self.lb_group_order_error.setStyleSheet("color:rgb(255, 0, 0)")
        self.lb_group_order_error.setText("")
        self.lb_group_order_error.setAlignment(QtCore.Qt.AlignCenter)
        self.lb_group_order_error.setObjectName("lb_group_order_error")
        self.label_9 = QtWidgets.QLabel(CompetencesView)
        self.label_9.setGeometry(QtCore.QRect(1280, 240, 81, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_9.setFont(font)
        self.label_9.setObjectName("label_9")
        self.groups_table = QtWidgets.QTableWidget(CompetencesView)
        self.groups_table.setGeometry(QtCore.QRect(990, 370, 481, 391))
        self.groups_table.setObjectName("groups_table")
        self.groups_table.setColumnCount(5)
        self.groups_table.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.groups_table.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.groups_table.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.groups_table.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.groups_table.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.groups_table.setHorizontalHeaderItem(4, item)
        self.btn_create_group = QtWidgets.QPushButton(CompetencesView)
        self.btn_create_group.setGeometry(QtCore.QRect(1390, 280, 101, 28))
        self.btn_create_group.setObjectName("btn_create_group")
        self.btn_see_all_groups = QtWidgets.QPushButton(CompetencesView)
        self.btn_see_all_groups.setGeometry(QtCore.QRect(1000, 330, 93, 28))
        self.btn_see_all_groups.setObjectName("btn_see_all_groups")
        self.lb_error_delete = QtWidgets.QLabel(CompetencesView)
        self.lb_error_delete.setGeometry(QtCore.QRect(40, 760, 891, 20))
        self.lb_error_delete.setStyleSheet("color:red;")
        self.lb_error_delete.setText("")
        self.lb_error_delete.setObjectName("lb_error_delete")

        self.retranslateUi(CompetencesView)
        QtCore.QMetaObject.connectSlotsByName(CompetencesView)

    def retranslateUi(self, CompetencesView):
        _translate = QtCore.QCoreApplication.translate
        CompetencesView.setWindowTitle(_translate("CompetencesView", "Dialog"))
        self.label.setText(_translate("CompetencesView", "CONFIGURAR COMPETENCIAS"))
        self.label_2.setText(_translate("CompetencesView", "Nombre"))
        self.label_3.setText(_translate("CompetencesView", "Lugar"))
        self.label_4.setText(_translate("CompetencesView", "Fecha"))
        self.label_5.setText(_translate("CompetencesView", "Hora"))
        self.label_6.setText(_translate("CompetencesView", "Recompensa"))
        self.btn_create_competition.setText(_translate("CompetencesView", "CREAR"))
        item = self.competences_table.horizontalHeaderItem(0)
        item.setText(_translate("CompetencesView", "Nombre"))
        item = self.competences_table.horizontalHeaderItem(1)
        item.setText(_translate("CompetencesView", "Lugar"))
        item = self.competences_table.horizontalHeaderItem(2)
        item.setText(_translate("CompetencesView", "Fecha"))
        item = self.competences_table.horizontalHeaderItem(3)
        item.setText(_translate("CompetencesView", "Hora"))
        item = self.competences_table.horizontalHeaderItem(4)
        item.setText(_translate("CompetencesView", "Recompensas"))
        item = self.competences_table.horizontalHeaderItem(5)
        item.setText(_translate("CompetencesView", "Grupos"))
        item = self.competences_table.horizontalHeaderItem(6)
        item.setText(_translate("CompetencesView", "Ver"))
        item = self.competences_table.horizontalHeaderItem(7)
        item.setText(_translate("CompetencesView", "Modificar"))
        self.btn_get_all_competitions.setText(_translate("CompetencesView", "CONSULTAR"))
        self.label_7.setText(_translate("CompetencesView", "GRUPOS/OLEADAS"))
        self.lb_competence_selected.setText(_translate("CompetencesView", "POR FAVOR SELECCIONE UNA COMPETENCIA"))
        self.label_8.setText(_translate("CompetencesView", "Nombre"))
        self.label_9.setText(_translate("CompetencesView", "Orden"))
        item = self.groups_table.horizontalHeaderItem(0)
        item.setText(_translate("CompetencesView", "Nombre"))
        item = self.groups_table.horizontalHeaderItem(1)
        item.setText(_translate("CompetencesView", "Orden"))
        item = self.groups_table.horizontalHeaderItem(2)
        item.setText(_translate("CompetencesView", "Ver"))
        item = self.groups_table.horizontalHeaderItem(3)
        item.setText(_translate("CompetencesView", "Modificar"))
        item = self.groups_table.horizontalHeaderItem(4)
        item.setText(_translate("CompetencesView", "Eliminar"))
        self.btn_create_group.setText(_translate("CompetencesView", "Agregar"))
        self.btn_see_all_groups.setText(_translate("CompetencesView", "Recargar"))
