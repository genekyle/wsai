from PyQt6.QtWidgets import (QMainWindow, QStackedWidget, QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, 
                             QTableWidgetItem, QHeaderView, QLabel, QPushButton, QDialog)
from PyQt6.QtCore import QSize, Qt
from PyQt6.QtGui import QPalette, QColor
from ui.custom_title_bar import CustomTitleBar
from ui.icon_button import IconButton
from dialogs.task_config_dialog import TaskConfigDialog

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setMinimumSize(QSize(1600, 900))

        palette = QPalette()
        palette.setColor(QPalette.ColorRole.Window, QColor(15, 17, 26))
        self.setPalette(palette)
        self.setAutoFillBackground(True)

        self.titleBar = CustomTitleBar(self)

        self.sidebar_container = QWidget()
        self.sidebar_container.setFixedWidth(120)
        self.sidebar_container.setStyleSheet("background-color: #090b10;")
        self.sidebar_layout = QVBoxLayout()
        self.sidebar_layout.setContentsMargins(0, 0, 0, 0)
        self.sidebar_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)

        self.home_button = IconButton('./resources/home.png', 
                                      './resources/home_hover.png', 
                                      './resources/home_clicked.png')
        self.tasks_button = IconButton('./resources/tasks.png', 
                                       './resources/tasks_hover.png', 
                                       './resources/tasks_clicked.png')
        self.sidebar_layout.addWidget(self.home_button)
        self.sidebar_layout.addWidget(self.tasks_button)
        self.sidebar_layout.addStretch()
        self.sidebar_container.setLayout(self.sidebar_layout)

        self.stacked_widget = QStackedWidget()
        self.home_screen = QWidget()
        self.tasks_screen = QWidget()
        self.stacked_widget.addWidget(self.home_screen)
        self.stacked_widget.addWidget(self.tasks_screen)

        self.home_layout = QVBoxLayout(self.home_screen)
        self.home_layout.addWidget(QLabel('Content of Home Screen'))
        self.tasks_layout = QVBoxLayout(self.tasks_screen)

        self.setup_tasks_screen()

        self.home_button.clicked.connect(lambda: self.display_screen(0))
        self.tasks_button.clicked.connect(lambda: self.display_screen(1))

        self.main_layout = QHBoxLayout()
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)
        self.main_layout.addWidget(self.sidebar_container)
        self.main_layout.addWidget(self.stacked_widget)

        self.overall_layout = QVBoxLayout()
        self.overall_layout.addWidget(self.titleBar)
        self.overall_layout.addLayout(self.main_layout)

        self.central_widget = QWidget()
        self.central_widget.setLayout(self.overall_layout)
        self.setCentralWidget(self.central_widget)

    def setup_tasks_screen(self):
        self.add_task_button = QPushButton("Add Task")
        self.add_task_button.clicked.connect(self.open_task_config_dialog)
        self.tasks_layout.addWidget(self.add_task_button)

        self.tableWidget = QTableWidget()
        self.tableWidget.setRowCount(0)
        self.tableWidget.setColumnCount(3)
        headers = ["Task", "Status", "Actions"]
        self.tableWidget.setHorizontalHeaderLabels(headers)
        self.tableWidget.setShowGrid(False)
        self.tableWidget.verticalHeader().setVisible(False)
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.tasks_layout.addWidget(self.tableWidget)

    def open_task_config_dialog(self):
        dialog = TaskConfigDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            task_config = dialog.get_task_config()
            self.add_task_to_table(task_config)

    def add_task_to_table(self, task_config):
        row_count = self.tableWidget.rowCount()
        self.tableWidget.insertRow(row_count)
        self.tableWidget.setItem(row_count, 0, QTableWidgetItem(task_config))
        self.tableWidget.setItem(row_count, 1, QTableWidgetItem("Pending"))
        self.tableWidget.setItem(row_count, 2, QTableWidgetItem("Edit/Delete"))

    def display_screen(self, index):
        self.stacked_widget.setCurrentIndex(index)
