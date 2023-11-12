from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QStackedWidget, QWidget,
    QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QSizePolicy
)
from PyQt6.QtCore import QSize, Qt
from PyQt6.QtGui import QIcon, QPalette, QColor

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
        self.setMinimumSize(QSize(1600, 900))  # Set the window size

        # Set the background color of the MainWindow using QPalette
        palette = QPalette()
        palette.setColor(QPalette.ColorRole.Window, QColor(15, 17, 26))  # Navy blue background
        self.setPalette(palette)
        self.setAutoFillBackground(True)

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
        self.tasks_layout.addWidget(QLabel('Content of Tasks Screen'))

        # Connect buttons to screens
        self.home_button.clicked.connect(lambda: self.display_screen(0))
        self.tasks_button.clicked.connect(lambda: self.display_screen(1))

        # Main layout of the window
        self.central_widget = QWidget()
        self.main_layout = QHBoxLayout(self.central_widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)
        self.main_layout.addWidget(self.sidebar_container)
        self.main_layout.addWidget(self.stacked_widget)
        self.central_widget.setLayout(self.main_layout)
        self.setCentralWidget(self.central_widget)

    def display_screen(self, index):
        # Switch to the corresponding screen in the stacked widget
        self.stacked_widget.setCurrentIndex(index)

if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()
