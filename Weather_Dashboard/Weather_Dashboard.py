import pandas as pd
from PySide6.QtWidgets import QApplication, QMainWindow, QTableView, QPushButton, QLabel, QFileDialog, QComboBox
from PySide6.QtUiTools import QUiLoader
from TableModel import TableModel

# MainWindow
class MainWindow:
    def __init__(self):
        self.app = QApplication()
        self.loader = QUiLoader()
        self.window = self.loader.load("../Qt_Designer/mainwindow.ui", None)
        self.data_path = None
        self.df = pd.DataFrame()
        self.model = None

        # GUI Initialization
        self.load_csv_button = self.window.findChild(QPushButton, "loadCSVButton")
        self.table = self.window.findChild(QTableView, "dataTable")
        self.filter_button = self.window.findChild(QPushButton, "filterButton")
        self.combo_box = self.window.findChild(QComboBox, "comboBox")
        self.combo_box.addItem("All")

        # Binding methods to buttons
        if self.load_csv_button:
            self.load_csv_button.clicked.connect(self.load_data)

        if self.filter_button:
            self.filter_button.clicked.connect(self.filter_data)

        # Binding methods to comboBox
        self.combo_box.activated.connect(self.check_index)

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
        columns = df.columns
        for column in columns:
            self.combo_box.addItem(column)

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
            print("First choose file")
        else:
            if self.check_index() == 0:
                self.display_data(self.df)
            elif self.check_index() == 1:
                self.display_data(self.df[["Temperature[C]"]])
            elif self.check_index() == 2:
                self.display_data(self.df[["Precipitation"]])
            elif self.check_index() == 3:
                self.display_data(self.df[["Wind"]])


    # Showing data on tabel
    def display_data(self, df):
        self.model = TableModel(df)
        self.table.setModel(self.model)
        self.table.resizeColumnsToContents()

    # Run application
    def run(self):
        self.window.show()
        self.app.exec()

