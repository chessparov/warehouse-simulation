import pandas as pd
from pathlib import Path
from PyQt5 import QtGui
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
import Visualization


class TMainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.timer = None
        self.clock = None
        self.counter = int(0)
        self.setWindowTitle("Warehouse DES Info")
        self.setWindowIcon(QtGui.QIcon('Images/Icon.jpg'))
        self.setGeometry(1200, 100, 600, 600)
        self.initUI()

    def initUI(self):

        # Title
        title = QLabel(self)
        title.setText("Delivered items")
        title.move(50, 50)
        title.setAlignment(Qt.AlignLeft)
        font = QFont("Segoe UI", 18)
        title.setFont(font)
        title.setFixedSize(500, 100)

        # Time the clock
        self.clock = QLabel("0", self)
        clock_label = QLabel(self)
        self.clock.setFont(QFont("Segoe UI", 18))
        clock_label.setFont(QFont("Segoe UI", 18))
        self.clock.move(400, 90)
        clock_label.move(400, 50)
        self.beginTimer()
        clock_label.setText('Elapsed time')
        clock_label.adjustSize()

        # Create label
        layout = QVBoxLayout(self)

        # Add item labels
        path_name = Path(r'.\items_log.csv')
        dtfData = pd.read_csv(path_name)

        for i, item in enumerate(dtfData['Item']):
            art_label = QLabel(self)
            art_label.setFont(QFont("Segoe UI", 14))
            art_label.setText(item)
            art_label.move(50, 130 + 25 * i)
            art_label.setAlignment(Qt.AlignLeft)
            layout.addWidget(art_label)

        for j, time in enumerate(dtfData['Deliver Time']):
            deliv_time = QLabel(self)
            deliv_time.setFont(QFont("Segoe UI", 14))
            deliv_time.setText(str(time) + 's')
            deliv_time.move(200, 130 + 25 * j)
            deliv_time.setAlignment(Qt.AlignLeft)
            layout.addWidget(deliv_time)

        # Column titles
        col1_title = QLabel(self)
        column_font = QFont("Segoe UI", 13)
        column_font.setBold(True)
        col1_title.setFont(column_font)
        col1_title.setText('Item name')
        col1_title.move(50, 100)
        col1_title.setAlignment(Qt.AlignLeft)
        layout.addWidget(col1_title)

        col2_title = QLabel(self)
        col2_title.setFont(column_font)
        col2_title.setText('Deliver time')
        col2_title.move(200, 100)
        col2_title.setAlignment(Qt.AlignLeft)
        layout.addWidget(col2_title)

        # Add all the labels to the window
        layout.addWidget(title)
        layout.addWidget(clock_label)
        layout.addWidget(self.clock)
        self.setLayout(layout)

    # Clock
    def beginTimer(self):
        self.clock.setText(str(round(Visualization.elapsed_time/1000)) + ' s')



