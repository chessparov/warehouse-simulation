import pandas as pd
from pathlib import Path
from PyQt5 import QtGui
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
import Visualization
import Variables as v


class TMainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.timer = None
        self.clock = None
        self.scroll = QScrollArea(self)
        self.widget = QWidget(self)
        self.layout = QVBoxLayout(self)
        self.counter = int(0)
        self.setWindowTitle("Warehouse DES Info")
        self.setWindowIcon(QtGui.QIcon('Images/Icon.jpg'))
        self.setGeometry(1200, 100, 600, 600)
        self.initUI()

    def initUI(self):

        # Create title
        title = QLabel(self)
        title.setText("Delivered items")
        title.move(50, 50)
        title.setAlignment(Qt.AlignLeft)
        font = QFont("Segoe UI", 18)
        title.setFont(font)
        title.setFixedSize(500, 100)

        # Create elapsed time counter
        self.clock = QLabel("0", self)
        clock_label = QLabel(self)
        self.clock.setFont(QFont("Segoe UI", 18))
        clock_label.setFont(QFont("Segoe UI", 18))
        self.clock.move(400, 90)
        clock_label.move(400, 50)
        self.beginTimer()
        clock_label.setText('Elapsed time')
        clock_label.adjustSize()

        # Create column titles
        column_font = QFont("Segoe UI", 13)
        column_font.setBold(True)

        col1_title = QLabel(self)
        col1_title.setFont(column_font)
        col1_title.setText('Item name')
        col1_title.move(50, 100)
        col1_title.setAlignment(Qt.AlignLeft)

        col2_title = QLabel(self)
        col2_title.setFont(column_font)
        col2_title.setText('Deliver time')
        col2_title.move(200, 100)
        col2_title.setAlignment(Qt.AlignLeft)

        # Add to the main layout all the static labels
        self.layout.addWidget(title)
        self.layout.addWidget(clock_label)
        self.layout.addWidget(self.clock)
        self.layout.addWidget(col1_title)
        self.layout.addWidget(col2_title)

        # Create item labels
        path_name = Path(r'.\items_log.csv')
        dtfData = pd.read_csv(path_name)

        # Create space for the item labels for the scrollable box
        layout = QHBoxLayout(self)
        lower_layout_left = QVBoxLayout(self)
        lower_layout_right = QVBoxLayout(self)

        for i, item in enumerate(dtfData['Item']):
            art_label = QLabel(self)
            art_label.setFont(QFont("Segoe UI", 14))
            art_label.setText(item)
            art_label.move(50, 130 + 25 * i)
            art_label.setAlignment(Qt.AlignLeft)
            art_label.adjustSize()
            lower_layout_left.addWidget(art_label)

        for j, time in enumerate(dtfData['Deliver Time']):
            deliv_time = QLabel(self)
            deliv_time.setFont(QFont("Segoe UI", 14))
            deliv_time.setText(str(time) + 's')
            deliv_time.move(200, 130 + 25 * j)
            deliv_time.setAlignment(Qt.AlignLeft)
            deliv_time.adjustSize()
            lower_layout_right.addWidget(deliv_time)

        # Add all the labels to the scrollable window
        layout.addLayout(lower_layout_left)
        layout.addLayout(lower_layout_right)
        self.widget.setLayout(layout)

        # Create scrollable box
        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll.setWidget(self.widget)
        self.scroll.setWidgetResizable(True)
        self.scroll.setFixedSize(300, 350)
        self.scroll.move(50, 160)

        self.layout.addWidget(self.scroll)
        self.setLayout(self.layout)

    # Clock
    def beginTimer(self):
        self.clock.setText(str(round(Visualization.elapsed_time / 1000)) + ' s')


