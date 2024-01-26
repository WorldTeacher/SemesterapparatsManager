# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'setupwizard.ui'
##
## Created by: Qt User Interface Compiler version 6.5.2
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QFrame, QLabel,
    QLineEdit, QSizePolicy, QTextBrowser, QToolButton,
    QWidget, QWizard, QWizardPage)

class Ui_Wizard(object):
    def setupUi(self, Wizard):
        if not Wizard.objectName():
            Wizard.setObjectName(u"Wizard")
        Wizard.resize(640, 480)
        Wizard.setMaximumSize(QSize(640, 480))
        self.wizardPage1 = QWizardPage()
        self.wizardPage1.setObjectName(u"wizardPage1")
        self.textBrowser = QTextBrowser(self.wizardPage1)
        self.textBrowser.setObjectName(u"textBrowser")
        self.textBrowser.setGeometry(QRect(200, 10, 256, 192))
        Wizard.addPage(self.wizardPage1)
        self.wizardPage2 = QWizardPage()
        self.wizardPage2.setObjectName(u"wizardPage2")
        self.label = QLabel(self.wizardPage2)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(10, 0, 131, 16))
        self.label_2 = QLabel(self.wizardPage2)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(10, 40, 71, 16))
        self.default_apps = QCheckBox(self.wizardPage2)
        self.default_apps.setObjectName(u"default_apps")
        self.default_apps.setGeometry(QRect(100, 40, 70, 17))
        self.label_3 = QLabel(self.wizardPage2)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setGeometry(QRect(10, 70, 61, 16))
        self.custom_applications = QFrame(self.wizardPage2)
        self.custom_applications.setObjectName(u"custom_applications")
        self.custom_applications.setGeometry(QRect(280, 10, 331, 361))
        self.custom_applications.setFrameShape(QFrame.StyledPanel)
        self.custom_applications.setFrameShadow(QFrame.Raised)
        self.save_path = QLineEdit(self.wizardPage2)
        self.save_path.setObjectName(u"save_path")
        self.save_path.setGeometry(QRect(80, 70, 113, 20))
        self.btn_save_path_select = QToolButton(self.wizardPage2)
        self.btn_save_path_select.setObjectName(u"btn_save_path_select")
        self.btn_save_path_select.setGeometry(QRect(200, 70, 25, 19))
        Wizard.addPage(self.wizardPage2)

        self.retranslateUi(Wizard)

        QMetaObject.connectSlotsByName(Wizard)
    # setupUi

    def retranslateUi(self, Wizard):
        Wizard.setWindowTitle(QCoreApplication.translate("Wizard", u"Wizard", None))
        self.textBrowser.setHtml(QCoreApplication.translate("Wizard", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:'MS Shell Dlg 2'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Setup f\u00fcr das Semesterapparatsprogram.</p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Im Anschluss werden wichtige Einstellungen gesetzt, welche auch im sp\u00e4teren Verlauf ver\u00e4ndert werden k\u00f6nnen.</p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margi"
                        "n-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>", None))
        self.label.setText(QCoreApplication.translate("Wizard", u"Grundeinstellungen", None))
#if QT_CONFIG(tooltip)
        self.label_2.setToolTip(QCoreApplication.translate("Wizard", u"Opens the downloaded files with the default applications set in the OS", None))
#endif // QT_CONFIG(tooltip)
        self.label_2.setText(QCoreApplication.translate("Wizard", u"Default Apps", None))
        self.default_apps.setText("")
#if QT_CONFIG(tooltip)
        self.label_3.setToolTip(QCoreApplication.translate("Wizard", u"Path where the downloaded files are stored. Defaults to ~/Desktop/SemapFiles", None))
#endif // QT_CONFIG(tooltip)
        self.label_3.setText(QCoreApplication.translate("Wizard", u"Save Path", None))
        self.save_path.setPlaceholderText(QCoreApplication.translate("Wizard", u"~/Desktop/SemapFiles", None))
        self.btn_save_path_select.setText(QCoreApplication.translate("Wizard", u"...", None))
    # retranslateUi

