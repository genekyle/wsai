from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QPushButton, QTableWidget, 
                             QTableWidgetItem, QHeaderView, QHBoxLayout, QLabel, QDialog)
from PyQt6.QtCore import pyqtSignal, QDateTime
from task_management.task_manager import TaskManager
from shared.shared_data import tasks_data, TASK_DISPLAY_NAMES
from dialogs.task_config_dialog import TaskConfigDialog
from automated_tasks.tasks.IndeedBot.config_dialog import IndeedBotConfigDialog
import uuid

class TaskRowWidget(QWidget):
    
    def __init__(self, task_name, task_id, task_screen, parent=None):
        super().__init__(parent)
        self.task_id = task_id
        self.task_screen = task_screen
        self.is_paused = False  # To track pause state
        layout = QHBoxLayout()

        self.task_label = QLabel(task_name)
        layout.addWidget(self.task_label)

        self.status_label = QLabel("Pending")
        layout.addWidget(self.status_label)

        self.playButton = QPushButton("Play")
        self.playButton.clicked.connect(lambda: self.task_screen.start_task(self.task_id))
        layout.addWidget(self.playButton)

        self.pauseButton = QPushButton("Pause")
        self.pauseButton.clicked.connect(self.toggle_pause_resume)
        layout.addWidget(self.pauseButton)

        self.editButton = QPushButton("Edit")
        layout.addWidget(self.editButton)

        self.deleteButton = QPushButton("Delete")
        self.deleteButton.clicked.connect(lambda: self.task_screen.remove_row(self, self.task_id))
        layout.addWidget(self.deleteButton)

        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(10)
        self.setLayout(layout)
        self.pauseButton.clicked.connect(self.toggle_pause)

    def toggle_pause(self):
        orchestrator = self.task_screen.task_manager.get_orchestrator(self.task_id)
        if orchestrator and orchestrator._is_paused:
            orchestrator.resume_task()
            self.pauseButton.setText("Pause")
        else:
            orchestrator.pause_task()
            self.pauseButton.setText("Resume")


    def toggle_pause_resume(self):
        if self.is_paused:
            self.task_screen.resume_task(self.task_id)
            self.pauseButton.setText("Pause")
            self.is_paused = False
        else:
            self.task_screen.pause_task(self.task_id)
            self.pauseButton.setText("Resume")
            self.is_paused = True

class TaskScreen(QWidget):
    taskChanged = pyqtSignal()

    def __init__(self, task_manager: TaskManager, parent=None):
        super().__init__(parent)
        self.task_manager = task_manager
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
        dialog = TaskConfigDialog(parent=self, session_manager=self.task_manager.session_manager)
        result = dialog.exec()

        if result == QDialog.DialogCode.Accepted:
            task_config = dialog.get_task_config()
            if task_config and 'open_next_dialog' in task_config:
                self.open_specific_task_config_dialog(task_config['task_name'], task_config)
            elif task_config:
                self.add_task_to_table(task_config["task_name"], task_config)
    
    def open_specific_task_config_dialog(self, task_name, previous_config):
        if task_name == "IndeedBot":
            indeed_bot_dialog = IndeedBotConfigDialog()
            indeed_bot_dialog.set_initial_config(previous_config)  # Set initial values if needed
            result = indeed_bot_dialog.exec()

            if result == QDialog.DialogCode.Accepted:
                indeed_bot_config = indeed_bot_dialog.get_config()
                combined_config = {**previous_config, **indeed_bot_config}  # Merge configurations
                self.add_task_to_table(task_name, combined_config)

    def add_task_to_table(self, task_name, task_config):
        task_id = str(uuid.uuid4())
        self.tasks_data[task_id] = {
            "name": TASK_DISPLAY_NAMES.get(task_name, task_name),
            "status": "Pending",
            "config": task_config,
            "timestamp": QDateTime.currentDateTime().toString()
        }
        self.taskChanged.emit()

        task_row_widget = TaskRowWidget(TASK_DISPLAY_NAMES.get(task_name, task_name), task_id, self)
        row_position = self.tableWidget.rowCount()
        self.tableWidget.insertRow(row_position)
        self.tableWidget.setCellWidget(row_position, 0, task_row_widget)
        self.task_row_widgets.append(task_row_widget)

        self.task_manager.start_task(task_id, task_name, task_config)
        self.tasks_data[task_id]["status"] = "Running"
        self.taskChanged.emit()

        orchestrator = self.task_manager.get_orchestrator(task_id)
        if orchestrator:
            orchestrator.stateChanged.connect(lambda task_id, state: self.update_status(task_id, "Playing: " + state))

    def start_task(self, task_id):
        task_data = self.tasks_data.get(task_id)
        if task_data:
            task_name = next(key for key, value in TASK_DISPLAY_NAMES.items() if value == task_data['name'])
            self.task_manager.start_task(task_id, task_name, task_data['config'])
            task_data["status"] = "Running"
            self.taskChanged.emit()

    def pause_task(self, task_id):
        orchestrator = self.task_manager.get_orchestrator(task_id)
        if orchestrator:
            orchestrator.pause_task()

    def resume_task(self, task_id):
        orchestrator = self.task_manager.get_orchestrator(task_id)
        if orchestrator:
            orchestrator.resume_task()

    def remove_row(self, task_row_widget, task_id):
        self.task_manager.stop_task(task_id)
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

    def on_task_stopped(self, task_id):
        for task_row_widget in self.task_row_widgets:
            if task_row_widget.task_id == task_id:
                task_row_widget.playButton.setEnabled(True)

    def update_status(self, task_id, new_status):
        for row_widget in self.task_row_widgets:
            if row_widget.task_id == task_id:
                row_widget.status_label.setText(new_status)
                row_widget.status_label.repaint()
                break

    # ... any additional methods or code for TaskScreen ...
