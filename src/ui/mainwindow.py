# Form implementation generated from reading ui file 'untitled.ui'
#
# Created by: PyQt6 UI code generator 6.3.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1280, 720)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(0, 0, 1271, 671))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.tabWidget = QtWidgets.QTabWidget(self.verticalLayoutWidget)
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtWidgets.QWidget()
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tab.sizePolicy().hasHeightForWidth())
        self.tab.setSizePolicy(sizePolicy)
        self.tab.setObjectName("tab")
        self.horizontalLayoutWidget_2 = QtWidgets.QWidget(self.tab)
        self.horizontalLayoutWidget_2.setGeometry(QtCore.QRect(0, 0, 1261, 161))
        self.horizontalLayoutWidget_2.setObjectName("horizontalLayoutWidget_2")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_2)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.formLayout = QtWidgets.QFormLayout()
        self.formLayout.setObjectName("formLayout")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        self.verticalLayout_2.addItem(spacerItem)
        self.load_app = QtWidgets.QPushButton(self.horizontalLayoutWidget_2)
        self.load_app.setObjectName("load_app")
        self.verticalLayout_2.addWidget(self.load_app)
        self.create_new_app = QtWidgets.QPushButton(self.horizontalLayoutWidget_2)
        self.create_new_app.setObjectName("create_new_app")
        self.verticalLayout_2.addWidget(self.create_new_app)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        self.verticalLayout_2.addItem(spacerItem1)
        self.formLayout.setLayout(0, QtWidgets.QFormLayout.ItemRole.LabelRole, self.verticalLayout_2)
        self.tableWidget_apparate = QtWidgets.QTableWidget(self.horizontalLayoutWidget_2)
        self.tableWidget_apparate.setObjectName("tableWidget_apparate")
        self.tableWidget_apparate.setColumnCount(4)
        self.tableWidget_apparate.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_apparate.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_apparate.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_apparate.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_apparate.setHorizontalHeaderItem(3, item)
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.ItemRole.FieldRole, self.tableWidget_apparate)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.formLayout.setLayout(2, QtWidgets.QFormLayout.ItemRole.LabelRole, self.horizontalLayout_3)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.formLayout.setLayout(1, QtWidgets.QFormLayout.ItemRole.FieldRole, self.horizontalLayout_4)
        self.horizontalLayout_2.addLayout(self.formLayout)
        self.line = QtWidgets.QFrame(self.tab)
        self.line.setGeometry(QtCore.QRect(0, 160, 1261, 21))
        self.line.setFrameShape(QtWidgets.QFrame.Shape.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.line.setObjectName("line")
        self.gridLayoutWidget_2 = QtWidgets.QWidget(self.tab)
        self.gridLayoutWidget_2.setGeometry(QtCore.QRect(0, 180, 1261, 461))
        self.gridLayoutWidget_2.setObjectName("gridLayoutWidget_2")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.gridLayoutWidget_2)
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.tableWidget_apparat_media = QtWidgets.QTableWidget(self.gridLayoutWidget_2)
        self.tableWidget_apparat_media.setObjectName("tableWidget_apparat_media")
        self.tableWidget_apparat_media.setColumnCount(4)
        self.tableWidget_apparat_media.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_apparat_media.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_apparat_media.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_apparat_media.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_apparat_media.setHorizontalHeaderItem(3, item)
        self.gridLayout_2.addWidget(self.tableWidget_apparat_media, 3, 0, 1, 1)
        self.label = QtWidgets.QLabel(self.gridLayoutWidget_2)
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.gridLayout_2.addWidget(self.label, 1, 0, 1, 1)
        self.app_group_box = QtWidgets.QGroupBox(self.gridLayoutWidget_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.app_group_box.sizePolicy().hasHeightForWidth())
        self.app_group_box.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.app_group_box.setFont(font)
        self.app_group_box.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeading|QtCore.Qt.AlignmentFlag.AlignLeft|QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.app_group_box.setCheckable(False)
        self.app_group_box.setObjectName("app_group_box")
        self.tableWidget = QtWidgets.QTableWidget(self.app_group_box)
        self.tableWidget.setGeometry(QtCore.QRect(820, 20, 256, 192))
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(2)
        self.tableWidget.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)
        self.frame = QtWidgets.QFrame(self.app_group_box)
        self.frame.setGeometry(QtCore.QRect(10, 30, 731, 151))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame.sizePolicy().hasHeightForWidth())
        self.frame.setSizePolicy(sizePolicy)
        self.frame.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame.setObjectName("frame")
        self.drpdwn_prof_title = QtWidgets.QComboBox(self.frame)
        self.drpdwn_prof_title.setGeometry(QtCore.QRect(110, 50, 69, 22))
        self.drpdwn_prof_title.setObjectName("drpdwn_prof_title")
        self.label_5 = QtWidgets.QLabel(self.frame)
        self.label_5.setGeometry(QtCore.QRect(250, 20, 91, 21))
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(False)
        font.setWeight(50)
        self.label_5.setFont(font)
        self.label_5.setObjectName("label_5")
        self.lineEdit = QtWidgets.QLineEdit(self.frame)
        self.lineEdit.setGeometry(QtCore.QRect(110, 80, 121, 20))
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(False)
        font.setWeight(50)
        self.lineEdit.setFont(font)
        self.lineEdit.setObjectName("lineEdit")
        self.sem_winter = QtWidgets.QRadioButton(self.frame)
        self.sem_winter.setGeometry(QtCore.QRect(340, 50, 82, 17))
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(False)
        font.setWeight(50)
        self.sem_winter.setFont(font)
        self.sem_winter.setObjectName("sem_winter")
        self.label_4 = QtWidgets.QLabel(self.frame)
        self.label_4.setGeometry(QtCore.QRect(10, 80, 71, 21))
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(False)
        font.setWeight(50)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.drpdwn_app_nr = QtWidgets.QComboBox(self.frame)
        self.drpdwn_app_nr.setGeometry(QtCore.QRect(110, 20, 69, 22))
        self.drpdwn_app_nr.setObjectName("drpdwn_app_nr")
        self.app_name = QtWidgets.QLineEdit(self.frame)
        self.app_name.setGeometry(QtCore.QRect(340, 20, 113, 20))
        self.app_name.setObjectName("app_name")
        self.sem_sommer = QtWidgets.QRadioButton(self.frame)
        self.sem_sommer.setGeometry(QtCore.QRect(340, 70, 82, 17))
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(False)
        font.setWeight(50)
        self.sem_sommer.setFont(font)
        self.sem_sommer.setObjectName("sem_sommer")
        self.label_3 = QtWidgets.QLabel(self.frame)
        self.label_3.setGeometry(QtCore.QRect(10, 50, 61, 20))
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(False)
        font.setWeight(50)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.label_6 = QtWidgets.QLabel(self.frame)
        self.label_6.setGeometry(QtCore.QRect(270, 60, 51, 21))
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(False)
        font.setWeight(50)
        self.label_6.setFont(font)
        self.label_6.setObjectName("label_6")
        self.sem_year = QtWidgets.QLineEdit(self.frame)
        self.sem_year.setGeometry(QtCore.QRect(410, 60, 113, 20))
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(False)
        font.setWeight(50)
        self.sem_year.setFont(font)
        self.sem_year.setObjectName("sem_year")
        self.label_2 = QtWidgets.QLabel(self.frame)
        self.label_2.setGeometry(QtCore.QRect(10, 20, 101, 21))
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(False)
        font.setWeight(50)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.btn_apparat_save = QtWidgets.QPushButton(self.frame)
        self.btn_apparat_save.setGeometry(QtCore.QRect(260, 120, 75, 23))
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(False)
        font.setWeight(50)
        self.btn_apparat_save.setFont(font)
        self.btn_apparat_save.setObjectName("btn_apparat_save")
        self.btn_apparat_apply = QtWidgets.QPushButton(self.frame)
        self.btn_apparat_apply.setGeometry(QtCore.QRect(350, 120, 75, 23))
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(False)
        font.setWeight(50)
        self.btn_apparat_apply.setFont(font)
        self.btn_apparat_apply.setObjectName("btn_apparat_apply")
        self.checkBox = QtWidgets.QCheckBox(self.frame)
        self.checkBox.setGeometry(QtCore.QRect(340, 90, 101, 17))
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(False)
        font.setWeight(50)
        self.checkBox.setFont(font)
        self.checkBox.setObjectName("checkBox")
        self.btn_add_document = QtWidgets.QPushButton(self.app_group_box)
        self.btn_add_document.setGeometry(QtCore.QRect(1100, 40, 131, 25))
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(False)
        font.setWeight(50)
        self.btn_add_document.setFont(font)
        self.btn_add_document.setObjectName("btn_add_document")
        self.btn_open_document = QtWidgets.QPushButton(self.app_group_box)
        self.btn_open_document.setGeometry(QtCore.QRect(1100, 80, 131, 25))
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(False)
        font.setWeight(50)
        self.btn_open_document.setFont(font)
        self.btn_open_document.setObjectName("btn_open_document")
        self.toolButton = QtWidgets.QToolButton(self.app_group_box)
        self.toolButton.setGeometry(QtCore.QRect(1110, 110, 25, 19))
        self.toolButton.setObjectName("toolButton")
        self.gridLayout_2.addWidget(self.app_group_box, 2, 0, 1, 1)
        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.tabWidget.addTab(self.tab_2, "")
        self.gridLayout.addWidget(self.tabWidget, 0, 0, 1, 1)
        self.horizontalLayout.addLayout(self.gridLayout)
        self.verticalLayout.addLayout(self.horizontalLayout)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1280, 21))
        self.menubar.setObjectName("menubar")
        self.menuDatei = QtWidgets.QMenu(self.menubar)
        self.menuDatei.setObjectName("menuDatei")
        self.menuEinstellungen = QtWidgets.QMenu(self.menubar)
        self.menuEinstellungen.setObjectName("menuEinstellungen")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.menubar.addAction(self.menuDatei.menuAction())
        self.menubar.addAction(self.menuEinstellungen.menuAction())

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.load_app.setToolTip(_translate("MainWindow", "Load the Semesterapparate from the database"))
        self.load_app.setText(_translate("MainWindow", "App. Laden"))
        self.create_new_app.setText(_translate("MainWindow", "neu. App anlegen"))
        item = self.tableWidget_apparate.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "AppNr"))
        item = self.tableWidget_apparate.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "App Name"))
        item = self.tableWidget_apparate.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "Professor"))
        item = self.tableWidget_apparate.horizontalHeaderItem(3)
        item.setText(_translate("MainWindow", "Dauerapparat"))
        item = self.tableWidget_apparat_media.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "Buchtitel"))
        item = self.tableWidget_apparat_media.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "Autor"))
        item = self.tableWidget_apparat_media.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "Auflage"))
        item = self.tableWidget_apparat_media.horizontalHeaderItem(3)
        item.setText(_translate("MainWindow", "Signatur"))
        self.label.setText(_translate("MainWindow", "Medienliste"))
        self.app_group_box.setTitle(_translate("MainWindow", "Apparatsdetails"))
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "Dokumentname"))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "Typ"))
        self.label_5.setText(_translate("MainWindow", "Apparatsname"))
        self.lineEdit.setPlaceholderText(_translate("MainWindow", "Nachname, Vorname"))
        self.sem_winter.setText(_translate("MainWindow", "Winter"))
        self.label_4.setText(_translate("MainWindow", "Prof. Name"))
        self.sem_sommer.setText(_translate("MainWindow", "Sommer"))
        self.label_3.setText(_translate("MainWindow", "Prof. Titel"))
        self.label_6.setText(_translate("MainWindow", "Semester"))
        self.sem_year.setPlaceholderText(_translate("MainWindow", "2023"))
        self.label_2.setText(_translate("MainWindow", "Apparatsnummer"))
        self.btn_apparat_save.setText(_translate("MainWindow", "Speichern"))
        self.btn_apparat_apply.setText(_translate("MainWindow", "Aktualisieren"))
        self.checkBox.setText(_translate("MainWindow", "Dauerapparat"))
        self.btn_add_document.setText(_translate("MainWindow", "Dokument hinzufügen"))
        self.btn_open_document.setText(_translate("MainWindow", "Dokument öffnen"))
        self.toolButton.setText(_translate("MainWindow", "..."))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("MainWindow", "Tab 1"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("MainWindow", "Tab 2"))
        self.menuDatei.setTitle(_translate("MainWindow", "Datei"))
        self.menuEinstellungen.setTitle(_translate("MainWindow", "Einstellungen"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec())
