from PyQt6.QtCore import QObject, QThreadPool, pyqtSignal

from selenium.webdriver.common.by import By

from .state_manager import IndeedBotStateManager

from automated_tasks.browser_session_manager import BrowserSessionManager

from automated_tasks.subtasks.Indeed.check_login_indeed import check_login_indeed
from automated_tasks.subtasks.Indeed.check_search_success_indeed import check_search_success
from automated_tasks.subtasks.Indeed.login_to_indeed import login_to_indeed
from automated_tasks.subtasks.random_sleep import random_sleep
from automated_tasks.subtasks.navigate_to import navigate_to
from automated_tasks.subtasks.Indeed.redirect_to_homepage_indeed import redirect_to_homepage_indeed
from automated_tasks.subtasks.Indeed.start_search_indeed import start_search_indeed

from db.DatabaseManager import UserProfile  # Import the UserProfile model

from automated_tasks.tasks.IndeedBot.user_profile_manager import load_user_profiles
import time

class IndeedBotOrchestrator(QObject):
    taskStarted = pyqtSignal(str)
    taskStopped = pyqtSignal(str)
    stateChanged = pyqtSignal(str, str)  # New signal for state changes

    def __init__(self, config, session_manager: BrowserSessionManager, db_session, session_id):
        super().__init__()
        self.config = config
        self.task_id = config.get('task_id')
        self.session_manager = session_manager
        self.db_session = db_session  # Add this line to store db_session
        self.session_id = session_id
        self._should_stop = False
        self._is_paused = False 

        # Initialize the driver and state manager here
        if self.session_id and self.session_id in self.session_manager.sessions:
            self.driver = self.session_manager.get_browser_session(self.session_id)
        else:
            self.session_id, self.driver = self.session_manager.create_browser_session(is_warm_up=False)

        self.state_manager = IndeedBotStateManager(self.driver)

    def execute(self):
        # Retrieve the selected user profile name
        selected_profile_name = self.config["user_profile"]["username"]
        print(f"Selected Profile Name: {selected_profile_name}")  # Debug print

        selected_profile = self.db_session.query(UserProfile).filter_by(username=selected_profile_name).first()
        
        print(f"{selected_profile}")

        print("loading user profiles")
        user_profiles = load_user_profiles()
        print("user profiles loaded")
        if selected_profile is None:
            print(f"No profile found for {selected_profile_name}")
            return  # Terminate task execution if no profile is found
        
        print("selecting profile")
        try:
            selected_profile = next((profile for profile in user_profiles if profile.username == selected_profile_name), None)
        except:
            print("broken")
        print(f"{selected_profile}")

        if selected_profile is None:
            print(f"No profile found for {selected_profile_name}")
            return  # Terminate task execution if no profile is found

        # Use the credentials from the selected profile
        print("Assigning Credentials")
        username = selected_profile.username
        password = selected_profile.password
        print(username, ":", password)
        print("Credentials Assigned")

        # Retrieve job search, location, and radius from config
        job_search = self.config.get("job_search", "")
        location = self.config.get("location", "")
        radius = self.config.get("radius", "")
        print("search inputs assigned")
        print(job_search, ":", location, ":", radius)
        
        try:
            self.taskStarted.emit(self.task_id)
            self.update_state("Initializing Browser")

            if self.session_id and self.session_id in self.session_manager.sessions:
                self.driver = self.session_manager.get_browser_session(self.session_id)
            else:
                self.session_id, self.driver = self.session_manager.create_browser_session(is_warm_up=False)

            self.update_state("Navigating to Indeed")
            navigate_to(self.session_manager, self.session_id, "https://www.indeed.com/")
            self.update_state("Passing To Login Manager")

            # If Not Logged in, go through login process
            if not check_login_indeed(self.driver):
                self.update_state("Attempting To Login...")
                print("Check Login Returned False, Attempting To Logging In...")
                login_to_indeed(self.driver, username, password)

                print("Finished Logging Into Indeed Checking Login")

                random_sleep(2,4)

                self.update_state("Checking If Fully Logged In...")
                if check_login_indeed(self.driver):
                    print("Successfully logged in to Indeed.")
                    self.update_state("Successfully Logged in to Indeed...")

                    self.update_state("Redirecting to homepage...")
                    redirect_to_homepage_indeed(self.driver)
                    
                else:
                    print("Unsuccessful Login Attempt Trying one more time...")
                
                print("Starting The Job Search Query on Indeed...")
                self.update_state("Attempting To Start Search Using Inputs...")
                start_search_indeed(self.driver, job_search, location, radius)

                print("Checking to see if our inputs are matching to the query on Indeed...")
                self.update_state("Checking to see if search is successful...")
                check_search_success(self.driver, job_search, location, radius)
                print("Search Successful")

            while not self._should_stop:
                # Check if paused
                while self._is_paused:
                    time.sleep(1)  # Wait for a bit before checking again



                time.sleep(2)
                if self._should_stop:
                    break

            self.update_state("Completed")
        finally:
            self.taskStopped.emit(self.task_id)
            self.update_state("Closing Browser")
            QThreadPool.globalInstance().start(lambda: self.close_browser_async())

    def close_browser_async(self):
        # Use the session manager to close the browser session
        self.session_manager.close_browser_session(self.session_id)
        self.update_state("Browser Closed")

    def stop_task(self):
        self._should_stop = True
        # Release the browser session when stopping the task
        self.session_manager.release_browser_session(self.session_id)

    def update_state(self, new_state):
        self.state_manager.update_state(new_state)
        print(f"Emitting stateChanged signal for {self.task_id} with state {new_state}")
        self.stateChanged.emit(self.task_id, new_state)
