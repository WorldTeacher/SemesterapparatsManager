# Form implementation generated from reading ui file 'ui\dialogs\confirm_extend.ui'
#
# Created by: PyQt6 UI code generator 6.3.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_extend_confirm(object):
    def setupUi(self, extend_confirm):
        extend_confirm.setObjectName("extend_confirm")
        extend_confirm.resize(380, 97)
        # icon=QtGui.QIcon(f"ui/icons/{icon}.png")
        # extend_confirm.setWindowIcon(icon)
        self.buttonBox = QtWidgets.QDialogButtonBox(extend_confirm)
        self.buttonBox.setGeometry(QtCore.QRect(290, 20, 81, 241))
        self.buttonBox.setOrientation(QtCore.Qt.Orientation.Vertical)
        self.buttonBox.setStandardButtons(
            QtWidgets.QDialogButtonBox.StandardButton.Cancel
            | QtWidgets.QDialogButtonBox.StandardButton.Ok
        )
        self.buttonBox.setObjectName("buttonBox")
        self.textEdit = QtWidgets.QTextEdit(extend_confirm)
        self.textEdit.setGeometry(QtCore.QRect(10, 10, 271, 81))
        self.textEdit.setObjectName("textEdit")

        self.retranslateUi(extend_confirm)
        self.buttonBox.accepted.connect(extend_confirm.accept)  # type: ignore
        self.buttonBox.rejected.connect(extend_confirm.reject)  # type: ignore
        QtCore.QMetaObject.connectSlotsByName(extend_confirm)

    def retranslateUi(self, extend_confirm):
        _translate = QtCore.QCoreApplication.translate
        extend_confirm.setWindowTitle(_translate("extend_confirm", "Dialog"))


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    extend_confirm = QtWidgets.QDialog()
    ui = Ui_extend_confirm()
    ui.setupUi(extend_confirm)
    extend_confirm.show()
    sys.exit(app.exec())
