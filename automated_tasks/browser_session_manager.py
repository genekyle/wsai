import uuid
from selenium import webdriver
from PyQt6.QtCore import QObject

class BrowserSessionManager(QObject):
    def __init__(self):
        super().__init__()
        self.sessions = {}

    def create_browser_session(self, is_warm_up=False):
        session_id = str(uuid.uuid4())
        driver = self._initialize_browser()
        self.sessions[session_id] = {
            "driver": driver,
            "is_warm_up": is_warm_up,
            "in_use": False
        }
        return session_id, driver

    def _initialize_browser(self):
        return webdriver.Chrome()

    def get_browser_session(self, session_id):
        # Return the WebDriver instance for the given session ID
        return self.sessions[session_id]["driver"]

    def release_browser_session(self, session_id):
        # Check if the session ID exists before marking it as not in use
        if session_id in self.sessions:
            self.sessions[session_id]["in_use"] = False

    def close_browser_session(self, session_id):
        print("Checking to see if the session ID exists and it's not a warm-up session before closing")
        if session_id in self.sessions and not self.sessions[session_id]["is_warm_up"]:
            session = self.sessions[session_id]
            if session["driver"]:
                session["driver"].quit()
            del self.sessions[session_id]  # Remove the session from the manager

    def list_sessions(self):
        # Return a list of session details for UI purposes
        session_details = []
        for session_id, session_info in self.sessions.items():
            detail = {
                "id": session_id,
                "status": "Warm-Up" if session_info["is_warm_up"] else "Non-Warm-Up",
                "in_use": session_info["in_use"]
            }
            session_details.append(detail)
        return session_details
