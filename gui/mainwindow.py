from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QStackedWidget, QWidget,
    QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QSizePolicy,
    QTableWidget, QTableWidgetItem, QHeaderView
)
from PyQt6.QtCore import QSize, Qt, QPoint
from PyQt6.QtGui import QIcon, QPalette, QColor, QMouseEvent

class CustomTitleBar(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QHBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        self.setStyleSheet("background-color: #123456;")  # Set a distinct color for the title bar

        # Program name label
        self.titleLabel = QLabel("WSAI")  # Replace with your program's name
        self.titleLabel.setStyleSheet("color: #D3D3D3;")  # Light gray text
        self.layout.addWidget(self.titleLabel)

        # Spacer to push control buttons to the right
        self.layout.addStretch()

        # Minimize button
        self.minimizeButton = QPushButton("Min")
        self.minimizeButton.clicked.connect(self.minimize_window)
        self.layout.addWidget(self.minimizeButton)

        # Maximize/Restore button
        self.maximizeButton = QPushButton("Max")
        self.maximizeButton.clicked.connect(self.maximize_restore_window)
        self.layout.addWidget(self.maximizeButton)

        # Close button
        self.closeButton = QPushButton("Close")
        self.closeButton.clicked.connect(self.close_window)
        self.layout.addWidget(self.closeButton)

        self.setLayout(self.layout)
        self.start = QPoint(0, 0)
        self.pressing = False

    def minimize_window(self):
        self.window().showMinimized()

    def maximize_restore_window(self):
        if self.window().isMaximized():
            self.window().showNormal()
        else:
            self.window().showMaximized()

    def close_window(self):
        self.window().close()

    def mousePressEvent(self, event: QMouseEvent):
        self.start = event.position().toPoint()
        self.pressing = True

    def mouseMoveEvent(self, event: QMouseEvent):
        if self.pressing:
            self.window().move(self.window().pos() + (event.position().toPoint() - self.start))

    def mouseReleaseEvent(self, event: QMouseEvent):
        self.pressing = False

class IconButton(QPushButton):
    def __init__(self, normal_icon_path, hover_icon_path, pressed_icon_path, parent=None):
        super().__init__(parent)
        self.normal_icon = QIcon(normal_icon_path)
        self.hover_icon = QIcon(hover_icon_path)
        self.pressed_icon = QIcon(pressed_icon_path)
        self.setIcon(self.normal_icon)
        self.setIconSize(QSize(36, 36))
        self.setFixedSize(96, 96)
        self.setStyleSheet("QPushButton { border: none; background-color: transparent; }")

    def enterEvent(self, event):
        self.setIcon(self.hover_icon)
        super().enterEvent(event)

    def leaveEvent(self, event):
        self.setIcon(self.normal_icon)
        super().leaveEvent(event)

    def mousePressEvent(self, event):
        self.setIcon(self.pressed_icon)
        super().mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        if self.rect().contains(event.pos()):
            self.setIcon(self.hover_icon)
        else:
            self.setIcon(self.normal_icon)
        super().mouseReleaseEvent(event)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)  # Remove the title bar
        self.setMinimumSize(QSize(1600, 900))  # Set the window size

        # Set the background color of the MainWindow using QPalette
        palette = QPalette()
        palette.setColor(QPalette.ColorRole.Window, QColor(15, 17, 26))  # Navy blue background
        self.setPalette(palette)
        self.setAutoFillBackground(True)

        # Custom title bar
        self.titleBar = CustomTitleBar(self)

        # Sidebar container and layout
        self.sidebar_container = QWidget()
        self.sidebar_container.setFixedWidth(120)
        self.sidebar_container.setStyleSheet("background-color: #090b10;")  # Dark gray background for the sidebar
        self.sidebar_layout = QVBoxLayout()
        self.sidebar_layout.setContentsMargins(0, 0, 0, 0)
        self.sidebar_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)

        # Create and add buttons
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

        # Main content area
        self.stacked_widget = QStackedWidget()
        self.home_screen = QWidget()
        self.tasks_screen = QWidget()
        self.stacked_widget.addWidget(self.home_screen)
        self.stacked_widget.addWidget(self.tasks_screen)

        # Set layout for screens
        self.home_layout = QVBoxLayout(self.home_screen)
        self.home_layout.addWidget(QLabel('Content of Home Screen'))
        self.tasks_layout = QVBoxLayout(self.tasks_screen)

        # Setup for tasks_screen with QTableWidget
        self.setup_tasks_screen()

        # Connect buttons to screens
        self.home_button.clicked.connect(lambda: self.display_screen(0))
        self.tasks_button.clicked.connect(lambda: self.display_screen(1))

        # Main layout of the window (contains sidebar and content area)
        self.main_layout = QHBoxLayout()
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)
        self.main_layout.addWidget(self.sidebar_container)
        self.main_layout.addWidget(self.stacked_widget)

        # Overall layout (contains title bar and main_layout)
        self.overall_layout = QVBoxLayout()
        self.overall_layout.addWidget(self.titleBar)  # Add title bar at the top
        self.overall_layout.addLayout(self.main_layout)  # Add main_layout below the title bar

        # Central widget setup
        self.central_widget = QWidget()
        self.central_widget.setLayout(self.overall_layout)
        self.setCentralWidget(self.central_widget)

    def setup_tasks_screen(self):
        self.tableWidget = QTableWidget()
        self.tableWidget.setRowCount(5)  # Set the number of rows
        self.tableWidget.setColumnCount(3)  # Set the number of columns

        # Rename headers and update data
        headers = ["Task", "Status", "Actions"]
        self.tableWidget.setHorizontalHeaderLabels(headers)
        self.tableWidget.setItem(0, 0, QTableWidgetItem("Task 1"))
        self.tableWidget.setItem(0, 1, QTableWidgetItem("In Progress"))
        self.tableWidget.setItem(0, 2, QTableWidgetItem("Button/Link"))

        # Hide the grid lines and the row numbers
        self.tableWidget.setShowGrid(False)
        self.tableWidget.verticalHeader().setVisible(False)

        # Make the columns stretch to take available space
        header = self.tableWidget.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        # Add the table to the tasks_layout
        self.tasks_layout.addWidget(self.tableWidget)

    def display_screen(self, index):
        # Switch to the corresponding screen in the stacked widget
        self.stacked_widget.setCurrentIndex(index)

if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()