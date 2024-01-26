# -*- coding: utf-8 -*-

################################################################################
# Form generated from reading UI file 'untitled.ui'
##
# Created by: Qt User Interface Compiler version 6.5.2
##
# WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (
    QCoreApplication,
    QDate,
    QDateTime,
    QLocale,
    QMetaObject,
    QObject,
    QPoint,
    QRect,
    QSize,
    Qt,
    QTime,
    QUrl,
)
from PySide6.QtGui import (
    QAction,
    QBrush,
    QColor,
    QConicalGradient,
    QCursor,
    QFont,
    QFontDatabase,
    QGradient,
    QIcon,
    QImage,
    QKeySequence,
    QLinearGradient,
    QPainter,
    QPalette,
    QPixmap,
    QRadialGradient,
    QTransform,
)
from PySide6.QtWidgets import (
    QApplication,
    QCheckBox,
    QComboBox,
    QFormLayout,
    QFrame,
    QGridLayout,
    QGroupBox,
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QLineEdit,
    QMainWindow,
    QMenu,
    QMenuBar,
    QPushButton,
    QRadioButton,
    QSizePolicy,
    QSpacerItem,
    QStatusBar,
    QTableWidget,
    QTableWidgetItem,
    QTabWidget,
    QToolButton,
    QVBoxLayout,
    QWidget,
)


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1280, 720)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        sizePolicy1 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(
            self.centralwidget.sizePolicy().hasHeightForWidth()
        )
        self.centralwidget.setSizePolicy(sizePolicy1)
        self.verticalLayoutWidget = QWidget(self.centralwidget)
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayoutWidget.setGeometry(QRect(0, 0, 1271, 671))
        self.verticalLayout = QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.tabWidget = QTabWidget(self.verticalLayoutWidget)
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QWidget()
        self.tab.setObjectName("tab")
        sizePolicy2 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.tab.sizePolicy().hasHeightForWidth())
        self.tab.setSizePolicy(sizePolicy2)
        self.horizontalLayoutWidget_2 = QWidget(self.tab)
        self.horizontalLayoutWidget_2.setObjectName("horizontalLayoutWidget_2")
        self.horizontalLayoutWidget_2.setGeometry(QRect(0, 0, 1261, 161))
        self.horizontalLayout_2 = QHBoxLayout(self.horizontalLayoutWidget_2)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.formLayout = QFormLayout()
        self.formLayout.setObjectName("formLayout")
        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalSpacer = QSpacerItem(
            20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding
        )

        self.verticalLayout_2.addItem(self.verticalSpacer)

        self.load_app = QPushButton(self.horizontalLayoutWidget_2)
        self.load_app.setObjectName("load_app")

        self.verticalLayout_2.addWidget(self.load_app)

        self.create_new_app = QPushButton(self.horizontalLayoutWidget_2)
        self.create_new_app.setObjectName("create_new_app")

        self.verticalLayout_2.addWidget(self.create_new_app)

        self.verticalSpacer_2 = QSpacerItem(
            20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding
        )

        self.verticalLayout_2.addItem(self.verticalSpacer_2)

        self.formLayout.setLayout(0, QFormLayout.LabelRole, self.verticalLayout_2)

        self.tableWidget_apparate = QTableWidget(self.horizontalLayoutWidget_2)
        if self.tableWidget_apparate.columnCount() < 4:
            self.tableWidget_apparate.setColumnCount(4)
        __qtablewidgetitem = QTableWidgetItem()
        self.tableWidget_apparate.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.tableWidget_apparate.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.tableWidget_apparate.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        __qtablewidgetitem3 = QTableWidgetItem()
        self.tableWidget_apparate.setHorizontalHeaderItem(3, __qtablewidgetitem3)
        self.tableWidget_apparate.setObjectName("tableWidget_apparate")

        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.tableWidget_apparate)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")

        self.formLayout.setLayout(2, QFormLayout.LabelRole, self.horizontalLayout_3)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")

        self.formLayout.setLayout(1, QFormLayout.FieldRole, self.horizontalLayout_4)

        self.horizontalLayout_2.addLayout(self.formLayout)

        self.line = QFrame(self.tab)
        self.line.setObjectName("line")
        self.line.setGeometry(QRect(0, 160, 1261, 21))
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)
        self.gridLayoutWidget_2 = QWidget(self.tab)
        self.gridLayoutWidget_2.setObjectName("gridLayoutWidget_2")
        self.gridLayoutWidget_2.setGeometry(QRect(0, 180, 1261, 461))
        self.gridLayout_2 = QGridLayout(self.gridLayoutWidget_2)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.tableWidget_apparat_media = QTableWidget(self.gridLayoutWidget_2)
        if self.tableWidget_apparat_media.columnCount() < 4:
            self.tableWidget_apparat_media.setColumnCount(4)
        __qtablewidgetitem4 = QTableWidgetItem()
        self.tableWidget_apparat_media.setHorizontalHeaderItem(0, __qtablewidgetitem4)
        __qtablewidgetitem5 = QTableWidgetItem()
        self.tableWidget_apparat_media.setHorizontalHeaderItem(1, __qtablewidgetitem5)
        __qtablewidgetitem6 = QTableWidgetItem()
        self.tableWidget_apparat_media.setHorizontalHeaderItem(2, __qtablewidgetitem6)
        __qtablewidgetitem7 = QTableWidgetItem()
        self.tableWidget_apparat_media.setHorizontalHeaderItem(3, __qtablewidgetitem7)
        self.tableWidget_apparat_media.setObjectName("tableWidget_apparat_media")

        self.gridLayout_2.addWidget(self.tableWidget_apparat_media, 2, 0, 1, 1)

        self.app_group_box = QGroupBox(self.gridLayoutWidget_2)
        self.app_group_box.setObjectName("app_group_box")
        sizePolicy3 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(
            self.app_group_box.sizePolicy().hasHeightForWidth()
        )
        self.app_group_box.setSizePolicy(sizePolicy3)
        font = QFont()
        font.setPointSize(12)
        font.setBold(True)
        self.app_group_box.setFont(font)
        self.app_group_box.setAlignment(
            Qt.AlignLeading | Qt.AlignLeft | Qt.AlignVCenter
        )
        self.app_group_box.setCheckable(False)
        self.dokument_list = QTableWidget(self.app_group_box)
        if self.dokument_list.columnCount() < 2:
            self.dokument_list.setColumnCount(2)
        __qtablewidgetitem8 = QTableWidgetItem()
        self.dokument_list.setHorizontalHeaderItem(0, __qtablewidgetitem8)
        __qtablewidgetitem9 = QTableWidgetItem()
        self.dokument_list.setHorizontalHeaderItem(1, __qtablewidgetitem9)
        self.dokument_list.setObjectName("dokument_list")
        self.dokument_list.setGeometry(QRect(820, 20, 256, 192))
        self.frame = QFrame(self.app_group_box)
        self.frame.setObjectName("frame")
        self.frame.setGeometry(QRect(10, 30, 731, 151))
        sizePolicy1.setHeightForWidth(self.frame.sizePolicy().hasHeightForWidth())
        self.frame.setSizePolicy(sizePolicy1)
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.drpdwn_prof_title = QComboBox(self.frame)
        self.drpdwn_prof_title.setObjectName("drpdwn_prof_title")
        self.drpdwn_prof_title.setGeometry(QRect(110, 50, 69, 22))
        self.label_5 = QLabel(self.frame)
        self.label_5.setObjectName("label_5")
        self.label_5.setGeometry(QRect(250, 20, 91, 21))
        font1 = QFont()
        font1.setPointSize(9)
        font1.setBold(False)
        self.label_5.setFont(font1)
        self.lineEdit = QLineEdit(self.frame)
        self.lineEdit.setObjectName("lineEdit")
        self.lineEdit.setGeometry(QRect(110, 80, 121, 20))
        self.lineEdit.setFont(font1)
        self.sem_winter = QRadioButton(self.frame)
        self.sem_winter.setObjectName("sem_winter")
        self.sem_winter.setGeometry(QRect(340, 50, 82, 17))
        self.sem_winter.setFont(font1)
        self.label_4 = QLabel(self.frame)
        self.label_4.setObjectName("label_4")
        self.label_4.setGeometry(QRect(10, 80, 71, 21))
        self.label_4.setFont(font1)
        self.drpdwn_app_nr = QComboBox(self.frame)
        self.drpdwn_app_nr.setObjectName("drpdwn_app_nr")
        self.drpdwn_app_nr.setGeometry(QRect(110, 20, 69, 22))
        self.app_name = QLineEdit(self.frame)
        self.app_name.setObjectName("app_name")
        self.app_name.setGeometry(QRect(340, 20, 113, 20))
        self.sem_sommer = QRadioButton(self.frame)
        self.sem_sommer.setObjectName("sem_sommer")
        self.sem_sommer.setGeometry(QRect(340, 70, 82, 17))
        self.sem_sommer.setFont(font1)
        self.label_3 = QLabel(self.frame)
        self.label_3.setObjectName("label_3")
        self.label_3.setGeometry(QRect(10, 50, 61, 20))
        self.label_3.setFont(font1)
        self.label_6 = QLabel(self.frame)
        self.label_6.setObjectName("label_6")
        self.label_6.setGeometry(QRect(270, 60, 51, 21))
        self.label_6.setFont(font1)
        self.sem_year = QLineEdit(self.frame)
        self.sem_year.setObjectName("sem_year")
        self.sem_year.setGeometry(QRect(410, 60, 113, 20))
        self.sem_year.setFont(font1)
        self.label_2 = QLabel(self.frame)
        self.label_2.setObjectName("label_2")
        self.label_2.setGeometry(QRect(10, 20, 101, 21))
        self.label_2.setFont(font1)
        self.btn_apparat_save = QPushButton(self.frame)
        self.btn_apparat_save.setObjectName("btn_apparat_save")
        self.btn_apparat_save.setGeometry(QRect(260, 120, 75, 23))
        self.btn_apparat_save.setFont(font1)
        self.btn_apparat_apply = QPushButton(self.frame)
        self.btn_apparat_apply.setObjectName("btn_apparat_apply")
        self.btn_apparat_apply.setGeometry(QRect(350, 120, 75, 23))
        self.btn_apparat_apply.setFont(font1)
        self.checkBox = QCheckBox(self.frame)
        self.checkBox.setObjectName("checkBox")
        self.checkBox.setGeometry(QRect(340, 90, 101, 17))
        self.checkBox.setFont(font1)
        self.btn_add_document = QPushButton(self.app_group_box)
        self.btn_add_document.setObjectName("btn_add_document")
        self.btn_add_document.setGeometry(QRect(1100, 40, 131, 25))
        self.btn_add_document.setFont(font1)
        self.btn_open_document = QPushButton(self.app_group_box)
        self.btn_open_document.setObjectName("btn_open_document")
        self.btn_open_document.setGeometry(QRect(1100, 80, 131, 25))
        self.btn_open_document.setFont(font1)
        self.toolButton = QToolButton(self.app_group_box)
        self.toolButton.setObjectName("toolButton")
        self.toolButton.setGeometry(QRect(1110, 110, 25, 19))
        self.label_7 = QLabel(self.app_group_box)
        self.label_7.setObjectName("label_7")
        self.label_7.setGeometry(QRect(20, 200, 47, 21))
        self.label_7.setFont(font1)
        self.lineEdit_2 = QLineEdit(self.app_group_box)
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.lineEdit_2.setGeometry(QRect(80, 200, 211, 20))
        self.lineEdit_2.setFont(font1)
        self.label = QLabel(self.app_group_box)
        self.label.setObjectName("label")
        self.label.setGeometry(QRect(0, 180, 1259, 18))
        font2 = QFont()
        font2.setPointSize(11)
        font2.setBold(True)
        self.label.setFont(font2)

        self.gridLayout_2.addWidget(self.app_group_box, 1, 0, 1, 1)

        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QWidget()
        self.tab_2.setObjectName("tab_2")
        self.tabWidget.addTab(self.tab_2, "")

        self.gridLayout.addWidget(self.tabWidget, 0, 0, 1, 1)

        self.horizontalLayout.addLayout(self.gridLayout)

        self.verticalLayout.addLayout(self.horizontalLayout)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName("menubar")
        self.menubar.setGeometry(QRect(0, 0, 1280, 21))
        self.menuDatei = QMenu(self.menubar)
        self.menuDatei.setObjectName("menuDatei")
        self.menuEinstellungen = QMenu(self.menubar)
        self.menuEinstellungen.setObjectName("menuEinstellungen")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menuDatei.menuAction())
        self.menubar.addAction(self.menuEinstellungen.menuAction())

        self.retranslateUi(MainWindow)

        self.tabWidget.setCurrentIndex(0)

        QMetaObject.connectSlotsByName(MainWindow)

    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(
            QCoreApplication.translate("MainWindow", "MainWindow", None)
        )
        # if QT_CONFIG(tooltip)
        self.load_app.setToolTip(
            QCoreApplication.translate(
                "MainWindow", "Load the Semesterapparate from the database", None
            )
        )
        # endif // QT_CONFIG(tooltip)
        self.load_app.setText(
            QCoreApplication.translate("MainWindow", "App. aufrufen", None)
        )
        self.create_new_app.setText(
            QCoreApplication.translate("MainWindow", "neu. App anlegen", None)
        )
        ___qtablewidgetitem = self.tableWidget_apparate.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(
            QCoreApplication.translate("MainWindow", "AppNr", None)
        )
        ___qtablewidgetitem1 = self.tableWidget_apparate.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(
            QCoreApplication.translate("MainWindow", "App Name", None)
        )
        ___qtablewidgetitem2 = self.tableWidget_apparate.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(
            QCoreApplication.translate("MainWindow", "Professor", None)
        )
        ___qtablewidgetitem3 = self.tableWidget_apparate.horizontalHeaderItem(3)
        ___qtablewidgetitem3.setText(
            QCoreApplication.translate("MainWindow", "Dauerapparat", None)
        )
        ___qtablewidgetitem4 = self.tableWidget_apparat_media.horizontalHeaderItem(0)
        ___qtablewidgetitem4.setText(
            QCoreApplication.translate("MainWindow", "Buchtitel", None)
        )
        ___qtablewidgetitem5 = self.tableWidget_apparat_media.horizontalHeaderItem(1)
        ___qtablewidgetitem5.setText(
            QCoreApplication.translate("MainWindow", "Autor", None)
        )
        ___qtablewidgetitem6 = self.tableWidget_apparat_media.horizontalHeaderItem(2)
        ___qtablewidgetitem6.setText(
            QCoreApplication.translate("MainWindow", "Auflage", None)
        )
        ___qtablewidgetitem7 = self.tableWidget_apparat_media.horizontalHeaderItem(3)
        ___qtablewidgetitem7.setText(
            QCoreApplication.translate("MainWindow", "Signatur", None)
        )
        self.app_group_box.setTitle(
            QCoreApplication.translate("MainWindow", "Apparatsdetails", None)
        )
        ___qtablewidgetitem8 = self.dokument_list.horizontalHeaderItem(0)
        ___qtablewidgetitem8.setText(
            QCoreApplication.translate("MainWindow", "Dokumentname", None)
        )
        ___qtablewidgetitem9 = self.dokument_list.horizontalHeaderItem(1)
        ___qtablewidgetitem9.setText(
            QCoreApplication.translate("MainWindow", "Typ", None)
        )
        self.label_5.setText(
            QCoreApplication.translate("MainWindow", "Apparatsname", None)
        )
        self.lineEdit.setPlaceholderText(
            QCoreApplication.translate("MainWindow", "Nachname, Vorname", None)
        )
        self.sem_winter.setText(
            QCoreApplication.translate("MainWindow", "Winter", None)
        )
        self.label_4.setText(
            QCoreApplication.translate("MainWindow", "Prof. Name", None)
        )
        self.sem_sommer.setText(
            QCoreApplication.translate("MainWindow", "Sommer", None)
        )
        self.label_3.setText(
            QCoreApplication.translate("MainWindow", "Prof. Titel", None)
        )
        self.label_6.setText(QCoreApplication.translate("MainWindow", "Semester", None))
        self.sem_year.setPlaceholderText(
            QCoreApplication.translate("MainWindow", "2023", None)
        )
        self.label_2.setText(
            QCoreApplication.translate("MainWindow", "Apparatsnummer", None)
        )
        self.btn_apparat_save.setText(
            QCoreApplication.translate("MainWindow", "Speichern", None)
        )
        self.btn_apparat_apply.setText(
            QCoreApplication.translate("MainWindow", "Aktualisieren", None)
        )
        self.checkBox.setText(
            QCoreApplication.translate("MainWindow", "Dauerapparat", None)
        )
        self.btn_add_document.setText(
            QCoreApplication.translate("MainWindow", "Dokument hinzuf\u00fcgen", None)
        )
        self.btn_open_document.setText(
            QCoreApplication.translate("MainWindow", "Dokument \u00f6ffnen", None)
        )
        self.toolButton.setText(QCoreApplication.translate("MainWindow", "...", None))
        self.label_7.setText(QCoreApplication.translate("MainWindow", "Suche", None))
        self.lineEdit_2.setPlaceholderText(
            QCoreApplication.translate("MainWindow", "Buch oder  Signatur", None)
        )
        self.label.setText(
            QCoreApplication.translate("MainWindow", "Medienliste", None)
        )
        self.tabWidget.setTabText(
            self.tabWidget.indexOf(self.tab),
            QCoreApplication.translate("MainWindow", "Tab 1", None),
        )
        self.tabWidget.setTabText(
            self.tabWidget.indexOf(self.tab_2),
            QCoreApplication.translate("MainWindow", "Tab 2", None),
        )
        self.menuDatei.setTitle(QCoreApplication.translate("MainWindow", "Datei", None))
        self.menuEinstellungen.setTitle(
            QCoreApplication.translate("MainWindow", "Einstellungen", None)
        )

    # retranslateUi
