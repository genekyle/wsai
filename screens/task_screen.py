from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QPushButton, QTableWidget, 
                             QTableWidgetItem, QHeaderView, QHBoxLayout, QLabel, QDialog, QMessageBox)
from PyQt6.QtCore import pyqtSignal, QDateTime
from shared.shared_data import tasks_data
from dialogs.task_config_dialog import TaskConfigDialog
import importlib
import uuid

class TaskRowWidget(QWidget):
    def __init__(self, task_name, parent=None):
        super().__init__(parent)
        layout = QHBoxLayout()

        self.task_label = QLabel(task_name)
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
        layout.setSpacing(10)
        self.setLayout(layout)

class TaskScreen(QWidget):
    taskChanged = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout(self)

        self.add_task_button = QPushButton("Add Task")
        self.add_task_button.clicked.connect(self.open_task_config_dialog)
        self.layout.addWidget(self.add_task_button)

        self.tableWidget = QTableWidget()
        self.tableWidget.setRowCount(0)
        self.tableWidget.setColumnCount(1)
        headers = ["Tasks"]
        self.tableWidget.setHorizontalHeaderLabels(headers)
        self.tableWidget.setShowGrid(False)
        self.tableWidget.verticalHeader().setVisible(False)
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.layout.addWidget(self.tableWidget)

        self.task_row_widgets = []

    def open_task_config_dialog(self):
        dialog = TaskConfigDialog(self)
        result = dialog.exec()
        print(f"Dialog result: {result}")  # Debug print
        if result == QDialog.DialogCode.Accepted:
            task_config = dialog.get_task_config()
            task_name = task_config["task_name"]
            try:
                config_dialog_module = importlib.import_module(f"automated_tasks.{task_name.lower()}.config_dialog")
                config_dialog_class = getattr(config_dialog_module, "ConfigDialog")
                config_dialog = config_dialog_class(self)
                if config_dialog.exec() == QDialog.DialogCode.Accepted:
                    task_specific_config = config_dialog.get_task_config()
                    self.add_task_to_table(task_name, task_specific_config)
            except ModuleNotFoundError:
                QMessageBox.warning(self, "Error", f"No configuration dialog found for {task_name}")

    def add_task_to_table(self, task_name, task_config):
        task_id = str(uuid.uuid4())
        tasks_data[task_id] = {
            "name": task_name,
            "status": "Pending",
            "config": task_config,
            "timestamp": QDateTime.currentDateTime().toString()
        }
        self.taskChanged.emit()

        # Execute the task based on its type and configuration
        task_module = importlib.import_module(f"automated_tasks.{task_name.lower()}.task")
        task_function = getattr(task_module, "execute_task")
        task_function(task_config)

        task_row_widget = TaskRowWidget(task_name)
        row_position = self.tableWidget.rowCount()
        self.tableWidget.insertRow(row_position)
        self.tableWidget.setCellWidget(row_position, 0, task_row_widget)
        self.task_row_widgets.append(task_row_widget)

        task_row_widget.deleteButton.clicked.connect(lambda: self.remove_row(task_row_widget, task_id))

    def remove_row(self, task_row_widget, task_id):
        if task_row_widget in self.task_row_widgets:
            self.task_row_widgets.remove(task_row_widget)
            row_index = self.tableWidget.indexAt(task_row_widget.pos()).row()
            self.tableWidget.removeRow(row_index)
            del tasks_data[task_id]
            self.taskChanged.emit()

# Additional methods or logic for TaskScreen as required
