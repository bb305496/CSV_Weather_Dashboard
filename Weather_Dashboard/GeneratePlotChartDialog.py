from PySide6.QtWidgets import QDialog, QPushButton, QComboBox
from PySide6.QtUiTools import QUiLoader
import pandas as pd

class PlotChartDialog(QDialog):
    def __init__(self, colums: pd.DataFrame):
        super().__init__()
        self.loader = QUiLoader()
        self.dlg = self.loader.load("../Qt_Designer/chartdialog.ui")
        self.dlg.setWindowTitle("Chart generator")
        self.colums = colums

        self.init_ui()
        self.add_items_to_combobox()
        self.bind_methods()

    # Adding data to combobox
    def add_items_to_combobox(self):
        for colum in self.colums:
            self.xaxis_combo_box.addItem(colum)
            self.yaxis_combo_box.addItem(colum)

    def show_dialog(self):
        return self.dlg.exec_()

    # Initializing UI
    def init_ui(self):
        self.cancel_button = self.dlg.findChild(QPushButton, "cancelButton")
        self.generate_button = self.dlg.findChild(QPushButton, "generateButton")
        self.xaxis_combo_box = self.dlg.findChild(QComboBox, "xAxisComboBox")
        self.yaxis_combo_box = self.dlg.findChild(QComboBox, "yAxisComboBox")

    # Binding methods to UI widgets
    def bind_methods(self):
        if self.cancel_button:
            self.cancel_button.clicked.connect(self.dlg.reject)

        if self.generate_button:
            self.generate_button.clicked.connect(self.dlg.accept)