import pandas as pd
from PySide6.QtWidgets import QApplication, QTableView, QPushButton, QFileDialog, QComboBox, QCheckBox, QLabel, QDialog
from PySide6.QtUiTools import QUiLoader
from TableModel import TableModel
from GeneratePlotChartDialog import PlotChartDialog
from EmptyDatadrameDialog import EmptyDataFrameDialog
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
        self.model = None
        self.columns = None
        self.available_charts = ["Plot chart", "Scatter chart"]

        self.init_ui()
        self.bind_methods()


    # Binding methods to UI widgets
    def bind_methods(self):
        # Binding methods to buttons
        if self.load_csv_button:
            self.load_csv_button.clicked.connect(self.load_data)

        if self.filter_button:
            self.filter_button.clicked.connect(self.filter_data)

        if self.calc_button:
            self.calc_button.clicked.connect(self.what_calc_selected)
            #self.calc_button.clicked.connect(self.calc_max)
            #self.calc_button.clicked.connect(self.calc_min)

        if self.generate_button:
            self.generate_button.clicked.connect(self.open_chart_dialog)

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

    # Opening chart dialog
    def open_chart_dialog(self):
        if self.df.empty:
            self.show_warning_no_csv_dialogue()
        elif self.combo_box2.currentText() == self.available_charts[0]:
            dialog = PlotChartDialog(self.df.columns)
            result = dialog.show_dialog()

            if result == QDialog.Accepted:
                print("Accept")
                x_axis = dialog.actual_combobox_x_item()
                y_axis = dialog.actual_combobox_y_item()
                x_axis_name = dialog.get_xaxis_name()
                y_axis_name = dialog.get_yaxis_name()
                title = dialog.get_title()

                plt.plot(self.df[x_axis], self.df[y_axis], label=y_axis_name if y_axis_name else y_axis)
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
                plt.show()

            elif result == QDialog.Rejected:
                print("Cancel")
        else:
            #TODO Scatter plot
            print("Wrong Combobox")


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

    def what_calc_selected(self):
        if self.is_avg_selected():
            self.calc_avg()
        if self.is_max_selected():
            self.calc_max()
        if self.is_min_selected():
            self.calc_min()
        if self.df.empty:
            self.show_warning_no_csv_dialogue()
        else:
            #TODO Dialog
            print("Select minimum 1")

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
            else:
                print("Operation canceled")

    # Dynamic adding items to combo box by loading csv file headers
    def add_items_to_combobox(self, df: pd.DataFrame):
        self.columns = df.columns
        self.clear_combobox(self.combo_box)
        for column in self.columns:
            self.combo_box.addItem(column)

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
    def filter_data(self):
        if self.df.empty:
            self.show_warning_no_csv_dialogue()
        else:
            if self.check_index() == 0:
                self.display_data(self.df)
            else:
                column = self.check_text()
                self.display_data(self.df[[column]])

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

    # Showing data on tabel
    def display_data(self, df):
        self.model = TableModel(df)
        self.table.setModel(self.model)
        self.table.resizeColumnsToContents()

    # Run application
    def run(self):
        self.window.show()
        self.app.exec()

