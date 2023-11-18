from PyQt6.QtWidgets import QPushButton
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import QSize

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
