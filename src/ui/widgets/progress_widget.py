from PyQt6 import QtCore, QtGui, QtWidgets
from Ui_progress_overview_widget import Ui_Form


class Progress_view(Ui_Form):
    def __init__(self, MainWindow):
        super().__init__()
        self.setupUi(MainWindow)
        self.retranslateUi(MainWindow)
        self.checkBox_3.setDisabled(True)
        self.pushButton.clicked.connect(self.pushButton_clicked)

    def pushButton_clicked(self):
        # copies text to clipboard
        clipboard = QtWidgets.QApplication.clipboard()
        clipboard.setText("")
