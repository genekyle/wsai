from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton

class ConfigDialog(QDialog):
    def __init__(self, task_name, parent=None):
        super().__init__(parent)
        self.setWindowTitle(f"Configure {task_name}")

        layout = QVBoxLayout(self)

        # Dynamic field generation based on the task
        if task_name == "Open Browser To Website":
            layout.addWidget(QLabel("URL:"))
            self.url_input = QLineEdit()
            layout.addWidget(self.url_input)

        # Additional configuration fields can be added here for different tasks

        submit_button = QPushButton("Submit")
        submit_button.clicked.connect(self.accept)
        layout.addWidget(submit_button)

    def get_task_config(self):
        # Return a dictionary of configurations; adjust based on task requirements
        return {"url": self.url_input.text()} if hasattr(self, 'url_input') else {}
