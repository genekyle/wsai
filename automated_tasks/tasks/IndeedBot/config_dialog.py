from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QHBoxLayout, QComboBox
from .user_profile_manager import load_user_profiles, save_user_profile
from .user_profile_creation_dialog import UserProfileCreationDialog

class IndeedBotConfigDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("IndeedBot Configuration")
        self.layout = QVBoxLayout(self)
        self.user_profiles = load_user_profiles()  # Load existing user profiles

        # User Profile Selection
        self.layout.addWidget(QLabel("Select User Profile:"))
        self.user_profile_selector = QComboBox()
        for profile in self.user_profiles:
            self.user_profile_selector.addItem(profile["username"])  # Assuming profiles have a username field
        self.user_profile_selector.addItem("New User Profile")
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
        for radius in ["10 miles", "20 miles", "30 miles", "40 miles", "50 miles"]:
            self.radius_selector.addItem(radius)
        self.layout.addWidget(self.radius_selector)

        # Buttons layout
        self.buttons_layout = QHBoxLayout()
        self.submit_button = QPushButton("Submit")
        self.submit_button.clicked.connect(self.accept)
        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.clicked.connect(self.reject)
        self.buttons_layout.addWidget(self.submit_button)
        self.buttons_layout.addWidget(self.cancel_button)
        self.layout.addLayout(self.buttons_layout)

        # Connect the profile selector change event
        self.user_profile_selector.currentIndexChanged.connect(self.on_profile_selection_changed)

    def on_profile_selection_changed(self, index):
        selected_profile = self.user_profile_selector.currentText()
        if selected_profile == "New User Profile":
            self.create_new_profile()

    def create_new_profile(self):
        creation_dialog = UserProfileCreationDialog()
        result = creation_dialog.exec()
        if result == QDialog.DialogCode.Accepted:
            new_profile = creation_dialog.get_profile_data()
            save_user_profile(new_profile)
            self.user_profile_selector.addItem(new_profile["username"])
            self.user_profile_selector.setCurrentText(new_profile["username"])


    def get_config(self):
        selected_profile = self.user_profile_selector.currentText()
        if selected_profile != "New User Profile":
            for profile in self.user_profiles:
                if profile["username"] == selected_profile:
                    return {
                        "task_name": "IndeedBot",
                        "user_profile": profile,
                        "job_search": self.job_search_input.text(),
                        "location": self.location_input.text(),
                        "radius": self.radius_selector.currentText()
                    }
        # If "New User Profile" is selected or no matching profile found
        return {
            "task_name": "IndeedBot",
            "user_profile": None,  # No profile selected
            "job_search": self.job_search_input.text(),
            "location": self.location_input.text(),
            "radius": self.radius_selector.currentText()
        }