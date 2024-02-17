from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QHBoxLayout

class CheckEmailsConfigDialog(QDialog):
    def __init__(self, db_session, session_id=None):
        super().__init__()
        self.db_session = db_session
        self.session_id = session_id  # Store the session ID
        self.setWindowTitle("Check Emails Configuration")
        self.layout = QVBoxLayout(self)

        # Email service URL input
        self.layout.addWidget(QLabel("Email Service URL:"))
        self.url_input = QLineEdit()
        self.layout.addWidget(self.url_input)

        # Buttons layout
        self.buttons_layout = QHBoxLayout()
        self.submit_button = QPushButton("Submit")
        self.submit_button.clicked.connect(self.accept)
        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.clicked.connect(self.reject)

        self.buttons_layout.addWidget(self.submit_button)
        self.buttons_layout.addWidget(self.cancel_button)
        self.layout.addLayout(self.buttons_layout)

    def get_config(self):
        return {
            "task_name": "CheckEmails",
            "url": self.url_input.text()
        }
