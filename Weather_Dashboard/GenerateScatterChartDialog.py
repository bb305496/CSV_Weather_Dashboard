from PySide6.QtWidgets import QDialog, QPushButton, QComboBox
from PySide6.QtUiTools import QUiLoader
import pandas as pd


class ScatterCharDialog(QDialog):
    def __init__(self, colums: pd.DataFrame):
        super().__init__()
        self.loader = QUiLoader()
        self.dlg = self.loader.load("../Qt_Designer/scatterchartdialog.ui")
        self.dlg.setWindowTitle("Chart generator")
        self.colums = colums

        self.init_ui()
        self.add_items_to_combobox()
        self.bind_methods()


    def add_items_to_combobox(self):
        for colum in self.colums:
            self.first_value_combo_box.addItem(colum)
            self.second_value_combo_box.addItem(colum)
            self.xaxis_combo_box.addItem(colum)

    def actual_first_value(self) -> str:
        return self.first_value_combo_box.currentText()

    def actual_second_value(self) -> str:
        return self.second_value_combo_box.currentText()

    def xaxis_value(self) -> str:
        return self.xaxis_combo_box.currentText()

    def show_dialog(self):
        return self.dlg.exec()

    # Initializing UI
    def init_ui(self):
        self.cancel_button = self.dlg.findChild(QPushButton, "cancelButton")
        self.generate_button = self.dlg.findChild(QPushButton, "generateButton")
        self.first_value_combo_box = self.dlg.findChild(QComboBox, "firstValuecomboBox")
        self.second_value_combo_box = self.dlg.findChild(QComboBox, "secondValuecomboBox")
        self.xaxis_combo_box = self.dlg.findChild(QComboBox, "xAxiscomboBox")

    # Binding methods to UI widgets
    def bind_methods(self):
        if self.cancel_button:
            self.cancel_button.clicked.connect(self.dlg.reject)

        if self.generate_button:
            self.generate_button.clicked.connect(self.dlg.accept)