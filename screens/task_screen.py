from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton, QTableWidget, QTableWidgetItem, 
    QHeaderView, QHBoxLayout, QDialog, QLabel
)
from dialogs.task_config_dialog import TaskConfigDialog

# TaskRowWidget class to encapsulate task and action buttons
class TaskRowWidget(QWidget):
    def __init__(self, task_config, parent=None):
        super().__init__(parent)
        layout = QHBoxLayout()

        self.task_label = QLabel(task_config)
        layout.addWidget(self.task_label)

        self.status_label = QLabel("Pending")
        layout.addWidget(self.status_label)

        # Action buttons
        self.playButton = QPushButton("Play")
        layout.addWidget(self.playButton)
        self.pauseButton = QPushButton("Pause")
        layout.addWidget(self.pauseButton)
        self.editButton = QPushButton("Edit")
        layout.addWidget(self.editButton)
        self.deleteButton = QPushButton("Delete")
        layout.addWidget(self.deleteButton)

        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(10)  # Adjust the spacing as needed

        self.setLayout(layout)

# TaskScreen class
class TaskScreen(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout(self)

        self.add_task_button = QPushButton("Add Task")
        self.add_task_button.clicked.connect(self.open_task_config_dialog)
        self.layout.addWidget(self.add_task_button)

        self.tableWidget = QTableWidget()
        self.tableWidget.setRowCount(0)
        self.tableWidget.setColumnCount(1)  # We only need one column for the custom row widget
        headers = ["Tasks"]
        self.tableWidget.setHorizontalHeaderLabels(headers)
        self.tableWidget.setShowGrid(False)
        self.tableWidget.verticalHeader().setVisible(False)
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.layout.addWidget(self.tableWidget)

        # List to store TaskRowWidget instances
        self.task_row_widgets = []

    def open_task_config_dialog(self):
        dialog = TaskConfigDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            task_config = dialog.get_task_config()
            self.add_task_to_table(task_config)

    def add_task_to_table(self, task_config):
        task_row_widget = TaskRowWidget(task_config)
        row_position = self.tableWidget.rowCount()
        self.tableWidget.insertRow(row_position)
        self.tableWidget.setCellWidget(row_position, 0, task_row_widget)
        self.task_row_widgets.append(task_row_widget)

        # Connect the delete button's click event to remove the corresponding row widget
        task_row_widget.deleteButton.clicked.connect(lambda: self.remove_row(task_row_widget))

    def remove_row(self, task_row_widget):
        if task_row_widget in self.task_row_widgets:
            self.task_row_widgets.remove(task_row_widget)
            self.tableWidget.removeRow(self.tableWidget.indexAt(task_row_widget.pos()).row())
