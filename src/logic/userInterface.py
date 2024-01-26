# encoding: utf-8
import atexit
import os

# import re
import sys
import tempfile
import time
from pathlib import Path

from natsort import natsorted
from omegaconf import OmegaConf
from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtCore import QDate, QThread, pyqtSignal
from PyQt6.QtGui import QColor, QRegularExpressionValidator

from src.logic import c_sort
from src.backend.database import Database
from src.logic.constants import APP_NRS, PROF_TITLES
from src.logic.dataclass import ApparatData, BookData, MailData
from src.logic.log import MyLogger
from src.logic.threads import BookGrabber,AvailChecker
from src.ui import (
    App_Ext_Dialog,
    FilePicker,
    GraphWidget,
    Mail_Dialog,
    Message_Widget,
    Settings,
    StatusWidget,
    Ui_Semesterapparat,
    edit_bookdata_ui,
    fileparser_ui,
    login_ui,
    medienadder_ui,
    parsed_titles_ui,
    popus_confirm,
    reminder_ui,
    settings_ui,
    new_subject_ui,
)
# from src.logic.webrequest import BibTextTransformer, WebRequest
from src.backend.admin_console import AdminCommands
from src.logic.csvparser import csv_to_list
from src.logic.wordparser import word_docx_to_csv
from icecream import ic
config = OmegaConf.load("config.yaml")


class Medien(medienadder_ui):
    def __init__(self) -> None:
        self.logger = MyLogger("Medien")
        super().__init__()
        self.mode = ""
        self.data = []

    def get_list_data(self) -> list:
        signatures = self.listWidget.findItems("*", QtCore.Qt.MatchFlag.MatchWildcard)
        return [signature.text() for signature in signatures]

    def get_mode(self) -> str:
        return self.comboBox.currentText()


# class Setup(SetupWizard):
#     def __init__(self, MainWindow):
#         super().__init__()
#         self.setupUi(MainWindow)
#         self.settings = Settings()
#         self.setWindowTitle("Semesterapparatsmanagement Setup")
#         self.btn_save_path_select.clicked.connect(self.select_save_path)
#         # self.setWindowIcon(QtGui.QIcon("ui\icon.png"))

#     def select_save_path(self) -> None:
#         # open a dialog to select a save path
#         dialog = QtWidgets.QFileDialog()
#         dialog.setFileMode(QtWidgets.QFileDialog.FileMode.Directory)
#         dialog.setOption(QtWidgets.QFileDialog.Option.ShowDirsOnly)
#         dialog.exec()
#         self.settings.save_path = dialog.selectedFiles()[0]
#         self.save_path.setText(self.settings.save_path)
#         self.settings.save_settings()
class MyComboBox(QtWidgets.QComboBox):
    
    def __init__(self, parent=None):
        super().__init__(parent)

valid_input = (0, 0, 0, 0, 0, 0)


class MessageCalendar(QtWidgets.QCalendarWidget):
    #Widget for MessageCalendar
    def __init__(self, parent=None):
        super().__init__(parent)
        self.messages = {}  # Dictionary to store dates with messages

    def setMessages(self, messages):
        for message in messages:
            print(message)
            # Convert the date string to a QDate object
            date = QDate.fromString(message["remind_at"], "yyyy-MM-dd")
            # Store the message for the date
            self.messages[date] = message["message"]
        self.updateCells()

    def updateCells(self):
        self.repaint()

    def paintCell(self, painter, rect, date):
        super().paintCell(painter, rect, date)

        # Check if there is a message for the current date
        if date in self.messages:
            # If there is a message, color the cell background
            painter.fillRect(rect, QColor("#a7e681"))

    def change_stylesheet_cell(self, date: QDate, color: str):
        # change the stylesheet of a cell
        self.setStyleSheet(
            f"QCalendarWidget QTableView QTableCornerButton::section {{background-color: {color};}}"
        )


