from PySide6.QtWidgets import QDialog, QPushButton
from PySide6.QtUiTools import QUiLoader

class ChartDialogue(QDialog):
    def __init__(self):
        super().__init__()
        self.loader = QUiLoader()
        self.dlg = self.loader.load("../Qt_Designer/chartdialog.ui")

        self.cancel_button = self.dlg.findChild(QPushButton, "cancelButton")

        self.cancel_button.clicked.connect(self.dlg.reject)


    def show_dialog(self):
        return self.dlg.exec_()

