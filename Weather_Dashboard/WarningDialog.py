from PySide6.QtWidgets import QDialog, QPushButton
from PySide6.QtUiTools import QUiLoader

class WarningDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.loader = QUiLoader()
        self.dlg = self.loader.load("../Qt_Designer/warning.ui")
        self.dlg.setWindowTitle("Warning")

        self.init_ui()
        self.bind_methods()

    def show_dialog(self):
        return self.dlg.exec_()

    # Initializing UI
    def init_ui(self):
        self.ok_button = self.dlg.findChild(QPushButton, "okButton")

    # Binding methods to UI widgets
    def bind_methods(self):
        if self.ok_button:
            self.ok_button.clicked.connect(self.dlg.accept)