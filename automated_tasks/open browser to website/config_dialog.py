from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton

class ConfigDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Configure Open Browser To Website")

        layout = QVBoxLayout(self)

        layout.addWidget(QLabel("URL:"))
        self.url_input = QLineEdit()
        layout.addWidget(self.url_input)

        submit_button = QPushButton("Submit")
        submit_button.clicked.connect(self.accept)
        layout.addWidget(submit_button)

    def get_task_config(self):
        return {"url": self.url_input.text().strip()}  # Trim any whitespace from the URL
