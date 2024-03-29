# Form implementation generated from reading ui file 'c:\Users\aky547\GitHub\Semesterapparate\ui\dialogs\edit_bookdata.ui'
#
# Created by: PyQt6 UI code generator 6.3.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets

from src.logic.dataclass import BookData


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Metadaten")
        Dialog.resize(448, 572)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setGeometry(QtCore.QRect(260, 530, 161, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.buttonBox.setStandardButtons(
            QtWidgets.QDialogButtonBox.StandardButton.Cancel
            | QtWidgets.QDialogButtonBox.StandardButton.Ok
        )
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayoutWidget = QtWidgets.QWidget(Dialog)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(0, 0, 441, 531))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setSizeConstraint(
            QtWidgets.QLayout.SizeConstraint.SetDefaultConstraint
        )
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.label_10 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_10.setObjectName("label_10")
        self.gridLayout.addWidget(self.label_10, 10, 1, 1, 1)
        self.label = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 1, 1, 1)
        self.label_9 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_9.setObjectName("label_9")
        self.gridLayout.addWidget(self.label_9, 9, 1, 1, 1)
        self.label_8 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_8.setObjectName("label_8")
        self.gridLayout.addWidget(self.label_8, 8, 1, 1, 1)
        self.label_12 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_12.setObjectName("label_12")
        self.gridLayout.addWidget(self.label_12, 6, 1, 1, 1)
        self.line_edition = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.line_edition.setObjectName("line_edition")
        self.gridLayout.addWidget(self.line_edition, 2, 2, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 2, 1, 1, 1)
        self.label_4 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 3, 1, 1, 1)
        self.line_link = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.line_link.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.ArrowCursor))
        self.line_link.setReadOnly(True)
        self.line_link.setObjectName("line_link")
        self.gridLayout.addWidget(self.line_link, 6, 2, 1, 1)
        self.label_5 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_5.setObjectName("label_5")
        self.gridLayout.addWidget(self.label_5, 4, 1, 1, 1)
        self.label_7 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_7.setObjectName("label_7")
        self.gridLayout.addWidget(self.label_7, 7, 1, 1, 1)
        self.label_6 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_6.setObjectName("label_6")
        self.gridLayout.addWidget(self.label_6, 5, 1, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 1, 1, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(
            5,
            20,
            QtWidgets.QSizePolicy.Policy.Fixed,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.gridLayout.addItem(spacerItem, 8, 0, 1, 1)
        self.line_title = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.line_title.setObjectName("line_title")
        self.gridLayout.addWidget(self.line_title, 0, 2, 1, 1)
        self.line_signature = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.line_signature.setObjectName("line_signature")
        self.gridLayout.addWidget(self.line_signature, 1, 2, 1, 1)
        self.line_author = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.line_author.setObjectName("line_author")
        self.gridLayout.addWidget(self.line_author, 3, 2, 1, 1)
        self.line_lang = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.line_lang.setObjectName("line_lang")
        self.gridLayout.addWidget(self.line_lang, 8, 2, 1, 1)
        self.line_ppn = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.line_ppn.setObjectName("line_ppn")
        self.gridLayout.addWidget(self.line_ppn, 5, 2, 1, 1)
        self.line_isbn = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.line_isbn.setObjectName("line_isbn")
        self.gridLayout.addWidget(self.line_isbn, 7, 2, 1, 1)
        self.line_year = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.line_year.setObjectName("line_year")
        self.gridLayout.addWidget(self.line_year, 9, 2, 1, 1)
        self.line_pages = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.line_pages.setObjectName("line_pages")
        self.gridLayout.addWidget(self.line_pages, 10, 2, 1, 1)
        self.line_publisher = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.line_publisher.setObjectName("line_publisher")
        self.gridLayout.addWidget(self.line_publisher, 4, 2, 1, 1)

        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)  # type: ignore
        self.buttonBox.rejected.connect(Dialog.reject)  # type: ignore
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.label_10.setText(_translate("Dialog", "Seiten"))
        self.label.setText(_translate("Dialog", "Titel"))
        self.label_9.setText(_translate("Dialog", "Jahr"))
        self.label_8.setText(_translate("Dialog", "Sprache"))
        self.label_12.setText(_translate("Dialog", "Link"))
        self.label_3.setText(_translate("Dialog", "Auflage"))
        self.label_4.setText(_translate("Dialog", "Autor"))
        self.label_5.setText(_translate("Dialog", "Herausgeber"))
        self.label_7.setText(_translate("Dialog", "ISBN(s)"))
        self.label_6.setText(_translate("Dialog", "PPN"))
        self.label_2.setText(_translate("Dialog", "Signatur"))

    def populate_fields(self, data: BookData):
        self.line_author.setText(data.author)
        self.line_edition.setText(data.edition)
        self.line_isbn.setText(", ".join(data.isbn))
        self.line_lang.setText(data.language)
        self.line_link.setText(data.link)
        self.line_pages.setText(data.pages)
        self.line_ppn.setText(data.ppn)
        self.line_publisher.setText(data.publisher)
        self.line_signature.setText(data.signature)
        self.line_title.setText(data.title)
        self.line_year.setText(data.year)

    def get_data(self) -> BookData:
        return BookData(
            ppn=self.line_ppn.text().strip(),
            title=self.line_title.text().strip(),
            signature=self.line_signature.text().strip(),
            edition=self.line_edition.text().strip(),
            link=self.line_link.text().strip(),
            isbn=self.line_isbn.text().split(","),
            author=self.line_author.text().strip(),
            language=self.line_lang.text().strip(),
            publisher=self.line_publisher.text().strip(),
            year=self.line_year.text().strip(),
            pages=self.line_pages.text().strip(),
        )