class Ui(Ui_Semesterapparat):
    # use the Ui_MainWindow class from mainwindow.py
    def __init__(self, MainWindow, username: str) -> None:
        self.logger = MyLogger("Ui")
        self.logger.log_info("Starting Semesterapparatsmanagement")
        super().__init__()
        self.active_user = username
        self.setupUi(MainWindow)
        self.MainWindow = MainWindow
        # set the window title
        MainWindow.setWindowTitle("Semesterapparatsmanagement")

        self.db = Database()
        # self.show()
        # self.setWindowTitle("Semesterapparatsmanagement")
        # self.setWindowIcon(QIcon("ui\icon.png"))
        # self.sem_sommer.clicked.connect(self.buttonClicked)
        self.btn_add_document.clicked.connect(self.add_document)
        self.check_file.clicked.connect(
            self.btn_check_file_threaded
        )  # default: self.add_media_from_file)
        self.create_new_app.clicked.connect(self.btn_create_new_apparat)
        # self.load_app.clicked.connect(self.btn_load_apparat)
        self.btn_apparat_save.clicked.connect(self.btn_save_apparat)
        self.btn_apparat_apply.clicked.connect(self.update_apparat)
        self.btn_open_document.clicked.connect(self.open_document)
        self.add_medium.clicked.connect(self.btn_add_medium)
        self.btn_copy_adis_command.clicked.connect(self.text_to_clipboard)
        self.btn_reserve.clicked.connect(self.check_availability)
        self.calendarWidget = MessageCalendar(self.frame_2)
        self.calendarWidget.setGeometry(QtCore.QRect(0, 0, 291, 191))
        self.calendarWidget.setGridVisible(True)
        self.calendarWidget.setVerticalHeaderFormat(
            QtWidgets.QCalendarWidget.VerticalHeaderFormat.NoVerticalHeader
        )
        self.calendarWidget.setObjectName("MessageCalendar")
        self.calendarWidget.clicked.connect(self.open_reminder)
        self.tableWidget_apparat_media.horizontalHeader().setSectionResizeMode(
            QtWidgets.QHeaderView.ResizeMode.Stretch
        )
        self.tableWidget_apparate.horizontalHeader().setSectionResizeMode(
            QtWidgets.QHeaderView.ResizeMode.Stretch
        )
        self.tableWidget_apparate.setSortingEnabled(True)
        # self.tableWidget_apparate.text
        self.actionEinstellungen.triggered.connect(self.open_settings)
        # set validators
        self.sem_year.setValidator(QtGui.QIntValidator())
        self.sem_year.setText(str(QtCore.QDate.currentDate().year()))
        self.prof_mail.setValidator(
            QRegularExpressionValidator(
                QtCore.QRegularExpression(
                    r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}"
                )
            )
        )
        self.prof_tel_nr.setValidator(QtGui.QIntValidator())
        # set the validator for the app name, allow all letters and umlauts
        self.app_fach.setValidator(
            QtGui.QRegularExpressionValidator(
                QtCore.QRegularExpression(r"[a-zA-Z\s\W]+")
            )
        )

        # allow only letters, numbers, whitespaces, symbols for the apparat name
        self.app_name.setValidator(
            QtGui.QRegularExpressionValidator(
                QtCore.QRegularExpression(r"[a-zA-Z0-9\s\W]+")
            )
        )
        self.tableWidget_apparate.addScrollBarWidget(
            QtWidgets.QScrollBar(), QtCore.Qt.AlignmentFlag.AlignRight
        )
        # connect contextmenuevent to tablewidget
        self.tableWidget_apparate.setContextMenuPolicy(
            QtCore.Qt.ContextMenuPolicy.CustomContextMenu
        )
        self.tableWidget_apparate.customContextMenuRequested.connect(
            self.open_context_menu
        )
        self.tableWidget_apparat_media.setContextMenuPolicy(
            QtCore.Qt.ContextMenuPolicy.CustomContextMenu
        )
        self.tableWidget_apparat_media.customContextMenuRequested.connect(
            self.media_context_menu
        )
        #enable automatic resizing of columns for book_search_result
        self.book_search_result.horizontalHeader().setSectionResizeMode(
            QtWidgets.QHeaderView.ResizeMode.Stretch
        )
        self.tableWidget_apparate.doubleClicked.connect(self.load_app_data)
        self.load_app.hide()
        print(f"user:{self.active_user}")
        userrole = self.db.get_role(self.active_user)
        if userrole == "admin":
            self.tabWidget.setTabVisible(2, True)
        else:
            self.tabWidget.setTabVisible(2, False)
        # self.update_app_media_list()
        self.populate_prof_dropdown()
        self.frame.setEnabled(False)
        # if the focus is changed from the prof name dropdown, set the prof data if the prof exists in the database, otherwise show a message
        self.drpdwn_prof_name.currentIndexChanged.connect(self.set_prof_data)
        self.cancel_active_selection.clicked.connect(self.btn_cancel_active_selection)
        self.check_eternal_app.stateChanged.connect(self.set_state)
        # validate inputs
        self.prof_mail.textChanged.connect(self.validate_prof_mail)
        self.drpdwn_prof_name.editTextChanged.connect(self.validate_prof_name)
        self.prof_tel_nr.textChanged.connect(self.validate_prof_tel)
        self.app_name.textChanged.connect(self.validate_app_name)
        self.app_fach.currentTextChanged.connect(self.validate_app_fach)
        self.sem_year.textChanged.connect(self.validate_semester)
        self.check_eternal_app.stateChanged.connect(self.validate_semester)
        self.chkbx_show_del_media.setEnabled(False)
        self.chkbx_show_del_media.stateChanged.connect(self.update_app_media_list)
        self.label_info.hide()
        self.progress_label.setText("Bitte warten...")
        self.line_2.hide()
        self.progress_label.hide()
        self.message_frame.hide()
        self.btn_reserve.hide()
        self.check_deletable.stateChanged.connect(self.gridchange)
        self.tableWidget.horizontalHeader().setSectionResizeMode(
            QtWidgets.QHeaderView.ResizeMode.Stretch
        )
        self.btn_del_select_apparats.setEnabled(False)
        self.btn_del_select_apparats.clicked.connect(self.delete_selected_apparats)
        self.statistics_table.doubleClicked.connect(self.display_detailed_data)
        self.tabWidget_2.currentChanged.connect(self.tabW2_changed)
        self.tabWidget.currentChanged.connect(self.tabW1_changed)
        self.tableWidget.resizeColumnsToContents()
        self.tableWidget.resizeRowsToContents()
        # set self.app_fach viable inputs to be

        # create a thread, that continually checks the validity of the inputs
        self.grabbers = []
        self.thread = QThread()
        self.validate_thread = QThread()
        self.validate_thread.started.connect(self.thread_check)
        self.validate_thread.start()

        # get all current apparats and cache them in a list
        self.apparats = self.db.get_all_apparts(deleted=0)
        print(self.apparats)
        self.apparats = natsorted(self.apparats, key=lambda x: x[4], reverse=True)

        for apparat in self.apparats:
            self.insert_apparat_into_table(apparat)

        self.old_apparats = self.apparats #create a clone to compare against later
        # if length of apparats changes, update box_apparats
        # if tab is changed, gather data needed
        self.tabWidget.currentChanged.connect(self.tab_changed)
        self.btn_search.clicked.connect(self.statistics)
        # self.thread_check()
        
        ### Admin interface ###
        #!admin - create user
        #!admin - delete user
        #!admin - change user
        #TODO:admin - change faculty        
        self.select_action_box.addItem("")
        self.select_action_box.setCurrentText("")
        self.hide_all() 
        self.select_action_box.currentTextChanged.connect(self.admin_action_changed)
        self.edit_faculty_member_select_member.currentTextChanged.connect(self.edit_faculty_member_set_data)
        self.book_search.clicked.connect(self.search_book)
        
        #enable click functionality for the combobox to allow selection of roles
        
        #admin buttons
        self.user_frame_addUser.clicked.connect(self.add_user)
        self.pushButton.clicked.connect(self.delete_user)
        self.update_user.clicked.connect(self.update_user_data)
        self.update_faculty_member.clicked.connect(self.edit_faculty_member_action)
        
        
    def tabW1_changed(self):
        if self.tabWidget.currentIndex() == 1:
            # self.tabWidget.setCurrentIndex(1)
            self.tabWidget_2.setCurrentIndex(1)
            self.tabWidget_2.setCurrentIndex(0)
            
        
    def search_book(self):
        self.book_search_result.setRowCount(0)
        signature = self.seach_by_signature.text()
        title = self.search_by_title.text()
        params = {
            "signature": signature if signature != "" else None,
            "title": title if title != "" else None
        }
        params = {key: value for key, value in params.items() if value is not None}
        ic(params)
        retdata = self.db.search_book(params)
        
        for book in retdata:
            ic(book)
            self.book_search_result.insertRow(0)
            self.book_search_result.setItem(0,0,QtWidgets.QTableWidgetItem(book[0].title))
            self.book_search_result.setItem(0,1,QtWidgets.QTableWidgetItem(book[0].signature))
            print(book[1])
            self.book_search_result.setItem(0,2,QtWidgets.QTableWidgetItem(self.db.get_apparats_name(book[1],book[2])))
            
        
    def edit_faculty_member_set_data(self):
        #get the selected member
        name = self.edit_faculty_member_select_member.currentText()
        fullname = name.replace(",","") 
        print(fullname,name)
        #get the data for the selected member
        data = self.db.faculty_data(fullname)
        #set the data
        print(data)
        if data == None:
            self.edit_faculty_member_title.setText("")
            self.faculty_member_old_telnr.setText("")
            self.faculty_member_oldmail.setText("")
            self.edit_faculty_member_title.setText("")
        else:
            self.edit_faculty_member_title.setText(data[1])
            self.faculty_member_old_telnr.setText(data[6])
            self.faculty_member_oldmail.setText(data[5])
            self.edit_faculty_member_title.setText(data[1]) if data[1] != None else self.edit_faculty_member_title.setText("")
            
    
        # self.edit_faculty_member_name.setText(f"{data[3]} {data[2]}")
        # self.edit_faculty_member_title.setCurrentText(data[1])
        # self.edit_faculty_member_mail.setText(data[4])
        # self.edit_faculty_member_tel.setText(data[5])
        # self.edit_faculty_member_adis_id.setText(str(data[0]))
        # self.edit_faculty_member_id.setText(str(data[6]))
    
    def add_user(self):
        username = self.user_create_frame_username.text()
        password = self.user_create_frame_password.text()
        role = self.user_frame_userrole.currentText()
        if self.db.check_username(username):
            ic("username already exists")
            # self.user_create_frame_error.setText("Der Nutzername ist bereits vergeben")#TODO: implement error message
            return
        userdata = AdminCommands().create_password(password)
        self.db.create_user(username=username, password=f"{userdata[1]}{userdata[0]}", salt=userdata[1], role=role)
        self.user_create_frame_username.clear()
        self.user_create_frame_password.clear()
        self.user_frame_userrole.setCurrentText("")
        self.admin_action_changed()
        
    def delete_user(self):
        if self.user_delete_confirm.isChecked():
            username = self.user_delete_frame_user_select.currentText()
            self.db.delete_user(username)
            self.user_delete_frame_user_select.removeItem(self.user_delete_frame_user_select.currentIndex())
            self.user_delete_confirm.setChecked(False)
        else:
            # self.user_delete_err_message.setText("Bitte bestätigen Sie die Löschung des Nutzers") # TODO: implement error message
            ic("please confirm the deletion of the user")
            
    def update_user_data(self):
        username = self.user_edit_frame_user_select.currentText()
        password = self.user_edit_frame_new_password.text() if self.user_edit_frame_new_password.text() != "" else None
        role = self.user_edit_frame_role_select.currentText() if self.user_edit_frame_role_select.currentText() != "" else None
        
        userdata = AdminCommands().create_password(password)
        data = {
            "password": f"{userdata[1]}{userdata[0]}",
            "salt": userdata[1],
            "role": role
        }
        data = {key: value for key, value in data.items() if value is not None}
        print(data)
        self.db.update_user(username=username,data = data)
        self.user_edit_frame_user_select.setCurrentText("")
        self.user_edit_frame_new_password.clear()
        self.user_edit_frame_role_select.setCurrentText("")
        
    def edit_faculty_member_action(self):
        def __gen_fullname(fname,lname,data):
            if fname == "" and lname == "":
                return data[3]
            if fname == ""and lname != "":
                return f"{lname} {data[1]}"
            if fname != "" and lname == "":
                return f"{data[2]} {fname}"
            if fname != "" and lname != "":
                return f"{lname} {fname}"
        #get the data and use new value if it is not none and does not mach the old value
        if self.edit_faculty_member_select_member.currentText(""):
            return
        olddata = self.db.get_faculty_members(self.edit_faculty_member_select_member.currentText())
        
        data = olddata[0]
        oldlname = data[2]
        oldfname = data[1]
        #take data except first and last entry
        
        titel = self.edit_faculty_member_new_title.currentText() if self.edit_faculty_member_new_title.currentText() != "Kein Titel" else None
        fname = self.edit_faculty_member_new_surname.text() if self.edit_faculty_member_new_surname.text() != "" else self.edit_faculty_member_select_member.currentText().split(" ")[1].strip()
        lname = self.user_faculty_member_new_name.text() if self.user_faculty_member_new_name.text() != "" else self.edit_faculty_member_select_member.currentText().split(" ")[0].strip()
        fullname = __gen_fullname(fname,lname,data)
        mail = self.user_faculty_member_new_telnr.text()
        telnr = self.user_faculty_member_new_mail.text()
        new_data = {
            "titel":titel,
            "fname":fname,
            "lname":lname,
            "fullname":fullname,
            "mail":mail,
            "telnr":telnr,
        }
        new_data = {key: value for key, value in new_data.items() if value != ""}
        self.db.update_faculty_member(data = new_data,oldlname=oldlname,oldfname=oldfname)
        self.add_faculty_member_data()
        self.edit_faculty_member_new_title.setCurrentText("")
        self.edit_faculty_member_new_surname.clear()    
        self.user_faculty_member_new_name.clear()
        self.user_faculty_member_new_telnr.clear()
        self.user_faculty_member_new_mail.clear()
        
    def hide_all(self):
        self.user_create_frame.hide()
        self.user_edit_frame.hide()
        self.user_delete_frame.hide()
        self.edit_faculty_member.hide()
        
    def admin_action_changed(self):
        action = self.select_action_box.currentText()
        roles = self.db.get_roles()
        roles = [role[0] for role in roles]
        #remove duplicates
        roles = list(dict.fromkeys(roles))
        users = self.db.get_users()
        users = [user[2] for user in users]
        users.remove(self.active_user)  
        if "admin" in users:
            users.remove("admin")
        if action == "Nutzer anlegen":
            self.hide_all()
            self.user_create_frame.show()
            self.user_frame_userrole.addItems(roles)
        elif action == "Nutzer aktualisieren":
            self.hide_all()
            self.user_edit_frame.show()
            self.user_edit_frame_role_select.addItems(roles)
            self.user_edit_frame_user_select.addItems(users)
        elif action == "Nutzer löschen":
            self.hide_all()
            self.user_delete_frame.show()
            self.user_delete_frame_user_select.addItems(users)
            self.user_delete_frame_user_select.setCurrentText("")
            self.user_delete_frame_user_select.addItems(users)
            
        elif action == "Lehrperson bearbeiten":
            self.hide_all()
            self.edit_faculty_member.show()
            self.add_faculty_member_data()
            self.edit_faculty_member_new_title.addItems(PROF_TITLES)
            
            
        else:
            self.hide_all()
        return
    
    def add_faculty_member_data(self):
        faculty_members = self.db.get_faculty_members()
        names = [f"{member[5]}" for member in faculty_members]
        self.edit_faculty_member_select_member.clear()
        self.edit_faculty_member_select_member.addItems(names) 
        self.edit_faculty_member_select_member.addItem("")
        self.edit_faculty_member_select_member.setCurrentText("")
    
    def tabW2_changed(self):

        if self.tabWidget_2.currentIndex() == 0:
            self.stackedWidget_4.setCurrentIndex(0)
        else:
            self.stackedWidget_4.setCurrentIndex(1)

    def generateSemester(self, today=False):
        """Generates the current semester.

        Args:
        -----
            today (bool, optional): If True, the current semester is generated. Defaults to False.
        Returns:
        --------
            str: The current semester
        """
        if today:
            currentYear = QDate.currentDate().year()
            currentYear = int(str(currentYear)[-2:])
            month = QDate.currentDate().month()
            if month >= 4 and month <= 9:
                return "SoSe " + str(currentYear)
            else:
                return f"WiSe {currentYear}/{currentYear+1}"
        currentYear = self.sem_year.text()
        currentYear = int(currentYear[-2:])

        semester = (
            self.sem_sommer.text()
            if self.sem_sommer.isChecked()
            else self.sem_winter.text()
        )
        if semester == "Sommer":
            return "SoSe " + str(currentYear)
        else:
            return f"WiSe {currentYear}/{currentYear+1}"

    def display_detailed_data(self):
        selected_semester = self.statistics_table.item(
            self.statistics_table.currentRow(), 0
        ).text()
        # get all apparats from the selected semester
        data = self.db.apparats_by_semester(selected_semester)
        # replace keys for german names
        # split to two lists
        created = {"Erstellt": data["created"]}
        deleted = {"Gelöscht": data["deleted"]}
        created_status = StatusWidget(created, selected_semester)
        deleted_status = StatusWidget(deleted, selected_semester)
        created_status.setSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Expanding,
        )
        deleted_status.setSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Expanding,
        )

        # add them to the gridLayout_4
        self.gridLayout_4.addWidget(created_status, 1, 0)
        self.gridLayout_4.addWidget(deleted_status, 1, 1)
        created_status.person_double_clicked.connect(self.open_apparat)
        deleted_status.person_double_clicked.connect(self.open_apparat)
        
    def open_apparat(self, header:str, apparat:str, parent_depth:int):
        print(header)
        if header == "deleted" and parent_depth == 2:
                #TODO: warn message here
                print("warning")
        if parent_depth == 1:
            print(apparat)
            #person selected case - open all apparats from this person in the tableWidget
            self.tableWidget.setRowCount(0)
            prof_id = self.db.get_prof_id(apparat.split("(")[0].strip())
            apparats = self.db.get_apparats_by_prof(prof_id)
            for app in apparats:
                print(app)
                #set the items 0 = clickable checkbox, 1 = appname, 2 = profname, 3 = fach
                #insert new row
                self.tableWidget.insertRow(0)
                self.tableWidget.setItem(0,0, QtWidgets.QTableWidgetItem(""))
                self.tableWidget.setItem(0, 1, QtWidgets.QTableWidgetItem(app[1]))
                self.tableWidget.setItem(
                    0, 2, QtWidgets.QTableWidgetItem(str(app[4]))
                )
                self.tableWidget.setItem(0, 3, QtWidgets.QTableWidgetItem(app[2]))
                self.tableWidget.setItem(0, 4, QtWidgets.QTableWidgetItem(app[3]))
                # replace the 0 with a checkbox
                checkbox = QtWidgets.QCheckBox()
                checkbox.setChecked(False)
                self.tableWidget.setCellWidget(0, 0, checkbox)
                # if i[9] is 1, set the background of the row to red
                if int(app[9]) == 1:
                    for j in range(5):
                        self.tableWidget.item(0, j).setBackground(QtGui.QColor(235, 74, 71))
                    # disable the checkbox
                    self.tableWidget.cellWidget(0, 0).setEnabled(False)
                    # set the tooltip
                    self.tableWidget.cellWidget(0, 0).setToolTip(
                        "Dieser Semesterapparat kann nicht gelöscht werden, da er bereits gelöscht wurde"
                    )
        elif parent_depth == 2:
            #apparat selected case - open the apparat in the frame
            self.load_app_data(apparat)
            #change tab focus to tab 0 
            self.tabWidget.setCurrentIndex(0)
        return

    def gridchange(self):
        if self.check_deletable.isChecked():
            self.box_semester.setEnabled(False)
            self.box_semester.clear()
            self.box_appnrs.setEnabled(False)
            self.box_appnrs.clear()
            self.box_person.setEnabled(False)
            self.box_person.clear()
            self.box_fach.setEnabled(False)
            self.box_fach.clear()
            self.box_erstellsemester.setEnabled(False)
            self.box_erstellsemester.clear()
            self.box_dauerapp.setEnabled(False)
            self.box_dauerapp.clear()
        else:
            self.box_semester.setEnabled(True)
            self.box_appnrs.setEnabled(True)
            self.box_person.setEnabled(True)
            self.box_fach.setEnabled(True)
            self.box_erstellsemester.setEnabled(True)
            self.box_dauerapp.setEnabled(True)
            self.tab_changed()

    def populate_tab(self):
        #add default values to the dropdowns
        self.box_appnrs.clear()
        self.box_appnrs.addItem("")
        self.box_appnrs.setCurrentText("")
        self.box_person.clear()
        self.box_person.addItem("")
        self.box_person.setCurrentText("")
        self.box_fach.clear()
        self.box_fach.addItem("")
        self.box_fach.setCurrentText("")
        self.box_erstellsemester.clear()
        self.box_erstellsemester.addItem("")
        self.box_erstellsemester.setCurrentText("")
        self.box_semester.clear()
        self.box_semester.addItem("")
        self.box_semester.setCurrentText("")
        self.box_dauerapp.clear()
        self.box_dauerapp.addItems(["Ja", "Nein", ""])
        self.box_dauerapp.setCurrentText("")
        #add custom vaules
        appnrs = self.db.get_apparat_nrs()
        apparats = natsorted(appnrs)
        apparats = [str(apparat) for apparat in apparats]
        self.box_appnrs.addItems(apparats)
        persons = self.db.get_profs()
        self.box_person.addItems(
            [f"{person[3]}, {person[2]}" for person in persons]
        )
        self.box_fach.addItems(subject[1] for subject in self.db.get_subjects())
        semester = self.db.get_semester()
        self.box_erstellsemester.addItems([sem[0] for sem in semester])
        self.statistics_table.setRowCount(0)
        
        #set data for table and graph in tab 2 tableWidget_3
        data = self.db.get_app_count_by_semester()
        data = c_sort.custom_sort(data)
        # self.tabWidget_3.clear()
        self.tabWidget_3.removeTab(1)
        self.statistics_table.setRowCount(len(data))
        for i in range(len(data)):
            self.statistics_table.setItem(
                i, 0, QtWidgets.QTableWidgetItem(data[i][0])
            )
            self.statistics_table.setItem(
                i, 1, QtWidgets.QTableWidgetItem(str(data[i][1]))
            )
            self.statistics_table.setItem(
                i, 2, QtWidgets.QTableWidgetItem(str(data[i][2]))
            )
        self.statistics_table.resizeColumnsToContents()
        self.statistics_table.resizeRowsToContents()
        # create graph

        graph_data = {
            "x": [i[0] for i in data],
            "y": [i[1] for i in data],
            "y2": [i[2] for i in data],
        }
        graph = GraphWidget(data=graph_data, legend_labels=["Erstellt", "Gelöscht"])

        # place the graph into tabWidget_3
        self.tabWidget_3.addTab(graph, "Erstellte und gelöschte Semesterapparate")
        self.tabWidget_3.setCurrentIndex(0)

    def tab_changed(self):
        curr_tab = self.tabWidget.currentIndex()
        if curr_tab == 0: # create tab
            return
        elif curr_tab == 1: # statistics tab
            self.populate_tab()
        elif curr_tab == 2: #admin tab
            self.populate_admin_tab()
            
    def populate_admin_tab(self):
        pass
      
    def populate_dropdown(self, box, data):
        box.clear()
        box.addItem("")
        box.setCurrentText("")
        box.addItems(data)
        
    def delete_selected_apparats(self):
        # get all selected apparats
        selected_apparats = []
        for i in range(self.tableWidget.rowCount()):
            if self.tableWidget.cellWidget(i, 0).isChecked():
                selected_apparats.append(self.tableWidget.item(i, 2).text())
        # delete all selected apparats
        print(selected_apparats)
        for apparat in selected_apparats:
            self.db.delete_apparat(apparat, self.generateSemester(today=True))
        # refresh the table
        self.tab_changed()
        self.btn_del_select_apparats.setEnabled(False)

    def statistics(self):
        """Generate the statistics based on the selected filters."""
        self.db_err_message.setText("")
        self.btn_del_select_apparats.setEnabled(True)
        params = {
            "appnr": self.box_appnrs.currentText()
            if self.box_appnrs.currentText() != ""
            else None,
            "prof_id": self.db.get_prof_id(self.box_person.currentText())
            if self.box_person.currentText() != ""
            else None,
            "fach": self.box_fach.currentText()
            if self.box_fach.currentText() != ""
            else None,
            "erstellsemester": self.box_erstellsemester.currentText()
            if self.box_erstellsemester.currentText() != ""
            else None,
            "dauer": "1"
            if self.box_dauerapp.currentText() == "Ja"
            else "0"
            if self.box_dauerapp.currentText() == "Nein"
            else None,
            "endsemester": self.box_semester.currentText()
            if self.box_semester.currentText() != ""
            else None,
            "deletable": "True" if self.check_deletable.isChecked() else None,
            "deletesemester": self.generateSemester(today=True),
        }
        params = {key: value for key, value in params.items() if value is not None}  #remove empty lines to prevent errors	 
        print(params)
        params = {key: value for key, value in params.items() if value != "Alle"}  #remove empty lines to prevent errors
        print(params)   
        result = self.db.statistic_request(**params)
        # add QTableWidgetItems to the table
        self.tableWidget.setRowCount(len(result))
        if len(result) == 0:
            self.db_err_message.setText("Keine Ergebnisse gefunden")
            return
        for i in range(len(result)):
            print(result[i])
            # set the items 0 = clickable checkbox, 1 = appname, 2 = profname, 3 = fach
            self.tableWidget.setItem(i, 0, QtWidgets.QTableWidgetItem(""))
            self.tableWidget.setItem(i, 1, QtWidgets.QTableWidgetItem(result[i][1]))
            self.tableWidget.setItem(
                i, 2, QtWidgets.QTableWidgetItem(str(result[i][4]))
            )
            self.tableWidget.setItem(i, 3, QtWidgets.QTableWidgetItem(result[i][2]))
            self.tableWidget.setItem(i, 4, QtWidgets.QTableWidgetItem(result[i][3]))
            # replace the 0 with a checkbox
            checkbox = QtWidgets.QCheckBox()
            checkbox.setChecked(False)
            self.tableWidget.setCellWidget(i, 0, checkbox)
            # if i[9] is 1, set the background of the row to red
            if int(result[i][9]) == 1:
                for j in range(5):
                    self.tableWidget.item(i, j).setBackground(QtGui.QColor(235, 74, 71))
                # disable the checkbox
                self.tableWidget.cellWidget(i, 0).setEnabled(False)
                # set the tooltip
                self.tableWidget.cellWidget(i, 0).setToolTip(
                    "Dieser Semesterapparat kann nicht gelöscht werden, da er bereits gelöscht wurde"
                )
        


    def populate_frame(self, appdata: ApparatData):
        # populate the frame with the data from the database
        self.drpdwn_app_nr.setCurrentText(str(appdata.appnr))
        self.drpdwn_prof_title.setCurrentText(appdata.prof_title)
        self.drpdwn_prof_name.setCurrentText(appdata.profname)
        self.prof_mail.setText(appdata.prof_mail)
        self.prof_tel_nr.setText(appdata.prof_tel)
        self.app_name.setText(appdata.appname)
        self.app_fach.setCurrentText(appdata.app_fach)
        if appdata.semester is not None:
            self.sem_sommer.setChecked(
                True if appdata.semester.split(" ")[0] == "SoSe" else False
            )
            self.sem_winter.setChecked(
                True if appdata.semester.split(" ")[0] == "WiSe" else False
            )
            self.sem_year.setText(appdata.semester.split(" ")[1])
        else:
            self.sem_sommer.setChecked(
                True if appdata.erstellsemester.split(" ")[0] == "SoSe" else False
            )
            self.sem_winter.setChecked(
                True if appdata.erstellsemester.split(" ")[0] == "WiSe" else False
            )
            self.sem_year.setText(appdata.erstellsemester.split(" ")[1])
        self.check_eternal_app.setChecked(appdata.dauerapp)
        self.prof_id_adis.setText(str(appdata.prof_adis_id))
        self.apparat_id_adis.setText(str(appdata.apparat_adis_id))
        self.frame.setEnabled(True)

    def update_apparat(self):
        appdata = ApparatData()
        appdata.app_fach = self.app_fach.text()
        appdata.appname = self.app_name.text()
        appdata.appnr = self.active_apparat()
        appdata.dauerapp = self.check_eternal_app.isChecked()
        appdata.prof_mail = self.prof_mail.text()
        appdata.prof_tel = self.prof_tel_nr.text()
        appdata.prof_title = self.drpdwn_prof_title.currentText()
        appdata.profname = self.drpdwn_prof_name.currentText()
        appdata.semester = (
            self.sem_sommer.text() + " " + self.sem_year.text()
            if self.sem_sommer.isChecked()
            else self.sem_winter.text() + " " + self.sem_year.text()
        )
        appdata.prof_adis_id = self.prof_id_adis.text()
        self.add_files()
        appdata.apparat_adis_id = self.apparat_id_adis.text()

        self.db.update_apparat(appdata)

        self.update_app_media_list()
        self.cancel_active_selection.click()



    def confirm_popup(self, message: str):
        dial = QtWidgets.QDialog()
        popup = popus_confirm()
        popup.setupUi(dial)
        popup.textEdit.setReadOnly(True)
        popup.textEdit.setText(message)
        dial.exec()
        return dial.result()

    def threads(self):
        while True:
            self.validate_prof_mail()
            self.validate_prof_name()
            self.validate_prof_tel()
            self.validate_app_name()
            self.validate_app_fach()
            self.validate_semester()

    def thread_check(self):
        self.prof_mail.textChanged.connect(self.validate_prof_mail)
        self.drpdwn_prof_name.editTextChanged.connect(self.validate_prof_name)
        self.prof_tel_nr.textChanged.connect(self.validate_prof_tel)
        self.app_name.textChanged.connect(self.validate_app_name)
        self.app_fach.currentTextChanged.connect(self.validate_app_fach)
        self.sem_year.textChanged.connect(self.validate_semester)
        self.check_eternal_app.stateChanged.connect(self.validate_semester)

    def validate_prof_name(self):
        if self.frame.isEnabled():
            if "," in self.drpdwn_prof_name.currentText():
                self.drpdwn_prof_name.setStyleSheet("border: 1px solid green;")
                self.profname_mand.setText("")
                self.change_state(0, 1)
            else:
                self.drpdwn_prof_name.setStyleSheet("border: 1px solid red;")
                self.profname_mand.setText("*")
                self.change_state(0, 0)
        else:
            self.drpdwn_prof_name.setStyleSheet("border: 1px solid black;")

    def validate_prof_mail(self):
        if self.frame.isEnabled():
            if self.prof_mail.hasAcceptableInput():
                self.prof_mail.setStyleSheet("border: 1px solid green;")
                self.mail_mand.setText("")
                self.change_state(1, 1)
            else:
                self.prof_mail.setStyleSheet("border: 1px solid red;")
                self.mail_mand.setText("*")
                self.change_state(1, 0)
        else:
            self.prof_mail.setStyleSheet("border: 1px solid black;")

    def validate_prof_tel(self):
        if self.frame.isEnabled():
            if self.prof_tel_nr.text() != "":
                self.prof_tel_nr.setStyleSheet("border: 1px solid green;")
                self.telnr_mand.setText("")
                self.change_state(2, 1)
            else:
                self.prof_tel_nr.setStyleSheet("border: 1px solid red;")
                self.telnr_mand.setText("*")
                self.change_state(2, 0)

    def validate_app_name(self):
        if self.frame.isEnabled():
            if self.app_name.hasAcceptableInput():
                self.app_name.setStyleSheet("border: 1px solid green;")
                self.appname_mand.setText("")
                self.change_state(3, 1)
            else:
                self.app_name.setStyleSheet("border: 1px solid red;")
                self.appname_mand.setText("*")
                self.change_state(3, 0)

    def validate_app_fach(self):
        if self.frame.isEnabled():
            if self.app_fach.currentText() != "":
                self.app_fach.setStyleSheet("border: 1px solid green;")
                self.fach_mand.setText("")
                self.change_state(4, 1)
            else:
                self.app_fach.setStyleSheet("border: 1px solid red;")
                self.fach_mand.setText("*")
                self.change_state(4, 0)

    def validate_semester(self):
        if self.frame.isEnabled():
            if (
                (self.sem_sommer.isChecked() or self.sem_winter.isChecked())
                and self.sem_year.hasAcceptableInput()
            ) or self.check_eternal_app.isChecked():
                self._mand.setText("")
                self.change_state(5, 1)
            else:
                self._mand.setText("*")
                self.change_state(5, 0)

    def change_state(self, index, state):
        global valid_input
        valid_input = list(valid_input)
        valid_input[index] = state
        valid_input = tuple(valid_input)

    def set_state(self):
        # set state of semester and year
        if self.check_eternal_app.isChecked():
            self.sem_winter.setEnabled(False)
            self.sem_sommer.setEnabled(False)
            self.sem_year.setEnabled(False)
        else:
            self.sem_winter.setEnabled(True)
            self.sem_sommer.setEnabled(True)
            self.sem_year.setEnabled(True)

    def validate_fields(self):
        return all(valid_input)

    # def req_fields_filled(self):
    #     # check if all required fields are filled
    #     values = []
    #     for item in self.frame.findChildren(QtWidgets.QLabel):
    #         # if label name contains "req" and the text is empty, return false
    #         if "mand" in item.objectName() and item.text() == "":
    #             values.append(True)
    #         elif "mand" in item.objectName() and item.text() != "":
    #             values.append(False)
    #     return all(values)
    #
    def buttonClicked(self):
        print("Button clicked")

    def set_prof_data(self):
        if "," not in self.drpdwn_prof_name.currentText():
            self.prof_mail.clear()
            self.prof_tel_nr.clear()
            return
        selected_prof = self.drpdwn_prof_name.currentText()
        data = self.db.get_prof_data(selected_prof)
        prof_title = data["prof_title"]
        if prof_title == "None":
            prof_title = "Kein Titel"
        self.drpdwn_prof_title.setCurrentText(prof_title)
        self.prof_tel_nr.setText(data["prof_tel"])
        self.prof_mail.setText(data["prof_mail"])

    def get_index_of_value(self, table_widget, value):
        for i in range(table_widget.rowCount()):
            for j in range(table_widget.columnCount()):
                if table_widget.item(i, j) is not None and table_widget.item(i, j).text() == value:
                    return i, j
        return None

    def load_app_data(self,app_id=None):
        print(type(app_id))
        if isinstance(app_id, str):
            #double click the tableWidget_apparate row with the given app_id
            row,column = self.get_index_of_value(self.tableWidget_apparate,app_id)
            #set the current index to the row
            self.tableWidget_apparate.setCurrentCell(row,0)
        app_pos = self.tableWidget_apparate.currentIndex()
        appnr = self.tableWidget_apparate.item(app_pos.row(), 0).text()
        appname = self.tableWidget_apparate.item(app_pos.row(), 1).text()
        self.sem_sommer.setEnabled(False)
        self.sem_winter.setEnabled(False)
        self.sem_year.setEnabled(False)
        self.dokument_list.setRowCount(0)
        self.chkbx_show_del_media.setEnabled(True)
        appdata = self.db.get_app_data(appnr, appname)
        self.populate_frame(appdata)
        self.btn_apparat_save.hide()
        self.btn_reserve.show()
        self.drpdwn_app_nr.setDisabled(True)
        self.app_fach.setDisabled(True)
        self.update_app_media_list()
        self.update_documemt_list()

    def update_documemt_list(self):
        app_id = self.active_apparat()
        prof_id = self.db.get_prof_id(
            self.drpdwn_prof_name.currentText().replace(", ", " ")
        )
        files = self.db.get_files(app_id, prof_id)
        for file in files:
            self.dokument_list.insertRow(0)
            self.dokument_list.setItem(0, 0, QtWidgets.QTableWidgetItem(file[0]))
            self.dokument_list.setItem(0, 1, QtWidgets.QTableWidgetItem(file[1]))
            self.dokument_list.setItem(0, 2, QtWidgets.QTableWidgetItem(""))
            self.dokument_list.setItem(0, 3, QtWidgets.QTableWidgetItem("Database"))

    # def btn_load_apparat(self):
    #     # remove all rows from table
    #     #get all
    #     self.tableWidget_apparate.sortItems(0, QtCore.Qt.SortOrder.AscendingOrder)
    #     self.frame.setDisabled(True)
    #     for child in self.frame.findChildren(QtWidgets.QLineEdit):
    #         child.clear()

    def btn_create_new_apparat(self):
        global valid_input
        # *create a new apparat
        self.btn_apparat_save.show() if self.btn_apparat_save.isHidden() else None
        # clear dokumemt_list
        self.dokument_list.setRowCount(0)
        self.frame.setEnabled(True)
        
        self.sem_year.setEnabled(True)
        self.sem_sommer.setEnabled(True)
        self.sem_winter.setEnabled(True)
        self.chkbx_show_del_media.setEnabled(True)
        self.drpdwn_app_nr.setEnabled(True)
        self.app_fach.setEnabled(True)
        self.app_fach.addItems([subject[1] for subject in self.db.get_subjects()])
        self.app_fach.addItem("")
        self.app_fach.setCurrentText("")
        if self.tableWidget_apparat_media.rowCount() > 0:
            self.tableWidget_apparat_media.setRowCount(0)
        # clear all fields
        for item in self.frame.findChildren(QtWidgets.QLineEdit):
            item.clear()
        self.drpdwn_app_nr.clear()
        self.drpdwn_prof_title.clear()
        self.drpdwn_prof_name.clear()
        # set drop down menu for apparat numbers to only available numbers
        self.drpdwn_app_nr.addItems(
            [str(i) for i in APP_NRS if i not in self.db.get_apparat_nrs()]
        )
        self.drpdwn_prof_title.addItems(PROF_TITLES)
        valid_input = (0, 0, 0, 0, 0, 0)
        self.populate_prof_dropdown()
        # self.horizontalLayout_6.show()
        # increase size by 300px

    def update_progress_label(self, curr, total):
        text = f"Medium {curr}/{total}"
        self.logger.log_info(text)
        self.progress_label.setText(text)
        # update tableWidget_apparat_media
        self.update_app_media_list()

    def hide_progress_label(self):
        self.logger.log_info("Finished adding media, hiding progress label")
        self.progress_label.hide()
        self.line_2.hide()
        self.label_info.hide()

    def btn_add_medium(self):
        if not self.frame.isEnabled():
            self.confirm_popup("Bitte erst einen Apparat auswählen!")
            return

        def __new_ui():
            dialog = QtWidgets.QDialog()
            frame = Medien()
            frame.setupUi(dialog)
            dialog.exec()
            mode = frame.get_mode()
            data = frame.get_list_data()
            return mode, data, dialog.result()

        self.progress_label.show()
        self.line_2.show()
        self.label_info.show()
        self.progress_label.setText("Bitte warten...")
        mode, data, result = __new_ui()
        if result == 1:
            if data == []:
                self.confirm_popup("Bitte mindestens ein Medium hinzufügen!")

            app_id = self.active_apparat()
            prof_id = self.db.get_prof_id(self.drpdwn_prof_name.currentText())
            # check if app_id is in database
            if not self.db.app_exists(app_id):
                # create apparat
                self.btn_save_apparat()
            # create a thread that updates the progress label after each medium
            count = len(data)
            thread = QThread()
            grabber = BookGrabber(mode, data, app_id, prof_id)
            grabber.moveToThread(thread)
            grabber.finished.connect(thread.quit)
            grabber.finished.connect(grabber.deleteLater)
            grabber.finished.connect(self.hide_progress_label)
            grabber.finished.connect(self.update_app_media_list)
            grabber.updateSignal.connect(self.update_progress_label)
            # worker.finished.connect(worker.deleteLater)

            grabber.start()
            self.thread = thread
            self.grabbers.append(grabber)

            # for book in data:
            #     # self.progress_label.setText(f"Medium {ct}/{len(data)}")
            #     # update the progress label
            #     self.logger.log_info(f"trying to add BookData for Signature {book}")
            #     webdata = WebRequest().get_ppn(book).get_data()
            #     bd: BookData = BibTextTransformer(mode).get_data(webdata).return_data()
            #     bd.signature = book
            #     self.db.add_medium(bookdata=bd, app_id=app_id, prof_id=prof_id)

            # get all media list books

        else:
            return

    def check_availability(self):
        # get all links from the table
        # if no index in tableWidget_apparat_media is selected, check all
        if self.tableWidget_apparat_media.currentRow() == -1:
            links = [
                self.tableWidget_apparat_media.item(i, 1).text()
                for i in range(self.tableWidget_apparat_media.rowCount())
                if self.tableWidget_apparat_media.item(i, 4).text() == "❌"
                or self.tableWidget_apparat_media.item(i, 4).text() == ""
            ]
        else:
            links = [
                self.tableWidget_apparat_media.item(
                    self.tableWidget_apparat_media.currentRow(), 1
                ).text()
            ]

        self.label_info.setText("Verfügbarkeit wird geprüft, bitte warten...")
        self.label_info.show()
        books = self.db.get_media(
            self.active_apparat(),
            self.db.get_prof_id(self.drpdwn_prof_name.currentText()),
            del_state=0,
        )

        thread = QThread()
        appnumber = self.active_apparat()
        print(links)
        availcheck = AvailChecker(links, appnumber, books=books)
        availcheck.moveToThread(thread)
        availcheck.finished.connect(thread.quit)
        availcheck.finished.connect(availcheck.deleteLater)
        availcheck.finished.connect(self.hide_progress_label)
        availcheck.finished.connect(self.update_app_media_list)
        availcheck.start()
        self.thread = thread
        self.grabbers.append(availcheck)

    def btn_cancel_active_selection(self):
        # clear the rows of the table
        self.tableWidget_apparat_media.setRowCount(0)
        self.dokument_list.setRowCount(0)
        self.frame.setEnabled(False)
        for child in self.frame.findChildren(QtWidgets.QLineEdit):
            child.clear()

    def update_app_media_list(self):
        deleted = 0 if not self.chkbx_show_del_media.isChecked() else 1
        app_id = self.active_apparat()
        prof_id = self.db.get_prof_id(self.drpdwn_prof_name.currentText())
        books: list[dict[int, BookData, int]] = self.db.get_media(
            app_id, prof_id, deleted
        )

        # print(books)
        # take the dataclass from the tuple
        # booklist:list[BookData]=[book[0] for book in books]
        self.tableWidget_apparat_media.setRowCount(0)
        for book in books:
            book_id = book["id"]
            book_data = book["bookdata"]
            availability = book["available"]
            # bd = BookData().from_string(book)
            # print(bd, type(bd))
            # create a new row below the last one
            self.tableWidget_apparat_media.insertRow(
                self.tableWidget_apparat_media.rowCount()
            )
            # #set the data
            self.tableWidget_apparat_media.setItem(
                self.tableWidget_apparat_media.rowCount() - 1,
                0,
                QtWidgets.QTableWidgetItem(book_data.title),
            )
            self.tableWidget_apparat_media.setItem(
                self.tableWidget_apparat_media.rowCount() - 1,
                1,
                QtWidgets.QTableWidgetItem(book_data.signature),
            )
            self.tableWidget_apparat_media.setItem(
                self.tableWidget_apparat_media.rowCount() - 1,
                2,
                QtWidgets.QTableWidgetItem(book_data.edition),
            )
            self.tableWidget_apparat_media.setItem(
                self.tableWidget_apparat_media.rowCount() - 1,
                3,
                QtWidgets.QTableWidgetItem(book_data.author),
            )
            self.tableWidget_apparat_media.setItem(
                self.tableWidget_apparat_media.rowCount() - 1,
                6,
                QtWidgets.QTableWidgetItem(book_data.link),
            )
            if availability == 1:
                # display green checkmark at column 4 in the row
                self.tableWidget_apparat_media.setItem(
                    self.tableWidget_apparat_media.rowCount() - 1,
                    4,
                    QtWidgets.QTableWidgetItem("✅"),
                )
                # set tooltip
                self.tableWidget_apparat_media.item(
                    self.tableWidget_apparat_media.rowCount() - 1, 4
                ).setToolTip("Das Medium wurde im Apparat gefunden")
            else:
                self.tableWidget_apparat_media.setItem(
                    self.tableWidget_apparat_media.rowCount() - 1,
                    4,
                    QtWidgets.QTableWidgetItem("❌"),
                )
                self.tableWidget_apparat_media.item(
                    self.tableWidget_apparat_media.rowCount() - 1, 4
                ).setToolTip("Das Medium wurde nicht im Apparat gefunden")

        # make table link clickable
        self.tableWidget_apparat_media.itemClicked.connect(self.open_link)

    def open_link(self, item):
        # get the name of the column
        columnname = self.tableWidget_apparat_media.horizontalHeaderItem(
            item.column()
        ).text()
        if columnname == "Link":
            QtGui.QDesktopServices.openUrl(QtCore.QUrl(item.text()))
        else:
            pass

    def text_to_clipboard(self):
        app_id = self.active_apparat()
        text = f"SQ=select distinct akkey from aupr01 where aufst='{app_id}' union select pr_isn from aks4pd where akruf ='{app_id}'"
        clipboard = QtWidgets.QApplication.clipboard()
        clipboard.setText(text)

    def populate_prof_dropdown(self):
        profs = self.db.get_profs()
        # add empty entry to dropdown and set it as current
        self.drpdwn_prof_name.addItem("Kein Name")
        for prof in profs:
            self.drpdwn_prof_name.addItem(f"{prof[3]}, {prof[2]}")

    def add_document(self):
        print("Add document")
        picker = FilePicker()
        files = picker.pick_files()

        for file in files:
            print(file)
            filename = file.split("/")[-1]
            filetype = filename.split(".")[-1]
            self.dokument_list.insertRow(0)
            self.dokument_list.setItem(0, 0, QtWidgets.QTableWidgetItem(filename))
            self.dokument_list.setItem(0, 1, QtWidgets.QTableWidgetItem(filetype))
            self.dokument_list.setItem(0, 2, QtWidgets.QTableWidgetItem("*"))
            self.dokument_list.setItem(0, 3, QtWidgets.QTableWidgetItem(file))
            # set tooltip of row 3 to the file path for each row
            self.dokument_list.item(0, 3).setToolTip(file)

