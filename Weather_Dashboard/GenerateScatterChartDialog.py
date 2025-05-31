from PySide6.QtWidgets import QDialog, QPushButton, QComboBox, QLineEdit, QCheckBox
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

    def get_title(self) -> str:
        return self.title_line_edit.text()

    def get_x_axis_name(self) -> str:
        return self.x_axis_name.text()

    def get_y_axis_name(self) -> str:
        return self.y_axis_name.text()

    def is_legend_selected(self) -> bool:
        return self.legend_check_box.isChecked()

    def is_grid_selected(self) -> bool:
        return self.grid_check_box.isChecked()

    def show_dialog(self):
        return self.dlg.exec()

    # Initializing UI
    def init_ui(self):
        self.cancel_button = self.dlg.findChild(QPushButton, "cancelButton")
        self.generate_button = self.dlg.findChild(QPushButton, "generateButton")
        self.first_value_combo_box = self.dlg.findChild(QComboBox, "firstValuecomboBox")
        self.second_value_combo_box = self.dlg.findChild(QComboBox, "secondValuecomboBox")
        self.second_value_combo_box.addItem("None")
        self.xaxis_combo_box = self.dlg.findChild(QComboBox, "xAxiscomboBox")
        self.title_line_edit = self.dlg.findChild(QLineEdit, "titleLineEdit")
        self.title_line_edit.setPlaceholderText("Leave empty to skip Title label")
        self.x_axis_name = self.dlg.findChild(QLineEdit, "xAxislineEdit")
        self.x_axis_name.setPlaceholderText("Leave empty to skip X-axis label")
        self.y_axis_name = self.dlg.findChild(QLineEdit, "yAxislineEdit")
        self.y_axis_name.setPlaceholderText("Leave empty to skip Y-axis label")
        self.legend_check_box = self.dlg.findChild(QCheckBox, "legendCheckBox")
        self.grid_check_box = self.dlg.findChild(QCheckBox, "gridCheckBox")

    # Binding methods to UI widgets
    def bind_methods(self):
        if self.cancel_button:
            self.cancel_button.clicked.connect(self.dlg.reject)

        if self.generate_button:
            self.generate_button.clicked.connect(self.dlg.accept)