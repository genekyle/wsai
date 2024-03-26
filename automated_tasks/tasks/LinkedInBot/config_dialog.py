from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QComboBox, QLineEdit
from db.DatabaseManager import get_session, LinkedInUserProfile, LinkedInLocation

class LinkedInBotConfigDialog(QDialog):
    def __init__(self, db_session, session_id=None):
        super().__init__()
        self.db_session = get_session("LinkedIn")()  # Notice we call the returned session class to create an instance
        self.session_id = session_id  # Store the session ID
        self.setWindowTitle("LinkedInBot")
        self.layout = QVBoxLayout(self)

        # Initial setup
        self.setup_initial_buttons()

    def setup_initial_buttons(self):
        # Clear the existing layout
        self.clear_layout(self.layout)

        # Add initial buttons for New Search or Previous Search
        self.new_search_button = QPushButton("New Search")
        self.new_search_button.clicked.connect(self.setup_new_search)
        self.previous_search_button = QPushButton("Previous Search")
        self.previous_search_button.clicked.connect(self.setup_previous_search)

        self.layout.addWidget(self.new_search_button)
        self.layout.addWidget(self.previous_search_button)

    def setup_new_search(self):
        # Setup layout for new search
        self.clear_layout(self.layout)
        
        # Dropdown for selecting or creating a user profile
        self.layout.addWidget(QLabel("Select User Profile:"))
        self.user_profile_dropdown = QComboBox()
        self.populate_user_profiles()
        self.layout.addWidget(self.user_profile_dropdown)

        # Dropdown for selecting Area (Location)
        self.layout.addWidget(QLabel("Select Area:"))
        self.area_dropdown = QComboBox()
        self.populate_locations()  # Populate the dropdown with locations
        self.layout.addWidget(self.area_dropdown)

        # Add input field for search input
        self.layout.addWidget(QLabel("Search Input:"))
        self.search_input = QLineEdit()
        self.layout.addWidget(self.search_input)

        # Setup submit and cancel buttons for new search
        self.add_submit_cancel_buttons()

    def populate_locations(self):
        # Query the database for existing locations and add them to the dropdown
        locations = self.db_session.query(LinkedInLocation).all()
        for location in locations:
            self.area_dropdown.addItem(location.name, location.id)

    def populate_user_profiles(self):
        # Query the database for existing LinkedIn user profiles and add them to the dropdown
        user_profiles = self.db_session.query(LinkedInUserProfile).all()
        for profile in user_profiles:
            self.user_profile_dropdown.addItem(profile.username, profile.id)
        self.user_profile_dropdown.addItem("New User Profile", None)  # For creating a new profile

    def setup_previous_search(self):
        # Setup layout for previous search
        self.clear_layout(self.layout)
        
        # For previous search, you might want to display different content
        # This is a placeholder for whatever content you'd like to display or configure
        self.layout.addWidget(QLabel("Placeholder for previous search settings"))

        # Setup submit and cancel buttons for previous search
        self.add_submit_cancel_buttons()

    def add_submit_cancel_buttons(self):
        # Add Submit and Cancel buttons
        self.submit_button = QPushButton("Submit")
        self.submit_button.clicked.connect(self.accept)
        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.clicked.connect(self.reject)
        
        self.buttons_layout = QHBoxLayout()
        self.buttons_layout.addWidget(self.submit_button)
        self.buttons_layout.addWidget(self.cancel_button)
        self.layout.addLayout(self.buttons_layout)

    def clear_layout(self, layout):
        # Function to clear the layout
        for i in reversed(range(layout.count())): 
            widget = layout.itemAt(i).widget()
            if widget is not None:
                widget.deleteLater()
            else:
                layout.itemAt(i).layout().deleteLater()

    def get_config(self):
        # Fetch configurations like this
        selected_profile_id = self.user_profile_dropdown.currentData()
        # Fetching the text from the search input field
        search_input = self.search_input.text()
        selected_location_id = self.area_dropdown.currentData()  # Get the selected location ID

        if selected_profile_id is None:
            # Handle new user profile creation
            pass  # Placeholder for actual logic

        return {
            "task_name": "LinkedInBot",
            "user_profile_id": selected_profile_id,
            "task_type": "LinkedIn",
            "search_input": search_input,
            "location_id": selected_location_id
        }