#        self.db.insert_file(files, self.active_apparat(), self.db.get_prof_id(self.drpdwn_prof_name.currentText()))

    def open_document(self):
        print("trying to open document:")

        _selected_doc_name = ""
        _selected_doc_filetype = ""
        try:
            _selected_doc_name = self.dokument_list.item(
                self.dokument_list.currentRow(), 0
            ).text()
            _selected_doc_location = self.dokument_list.item(
                self.dokument_list.currentRow(), 3
            ).text()
            _selected_doc_filetype = self.dokument_list.item(
                self.dokument_list.currentRow(), 1
            ).text()
        except AttributeError:
            self.confirm_popup("Bitte erst ein Dokument auswählen!")
            return
        print(_selected_doc_name, _selected_doc_filetype)
        if not _selected_doc_location == "Database":
            path = Path(_selected_doc_location)
            path = path + "/" + _selected_doc_name
            if os.getenv("OS") == "Windows_NT":
                path = path.resolve()
                os.startfile(path)
            else:
                path = path.resolve()
                os.system(f"open {path}")
        else:
            try:
                self.db.recreate_file(_selected_doc_name, self.active_apparat())
            except Exception as e:
                self.logger.log_exception(e)
            path = config.save_path + _selected_doc_name
            # if ~ in path, replace it with the home directory
            if "~" in path:
                path = path.replace("~", str(Path.home()))
            path = Path(path)
            if os.getenv("OS") == "Windows_NT":
                path = path.resolve()
                os.startfile(path)
            else:
                path = path.resolve()
                os.system(f"open {path}")
            # filebytes = self.db.get_blob(
            #     _selected_doc_name,
            #     self.active_apparat(),
            # )
            # # use io.BytesIO to create a file-like object from the bytes and open it in the respective program
            # file = io.BytesIO(filebytes)
            # file.name = _selected_doc_name

            # QtGui.QDesktopServices.openUrl(QtCore.QUrl(file))
            # print(type(filebytes))

    def add_media_from_file(self):
        def __open_dialog(signatures):
            dialog = QtWidgets.QDialog()
            frame = parsed_titles_ui()
            frame.setupUi(dialog)
            dialog.show()
            frame.signatures = signatures
            frame.populate_table()
            frame.progressBar.setMaximum(len(signatures))
            frame.progressBar.setValue(0)
            frame.progressBar.show()
            frame.count.setText(str(len(signatures)))
            frame.toolButton.click()
            data = frame.return_data()
            print(data)
            # if no data was returned, return

            return data
            # get

        # if files are in the table, and are selected, check for books in the file
        if self.dokument_list.rowCount() == 0:
            return
        else:
            # if file is selected, check for books in the file
            if self.dokument_list.currentRow() != -1:
                print("File selected")
                file = self.dokument_list.item(
                    self.dokument_list.currentRow(), 3
                ).text()

                file_type = self.dokument_list.item(
                    self.dokument_list.currentRow(), 1
                ).text()
                file_location = self.dokument_list.item(
                    self.dokument_list.currentRow(), 3
                ).text()
                file_name = self.dokument_list.item(
                    self.dokument_list.currentRow(), 0
                ).text()
                if file_location == "Database":
                    # create a temporaty file to use, delete it after use
                    temp_file = tempfile.NamedTemporaryFile(
                        delete=False, suffix="." + file_type
                    )
                    temp_file.write(
                        self.db.get_blob(file_name, int(self.active_apparat()))
                    )
                    temp_file.close()
                    file = temp_file.name
                    print(file)
                if file_type == "pdf":
                    # Todo: implement parser here
                    self.confirm_popup("PDF Dateien werden nochnicht unterstützt!")
                    return
                if file_type == "csv":
                    signatures = utils.csv_to_list(file)
                    data = __open_dialog(signatures)
                    # get the app_id and prof_id
                    app_id = self.active_apparat()
                    prof_id = self.db.get_prof_id(self.drpdwn_prof_name.currentText())
                    # add the data to the database
                    for book in data:
                        if type(book) != BookData:
                            continue
                        self.db.add_medium(
                            bookdata=book, app_id=app_id, prof_id=prof_id
                        )
                if file_type == "docx":
                    data = utils.word_docx_to_csv(file)
                    signatures = [
                        i
                        for i in data["Standnummer"].values
                        if i != "\u2002\u2002\u2002\u2002\u2002"
                    ]
                    data = __open_dialog(signatures)
                    # if no data was returned, return
                    if data == []:
                        return
                    # get the app_id and prof_id
                    app_id = self.active_apparat()
                    prof_id = self.db.get_prof_id(self.drpdwn_prof_name.currentText())
                    # add the data to the database
                    for book in data:
                        if type(book) != BookData:
                            continue
                        self.db.add_medium(
                            bookdata=book, app_id=app_id, prof_id=prof_id
                        )
                self.update_app_media_list()
                print(len(signatures))

    def btn_check_file_threaded(self):
        # get active app_id and prof_id
        self.tableWidget_apparate.setEnabled(False)
        self.tableWidget_apparate.setToolTip(
            "Bitte warten, bis alle Medien hinzugefügt wurden"
        )
        app_id = self.active_apparat()
        prof_id = self.db.get_prof_id(self.drpdwn_prof_name.currentText())
        # check if apparat in database
        if not self.db.app_exists(app_id):
            # create apparat
            self.btn_save_apparat()
        if self.dokument_list.rowCount() == 0:
            self.tableWidget_apparate.setEnabled(True)
            self.tableWidget_apparate.setToolTip("")
            return

        # if file is selected, check for books in the file
        if self.dokument_list.currentRow() != -1:
            print("File selected")
            file = self.dokument_list.item(self.dokument_list.currentRow(), 3).text()

            file_type = self.dokument_list.item(
                self.dokument_list.currentRow(), 1
            ).text()
            file_location = self.dokument_list.item(
                self.dokument_list.currentRow(), 3
            ).text()
            file_name = self.dokument_list.item(
                self.dokument_list.currentRow(), 0
            ).text()
            if file_location == "Database":
                # create a temporaty file to use, delete it after use
                temp_file = tempfile.NamedTemporaryFile(
                    delete=False, suffix="." + file_type
                )
                temp_file.write(self.db.get_blob(file_name, int(self.active_apparat())))
                temp_file.close()
                file = temp_file.name
                print(file)
            if file_type == "pdf":
                # Todo: implement parser here
                self.confirm_popup("PDF Dateien werden nochnicht unterstützt!")
                return
            if file_type == "csv":
                signatures = csv_to_list(file)
                # add the data to the database
            if file_type == "docx":
                data = word_docx_to_csv(file)
                signatures = [
                    i
                    for i in data["Standnummer"].values
                    if i != "\u2002\u2002\u2002\u2002\u2002"
                ]

        signatures = [i for i in signatures if i != ""]
        thread = QThread()
        grabber = BookGrabber("ARRAY", signatures, app_id, prof_id)
        grabber.moveToThread(thread)
        self.label_info.show()
        self.progress_label.show()
        self.line_2.show()
        grabber.finished.connect(thread.quit)
        grabber.finished.connect(grabber.deleteLater)
        grabber.finished.connect(self.hide_progress_label)
        grabber.finished.connect(self.update_app_media_list)
        grabber.finished.connect(self.unlock_apparate)
        grabber.updateSignal.connect(self.update_progress_label)
        # worker.finished.connect(worker.deleteLater)

        grabber.start()
        # self.thread = thread
        self.grabbers.append(grabber)

    def unlock_apparate(self):
        self.tableWidget_apparate.setEnabled(True)
        self.tableWidget_apparate.setToolTip("")

    def btn_save_apparat(self):
        def __clear_fields():
            self.drpdwn_app_nr.clear()
            self.drpdwn_prof_title.clear()
            self.drpdwn_prof_name.clearMask()
            self.app_name.clear()
            self.prof_mail.clear()
            self.prof_tel_nr.clear()
            self.app_fach.clear()
            self.app_name.clear()
            self.sem_year.clear()
            self.dokument_list.setRowCount(0)
            self.sem_winter.setChecked(False)
            self.sem_sommer.setChecked(False)
            self.check_eternal_app.setChecked(False)
            self.prof_id_adis.clear()
            self.prof_id_adis.clear()
            self.apparat_id_adis.clear()
            self.drpdwn_prof_name.clear()
            self.tableWidget_apparat_media.setRowCount(0)
            self.frame.setEnabled(False)

        if not self.validate_fields():
            self.confirm_popup("Bitte alle Pflichtfelder ausfüllen!")
            return
        appd = ApparatData()
        appd.appnr = self.active_apparat()
        appd.prof_title = (
            None
            if self.drpdwn_prof_title.currentText() == "Kein Titel"
            else self.drpdwn_prof_title.currentText()
        )
        appd.profname = self.drpdwn_prof_name.currentText()
        appd.appname = self.app_name.text()
        appd.semester = self.generateSemester()
        appd.dauerapp = 1 if self.check_eternal_app.isChecked() else 0
        appd.prof_tel = self.prof_tel_nr.text()
        appd.prof_mail = self.prof_mail.text()
        app_fach = self.app_fach.currentText()
        curr_fach_alias = self.db.get_subjects_and_aliases()
        for fach in curr_fach_alias:
            if app_fach in fach:
                appd.app_fach = app_fach
                break
        else:
            #create a popup to ask for the correct subject
            dialog = QtWidgets.QDialog()
            popup = new_subject_ui()
            popup.setupUi(dialog)
            new_subject = popup.return_state()
            dialog.exec()
            if dialog.result() == QtWidgets.QDialog.DialogCode.Accepted:
                appd.app_fach = new_subject
                self.db.add_subject(new_subject)
            else:
                return
            
        appd.deleted = 0
        appd.prof_adis_id = self.prof_id_adis.text()
        appd.apparat_adis_id = self.apparat_id_adis.text()
        self.add_files()
        if not self.validate_fields():
            pass
        self.db.create_apparat(appd)
        if self.dokument_list.rowCount() > 0:
            self.add_files()
        appdata = self.db.get_apparats()
        # merge self.appdata and appdata, remove duplicates
        self.apparats = list(set(self.apparats + appdata))
        self.apparats = natsorted(self.apparats, key=lambda x: x[4], reverse=True)
        self.update_apparat_list()

        # self.btn_load_apparat()

        __clear_fields()

    def active_apparat(self):
        return self.drpdwn_app_nr.currentText()

    def add_files(self):
        files = []
        for i in range(self.dokument_list.rowCount()):
            files.append(
                {
                    "name": self.dokument_list.item(i, 0).text(),
                    "type": self.dokument_list.item(i, 1).text(),
                    "date": self.dokument_list.item(i, 2).text(),
                    "path": self.dokument_list.item(i, 3).text(), 
                }
            )
            self.dokument_list.item(i, 2).setText("")
        self.db.insert_file(files, self.active_apparat(), self.db.get_prof_id(self.drpdwn_prof_name.currentText()))

    def update_apparat_list(self):
        # get a list of new apparats based on self.apparats and self.old_apparats
        new_apparats = [
            apparat for apparat in self.apparats if apparat not in self.old_apparats
        ]
        print(new_apparats)
        # insert the new apparats into the table
        for apparat in new_apparats:
            self.insert_apparat_into_table(apparat)
        # sort the table by apparat number using natural sorting
        self.tableWidget_apparate.sortItems(0, QtCore.Qt.SortOrder.AscendingOrder)
        self.old_apparats = self.apparats

    def insert_apparat_into_table(self, apparat):
        def __dauer_check(apparat):
            result = self.db.is_eternal(apparat[0])
            return "Ja" if result == ("True" or "1") else "Nein"

        self.tableWidget_apparate.insertRow(0)
        self.tableWidget_apparate.setItem(
            0, 0, QtWidgets.QTableWidgetItem(str(apparat[4]))
        )
        self.tableWidget_apparate.setItem(
            0, 1, QtWidgets.QTableWidgetItem(str(apparat[1]))
        )
        self.tableWidget_apparate.setItem(
            0,
            2,
            QtWidgets.QTableWidgetItem(
                self.db.get_prof_name_by_id(apparat[2], add_title=False)
            ),
        )
        self.tableWidget_apparate.setItem(
            0,
            3,
            QtWidgets.QTableWidgetItem(
                str(apparat[8]) if apparat[8] != None else apparat[5]
            ),
        )
        self.tableWidget_apparate.setItem(
            0, 4, QtWidgets.QTableWidgetItem(__dauer_check(apparat))
        )
        self.tableWidget_apparate.setItem(
            0, 5, QtWidgets.QTableWidgetItem(str(apparat[13]))
        )
        self.logger.log_info(f"Inserted apparat {apparat[4]}")

    def open_context_menu(self, position):
        menu = QtWidgets.QMenu()
        extend_action = menu.addAction("Verlängern")
        contact_action = menu.addAction("Kontaktieren")
        delete_action = menu.addAction("Löschen")
        remind_action = menu.addAction("Erinnerung")
        menu.addAction(extend_action)
        menu.addActions([contact_action, delete_action, remind_action])
        extend_action.triggered.connect(self.extend_apparat)
        delete_action.triggered.connect(self.delete_apparat)
        contact_action.triggered.connect(self.contact_prof)
        remind_action.triggered.connect(self.reminder)
        menu.exec(self.tableWidget_apparate.mapToGlobal(position))

    def reminder(self):
        dialog = QtWidgets.QDialog()
        reminder = reminder_ui()
        reminder.setupUi(dialog)
        dialog.exec()
        if dialog.result() == QtWidgets.QDialog.DialogCode.Accepted:
            data = reminder.return_message()
            print(data)
            self.db.add_message(
                data,
                self.active_user,
                self.active_apparat if self.active_apparat() != "" else None,
            )
            self.calendarWidget.setMessages([data])
            self.calendarWidget.updateCells()
            # self.db.update_bookdata(data, book_id)
            # self.db.update_bookdata(data)
            self.logger.log_info("Commited message to database")
            # self.update_app_media_list()

    def get_reminders(self):
        messages = self.db.get_messages()
        self.logger.log_info(f"Got {len(messages)} messages from database")
        self.calendarWidget.setMessages(messages)
        self.calendarWidget.updateCells()

    def open_reminder(self):
        def __update_message():
            message_select = self.spin_select_message.value()
            try:
                message = messages[message_select - 1]
            except IndexError:
                self.message_frame.hide()
                return
            self.message_box.setText(message["message"])
            self.line_app_info.setText(
                message["apparatnr"] if message["apparatnr"] != None else "/"
            )

        def __delete_message():
            message = messages[self.spin_select_message.value() - 1]
            self.db.delete_message(message["id"])
            # remove message from list
            messages.remove(message)
            self.spin_select_message.setMaximum(len(messages))
            self.spin_select_message.setValue(1)
            self.label_total_day_messages.setText("/ " + str(len(messages)))

        selected_date = self.calendarWidget.selectedDate().toString("yyyy-MM-dd")
        print(selected_date)
        messages = self.db.get_messages(selected_date)
        if messages == []:
            self.message_frame.hide() if self.message_frame.isVisible() else None
            return
        print(messages)
        message_count = len(messages)
        self.spin_select_message.setMaximum(message_count)
        self.message_frame.show()
        self.label_total_day_messages.setText("/ " + str(message_count))
        # if there is only one message, disable the spinbox
        self.spin_select_message.setEnabled(
            False
        ) if message_count == 1 else self.spin_select_message.setEnabled(True)
        self.spin_select_message.setValue(1)
        # load the first message
        __update_message()
        # on valuechanged, update the message
        self.spin_select_message.valueChanged.connect(__update_message)
        self.btn_delete_message.clicked.connect(__delete_message)

    def open_settings(self):
        dialog = QtWidgets.QDialog()
        settings = settings_ui()
        settings.setupUi(dialog)
        dialog.exec()
        if dialog.result() == QtWidgets.QDialog.DialogCode.Accepted:
            data = settings.return_data()
            print(data)
            OmegaConf.save(data, "config.yaml")
            #re-load the config
            config = OmegaConf.load("config.yaml")
            self.logger.log_info("Saved settings to config.yaml")
            self.reload()
            
    def reload(self):
        #create a new connection to the database, refresh table data and replace the old connection
        self.db = Database()
        self.apparats = self.db.get_all_apparts(deleted=0)
        self.apparats = natsorted(self.apparats, key=lambda x: x[4], reverse=True)
        self.tableWidget_apparate.setRowCount(0)
        for apparat in self.apparats:
            self.insert_apparat_into_table(apparat)

    def media_context_menu(self, position):
        menu = QtWidgets.QMenu()
        delete_action = menu.addAction("Löschen")
        edit_action = menu.addAction("Bearbeiten")
        menu.addAction(delete_action)
        menu.addAction(edit_action)
        delete_action.triggered.connect(self.delete_medium)
        edit_action.triggered.connect(self.edit_medium)
        menu.exec(self.tableWidget_apparat_media.mapToGlobal(position))

    def edit_medium(self):
        book = self.tableWidget_apparat_media.item(
            self.tableWidget_apparat_media.currentRow(), 1
        ).text()
        book_id = self.db.request_medium(
            app_id=self.active_apparat(),
            signature=book,
            prof_id=self.db.get_prof_id(self.drpdwn_prof_name.currentText()),
        )
        data = self.db.get_specific_book(book_id)
        widget = QtWidgets.QDialog()
        bookedit = edit_bookdata_ui()
        bookedit.setupUi(widget)
        # change title of dialog
        widget.setWindowTitle("Metadaten")
        bookedit.populate_fields(data)
        widget.exec()
        if widget.result() == QtWidgets.QDialog.DialogCode.Accepted:
            data = bookedit.get_data()
            print(data)
            self.db.update_bookdata(data, book_id)
            # self.db.update_bookdata(data)
            print("accepted")
            self.update_app_media_list()
        else:
            return
        pass

    def delete_medium(self):
        selected_apparat_id = self.tableWidget_apparate.item(
            self.tableWidget_apparate.currentRow(), 0
        ).text()
        signature = self.tableWidget_apparat_media.item(
            self.tableWidget_apparat_media.currentRow(), 1
        ).text()
        # bookdata= self.db.request_medium(selected_apparat_id,prof_id=self.db.get_prof_id(self.drpdwn_prof_name.currentText()),signature=signature)
        book_id = self.db.request_medium(
            selected_apparat_id,
            prof_id=self.db.get_prof_id(self.drpdwn_prof_name.currentText()),
            signature=signature,
        )
        message = f'Soll das Medium "{self.tableWidget_apparat_media.item(self.tableWidget_apparat_media.currentRow(),0).text()}" wirklich gelöscht werden?'
        state = self.confirm_popup(message)
        print(state)
        if state == 1:
            self.db.delete_medium(book_id)
            self.update_app_media_list()
        pass

    def extend_apparat(self):
        framework = QtWidgets.QDialog()
        frame = App_Ext_Dialog()
        frame.setupUi(framework)
        frame.sem_year.setValidator(QtGui.QIntValidator())
        frame.sem_year.setText(str(QtCore.QDate.currentDate().year()))
        framework.exec()
        # return data from dialog if ok is pressed
        if framework.result() == QtWidgets.QDialog.DialogCode.Accepted:
            data = frame.get_data()
            print(data)
            # return data
            selected_apparat_id = self.tableWidget_apparate.item(
                self.tableWidget_apparate.currentRow(), 0
            ).text()
            print(selected_apparat_id)
            # update self.apparats with the new data
            # find matching apparat
            # for apparat in self.apparats:
            #     if apparat[4] == int(selected_apparat_id):
            #         apparat[5]=data["semester"]
            #         apparat[7]=data["dauerapp"]
            #         break
            # self.old_apparats = self.apparats
            self.db.set_new_sem_date(
                selected_apparat_id, data["semester"], dauerapp=data["dauerapp"]
            )
        else:
            return

    def contact_prof(self):
        dialog = QtWidgets.QDialog()
        mail_prev = Mail_Dialog()
        mail_prev.setupUi(dialog)
        mail_prevs = os.listdir("mail_vorlagen")
        if self.app_name.text() == "":
            mail_prevs.remove("Information zum Semesterapparat.eml")
        mail_prev.comboBox.addItems(mail_prevs)
        active_apparat_id = self.tableWidget_apparate.item(
            self.tableWidget_apparate.currentRow(), 0
        ).text()
        general_data = {
            "Appname": self.app_name.text(),
            "AppSubject": self.app_fach.text(),
            "appnr": active_apparat_id,
        }
        print(active_apparat_id)
        mail_prev.appid = active_apparat_id
        base_data = self.db.get_prof_data(id=active_apparat_id)
        profname = self.db.get_prof_name_by_id(base_data["id"])
        profname = profname.split(" ")
        profname = f"{profname[1]} {profname[0]}"
        pass_data = {
            "prof_name": profname,
            "mail_name": base_data["prof_mail"],
            "general": general_data,
        }

        mail_prev.set_data(pass_data)
        mail_prev.set_mail()
        dialog.exec()

    def delete_apparat(self):
        selected_apparat_id = self.tableWidget_apparate.item(
            self.tableWidget_apparate.currentRow(), 0
        ).text()
        message = f"Soll der Apparat {selected_apparat_id} wirklich gelöscht werden?"
        state = self.confirm_popup(message)
        print(state)
        if state == 1:
            self.db.delete_apparat(
                selected_apparat_id, self.generateSemester(today=True)
            )
            # delete the corresponding entry from self.apparats
            for apparat in self.apparats:
                if apparat[4] == int(selected_apparat_id):
                    self.apparats.remove(apparat)
                    break
            self.old_apparats = self.apparats
            print(self.apparats)
            # remove the row from the table
            self.tableWidget_apparate.removeRow(self.tableWidget_apparate.currentRow())
        # if state==QtWidgets.QDialog.DialogCode.Accepted:
        # self.db.delete_apparat(selected_apparat_id)
        # pass


