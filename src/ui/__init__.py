import pathlib

from .dialogs import (
    App_Ext_Dialog,
    Mail_Dialog,
    Settings,
    edit_bookdata_ui,
    fileparser_ui,
    login_ui,
    medienadder_ui,
    parsed_titles_ui,
    popus_confirm,
    reminder_ui,
    settings_ui,
    new_subject_ui,
)
from .Ui_semesterapparat_ui import Ui_MainWindow as Ui_Semesterapparat
from .Ui_setupwizard import Ui_Wizard as SetupWizard
from .widgets import (
    FilePicker,
    GraphWidget,
    Message_Widget,
    StatusWidget,
)

path = pathlib.Path(__file__).parent.absolute()
# from .mainwindow import Ui_MainWindow as Ui_MainWindow
# from .sap import Ui_MainWindow as MainWindow_SAP
__all__ = ["mainwindow", "sap", "dialogs", "widgets"]
