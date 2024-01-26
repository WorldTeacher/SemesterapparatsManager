# Form implementation generated from reading ui file '/home/alexander/GitHub/Semesterapparate/ui/dialogs/login.ui'
#
# Created by: PyQt6 UI code generator 6.5.3
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


import hashlib

from PyQt6 import QtCore, QtWidgets

from src.backend.database import Database
from src.backend.admin_console import AdminCommands

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(218, 190)
        self.dialog = Dialog
        self.login_button = QtWidgets.QPushButton(parent=Dialog)
        self.login_button.setGeometry(QtCore.QRect(30, 140, 76, 32))
        self.login_button.setObjectName("login_button")
        self.login_button.setText("Login")
        self.login_button.setFocusPolicy(QtCore.Qt.FocusPolicy.ClickFocus)
        self.cancel_button = QtWidgets.QPushButton(parent=Dialog)
        self.cancel_button.setGeometry(QtCore.QRect(120, 140, 76, 32))
        self.cancel_button.setObjectName("cancel_button")
        self.cancel_button.setText("Cancel")
        self.cancel_button.setFocusPolicy(QtCore.Qt.FocusPolicy.ClickFocus)
        self.cancel_button.clicked.connect(self.cancel_buttonfn)
        self.label = QtWidgets.QLabel(parent=Dialog)
        self.label.setGeometry(QtCore.QRect(20, 40, 71, 21))
        self.label.setObjectName("label")
        self.lineEdit = QtWidgets.QLineEdit(parent=Dialog)
        self.lineEdit.setGeometry(QtCore.QRect(80, 40, 113, 21))
        self.lineEdit.setObjectName("lineEdit")
        # set strong focus to lineEdit
        self.lineEdit.setFocusPolicy(QtCore.Qt.FocusPolicy.StrongFocus)
        self.label_2 = QtWidgets.QLabel(parent=Dialog)
        self.label_2.setGeometry(QtCore.QRect(20, 80, 71, 21))
        self.label_2.setObjectName("label_2")
        self.lineEdit_2 = QtWidgets.QLineEdit(parent=Dialog)
        self.lineEdit_2.setGeometry(QtCore.QRect(80, 80, 113, 21))
        self.lineEdit_2.setInputMethodHints(QtCore.Qt.InputMethodHint.ImhSensitiveData)
        # set echo mode to password
        self.lineEdit_2.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
        self.lineEdit_2.setClearButtonEnabled(True)
        self.lineEdit_2.setObjectName("lineEdit_2")

        self.retranslateUi(Dialog)
        # if buttonbox accepted is clicked, launch login test
        self.login_button.clicked.connect(self.login)
        self.lresult = -1
        self.lusername = ""
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.label.setText(_translate("Dialog", "Username"))
        self.label_2.setText(_translate("Dialog", "Password"))

    def login(self):
        username = self.lineEdit.text()
        password = self.lineEdit_2.text()
        print(type(username), password)
        # Assuming 'Database' is a class to interact with your database
        db = Database()  

        hashed_password = hashlib.sha256(
            password.encode()
        ).hexdigest()
        if len(db.get_users()) == 0:
            AdminCommands().create_admin()
            self.lresult = 1  # Indicate successful login
            self.lusername = username
            self.dialog.accept()
        if db.login(username, hashed_password):
            self.lresult = 1  # Indicate successful login
            self.lusername = username
            self.dialog.accept()
            db.close()
        else:
            # Credentials are invalid, display a warning
            if username == "" or password == "":
                warning_dialog = QtWidgets.QMessageBox()
                warning_dialog.setIcon(QtWidgets.QMessageBox.Icon.Warning)
                warning_dialog.setText("Please enter a username and password.")
                warning_dialog.setWindowTitle("Login Failed")
                warning_dialog.exec()
            else:
                warning_dialog = QtWidgets.QMessageBox()
                warning_dialog.setIcon(QtWidgets.QMessageBox.Icon.Warning)
                warning_dialog.setText(
                    "Invalid username or password. Please try again."
                )
                warning_dialog.setWindowTitle("Login Failed")
                warning_dialog.exec()

    def cancel_buttonfn(self):
        self.dialog.reject()


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec())