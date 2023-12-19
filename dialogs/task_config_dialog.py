from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QComboBox, QPushButton, QHBoxLayout
from shared.shared_data import TASK_DISPLAY_NAMES
import importlib
import os

class TaskConfigDialog(QDialog):
    def __init__(self, parent=None, session_manager=None):
        super().__init__(parent)
        self.session_manager = session_manager
        self.setWindowTitle("Configure Task")
        self.layout = QVBoxLayout(self)

        # Task selection
        self.task_selector = QComboBox()
        self.config_dialogs = {}
        self.load_tasks()
        self.layout.addWidget(self.task_selector)

        # Browser session selection
        self.layout.addWidget(QLabel("Browser Session:"))
        self.session_selector = QComboBox()
        self.populate_sessions()
        self.layout.addWidget(self.session_selector)

        # Setup buttons
        self.buttons_layout = QHBoxLayout()
        self.setup_buttons()
        self.setLayout(self.layout)

    def load_tasks(self):
        tasks_path = 'automated_tasks/tasks'
        for task_name in os.listdir(tasks_path):
            if task_name == "__pycache__" or not os.path.isdir(os.path.join(tasks_path, task_name)):
                continue

            display_name = TASK_DISPLAY_NAMES.get(task_name, task_name)
            self.task_selector.addItem(display_name)
            self.load_config_dialog(task_name)

    def populate_sessions(self):
        for session_detail in self.session_manager.list_sessions():
            label = f"Session {session_detail['id']} - {session_detail['status']}"
            self.session_selector.addItem(label, session_detail['id'])
        self.session_selector.addItem("New Session", None)

    def load_config_dialog(self, task_name):
        try:
            config_module = importlib.import_module(f"automated_tasks.tasks.{task_name}.config_dialog")
            config_class = getattr(config_module, f"{task_name}ConfigDialog")
            self.config_dialogs[task_name] = config_class()
        except (ModuleNotFoundError, AttributeError):
            print(f"Config dialog not found for {task_name}")

    def setup_buttons(self):
        self.submit_button = QPushButton("Submit")
        self.submit_button.clicked.connect(self.accept)
        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.clicked.connect(self.reject)
        self.buttons_layout.addWidget(self.submit_button)
        self.buttons_layout.addWidget(self.cancel_button)
        self.layout.addLayout(self.buttons_layout)

    def get_task_config(self):
        display_name = self.task_selector.currentText()
        task_name = next((name for name, disp_name in TASK_DISPLAY_NAMES.items() if disp_name == display_name), display_name)
        config_dialog = self.config_dialogs.get(task_name)

        if config_dialog:
            result = config_dialog.exec()
            if result == QDialog.DialogCode.Accepted:
                task_config = config_dialog.get_config()
                task_config["session_id"] = self.session_selector.currentData()
                return task_config
            else:
                return None

        return {"task_name": task_name, "session_id": self.session_selector.currentData()}
