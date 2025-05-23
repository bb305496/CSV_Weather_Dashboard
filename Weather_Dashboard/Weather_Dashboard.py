import pandas as pd
from PySide6.QtWidgets import QApplication, QMainWindow, QTableView, QPushButton, QLabel, QFileDialog
from PySide6.QtUiTools import QUiLoader
from TableModel import TableModel

# MainWindow
class MainWindow:
    def __init__(self):
        self.app = QApplication()
        self.loader = QUiLoader()
        self.window = self.loader.load("../Qt_Designer/mainwindow.ui", None)
        self.data_path = None
        self.df = None
        self.model = None

        self.load_csv_button = self.window.findChild(QPushButton, "loadCSVButton")
        self.table = self.window.findChild(QTableView, "dataTable")

        if self.load_csv_button:
            self.load_csv_button.clicked.connect(self.load_data)

    def load_data(self):
        # Open File Dialog
        fname = QFileDialog.getOpenFileName(parent=None, caption="Open Data File", dir="../Data", filter="Data Files (*.csv)")

        # Loading data from csv
        # Separator is ";" for Polish Excel version, remove if using English version
        if fname:
            self.data_path = fname[0]
            self.df = pd.read_csv(self.data_path, sep=";")
            self.display_data(self.df)

    # Showing data on tabel
    def display_data(self, df):
        self.model = TableModel(self.df[:100])
        self.table.setModel(self.model)

    # Run application
    def run(self):
        self.window.show()
        self.app.exec()

