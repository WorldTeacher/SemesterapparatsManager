# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'apparat_extend.ui'
##
## Created by: Qt User Interface Compiler version 6.4.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QAbstractButton, QApplication, QCheckBox, QDialog,
    QDialogButtonBox, QFrame, QLabel, QLineEdit,
    QRadioButton, QSizePolicy, QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(388, 103)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Dialog.sizePolicy().hasHeightForWidth())
        Dialog.setSizePolicy(sizePolicy)
        Dialog.setMinimumSize(QSize(388, 103))
        Dialog.setMaximumSize(QSize(388, 103))
        self.buttonBox = QDialogButtonBox(Dialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setGeometry(QRect(290, 30, 81, 241))
        self.buttonBox.setOrientation(Qt.Vertical)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Abort|QDialogButtonBox.Save)
        self.label = QLabel(Dialog)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(10, 0, 281, 31))
        font = QFont()
        font.setPointSize(10)
        self.label.setFont(font)
        self.frame = QFrame(Dialog)
        self.frame.setObjectName(u"frame")
        self.frame.setGeometry(QRect(10, 30, 241, 41))
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.line = QFrame(self.frame)
        self.line.setObjectName(u"line")
        self.line.setGeometry(QRect(120, 0, 3, 61))
        self.line.setFrameShape(QFrame.VLine)
        self.line.setFrameShadow(QFrame.Sunken)
        self.rad_sommer = QRadioButton(self.frame)
        self.rad_sommer.setObjectName(u"rad_sommer")
        self.rad_sommer.setGeometry(QRect(10, 10, 82, 21))
        self.rad_winter = QRadioButton(self.frame)
        self.rad_winter.setObjectName(u"rad_winter")
        self.rad_winter.setGeometry(QRect(140, 10, 82, 21))
        self.sem_year = QLineEdit(Dialog)
        self.sem_year.setObjectName(u"sem_year")
        self.sem_year.setGeometry(QRect(10, 70, 121, 20))
        self.checkBox = QCheckBox(Dialog)
        self.checkBox.setObjectName(u"checkBox")
        self.checkBox.setGeometry(QRect(150, 70, 91, 21))

        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Dialog", None))
        self.label.setText(QCoreApplication.translate("Dialog", u"Bis wann soll der Apparat verl\u00e4ngert werden?", None))
        self.rad_sommer.setText(QCoreApplication.translate("Dialog", u"Sommer", None))
        self.rad_winter.setText(QCoreApplication.translate("Dialog", u"Winter", None))
        self.sem_year.setPlaceholderText(QCoreApplication.translate("Dialog", u"2023", None))
        self.checkBox.setText(QCoreApplication.translate("Dialog", u"Dauerapparat", None))
    # retranslateUi

