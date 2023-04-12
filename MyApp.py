import sys
import os
from PyQt5.QtWidgets import (
    QMainWindow, QApplication, QWidget, QTableWidget, QTableWidgetItem,
    QLabel, QCheckBox, QComboBox, QListWidget, QLineEdit, QFileDialog,
    QLineEdit, QSpinBox, QDoubleSpinBox, QSlider, QGridLayout, QPushButton, QStyleOptionTitleBar
)
from PyQt5.QtCore import Qt
from pathlib import Path
import pandas as pd
import numpy as np
import traceback


class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()

        self.setWindowTitle("My App")
        self.setMinimumSize(1000, 600)
        self.setMaximumSize(1200, 600)

        # Creating layout
        layout = QGridLayout()
        self.central_widget = QLabel()
        self.setCentralWidget(self.central_widget)
        self.central_widget.setLayout(layout)

        # file selection widgets
        self.file_label = QLabel('File:')
        self.file_browse = QPushButton('Browse')
        self.file_browse.clicked.connect(self.open_file_dialog)
        self.filename_edit = QLineEdit()

        # file selection widgets sizes
        self.file_browse.setFixedSize(50, 21)
        self.filename_edit.setFixedSize(400, 20)

        # check boxes
        self.check_box1 = QCheckBox("Basic Statistics")
        self.check_box2 = QCheckBox("Correlation Matrix")
        self.check_box3 = QCheckBox("Graphs")

        # run button
        self.run_button = QPushButton('RUN')
        self.run_button.setFixedSize(50,21)
        self.run_button.clicked.connect(self.run_process)

        # output
        self.metadata_shape = QLabel()
        self.metadata_info = QTableWidget()

        # Adding widgets to layout
        layout.addWidget(self.file_label, 0, 0)
        layout.addWidget(self.filename_edit, 0, 1)
        layout.addWidget(self.file_browse, 0, 2)
        layout.addWidget(self.check_box1, 1, 0)
        layout.addWidget(self.check_box2, 1, 1)
        layout.addWidget(self.check_box3, 2, 0)
        layout.addWidget(self.run_button, 5, 2)
        layout.addWidget(self.metadata_shape, 7, 0, 1, 3)
        layout.addWidget(self.metadata_info, 8, 0, 1, 3)

        # Set layout alignment
        layout.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        # Add empty cells to push filename_edit to the left
        layout.setColumnStretch(5, 2)

    def open_file_dialog(self):
        filename, _ = QFileDialog.getOpenFileName(
            self,
            "Select a File",
            str(Path.home()),
            "All Files (*.csv; *.xlsx);"
        )
        if filename:
            if os.path.isfile(filename) and os.access(filename, os.R_OK):
                path = Path(filename)
                self.filename_edit.setText(str(path))
            else:
                error_dialog = QLabel("Selected file is not valid or you don't have permission to access it.")
                error_dialog.exec_()

    def run_process(self):
        file_ext = self.filename_edit.text().split('.')[-1]
        if file_ext == 'xlsx':
            try:
                df = pd.read_excel(self.filename_edit.text())
            except Exception as e:
                print("Error reading Excel file:")
                traceback.print_exc()
                return
        elif file_ext == 'csv':
            try:
                df = pd.read_csv(self.filename_edit.text(), low_memory=False)
            except Exception as e:
                print("Error reading CSV file:")
                traceback.print_exc()
                return
        df.describe(include=[np.number])
        metadata_shape = str(df.shape)
        self.metadata_shape.setText(metadata_shape)

        # create table from
        metadata_info = df.describe(include=[np.number]).reset_index()
        self.metadata_info.setRowCount(metadata_info.shape[0])
        self.metadata_info.setColumnCount(metadata_info.shape[1])
        for i in range(metadata_info.shape[0]):
            for j in range(metadata_info.shape[1]):
                self.metadata_info.setItem(i, j, QTableWidgetItem(str(metadata_info.iloc[i, j])))

        # set table headers
        headers = [str(col) for col in metadata_info.columns]
        self.metadata_info.setHorizontalHeaderLabels(headers)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    app.exec_()
