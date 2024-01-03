from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QHBoxLayout, QComboBox
import os
import json

class IndeedBotConfigDialog(QDialog):
    def __init__(self, session_id=None):
        super().__init__()
        self.setWindowTitle("IndeedBot Configuration")
        self.layout = QVBoxLayout(self)
        self.session_id = session_id  # Store the session ID


        self.user_profiles = self.load_user_profiles()

        # User Profile Selection
        self.layout.addWidget(QLabel("Select User Profile:"))
        self.user_profile_selector = QComboBox()
        self.populate_user_profiles_dropdown()
        self.layout.addWidget(self.user_profile_selector)

        # Job Search Input
        self.layout.addWidget(QLabel("Job To Search:"))
        self.job_search_input = QLineEdit()
        self.layout.addWidget(self.job_search_input)

        # Location Input
        self.layout.addWidget(QLabel("Location:"))
        self.location_input = QLineEdit()
        self.layout.addWidget(self.location_input)

        # Radius Selection
        self.layout.addWidget(QLabel("Radius (miles):"))
        self.radius_selector = QComboBox()
        for radius in ["5 miles", "10 miles", "15 miles", "25 miles", "35 miles", "50 miles", "100 miles"]:
            self.radius_selector.addItem(radius)
        self.layout.addWidget(self.radius_selector)

        # Buttons layout
        self.setup_buttons()

        # Connect signals
        self.submit_button.clicked.connect(self.on_submit_clicked)

    def setup_buttons(self):
        self.buttons_layout = QHBoxLayout()
        self.submit_button = QPushButton("Submit")
        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.clicked.connect(self.reject)
        self.buttons_layout.addWidget(self.submit_button)
        self.buttons_layout.addWidget(self.cancel_button)
        self.layout.addLayout(self.buttons_layout)

    def populate_user_profiles_dropdown(self):
        self.user_profile_selector.clear()
        for profile in self.user_profiles:
            self.user_profile_selector.addItem(profile["username"])
        self.user_profile_selector.addItem("New User Profile")

    def load_user_profiles(self):
        file_path = os.path.join("automated_tasks", "tasks", "IndeedBot", "UserProfiles", "profiles.json")
        if os.path.exists(file_path):
            with open(file_path, "r") as file:
                return json.load(file)
        return []

    def save_new_profile(self, username, password):
        if username and password:
            new_profile = {"username": username, "password": password}
            self.user_profiles.append(new_profile)
            self.save_profiles_to_json()
            self.populate_user_profiles_dropdown()
            self.user_profile_selector.setCurrentText(username)

    def save_profiles_to_json(self):
        directory = os.path.join("automated_tasks", "tasks", "IndeedBot", "UserProfiles")
        if not os.path.exists(directory):
            os.makedirs(directory)
        file_path = os.path.join(directory, "profiles.json")
        with open(file_path, "w") as file:
            json.dump(self.user_profiles, file, indent=4)

    def on_submit_clicked(self):
        selected_profile = self.user_profile_selector.currentText()
        if selected_profile == "New User Profile":
            new_profile_dialog = NewProfileConfigDialog(self)
            if new_profile_dialog.exec() == QDialog.DialogCode.Accepted:
                new_profile = {
                    "username": new_profile_dialog.username_input.text(),
                    "password": new_profile_dialog.password_input.text()
                }
                self.user_profiles.append(new_profile)
                self.save_profiles_to_json()
                self.user_profile_selector.addItem(new_profile["username"])
                self.user_profile_selector.setCurrentText(new_profile["username"])
                # Now that a new profile is created and selected, call get_config
                self.task_config = self.get_config()
                self.accept()
            else:
                # Handle the case where new profile creation is cancelled
                return
        else:
            # If an existing profile is selected, just get the config and close
            self.task_config = self.get_config()
            self.accept()
        
    def open_new_profile_dialog(self):
        new_profile_dialog = NewProfileConfigDialog(self)
        new_profile_result = new_profile_dialog.exec()
        if new_profile_result == QDialog.DialogCode.Accepted:
            # Handle the test dialog submission here
            print("New Profile Dialog submitted.")
        self.accept()  # This will close the IndeedBotConfigDialog

    def get_config(self):
        selected_profile = self.user_profile_selector.currentText()
        job_search = self.job_search_input.text()
        location = self.location_input.text()
        radius = self.radius_selector.currentText()

        if selected_profile != "New User Profile":
            for profile in self.user_profiles:
                if profile["username"] == selected_profile:
                    return {
                        "task_name": "IndeedBot",
                        "user_profile": profile,
                        "job_search": job_search,
                        "location": location,
                        "radius": radius
                    }

        return {
            "task_name": "IndeedBot",
            "user_profile": None,
            "job_search": job_search,
            "location": location,
            "radius": radius
        }

class NewProfileConfigDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("New Profile Configuration")
        layout = QVBoxLayout(self)

        # Username Input
        layout.addWidget(QLabel("Username:"))
        self.username_input = QLineEdit()  # Define as an instance attribute
        layout.addWidget(self.username_input)

        # Username Input
        layout.addWidget(QLabel("Password:"))
        self.password_input = QLineEdit()  # Define as an instance attribute
        layout.addWidget(self.password_input)

        submit_button = QPushButton("Submit")
        submit_button.clicked.connect(self.accept)
        layout.addWidget(submit_button)

    def accept(self):
        # You can handle the data here or in another method
        username = self.username_input.text()
        password = self.password_input.text()
        print("Username:", username)
        print("Password:", password)
        super().accept()  # Ensure this is called to close the dialog properly