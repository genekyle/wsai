from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QPushButton, QTableWidget, 
                             QTableWidgetItem, QHeaderView, QHBoxLayout, QLabel, QDialog, QMessageBox)
from PyQt6.QtCore import pyqtSignal, QDateTime, QThread
from task_management.task_manager import TaskManager
import importlib
import uuid
import os

TASK_DISPLAY_NAMES = {
    "CheckEmails": "Check Emails",
    # Add other tasks here
}

class TaskRowWidget(QWidget):
    def __init__(self, task_name, task_id, task_screen, parent=None):
        super().__init__(parent)
        self.task_id = task_id  # Store the task ID
        self.task_screen = task_screen  # Store a reference to the TaskScreen
        layout = QHBoxLayout()

        self.task_label = QLabel(task_name)
        layout.addWidget(self.task_label)

        self.status_label = QLabel("Pending")
        layout.addWidget(self.status_label)

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

        # Update button connections to use the task ID
        self.playButton.clicked.connect(lambda: self.task_screen.start_task(self.task_id))
        self.deleteButton.clicked.connect(lambda: self.task_screen.remove_row(self, self.task_id))

class TaskScreen(QWidget):
    taskChanged = pyqtSignal()

    def __init__(self, task_manager: TaskManager, parent=None):
        super().__init__(parent)
        self.task_manager = task_manager
        
        # Connect signals
        self.task_manager.taskStarted.connect(self.on_task_started)
        self.task_manager.taskStopped.connect(self.on_task_stopped)

        self.tasks_data = {}
        self.task_count = {}

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

        self.task_manager.taskStarted.connect(self.on_task_started)
        self.task_manager.taskStopped.connect(self.on_task_stopped)


    def open_task_config_dialog(self):
        task_config_module = importlib.import_module("dialogs.task_config_dialog")
        TaskConfigDialog = getattr(task_config_module, "TaskConfigDialog")
        dialog = TaskConfigDialog(self)
        result = dialog.exec()

        if result == QDialog.DialogCode.Accepted:
            task_config = dialog.get_task_config()
            if task_config and 'task_name' in task_config:
                self.add_task_to_table(task_config["task_name"], task_config)

    def add_task_to_table(self, task_name, task_config):
        display_name = TASK_DISPLAY_NAMES.get(task_name, task_name)  # Get the display name

        task_id = str(uuid.uuid4())
        self.tasks_data[task_id] = {
            "name": display_name,  # Use the display name
            "status": "Pending",
            "config": task_config,
            "timestamp": QDateTime.currentDateTime().toString()
        }
        self.taskChanged.emit()

        # Create a TaskRowWidget for the new task
        task_row_widget = TaskRowWidget(display_name, task_id, self)  # Pass the display name
        # task_row_widget.playButton.clicked.connect(lambda: self.start_task(task_id))
        task_row_widget.deleteButton.clicked.connect(lambda: self.remove_row(task_row_widget, task_id))

        row_position = self.tableWidget.rowCount()
        self.tableWidget.insertRow(row_position)
        self.tableWidget.setCellWidget(row_position, 0, task_row_widget)
        self.task_row_widgets.append(task_row_widget)


    def start_task(self, task_id):
        task_data = self.tasks_data.get(task_id)
        if task_data:
            task_name = next(key for key, value in TASK_DISPLAY_NAMES.items() if value == task_data['name'])
            self.task_manager.start_task(task_id, task_name, task_data['config'])  # Use technical task name
            task_data["status"] = "Running"
            self.taskChanged.emit()

    
    def get_display_name(self, task_name):
        """ Generate a unique display name for the task """
        count = self.task_count.get(task_name, 0) + 1
        self.task_count[task_name] = count
        return f"{task_name} {count}" if count > 1 else task_name

    def thread_finished(self, task_id):
        if task_id in self.tasks_data:
            self.tasks_data[task_id]["status"] = "Finished"
            print(f"Task {task_id} finished.")

    def remove_row(self, task_row_widget, task_id):
        self.task_manager.stop_task(task_id)
        # Update GUI immediately
        if task_id in self.tasks_data:
            del self.tasks_data[task_id]
            self.taskChanged.emit()

        if task_row_widget in self.task_row_widgets:
            row_index = self.tableWidget.indexAt(task_row_widget.pos()).row()
            self.tableWidget.removeRow(row_index)
            self.task_row_widgets.remove(task_row_widget)

    def on_task_started(self, task_id):
        for task_row_widget in self.task_row_widgets:
            if task_row_widget.task_id == task_id:
                task_row_widget.playButton.setEnabled(False)
                break

    def on_task_stopped(self, task_id):
        for task_row_widget in self.task_row_widgets:
            if task_row_widget.task_id == task_id:
                task_row_widget.playButton.setEnabled(True)
                break
