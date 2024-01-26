# Form implementation generated from reading ui file 'c:\Users\aky547\GitHub\Semesterapparate\ui\widgets\progress_overview_widget.ui'
#
# Created by: PyQt6 UI code generator 6.3.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(300, 751)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Form.sizePolicy().hasHeightForWidth())
        Form.setSizePolicy(sizePolicy)
        Form.setMaximumSize(QtCore.QSize(300, 751))
        self.group_software = QtWidgets.QGroupBox(Form)
        self.group_software.setEnabled(True)
        self.group_software.setGeometry(QtCore.QRect(10, 10, 281, 211))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.group_software.setFont(font)
        self.group_software.setStatusTip("")
        self.group_software.setFlat(False)
        self.group_software.setCheckable(False)
        self.group_software.setChecked(False)
        self.group_software.setObjectName("group_software")
        self.checkBox = QtWidgets.QCheckBox(self.group_software)
        self.checkBox.setGeometry(QtCore.QRect(10, 20, 241, 41))
        font = QtGui.QFont()
        font.setPointSize(8)
        font.setBold(False)
        font.setWeight(50)
        self.checkBox.setFont(font)
        self.checkBox.setObjectName("checkBox")
        self.checkBox_2 = QtWidgets.QCheckBox(self.group_software)
        self.checkBox_2.setGeometry(QtCore.QRect(10, 50, 241, 41))
        font = QtGui.QFont()
        font.setPointSize(8)
        font.setBold(False)
        font.setWeight(50)
        self.checkBox_2.setFont(font)
        self.checkBox_2.setObjectName("checkBox_2")
        self.checkBox_3 = QtWidgets.QCheckBox(self.group_software)
        self.checkBox_3.setGeometry(QtCore.QRect(10, 130, 241, 41))
        font = QtGui.QFont()
        font.setPointSize(8)
        font.setBold(False)
        font.setWeight(50)
        self.checkBox_3.setFont(font)
        self.checkBox_3.setObjectName("checkBox_3")
        self.groupBox_2 = QtWidgets.QGroupBox(Form)
        self.groupBox_2.setGeometry(QtCore.QRect(10, 220, 281, 251))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setItalic(False)
        font.setUnderline(False)
        font.setWeight(75)
        font.setKerning(True)
        font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferDefault)
        self.groupBox_2.setFont(font)
        self.groupBox_2.setObjectName("groupBox_2")
        self.checkBox_4 = QtWidgets.QCheckBox(self.groupBox_2)
        self.checkBox_4.setGeometry(QtCore.QRect(10, 20, 241, 41))
        font = QtGui.QFont()
        font.setPointSize(8)
        font.setBold(False)
        font.setWeight(50)
        self.checkBox_4.setFont(font)
        self.checkBox_4.setObjectName("checkBox_4")
        self.checkBox_5 = QtWidgets.QCheckBox(self.groupBox_2)
        self.checkBox_5.setGeometry(QtCore.QRect(10, 50, 241, 41))
        font = QtGui.QFont()
        font.setPointSize(8)
        font.setBold(False)
        font.setWeight(50)
        self.checkBox_5.setFont(font)
        self.checkBox_5.setObjectName("checkBox_5")
        self.checkBox_6 = QtWidgets.QCheckBox(self.groupBox_2)
        self.checkBox_6.setGeometry(QtCore.QRect(10, 80, 161, 41))
        font = QtGui.QFont()
        font.setPointSize(8)
        font.setBold(False)
        font.setWeight(50)
        self.checkBox_6.setFont(font)
        self.checkBox_6.setObjectName("checkBox_6")
        self.pushButton = QtWidgets.QPushButton(self.groupBox_2)
        self.pushButton.setGeometry(QtCore.QRect(160, 90, 101, 23))
        font = QtGui.QFont()
        font.setPointSize(8)
        font.setBold(False)
        font.setWeight(50)
        self.pushButton.setFont(font)
        self.pushButton.setStatusTip("")
        self.pushButton.setWhatsThis("")
        self.pushButton.setAccessibleDescription("")
        self.pushButton.setAutoFillBackground(False)
        icon = QtGui.QIcon()
        icon.addPixmap(
            QtGui.QPixmap(
                "c:\\Users\\aky547\\GitHub\\Semesterapparate\\ui\\widgets\\../icons/information.png"
            ),
            QtGui.QIcon.Mode.Normal,
            QtGui.QIcon.State.Off,
        )
        self.pushButton.setIcon(icon)
        self.pushButton.setCheckable(False)
        self.pushButton.setChecked(False)
        self.pushButton.setObjectName("pushButton")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.group_software.setToolTip(
            _translate(
                "Form",
                "Hier klicken, um die aDIS Abfrage in die Zwischenablage zu kopieren",
            )
        )
        self.group_software.setTitle(_translate("Form", "Software"))
        self.checkBox.setText(_translate("Form", "Apparatsdaten eingegeben"))
        self.checkBox_2.setText(_translate("Form", "Medien hinzugefügt / importiert"))
        self.checkBox_3.setText(
            _translate("Form", "Prof-ID und Apparat-ID eingetragen")
        )
        self.groupBox_2.setTitle(_translate("Form", "aDIS"))
        self.checkBox_4.setText(_translate("Form", "Medien geprüft"))
        self.checkBox_5.setText(_translate("Form", "Medien bearbeitet"))
        self.checkBox_6.setText(_translate("Form", "Apparat angelegt"))
        self.pushButton.setToolTip(
            _translate(
                "Form",
                "Hier klicken, um die aDIS Abfrage in die Zwischenablage zu kopieren",
            )
        )
        self.pushButton.setText(_translate("Form", " aDIS Abfrage"))
