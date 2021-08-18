# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'takeTimeView.ui'
#
# Created by: PyQt5 UI code generator 5.15.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_TakeTime(object):
    def setupUi(self, TakeTime):
        TakeTime.setObjectName("TakeTime")
        TakeTime.resize(1166, 697)
        self.label = QtWidgets.QLabel(TakeTime)
        self.label.setGeometry(QtCore.QRect(420, 40, 361, 51))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(TakeTime)
        self.label_2.setGeometry(QtCore.QRect(250, 120, 141, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(TakeTime)
        self.label_3.setGeometry(QtCore.QRect(250, 160, 141, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.lb_competence_name = QtWidgets.QLabel(TakeTime)
        self.lb_competence_name.setGeometry(QtCore.QRect(380, 120, 141, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.lb_competence_name.setFont(font)
        self.lb_competence_name.setText("")
        self.lb_competence_name.setObjectName("lb_competence_name")
        self.lb_competence_date = QtWidgets.QLabel(TakeTime)
        self.lb_competence_date.setGeometry(QtCore.QRect(380, 160, 141, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.lb_competence_date.setFont(font)
        self.lb_competence_date.setText("")
        self.lb_competence_date.setObjectName("lb_competence_date")
        self.table_times = QtWidgets.QTableWidget(TakeTime)
        self.table_times.setGeometry(QtCore.QRect(70, 270, 1031, 361))
        self.table_times.setObjectName("table_times")
        self.table_times.setColumnCount(8)
        self.table_times.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.table_times.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.table_times.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.table_times.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.table_times.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.table_times.setHorizontalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.table_times.setHorizontalHeaderItem(5, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.table_times.setHorizontalHeaderItem(6, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.table_times.setHorizontalHeaderItem(7, item)
        self.cb_order_table = QtWidgets.QComboBox(TakeTime)
        self.cb_order_table.setGeometry(QtCore.QRect(120, 230, 201, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.cb_order_table.setFont(font)
        self.cb_order_table.setObjectName("cb_order_table")
        self.cb_order_table.addItem("")
        self.cb_order_table.addItem("")
        self.cb_order_table.addItem("")
        self.cb_order_table.addItem("")
        self.cb_order_table.addItem("")
        self.cb_order_table.addItem("")
        self.cb_order_table.addItem("")
        self.ed_filter = QtWidgets.QLineEdit(TakeTime)
        self.ed_filter.setGeometry(QtCore.QRect(640, 231, 181, 31))
        self.ed_filter.setObjectName("ed_filter")
        self.label_5 = QtWidgets.QLabel(TakeTime)
        self.label_5.setGeometry(QtCore.QRect(650, 130, 171, 16))
        self.label_5.setObjectName("label_5")
        self.btn_update_final_time = QtWidgets.QPushButton(TakeTime)
        self.btn_update_final_time.setGeometry(QtCore.QRect(840, 230, 41, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.btn_update_final_time.setFont(font)
        self.btn_update_final_time.setStyleSheet("background-color: rgb(54, 93, 42);\n"
"color:white;")
        self.btn_update_final_time.setObjectName("btn_update_final_time")
        self.label_7 = QtWidgets.QLabel(TakeTime)
        self.label_7.setGeometry(QtCore.QRect(120, 210, 111, 20))
        self.label_7.setObjectName("label_7")
        self.btn_reset_time = QtWidgets.QPushButton(TakeTime)
        self.btn_reset_time.setGeometry(QtCore.QRect(970, 230, 81, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.btn_reset_time.setFont(font)
        self.btn_reset_time.setStyleSheet("background-color:red;\n"
"color:white;")
        self.btn_reset_time.setObjectName("btn_reset_time")
        self.btn_pdf = QtWidgets.QPushButton(TakeTime)
        self.btn_pdf.setGeometry(QtCore.QRect(100, 650, 161, 31))
        self.btn_pdf.setObjectName("btn_pdf")
        self.lb_pdf = QtWidgets.QLabel(TakeTime)
        self.lb_pdf.setGeometry(QtCore.QRect(420, 650, 341, 31))
        self.lb_pdf.setStyleSheet("color:green")
        self.lb_pdf.setText("")
        self.lb_pdf.setObjectName("lb_pdf")
        self.ed_filter_group = QtWidgets.QLineEdit(TakeTime)
        self.ed_filter_group.setGeometry(QtCore.QRect(350, 230, 181, 31))
        self.ed_filter_group.setObjectName("ed_filter_group")
        self.label_6 = QtWidgets.QLabel(TakeTime)
        self.label_6.setGeometry(QtCore.QRect(340, 210, 221, 16))
        self.label_6.setObjectName("label_6")
        self.ed_filter_2 = QtWidgets.QLineEdit(TakeTime)
        self.ed_filter_2.setGeometry(QtCore.QRect(640, 190, 181, 31))
        self.ed_filter_2.setObjectName("ed_filter_2")
        self.ed_filter_3 = QtWidgets.QLineEdit(TakeTime)
        self.ed_filter_3.setGeometry(QtCore.QRect(640, 150, 181, 31))
        self.ed_filter_3.setObjectName("ed_filter_3")
        self.btn_update_final_time_2 = QtWidgets.QPushButton(TakeTime)
        self.btn_update_final_time_2.setGeometry(QtCore.QRect(840, 190, 41, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.btn_update_final_time_2.setFont(font)
        self.btn_update_final_time_2.setStyleSheet("background-color: rgb(54, 93, 42);\n"
"color:white;")
        self.btn_update_final_time_2.setObjectName("btn_update_final_time_2")
        self.btn_update_final_time_3 = QtWidgets.QPushButton(TakeTime)
        self.btn_update_final_time_3.setGeometry(QtCore.QRect(840, 150, 41, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.btn_update_final_time_3.setFont(font)
        self.btn_update_final_time_3.setStyleSheet("background-color: rgb(54, 93, 42);\n"
"color:white;")
        self.btn_update_final_time_3.setObjectName("btn_update_final_time_3")
        self.ed_reset = QtWidgets.QLineEdit(TakeTime)
        self.ed_reset.setGeometry(QtCore.QRect(940, 190, 131, 31))
        self.ed_reset.setObjectName("ed_reset")

        self.retranslateUi(TakeTime)
        QtCore.QMetaObject.connectSlotsByName(TakeTime)

    def retranslateUi(self, TakeTime):
        _translate = QtCore.QCoreApplication.translate
        TakeTime.setWindowTitle(_translate("TakeTime", "Dialog"))
        self.label.setText(_translate("TakeTime", "TOMAR TIEMPOS"))
        self.label_2.setText(_translate("TakeTime", "COMPETENCIA:"))
        self.label_3.setText(_translate("TakeTime", "FECHA:"))
        item = self.table_times.horizontalHeaderItem(0)
        item.setText(_translate("TakeTime", "Grupo"))
        item = self.table_times.horizontalHeaderItem(1)
        item.setText(_translate("TakeTime", "Iniciar"))
        item = self.table_times.horizontalHeaderItem(2)
        item.setText(_translate("TakeTime", "Atleta"))
        item = self.table_times.horizontalHeaderItem(3)
        item.setText(_translate("TakeTime", "Categoria"))
        item = self.table_times.horizontalHeaderItem(4)
        item.setText(_translate("TakeTime", "Dorsal"))
        item = self.table_times.horizontalHeaderItem(5)
        item.setText(_translate("TakeTime", "Hora inicio"))
        item = self.table_times.horizontalHeaderItem(6)
        item.setText(_translate("TakeTime", "Hora fin"))
        item = self.table_times.horizontalHeaderItem(7)
        item.setText(_translate("TakeTime", "Tiempo total"))
        self.cb_order_table.setItemText(0, _translate("TakeTime", "Dorsal"))
        self.cb_order_table.setItemText(1, _translate("TakeTime", "Nombre"))
        self.cb_order_table.setItemText(2, _translate("TakeTime", "Hora inicio"))
        self.cb_order_table.setItemText(3, _translate("TakeTime", "Hora fin"))
        self.cb_order_table.setItemText(4, _translate("TakeTime", "Tiempo total"))
        self.cb_order_table.setItemText(5, _translate("TakeTime", "Grupo ascendente"))
        self.cb_order_table.setItemText(6, _translate("TakeTime", "Grupo descendente"))
        self.label_5.setText(_translate("TakeTime", "Filtrar por dorsal"))
        self.btn_update_final_time.setText(_translate("TakeTime", "✔"))
        self.label_7.setText(_translate("TakeTime", "Ordernar"))
        self.btn_reset_time.setText(_translate("TakeTime", "Resetear"))
        self.btn_pdf.setText(_translate("TakeTime", "Generar PDF"))
        self.label_6.setText(_translate("TakeTime", "Filtrar por grupo/oleada/nombre/categoria"))
        self.btn_update_final_time_2.setText(_translate("TakeTime", "✔"))
        self.btn_update_final_time_3.setText(_translate("TakeTime", "✔"))
