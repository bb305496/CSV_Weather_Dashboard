from PySide6.QtWidgets import QDialog, QPushButton, QLabel
from PySide6.QtUiTools import QUiLoader

class WarningDialog(QDialog):
    def __init__(self, warning_text: str, font_size: int = 16):
        super().__init__()
        self.loader = QUiLoader()
        self.dlg = self.loader.load("../Qt_Designer/warning.ui")
        self.dlg.setWindowTitle("Warning")
        self.warning_text = warning_text
        self.font_size = font_size

        self.init_ui()
        self.bind_methods()

    def show_dialog(self):
        return self.dlg.exec_()

    # Initializing UI
    def init_ui(self):
        self.ok_button = self.dlg.findChild(QPushButton, "okButton")
        self.text_label = self.dlg.findChild(QLabel, "textLabel")
        self.text_label.setStyleSheet(f"font: {self.font_size}pt;")

    # Binding methods to UI widgets
    def bind_methods(self):
        if self.ok_button:
            self.ok_button.clicked.connect(self.dlg.accept)

        self.text_label.setText(self.warning_text)