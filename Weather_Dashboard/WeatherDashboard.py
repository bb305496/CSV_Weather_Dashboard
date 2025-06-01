import pandas as pd
from PySide6.QtWidgets import QApplication, QTableView, QPushButton, QFileDialog, QComboBox, QCheckBox, QLabel, QDialog, QLineEdit, QMessageBox, QDoubleSpinBox
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QTimer
from TableModel import TableModel
from GeneratePlotChartDialog import PlotChartDialog
from GenerateScatterChartDialog import ScatterCharDialog
from GenerateHeatmapChartDialog import HeatmapChartDialog
from EmptyDatadrameDialog import EmptyDataFrameDialog
from WarningDialog import WarningDialog
import matplotlib.pyplot as plt
import matplotlib

matplotlib.use('QtAgg')

# MainWindow
class MainWindow:
    def __init__(self):
        self.app = QApplication()
        self.loader = QUiLoader()
        self.window = self.loader.load("../Qt_Designer/mainwindow.ui", None)
        self.window.setWindowTitle("Weather Dashboard")
        self.data_path = None
        self.df = pd.DataFrame()
        self.filtered_df = pd.DataFrame()
        self.model = None
        self.columns = None
        self.show_pressed = False
        self.filter_pressed = False
        self.available_charts = ["Plot chart", "Scatter chart", "Heatmap"]

        self.init_ui()
        self.bind_methods()


    # Binding methods to UI widgets
    def bind_methods(self):
        # Binding methods to buttons
        if self.load_csv_button:
            self.load_csv_button.clicked.connect(self.load_data)

        if self.filter_button:
            self.filter_button.clicked.connect(self.show_single_column)

        if self.calc_button:
            self.calc_button.clicked.connect(self.what_calc_selected)
            #self.calc_button.clicked.connect(self.calc_max)
            #self.calc_button.clicked.connect(self.calc_min)

        if self.generate_button:
            self.generate_button.clicked.connect(self.open_chart_dialog)

        if self.count_button:
            self.count_button.clicked.connect(self.count_columns)

        # Binding methods to comboBox
        if self.combo_box:
            self.combo_box.activated.connect(self.check_index)

        # Binding methods to checksBox
        if self.avg_check_box:
            self.avg_check_box.stateChanged.connect(self.is_avg_selected)

        if self.max_check_box:
            self.max_check_box.stateChanged.connect(self.is_max_selected)

        if self.min_check_box:
            self.min_check_box.stateChanged.connect(self.is_min_selected)

        if self.lower_filter_button:
            self.lower_filter_button.clicked.connect(self.filter_data)

        if self.export_tocsv_button:
            self.export_tocsv_button.clicked.connect(self.save_data)

    def count_columns(self):
        if self.df.empty:
            self.show_warning_no_csv_dialogue()
        else:
            if self.show_pressed:
                self.count_df_columns()
            elif self.filter_pressed:
                self.count_filtered_df_columns()

    def count_df_columns(self):
        if self.check_index() == 0:
            self.count_label.setText(f"Number of: \n{self.df.count().to_string()}")
        else:
            column = self.check_text()
            df_count = self.df[[column]].count()
            self.count_label.setText(f"Number of: \n{df_count.to_string()}")

    def count_filtered_df_columns(self):
        if self.gen_csv_combo_box_1.currentText() == "All":
            self.count_label.setText(f"Number of: \n{self.filtered_df.count().to_string()}")
        else:
            column = self.gen_csv_combo_box_1.currentText()
            df_count = self.filtered_df[[column]].count()
            self.count_label.setText(f"Number of: \n{df_count.to_string()}")

    def filter_data(self):
        if not self.df.empty:
            data_to_show = self.gen_csv_combo_box_1.currentText()
            filtered_data = self.gen_csv_combo_box_2.currentText()
            sign = self.gen_csv_combo_box_3.currentText()
            value = self.value_spin_box.value()
            #print(type(data_to_show), type(filtered_data), type(sign), type(value))

            if value != "":
                self.filter_pressed = True
                self.show_pressed = False
                if data_to_show == "All":
                    if sign == "=":
                        self.filtered_df = self.df[self.df[filtered_data] == value]
                        self.display_data(self.filtered_df)
                    if sign == ">":
                        self.filtered_df = self.df[self.df[filtered_data] > value]
                        self.display_data(self.filtered_df)
                    if sign == "<":
                        self.filtered_df = self.df[self.df[filtered_data] < value]
                        self.display_data(self.filtered_df)
                    if sign == "≥":
                        self.filtered_df = self.df[self.df[filtered_data] >= value]
                        self.display_data(self.filtered_df)
                    if sign == "≤":
                        self.filtered_df = self.df[self.df[filtered_data] <= value]
                        self.display_data(self.filtered_df)
                    if sign == "≠":
                        self.filtered_df = self.df[self.df[filtered_data] != value]
                        self.display_data(self.filtered_df)

                else:
                    if sign == "=":
                        self.filtered_df = self.df[[data_to_show]][self.df[filtered_data] == value]
                        self.display_data(self.filtered_df)
                    if sign == ">":
                        self.filtered_df = self.df[[data_to_show]][self.df[filtered_data] > value]
                        self.display_data(self.filtered_df)
                    if sign == "<":
                        self.filtered_df = self.df[[data_to_show]][self.df[filtered_data] < value]
                        self.display_data(self.filtered_df)
                    if sign == "≥":
                        self.filtered_df = self.df[[data_to_show]][self.df[filtered_data] >= value]
                        self.display_data(self.filtered_df)
                    if sign == "≤":
                        self.filtered_df = self.df[[data_to_show]][self.df[filtered_data] <= value]
                        self.display_data(self.filtered_df)
                    if sign == "≠":
                        self.filtered_df = self.df[[data_to_show]][self.df[filtered_data] != value]
                        self.display_data(self.filtered_df)

            else:
                self.highlight_empty_value_field()
                print("Wpisz wartość")
        else:
            self.show_warning_no_csv_dialogue()

    def highlight_empty_value_field(self):
        self.lower_filter_button.setEnabled(False)
        for i in range(3):
            QTimer.singleShot(i * 500, self.pulse_red_field)

        QTimer.singleShot(1500, lambda: self.lower_filter_button.setEnabled(True))

    def pulse_red_field(self):
        original_style = self.value_spin_box.styleSheet()

        self.value_spin_box.setStyleSheet("""QLineEdit {background-color: #ff9999; border: 1px solid red;}""")

        QTimer.singleShot(250, lambda: self.value_spin_box.setStyleSheet(original_style))


    # Opening chart dialog
    def open_chart_dialog(self):
        if self.df.empty:
            self.show_warning_no_csv_dialogue()
        elif self.combo_box2.currentText() == self.available_charts[0]:
            if self.show_pressed:
                self.show_plot_chart_dialog(self.df)
            elif self.filter_pressed:
                self.show_plot_chart_dialog(self.filtered_df)
        elif self.combo_box2.currentText() == self.available_charts[1]:
            if self.show_pressed:
                self.show_scatter_chart_dialog(self.df)
            elif self.filter_pressed:
                self.show_scatter_chart_dialog(self.filtered_df)
        elif self.combo_box2.currentText() == self.available_charts[2]:
            if self.show_pressed:
                self.show_heatmap_chart_dialog()
        else:
            #TODO more charts
            # Pie Plot
            # Area Plot
            # Bar Graph
            # Histogram
            # Box Plot
            print("Wrong Combobox")

    def show_heatmap_chart_dialog(self):
        dialog = HeatmapChartDialog()
        result = dialog.show_dialog()

        if result == QDialog.Accepted:
            print("Accept")
        elif result == QDialog.Rejected:
            print("Cancel")

    def show_scatter_chart_dialog(self, df: pd.DataFrame):
        dialog = ScatterCharDialog(df.columns)
        result = dialog.show_dialog()

        if result == QDialog.Accepted:
            print("Accept")
            first_value = dialog.actual_first_value()
            second_value = dialog.actual_second_value()
            x_axis = dialog.xaxis_value()
            title = dialog.get_title()
            x_axis_name = dialog.get_x_axis_name()
            y_axis_name = dialog.get_y_axis_name()

            plt.scatter(df[x_axis], df[first_value], label= first_value)
            if second_value != "None":
                plt.scatter(df[x_axis], df[second_value], label= second_value)
            if title:
                plt.title(title)
            if x_axis_name:
                plt.xlabel(x_axis_name)
            if y_axis_name:
                plt.ylabel(y_axis_name)
            if dialog.is_legend_selected():
                plt.legend(loc="lower left")
            if dialog.is_grid_selected():
                plt.grid()

            plt.tight_layout()
            plt.show()

        elif result == QDialog.Rejected:
            print("Cancel")

    def show_plot_chart_dialog(self, df: pd.DataFrame):
        dialog = PlotChartDialog(df.columns)
        result = dialog.show_dialog()

        if result == QDialog.Accepted:
            print("Accept")
            x_axis = dialog.actual_combobox_x_item()
            y_axis = dialog.actual_combobox_y_item()
            x2_axis = dialog.actual_combobox_x2_item()
            y2_axis = dialog.actual_combobox_y2_item()
            x_axis_name = dialog.get_xaxis_name()
            y_axis_name = dialog.get_yaxis_name()
            title = dialog.get_title()

            print(x2_axis)

            plt.plot(df[x_axis], df[y_axis], label=y_axis_name if y_axis_name else y_axis)
            if x2_axis != "None" and y2_axis != "None":
                plt.plot(df[x2_axis], df[y2_axis], label=y2_axis)
            elif x2_axis != "None":
                plt.plot(df[x2_axis], df[y_axis], label=x2_axis)
            elif y2_axis != "None":
                plt.plot(df[x_axis], df[y2_axis], label=y2_axis)
            if x_axis_name:
                plt.xlabel(x_axis_name)
            if y_axis_name:
                plt.ylabel(y_axis_name)
            if title:
                plt.title(title)
            if dialog.is_legend_selected():
                plt.legend(loc="lower left")
            if dialog.is_grid_selected():
                plt.grid()
            plt.tight_layout()
            plt.show()

        elif result == QDialog.Rejected:
            print("Cancel")

    def is_avg_selected(self) -> bool:
        print(self.avg_check_box.isChecked())
        return self.avg_check_box.isChecked()

    def is_max_selected(self) -> bool:
        print(self.max_check_box.isChecked())
        return self.max_check_box.isChecked()

    def is_min_selected(self) -> bool:
        print(self.min_check_box.isChecked())
        return self.min_check_box.isChecked()

    def show_warning_no_csv_dialogue(self):
        dialog = EmptyDataFrameDialog()
        result = dialog.show_dialog()

        if result == QDialog.Accepted:
            print("OK pressed")

    def show_warning_dialog(self, warning_text, font_size: int = 16):
        dialog = WarningDialog(warning_text, font_size)
        result = dialog.show_dialog()

        if result == QDialog.Accepted:
            print("OK pressed")

    def what_calc_selected(self):
        if self.is_avg_selected():
            self.calc_avg()
        if self.is_max_selected():
            self.calc_max()
        if self.is_min_selected():
            self.calc_min()
        if self.df.empty:
            self.show_warning_no_csv_dialogue()
        elif not self.is_avg_selected() and not self.is_max_selected() and not self.is_min_selected():
            self.highlight_checkboxes()
            print("Select minimum 1")

    def highlight_checkboxes(self):
        self.calc_button.setEnabled(False)
        checkboxes = [self.avg_check_box, self.max_check_box, self.min_check_box]

        for i in range(3):
            QTimer.singleShot(i * 500, lambda: self.pulse_red_checkboxes(checkboxes))

        QTimer.singleShot(1500, lambda: self.calc_button.setEnabled(True))

    def pulse_red_checkboxes(self, checkboxes):
        original_styles = []
        for checkbox in checkboxes:
            original_styles.append(checkbox.styleSheet())

        for checkbox in checkboxes:
            checkbox.setStyleSheet("""QCheckBox::indicator {border: 2px solid #ff4444;}""")

        QTimer.singleShot(250, lambda: self.restore_checkbox_styles(checkboxes, original_styles))

    def restore_checkbox_styles(self, checkboxes, original_styles):
        for checkbox, style in zip(checkboxes, original_styles):
            checkbox.setStyleSheet(style)

    def calc_avg(self):
        if not self.df.empty:
            if self.avg_check_box.isChecked():
                if self.check_index() == 0:
                    self.label.setText(f"Average value: \n{self.df.mean().to_string()}")
                else:
                    column = self.check_text()
                    df_mean = self.df[[column]].mean()
                    self.label.setText(f"Average value: \n{df_mean.to_string()}")

    def calc_max(self):
        if not self.df.empty:
            if self.max_check_box.isChecked():
                if self.check_index() == 0:
                    self.label_2.setText(f"Max value: \n{self.df.max().to_string()}")
                else:
                    column = self.check_text()
                    df_mean = self.df[[column]].max()
                    self.label_2.setText(f"Max value: \n{df_mean.to_string()}")

    def calc_min(self):
        if not self.df.empty:
            if self.min_check_box.isChecked():
                if self.check_index() == 0:
                    self.label_3.setText(f"Min value: \n{self.df.min().to_string()}")
                else:
                    column = self.check_text()
                    df_mean = self.df[[column]].min()
                    self.label_3.setText(f"Min value: \n{df_mean.to_string()}")

    def save_data(self):
        if not self.filtered_df.empty:
            file_patch = QFileDialog.getSaveFileName(None, "Save CSV file", "", "Data Files (*.csv)")
            print(file_patch)

            if file_patch:
                try:
                    self.filtered_df.to_csv(file_patch[0], index=False, sep=";")
                except:
                    print("Saving data ERROR")
        else:
            self.show_warning_dialog("No Filtered Data")
            print("No df")

    # Loading data from csv file
    def load_data(self):
        # Open File Dialog
        fname = QFileDialog.getOpenFileName(parent=None, caption="Open Data File", dir="../Data", filter="Data Files (*.csv)")

        # Loading data from csv
        # Separator is ";" for Polish Excel version, remove if using English version
        if fname:
            self.data_path = fname[0]
            if len(self.data_path) != 0:
                self.df = pd.read_csv(self.data_path, sep=";")
                self.display_data(self.df)
                self.add_items_to_combobox(self.df)
                self.show_pressed = True
            else:
                print("Operation canceled")

    # Dynamic adding items to combo box by loading csv file headers
    def add_items_to_combobox(self, df: pd.DataFrame):
        self.columns = df.columns
        self.clear_combobox(self.combo_box)
        self.clear_combobox(self.gen_csv_combo_box_1)
        self.gen_csv_combo_box_2.clear()
        for column in self.columns:
            self.combo_box.addItem(column)
            self.gen_csv_combo_box_1.addItem(column)
            self.gen_csv_combo_box_2.addItem(column)

    # Adding "= < > <= >="sign to combo box
    def add_inequality_sign(self, combo_box: QComboBox):
        combo_box.addItem("=")
        combo_box.addItem("<")
        combo_box.addItem(">")
        combo_box.addItem("≥")
        combo_box.addItem("≤")
        combo_box.addItem("≠")

    # Adding available charts to combo box
    def add_charts_to_combobox(self):
        for chart in self.available_charts:
            self.combo_box2.addItem(chart)


    # Clearing comboBox
    def clear_combobox(self, combobox: QComboBox):
        combobox.clear()
        combobox.addItem("All")

    # Checking current comboBox index
    def check_index(self) -> int:
        cindex = self.combo_box.currentIndex()
        print(f"currentIndex {cindex}")
        return cindex

    # Checking current comboBox text
    def check_text(self) -> str:
        ctext = self.combo_box.currentText()
        print(f"currentText {ctext}")
        return ctext

    # Filtering data by column
    def show_single_column(self):
        if self.df.empty:
            self.show_warning_no_csv_dialogue()
        else:
            if self.check_index() == 0:
                self.display_data(self.df)
                self.show_pressed = True
                self.filter_pressed = False
            else:
                column = self.check_text()
                self.display_data(self.df[[column]])
                self.show_pressed = True
                self.filter_pressed = False

    # Initializing UI
    def init_ui(self):
        # GUI Initialization
        self.load_csv_button = self.window.findChild(QPushButton, "loadCSVButton")
        self.table = self.window.findChild(QTableView, "dataTable")
        self.filter_button = self.window.findChild(QPushButton, "filterButton")
        self.generate_button = self.window.findChild(QPushButton, "generateButton")
        self.combo_box = self.window.findChild(QComboBox, "comboBox")
        self.combo_box.addItem("All")
        self.combo_box2 = self.window.findChild(QComboBox, "comboBox_2")
        self.add_charts_to_combobox()
        self.avg_check_box = self.window.findChild(QCheckBox, "AVGCheckBox")
        self.max_check_box = self.window.findChild(QCheckBox, "MAXCheckBox")
        self.min_check_box = self.window.findChild(QCheckBox, "MINCheckBox")
        self.label = self.window.findChild(QLabel, "label")
        self.label_2 = self.window.findChild(QLabel, "label_2")
        self.label_3 = self.window.findChild(QLabel, "label_3")
        self.calc_button = self.window.findChild(QPushButton, "calcButton")
        self.gen_csv_combo_box_1 = self.window.findChild(QComboBox, "comboBox_3")
        self.gen_csv_combo_box_1.addItem("All")
        self.gen_csv_combo_box_2 = self.window.findChild(QComboBox, "comboBox_4")
        self.gen_csv_combo_box_3 = self.window.findChild(QComboBox, "comboBox_5")
        self.add_inequality_sign(self.gen_csv_combo_box_3)
        self.value_spin_box = self.window.findChild(QDoubleSpinBox, "doubleSpinBox")
        self.lower_filter_button = self.window.findChild(QPushButton, "Filter1Button")
        self.export_tocsv_button = self.window.findChild(QPushButton, "exportCSVButton")
        self.count_button = self.window.findChild(QPushButton, "countPushButton")
        self.count_label = self.window.findChild(QLabel, "countLabel")

    # Showing data on tabel
    def display_data(self, df):
        self.model = TableModel(df)
        self.table.setModel(self.model)
        self.table.resizeColumnsToContents()

    # Run application
    def run(self):
        self.window.show()
        self.app.exec()

