from PyQt6.QtWidgets import QMainWindow, QStackedWidget, QWidget, QVBoxLayout, QHBoxLayout
from PyQt6.QtCore import QSize, Qt, QEvent
from PyQt6.QtGui import QPalette, QColor
from ui.custom_title_bar import CustomTitleBar
from ui.icon_button import IconButton
from screens.task_screen import TaskScreen
from screens.home_screen import HomeScreen
from task_management.task_manager import TaskManager
from db.DatabaseManager import Session  # Import Session from your DatabaseManager
from db.DatabaseManager import UserProfile
from sqlalchemy.exc import SQLAlchemyError


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setMinimumSize(QSize(1600, 900))

        # Initialize DB using DatabaseManager.py
        self.db_session = Session()

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

        self.task_manager = TaskManager()

        self.stacked_widget = QStackedWidget()
        self.home_screen = HomeScreen()
        self.tasks_screen = TaskScreen(task_manager=self.task_manager, db_session=self.db_session)
        
        self.stacked_widget.addWidget(self.home_screen)
        self.stacked_widget.addWidget(self.tasks_screen)

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

        self.task_manager.tasksDataChanged.connect(self.home_screen.update_preview_table)
        print("Connected tasksDataChanged signal to HomeScreen's update_preview_table method.")
        
    def display_screen(self, index):
        if index == 0:
            self.home_screen.update_preview_table()
        self.stacked_widget.setCurrentIndex(index)
    
    def closeEvent(self, event: QEvent):
        print("Closing MainWindow. Stopping all tasks.")
        # Close the database session
        self.db_session.close()
         # Call the parent class's closeEvent method
        super().closeEvent(event)
        self.task_manager.stop_all_tasks()
        event.accept()
