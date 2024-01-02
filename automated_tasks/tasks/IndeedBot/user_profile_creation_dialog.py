from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton

class UserProfileCreationDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Create New User Profile")

        layout = QVBoxLayout(self)

        # Username input
        layout.addWidget(QLabel("Username:"))
        self.username_input = QLineEdit()
        layout.addWidget(self.username_input)

        # Password input
        layout.addWidget(QLabel("Password:"))
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(self.password_input)

        # Submit button
        submit_button = QPushButton("Create Profile")
        submit_button.clicked.connect(self.accept)
        layout.addWidget(submit_button)

    def get_profile_data(self):
        return {
            "username": self.username_input.text(),
            "password": self.password_input.text()
        }
