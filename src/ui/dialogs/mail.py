import subprocess
import tempfile

from PyQt6 import QtCore, QtGui, QtWidgets

from src.ui.dialogs.mail_preview import Ui_Dialog


class Mail_Dialog(QtWidgets.QDialog, Ui_Dialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.appid = ""
        self.mail_data = ""
        self.data = None
        self.buttonBox.accepted.connect(self.save_mail)

    def set_data(self, data: dict):
        self.prof_name.setText(data["prof_name"])
        self.mail_name.setText(data["mail_name"])
        # assign data["general"] to self.data
        self.data = data["general"]

    def set_mail(self):
        email_template = self.comboBox.currentText()
        with open(f"mail_vorlagen/{email_template}", "r", encoding="utf-8") as f:
            mail_template = f.read()
        email_header = email_template.split(".eml")[0]
        if "{AppNr}" in email_template:
            email_header = email_template.split(".eml")[0].format(AppNr=self.appid)
        self.mail_header.setText(email_header)
        self.mail_data = mail_template.split("<html>")[0]
        mail_html = mail_template.split("<html>")[1]
        mail_html = "<html>" + mail_html
        print(self.data)
        Appname = self.data["Appname"]
        mail_html = mail_html.format(
            Profname=self.prof_name.text().split(" ")[-1], Appname=Appname
        )

        self.mail_body.setHtml(mail_html)

    def save_mail(self):
        # create a temporary file
        mail_header = self.mail_header.text()
        mail_body = self.mail_body.toHtml()
        mail = self.mail_data + mail_body
        mail = mail.replace("Subject:", f"Subject: {mail_header}")
        with tempfile.NamedTemporaryFile(
            mode="w", delete=False, suffix=".eml", encoding="utf-8", dir="mails"
        ) as f:
            f.write(mail)
            self.mail_path = f.name
        print(self.mail_path)
        # open the file using thunderbird
        subprocess.Popen(["thunderbird", f"{self.mail_path}"])
        # delete the file
        # os.remove(self.mail_path)


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Mail_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec())
