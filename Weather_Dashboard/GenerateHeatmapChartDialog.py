from PySide6.QtWidgets import QDialog, QPushButton, QLineEdit, QComboBox
from PySide6.QtUiTools import QUiLoader
import pandas as pd

class HeatmapChartDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.loader = QUiLoader()
        self.dlg = self.loader.load("../Qt_Designer/heatmapchartdialog.ui")
        self.dlg.setWindowTitle("Chart generator")
        self.color_palette = ["rocket", "mako", "flare", "crest", "magma", "plasma", "inferno", "viridis", "cubehelix", "coolwarm", "Blues", "Reds", "Greens", "hot", "cool",
                              "spring", "summer", "autumn", "winter", "Spectral"]

        self.init_ui()
        self.add_colors_to_combo_box()
        self.bind_methods()

    def add_colors_to_combo_box(self):
        for color in self.color_palette:
            self.color_combo_box.addItem(color)

    def get_color(self) -> str:
        return self.color_combo_box.currentText()

    def get_title(self) -> str:
        return self.title_line_edit.text()

    def get_xaxis_name(self) -> str:
        return self.xaxis_line_edit.text()

    def get_yaxis_name(self) -> str:
        return self.yaxis_line_edit.text()

    # Initializing UI
    def init_ui(self):
        self.cancel_button = self.dlg.findChild(QPushButton, "cancelButton")
        self.generate_button = self.dlg.findChild(QPushButton, "generateButton")
        self.title_line_edit = self.dlg.findChild(QLineEdit, "titleLineEdit")
        self.title_line_edit.setPlaceholderText("Leave empty to skip Title label")
        self.xaxis_line_edit = self.dlg.findChild(QLineEdit, "xAxislineEdit")
        self.xaxis_line_edit.setPlaceholderText("Leave empty to skip X-axis label")
        self.yaxis_line_edit = self.dlg.findChild(QLineEdit, "yAxislineEdit")
        self.yaxis_line_edit.setPlaceholderText("Leave empty to skip Y-axis label")
        self.color_combo_box = self.dlg.findChild(QComboBox, "colorComboBox")

    # Binding methods to UI widgets
    def bind_methods(self):
        if self.cancel_button:
            self.cancel_button.clicked.connect(self.dlg.reject)

        if self.generate_button:
            self.generate_button.clicked.connect(self.dlg.accept)

    def show_dialog(self):
        return self.dlg.exec()