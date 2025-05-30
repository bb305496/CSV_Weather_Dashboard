from PySide6.QtWidgets import QDialog, QPushButton, QComboBox, QLineEdit, QCheckBox
from PySide6.QtUiTools import QUiLoader
import pandas as pd

class PlotChartDialog(QDialog):
    def __init__(self, colums: pd.DataFrame):
        super().__init__()
        self.loader = QUiLoader()
        self.dlg = self.loader.load("../Qt_Designer/plotchartdialog.ui")
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

    def actual_combobox_x_item(self) -> str:
        return self.xaxis_combo_box.currentText()

    def actual_combobox_y_item(self) -> str:
        return self.yaxis_combo_box.currentText()

    def get_xaxis_name(self) -> str:
        return self.xaxis_line_edit.text()

    def get_yaxis_name(self) -> str:
        return self.yaxis_line_edit.text()

    def get_title(self) -> str:
        return self.title_line_edit.text()

    def is_legend_selected(self) -> bool:
        return self.legend_check_box.isChecked()

    def is_grid_selected(self) -> bool:
        return self.legend_check_box.isChecked()

    def show_dialog(self):
        return self.dlg.exec()


    # Initializing UI
    def init_ui(self):
        self.cancel_button = self.dlg.findChild(QPushButton, "cancelButton")
        self.generate_button = self.dlg.findChild(QPushButton, "generateButton")
        self.xaxis_combo_box = self.dlg.findChild(QComboBox, "xAxisComboBox")
        self.yaxis_combo_box = self.dlg.findChild(QComboBox, "yAxisComboBox")
        self.xaxis_line_edit = self.dlg.findChild(QLineEdit, "xAxisLineEdit")
        self.xaxis_line_edit.setPlaceholderText("Leave empty to skip X-axis label")
        self.yaxis_line_edit = self.dlg.findChild(QLineEdit, "yAxisLineEdit")
        self.yaxis_line_edit.setPlaceholderText("Leave empty to skip Y-axis label")
        self.title_line_edit = self.dlg.findChild(QLineEdit, "titleLineEdit")
        self.title_line_edit.setPlaceholderText("Leave empty to skip Title label")
        self.legend_check_box = self.dlg.findChild(QCheckBox, "legendCheckBox")
        self.grid_check_box = self.dlg.findChild(QCheckBox, "gridCheckBox")


    # Binding methods to UI widgets
    def bind_methods(self):
        if self.cancel_button:
            self.cancel_button.clicked.connect(self.dlg.reject)

        if self.generate_button:
            self.generate_button.clicked.connect(self.dlg.accept)
