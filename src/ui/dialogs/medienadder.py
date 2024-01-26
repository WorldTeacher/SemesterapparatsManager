from PyQt6 import QtCore, QtGui, QtWidgets

from .Ui_medianadder import Ui_Dialog


class MedienAdder(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        # Connect signals and slots for your custom functionality
        self.ui.buttonBox.accepted.connect(self.accept)
        self.ui.buttonBox.rejected.connect(self.reject)
        self.ui.l_add.clicked.connect(self.add_to_list)
        self.ui.l_add.setShortcut("Shift+Return")
        # Initialize data variables to store the results
        self.result_data = []

        self.recolorize()

    def add_to_list(self):
        text = self.ui.lineEdit.text().strip()
        if text == "":
            return
        else:
            self.ui.listWidget.addItem(text)
            self.ui.list_amount.setText(str(self.ui.listWidget.count()))
            self.ui.lineEdit.clear()

    def recolorize(self):
        # set the color of the cells of the treeWidget to red if the field is not supported by the provider
        # else set it to green
        for i in range(self.ui.treeWidget.topLevelItemCount()):
            for j in range(1, self.ui.treeWidget.columnCount()):
                if self.ui.treeWidget.topLevelItem(i).text(j) == "0":
                    self.ui.treeWidget.topLevelItem(i).setBackground(
                        j, QtGui.QColor(255, 0, 0)
                    )
                else:
                    self.ui.treeWidget.topLevelItem(i).setBackground(
                        j, QtGui.QColor(0, 255, 0)
                    )
                # remove the text from the cells
                self.ui.treeWidget.topLevelItem(i).setText(j, "")

    def custom_context_menu(self):
        menu = QtWidgets.QMenu()
        menu.addAction("Remove")

        action = menu.exec(QtGui.QCursor.pos())
        if action.text() == "Remove":
            self.remove_from_list()

    def remove_from_list(self):
        self.ui.listWidget.takeItem(self.ui.listWidget.currentRow())
        self.ui.list_amount.setText(str(self.ui.listWidget.count()))

    def add_to_list(self):
        text = self.ui.lineEdit.text().strip()
        if text:
            self.ui.listWidget.addItem(text)
            self.ui.list_amount.setText(str(self.ui.listWidget.count()))
            self.ui.lineEdit.clear()

    def accept(self):
        # Gather and store the data you want to return
        self.result_data = [
            self.ui.listWidget.item(i).text() for i in range(self.ui.listWidget.count())
        ]
        super().accept()

    def keyPressEvent(self, event):
        if (
            event.key() == QtCore.Qt.Key.Key_Return
            or event.key() == QtCore.Qt.Key.Key_Enter
        ):
            # Handle the Return key press as needed (e.g., add to list)
            self.add_to_list()
            event.accept()
        else:
            super().keyPressEvent(event)
