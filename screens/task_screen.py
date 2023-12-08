from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QPushButton, QTableWidget, 
                             QTableWidgetItem, QHeaderView, QHBoxLayout, QLabel, QDialog, QMessageBox)
from PyQt6.QtCore import pyqtSignal, QDateTime, QThread
import importlib
import uuid
import os

class TaskRowWidget(QWidget):
    def __init__(self, task_name, parent=None):
        super().__init__(parent)
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

class TaskScreen(QWidget):
    taskChanged = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout(self)
        self.tasks_data = {}

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
        task_config_module = importlib.import_module("dialogs.task_config_dialog")
        TaskConfigDialog = getattr(task_config_module, "TaskConfigDialog")
        dialog = TaskConfigDialog(self)
        result = dialog.exec()
        if result == QDialog.DialogCode.Accepted:
            task_config = dialog.get_task_config()
            if 'task_name' in task_config:
                self.add_task_to_table(task_config["task_name"], task_config)

    def add_task_to_table(self, task_name, task_config):
        task_id = str(uuid.uuid4())
        self.tasks_data[task_id] = {
            "name": task_name,
            "status": "Pending",
            "config": task_config,
            "timestamp": QDateTime.currentDateTime().toString()
        }
        self.taskChanged.emit()

        task_row_widget = TaskRowWidget(task_name, self)
        task_row_widget.playButton.clicked.connect(lambda: self.start_task(task_id, task_name, task_config))
        task_row_widget.deleteButton.clicked.connect(lambda: self.remove_row(task_row_widget, task_id))

        row_position = self.tableWidget.rowCount()
        self.tableWidget.insertRow(row_position)
        self.tableWidget.setCellWidget(row_position, 0, task_row_widget)
        self.task_row_widgets.append(task_row_widget)

    def start_task(self, task_id, task_name, task_config):
        try:
            module_name = f"automated_tasks.tasks.{task_name}.task_orchestrator"
            task_orchestrator_module = importlib.import_module(module_name)
            class_name = f"{task_name}Orchestrator"
            task_orchestrator_class = getattr(task_orchestrator_module, class_name)
            task_orchestrator = task_orchestrator_class(task_config)

            thread = QThread()
            task_orchestrator.moveToThread(thread)
            thread.started.connect(task_orchestrator.execute)
            thread.finished.connect(lambda: self.thread_finished(task_id))
            thread.start()

            self.tasks_data[task_id] = {
                "orchestrator": task_orchestrator,
                "thread": thread,
                "status": "Running"
            }
            self.taskChanged.emit()
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to start task {task_name}: {str(e)}")

    def thread_finished(self, task_id):
        if task_id in self.tasks_data:
            self.tasks_data[task_id]["status"] = "Finished"
            print(f"Task {task_id} finished.")

    def remove_row(self, task_row_widget, task_id):
        if task_id in self.tasks_data:
            orchestrator = self.tasks_data[task_id].get("orchestrator")
            if orchestrator and hasattr(orchestrator, 'stop_task'):
                orchestrator.stop_task()

            thread = self.tasks_data[task_id].get("thread")
            if thread:
                thread.quit()
                if not thread.wait(1000):  # Wait for 1 second
                    thread.terminate()  # Force termination if not stopped
                thread.wait()  # Ensure thread is fully terminated

            del self.tasks_data[task_id]

        if task_row_widget in self.task_row_widgets:
            self.task_row_widgets.remove(task_row_widget)
            row_index = self.tableWidget.indexAt(task_row_widget.pos()).row()
            self.tableWidget.removeRow(row_index)
            self.taskChanged.emit()

        row_index = self.tableWidget.indexAt(task_row_widget.pos()).row()
        self.tableWidget.removeRow(row_index)
        self.taskChanged.emit()
