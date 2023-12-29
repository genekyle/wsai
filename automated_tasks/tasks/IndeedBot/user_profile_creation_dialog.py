from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QHBoxLayout

class UserProfileCreationDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Create New User Profile")
        self.layout = QVBoxLayout(self)

        # Username input
        self.layout.addWidget(QLabel("Username:"))
        self.username_input = QLineEdit()
        self.layout.addWidget(self.username_input)

        # Password input
        self.layout.addWidget(QLabel("Password:"))
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.layout.addWidget(self.password_input)

        # Buttons layout
        self.buttons_layout = QHBoxLayout()
        self.submit_button = QPushButton("Create Profile")
        self.submit_button.clicked.connect(self.accept)
        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.clicked.connect(self.reject)
        self.buttons_layout.addWidget(self.submit_button)
        self.buttons_layout.addWidget(self.cancel_button)
        self.layout.addLayout(self.buttons_layout)

    def get_profile_data(self):
        return {
            "username": self.username_input.text(),
            "password": self.password_input.text()
        }
