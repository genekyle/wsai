from PyQt6.QtWidgets import QWidget, QPushButton, QHBoxLayout

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