class TInitialDialog(QDialog):

    def __init__(self):
        super().__init__()
        self.setWindowIcon(QtGui.QIcon('Images/Icon.jpg'))
        self.setWindowTitle("Setup")
        self.layout = QVBoxLayout(self)
        self.isSizeGripEnabled()
        self.setup()

    def setup(self):

        def setFPS():
            if checkString(fps_box.text()):
                v.FPS = float(fps_box.text())
                self.notifyVarChange(fps_box.text())
                fps_box.setText("")
            else:
                self.raiseInvalidInput()
                fps_box.setText("")

        def setSimTime():
            if checkString(sim_time_box.text()):
                v.SIM_TIME = int(sim_time_box.text())
                self.notifyVarChange(sim_time_box.text())
                sim_time_box.setText("")
            else:
                self.raiseInvalidInput()
                sim_time_box.setText("")

        def setNumWorkers():
            if checkString(workers_box.text()):
                v.NUM_WORKERS = int(workers_box.text())
                self.notifyVarChange(workers_box.text())
                workers_box.setText("")
            else:
                self.raiseInvalidInput()
                workers_box.setText("")

        def setMTBO():
            if checkString(mtbo_box.text()):
                v.MTBO = float(mtbo_box.text())
                self.notifyVarChange(mtbo_box.text())
                mtbo_box.setText("")
            else:
                self.raiseInvalidInput()
                mtbo_box.setText("")

        def checkString(text: str):

            if text != "":
                for char in text:
                    if char.isdecimal():
                        continue
                    if char == ".":
                        continue
                    else:
                        return False
                return True
            else:
                return False

        GRID_WIDTH = 200
        font = QFont("Segoe UI", 10)

        grid_layout = QGridLayout(self)

        # Create main layout
        main_layout = QVBoxLayout()
        title = QLabel()
        title_font = QFont("Segoe UI", 15)
        title_font.setBold(True)
        title.setFont(title_font)
        title.setAlignment(Qt.AlignCenter)
        title.setText("Insert simulation parameters")
        title.setMinimumHeight(80)
        main_layout.addWidget(title)

        # FPS input, label and confirm boxes
        fps_layout = QVBoxLayout()

        # Label
        fps_label = QLabel(self)
        fps_label.setFont(font)
        fps_label.setText("FPS (The higher the faster)")
        fps_label.setAlignment(Qt.AlignCenter)

        # Typing box
        fps_box = QLineEdit(self)
        fps_box.setPlaceholderText("21.93")
        fps_box.setMinimumWidth(GRID_WIDTH)

        # Confirm button
        fps_button = QPushButton(self)
        fps_button.setText("OK")
        fps_button.clicked.connect(setFPS)

        # Sim time
        sim_time_layout = QVBoxLayout()

        # Label
        sim_time_label = QLabel(self)
        sim_time_label.setFont(font)
        sim_time_label.setText("Simulation time")
        sim_time_label.setAlignment(Qt.AlignCenter)

        # Typing box
        sim_time_box = QLineEdit(self)
        sim_time_box.setPlaceholderText("1000")
        sim_time_box.setMinimumWidth(GRID_WIDTH)

        # Confirm button
        sim_time_button = QPushButton(self)
        sim_time_button.setText("OK")
        sim_time_button.clicked.connect(setSimTime)

        # Num of workers
        workers_layout = QVBoxLayout()

        # Label
        workers_label = QLabel(self)
        workers_label.setFont(font)
        workers_label.setText("Number of workers")
        workers_label.setAlignment(Qt.AlignCenter)

        # Typing box
        workers_box = QLineEdit(self)
        workers_box.setPlaceholderText("1")
        workers_box.setMinimumWidth(GRID_WIDTH)

        # Confirm button
        workers_button = QPushButton(self)
        workers_button.setText("OK")
        workers_button.clicked.connect(setNumWorkers)

        # MTBO
        mtbo_layout = QVBoxLayout()

        # Label
        mtbo_label = QLabel(self)
        mtbo_label.setFont(font)
        mtbo_label.setText("Mean time between orders")
        mtbo_label.setAlignment(Qt.AlignCenter)

        # Typing box
        mtbo_box = QLineEdit(self)
        mtbo_box.setPlaceholderText("100")
        mtbo_box.setMinimumWidth(GRID_WIDTH)

        # Confirm button
        mtbo_button = QPushButton(self)
        mtbo_button.setText("OK")
        mtbo_button.clicked.connect(setMTBO)

        # Add all to the main layout
        fps_layout.addWidget(fps_label)
        fps_layout.addWidget(fps_box)
        fps_layout.addWidget(fps_button)

        sim_time_layout.addWidget(sim_time_label)
        sim_time_layout.addWidget(sim_time_box)
        sim_time_layout.addWidget(sim_time_button)

        workers_layout.addWidget(workers_label)
        workers_layout.addWidget(workers_box)
        workers_layout.addWidget(workers_button)

        mtbo_layout.addWidget(mtbo_label)
        mtbo_layout.addWidget(mtbo_box)
        mtbo_layout.addWidget(mtbo_button)

        # Setup layouts
        grid_layout.addLayout(fps_layout, 0, 0)
        grid_layout.addLayout(sim_time_layout, 0, 1)
        grid_layout.addLayout(workers_layout, 1, 0)
        grid_layout.addLayout(mtbo_layout, 1, 1)

        # Add an exit button
        lower_layout = QVBoxLayout()

        btn_font = QFont("Segoe UI", 10)
        btn_font.setBold(True)

        # Blank space
        blank_space = QLabel()
        blank_space.setMinimumHeight(5)
        blank_space.setText("")

        confirmation_button = QPushButton(self)
        confirmation_button.setText("Run simulation")
        confirmation_button.setFont(btn_font)
        confirmation_button.setMinimumHeight(60)
        confirmation_button.clicked.connect(self.hide)

        lower_layout.addWidget(blank_space)
        lower_layout.addWidget(confirmation_button)

        self.layout.addLayout(main_layout)
        self.layout.addLayout(grid_layout)
        self.layout.addLayout(lower_layout)
        self.setLayout(self.layout)


    def raiseInvalidInput(self):

        QMessageBox.critical(self, 'Invalid input', 'Please enter a valid number! ',
                             QMessageBox.Ok | QMessageBox.NoButton)

    def notifyVarChange(self, text):

        QMessageBox.information(self, 'Change successful', f'Value set to {text:10}',
                                QMessageBox.Ok | QMessageBox.NoButton)

    def closeEvent(self, event):

        reply = QMessageBox.question(self, 'Window Close', 'Are you sure you want to exit?',
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            Visualization.running = False
            event.accept()
        else:
            event.ignore()

    def keyPressEvent(self, e: QKeyEvent):

        if e.key() == Qt.Key_Escape:
            e.ignore()
            return
        else:
            super().keyPressEvent(e)