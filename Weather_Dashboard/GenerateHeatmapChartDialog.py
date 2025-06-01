from PySide6.QtWidgets import QDialog, QPushButton
from PySide6.QtUiTools import QUiLoader

class HeatmapChartDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.loader = QUiLoader()
        self.dlg = self.loader.load("../Qt_Designer/heatmapchartdialog.ui")
        self.dlg.setWindowTitle("Chart generator")

        self.init_ui()
        self.bind_methods()

    # Initializing UI
    def init_ui(self):
        self.cancel_button = self.dlg.findChild(QPushButton, "cancelButton")
        self.generate_button = self.dlg.findChild(QPushButton, "generateButton")

    # Binding methods to UI widgets
    def bind_methods(self):
        if self.cancel_button:
            self.cancel_button.clicked.connect(self.dlg.reject)

        if self.generate_button:
            self.generate_button.clicked.connect(self.dlg.accept)

    def show_dialog(self):
        return self.dlg.exec()