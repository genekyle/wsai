from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QComboBox, QPushButton, QHBoxLayout
from shared.shared_data import TASK_DISPLAY_NAMES
from automated_tasks.tasks.IndeedBot.config_dialog import IndeedBotConfigDialog
import importlib
import os

class TaskConfigDialog(QDialog):
    def __init__(self, parent=None, session_manager=None):
        super().__init__(parent)
        self.session_manager = session_manager
        self.setWindowTitle("Configure Task")
        self.layout = QVBoxLayout(self)
        self.selected_task = None  # Initialize the attribute

        # Define a mapping from display names to module names
        self.task_name_mapping = {
            "Test Task(Browser Open)": "CheckEmails",
            "Indeed Bot": "IndeedBot",  # Add other mappings as needed
            # ... other mappings ...
        }

        # Task selection
        self.task_selector = QComboBox()
        self.layout.addWidget(self.task_selector)

        # Browser session selection
        self.layout.addWidget(QLabel("Browser Session:"))
        self.session_selector = QComboBox()
        self.populate_sessions()
        self.layout.addWidget(self.session_selector)

        # Setup buttons
        self.setup_buttons()
        self.setLayout(self.layout)

        # Load tasks
        self.load_tasks()

    def load_tasks(self):
        tasks_path = 'automated_tasks/tasks'
        for task_name in os.listdir(tasks_path):
            if task_name == "__pycache__" or not os.path.isdir(os.path.join(tasks_path, task_name)):
                continue
            display_name = TASK_DISPLAY_NAMES.get(task_name, task_name)
            self.task_selector.addItem(display_name)
        self.task_selector.currentIndexChanged.connect(self.on_task_selected)


    def populate_sessions(self):
        for session_detail in self.session_manager.list_sessions():
            in_use_status = " (In Use)" if session_detail["in_use"] else ""
            label = f"Session {session_detail['id']} - {session_detail['status']}{in_use_status}"
            self.session_selector.addItem(label, session_detail['id'])
        self.session_selector.addItem("New Session", None)

    def setup_buttons(self):
        self.submit_button = QPushButton("Submit")
        self.submit_button.clicked.connect(self.on_submit_clicked)
        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.clicked.connect(self.reject)
        self.buttons_layout = QHBoxLayout()
        self.buttons_layout.addWidget(self.submit_button)
        self.buttons_layout.addWidget(self.cancel_button)
        self.layout.addLayout(self.buttons_layout)

    def on_submit_clicked(self):
        if self.selected_task:
            self.open_config_dialog_for_task(self.selected_task)
        else:
            print("No Task Selected")
            # Handle the case where no task is selected

    def on_task_selected(self, index):
        # Update the selected task name when a new task is chosen
        display_name = self.task_selector.currentText()
        self.selected_task = self.task_name_mapping.get(display_name, display_name)

    def open_config_dialog_for_task(self, task_name):
        try:
            # Translate the display name to module name
            module_name = self.task_name_mapping.get(task_name, task_name)
            config_module = importlib.import_module(f"automated_tasks.tasks.{module_name}.config_dialog")
            config_class = getattr(config_module, f"{module_name}ConfigDialog")
            config_dialog = config_class()
            result = config_dialog.exec()
            if result == QDialog.DialogCode.Accepted:
                self.task_config = config_dialog.task_config  # Assuming task_config is an attribute of IndeedBotConfigDialog
                self.task_config["session_id"] = self.session_selector.currentData()
                self.accept()  # Close the dialog after accepting
        except Exception as e:
            print(f"Error loading config dialog for {task_name}: {e}")

    def open_second_config_dialog(self):
        # Here, open the second dialog and pass the saved initial config
        # For example, if opening another instance of IndeedBotConfigDialog:
        second_dialog = IndeedBotConfigDialog()
        second_dialog.set_initial_config(self.initial_task_config)
        second_result = second_dialog.exec()
        # Handle the second dialog's result

    def get_task_config(self):
        # Return the saved task configuration
        return self.task_config if hasattr(self, 'task_config') else None
