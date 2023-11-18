from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QStackedWidget, QWidget, QDialog,
    QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QSizePolicy,
    QTableWidget, QTableWidgetItem, QHeaderView, QComboBox
)
from PyQt6.QtCore import QSize, Qt, QPoint
from PyQt6.QtGui import QIcon, QPalette, QColor, QMouseEvent


class TaskConfigDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Configure Task")
        self.layout = QVBoxLayout()

        self.task_selector = QComboBox()
        self.task_selector.addItems(["Task 1", "Task 2", "Task 3"])
        self.task_selector.currentIndexChanged.connect(self.update_config_options)
        self.layout.addWidget(self.task_selector)

        self.config_options_container = QWidget()
        self.config_options_layout = QVBoxLayout()
        self.config_options_container.setLayout(self.config_options_layout)
        self.layout.addWidget(self.config_options_container)

        self.buttons_layout = QHBoxLayout()
        self.submit_button = QPushButton("Submit")
        self.submit_button.clicked.connect(self.accept)
        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.clicked.connect(self.reject)
        self.buttons_layout.addWidget(self.submit_button)
        self.buttons_layout.addWidget(self.cancel_button)
        self.layout.addLayout(self.buttons_layout)

        self.setLayout(self.layout)
        self.update_config_options()

    
    def get_task_config(self):
        return self.task_selector.currentText()

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

if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()