from omegaconf import OmegaConf
from PyQt6 import QtWidgets

from src.ui.dialogs.Ui_settings import Ui_Dialog as _settings

config = OmegaConf.load("config.yaml")


class Settings(_settings):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.retranslateUi(self)
        self.load_config()

    def load_config(self):
        self.db_name.setText(config.database.name)
        self.db_path.setText(config.database.path)
        self.save_path.setText(config.save_path)
        self.os_apps.setChecked(config.default_apps)

    def select_db(self):
        # open file dialog, limit to .db files
        file_dialog = QtWidgets.QFileDialog()
        file_dialog.setFileMode(QtWidgets.QFileDialog.FileMode.AnyFile)
        file_dialog.setNameFilter("Datenbank (*.db)")
        file_dialog.setViewMode(QtWidgets.QFileDialog.ViewMode.Detail)
        if file_dialog.exec():
            self.db_name.setText(file_dialog.selectedFiles()[0].split("/")[-1])
            self.db_path.setText(
                file_dialog.selectedFiles()[0].split(self.db_name.text())[0]
            )

    def set_save_path(self):
        # open file dialog, limit to .db files
        file_dialog = QtWidgets.QFileDialog()
        file_dialog.setFileMode(QtWidgets.QFileDialog.FileMode.Directory)
        file_dialog.setViewMode(QtWidgets.QFileDialog.ViewMode.Detail)
        if file_dialog.exec():
            self.save_path.setText(file_dialog.selectedFiles()[0])

    def return_data(self):
        config.database.name = self.db_name.text()
        config.database.path = self.db_path.text()
        config.save_path = self.save_path.text()
        config.default_apps = self.os_apps.isChecked()

        return config
