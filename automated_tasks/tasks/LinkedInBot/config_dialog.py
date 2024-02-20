from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QHBoxLayout

class LinkedInBotConfigDialog(QDialog):
    def __init__(self, db_session, session_id=None):
        super().__init__()
        self.db_session = db_session
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
        
        # Assuming you want to reuse the email URL input for new search
        self.layout.addWidget(QLabel("Email Service URL:"))
        self.url_input = QLineEdit()
        self.layout.addWidget(self.url_input)

        # Setup submit and cancel buttons for new search
        self.add_submit_cancel_buttons()

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
        # Assuming you want to fetch configurations like this
        return {
            "task_name": "LinkedInBot",
            "url": self.url_input.text(),
            "task_type": "LinkedIn"
        }
