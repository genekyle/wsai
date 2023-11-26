from PyQt6.QtWidgets import QDialog, QVBoxLayout, QComboBox, QPushButton, QHBoxLayout, QLabel, QLineEdit

class TaskConfigDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        print("Initializing TaskConfigDialog")  # Debug print
        self.setWindowTitle("Configure Task")
        self.layout = QVBoxLayout()

        # Task selector dropdown
        self.task_selector = QComboBox()
        self.task_selector.addItems(["Open Browser To Website", "Task 2", "Task 3"])
        print("Task selector added with items.")  # Debug print
        self.task_selector.currentIndexChanged.connect(self.update_config_options)
        self.layout.addWidget(self.task_selector)

        # URL input for the "Open Browser To Website" task
        self.url_input = QLineEdit()
        self.layout.addWidget(self.url_input)
        self.url_input.hide()  # Initially hidden
        print("URL input initialized and hidden.")  # Debug print

        # Buttons layout
        self.buttons_layout = QHBoxLayout()
        self.submit_button = QPushButton("Submit")
        self.submit_button.clicked.connect(self.accept)
        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.clicked.connect(self.reject)
        self.buttons_layout.addWidget(self.submit_button)
        self.buttons_layout.addWidget(self.cancel_button)
        self.layout.addLayout(self.buttons_layout)

        self.setLayout(self.layout)
        print("Layout set for the dialog.")  # Debug print

    def update_config_options(self):
        task = self.task_selector.currentText()
        print(f"Task selected: {task}")  # Debug print
        if task == "Open Browser To Website":
            self.url_input.show()
            print("URL input shown.")  # Debug print
        else:
            self.url_input.hide()
            print("URL input hidden.")  # Debug print

    def get_task_config(self):
        task_name = self.task_selector.currentText()
        url = self.url_input.text() if task_name == "Open Browser To Website" else ""
        print(f"Task config collected: Task Name - {task_name}, URL - {url}")  # Debug print
        return {
            "task_name": task_name,
            "url": url
        }
