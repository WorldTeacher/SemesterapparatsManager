# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'confirm_extend.ui'
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
from PySide6.QtWidgets import (QAbstractButton, QApplication, QDialog, QDialogButtonBox,
    QSizePolicy, QTextEdit, QWidget)

class Ui_extend_confirm(object):
    def setupUi(self, extend_confirm):
        if not extend_confirm.objectName():
            extend_confirm.setObjectName(u"extend_confirm")
        extend_confirm.resize(380, 97)
        self.buttonBox = QDialogButtonBox(extend_confirm)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setGeometry(QRect(290, 20, 81, 241))
        self.buttonBox.setOrientation(Qt.Vertical)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)
        self.textEdit = QTextEdit(extend_confirm)
        self.textEdit.setObjectName(u"textEdit")
        self.textEdit.setGeometry(QRect(10, 10, 271, 81))

        self.retranslateUi(extend_confirm)
        self.buttonBox.accepted.connect(extend_confirm.accept)
        self.buttonBox.rejected.connect(extend_confirm.reject)

        QMetaObject.connectSlotsByName(extend_confirm)
    # setupUi

    def retranslateUi(self, extend_confirm):
        extend_confirm.setWindowTitle(QCoreApplication.translate("extend_confirm", u"Dialog", None))
    # retranslateUi