def launch_gui():
    print("trying to login")
    print("checking if database available")
    # database = config.database.path + config.database.name
    # print(database)
    # if not os.path.exists(database):
    #     print("Database not found, creating new database")
    #     db = Database()
    #     db.create_database()
    app = QtWidgets.QApplication(sys.argv)
    login_dialog = QtWidgets.QDialog()
    ui = login_ui()
    ui.setupUi(login_dialog)
    login_dialog.exec()  # This will block until the dialog is closed

    if ui.lresult == 1:
        # if login is successful, open main window
        # show login dialog
        print(ui.lusername)
        MainWindow = QtWidgets.QMainWindow()
        aui = Ui(MainWindow, username=ui.lusername)

        print(aui.active_user)
        MainWindow.show()
        atexit.register(aui.thread.terminate)
        sys.exit(app.exec())
    elif ui.lresult == 0:
        warning_dialog = QtWidgets.QMessageBox()
        warning_dialog.setIcon(QtWidgets.QMessageBox.Icon.Warning)
        warning_dialog.setText("Invalid username or password. Please try again.")
        warning_dialog.setWindowTitle("Login Failed")
        warning_dialog.exec()
    elif ui.lresult == 2:
        # TODO: implement admin functionality here
        """change passwords for apparats, change passwords for users, list users, create and delete users etc"""
        # open a console window
        # console = ""
        print("admin")


if __name__ == "__main__":
    print("This is the main window")
    # app = QtWidgets.QApplication(sys.argv)
    # window = MainWindow()
    # app.exec()
    # open login screen
    launch_gui()
