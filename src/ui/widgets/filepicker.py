from PyQt6.QtWidgets import QFileDialog, QApplication
from PyQt6.QtCore import QSettings
import sys

class FilePicker:
    def __init__(self):
        self.settings = QSettings("PH-Freiburg", "SAP")
        self.last_path = self.settings.value("last_path", "/")
        self.multi_select = True
        
    def pick_files(self):
        filepicker = QFileDialog()
        filepicker.setFileMode(QFileDialog.FileMode.ExistingFiles)
        filepicker.setDirectory(self.last_path)
        filepicker.setOption(QFileDialog.Option.DontUseNativeDialog, True)
        #enable multi select
        filepicker.setOption(QFileDialog.Option.DontUseCustomDirectoryIcons, True)

        files, _ = filepicker.getOpenFileNames(caption='Open file', directory=self.last_path)
        if files:
            self.last_path = files[0]
            self.settings.setValue("last_path", self.last_path)
        return files

if __name__ == '__main__':
    app = QApplication(sys.argv)
    picker = FilePicker()
    files = picker.pick_files()
    print(files)