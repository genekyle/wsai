from PyQt6.QtCore import QObject, QThreadPool, pyqtSignal, QMutex, QWaitCondition
from .state_manager import LinkedInBotStateManager
from automated_tasks.subtasks.navigate_to import navigate_to
from automated_tasks.browser_session_manager import BrowserSessionManager
from db.DatabaseManager import get_session, init_db, LinkedInUserProfile  # Assuming LinkedInUserProfile is the ORM class
import time
from .login_system import LinkedInLoginSystem
from .jobs import Jobs


class LinkedInBotOrchestrator(QObject):
    taskStarted = pyqtSignal(str)
    taskStopped = pyqtSignal(str)
    stateChanged = pyqtSignal(str, str)  # New signal for state changes

    def __init__(self, config, session_manager: BrowserSessionManager, session_id):
        super().__init__()
        self.config = config
        self.task_id = config.get('task_id')
        self.task_type = config.get('task_type', 'LinkedIn')  # Default to 'LinkedIn' if not specified
        self.user_profile_id = config.get('user_profile_id')  # Get the user profile ID from the config
        self.search_input = config.get('search_input')  # Get the search input from the config
        self.selected_location_id = config.get('location_id')  # Use 'location_id' to match the key used in get_config
        self.state_manager = LinkedInBotStateManager()
        self.session_manager = session_manager
        self.session_id = session_id
        self._should_stop = False
        self._is_paused = False
        self.pause_condition = QWaitCondition()
        self.mutex = QMutex()
        self.db_session = None  # Placeholder for the database session

        # Initialize the appropriate database
        print("Initializing Database")
        self.initialize_database()

    def initialize_database(self):
        # Dynamically initialize the database based on the task type
        try:
            init_db(self.task_type)
            Session = get_session(self.task_type)  # get_session now returns a class, not an instance
            self.db_session = Session()  # Correctly instantiate the session here
            print(f"{self.task_type} database initialized and session created.")
        except Exception as e:
            print(f"Error initializing {self.task_type} database: {e}")
    
    def confirm_user_profile(self):
        # Confirm the selected user profile
        if self.user_profile_id:
            user_profile = self.db_session.query(LinkedInUserProfile).filter_by(id=self.user_profile_id).first()
            if user_profile:
                print(f"Profile chosen: {user_profile.username}")
                return user_profile
            else:
                print("No profile found with the given ID.")
        else:
            print("No user profile ID provided.")

    def execute(self):
        self.session_manager.mark_session_in_use(self.session_id, in_use=True)
        user_profile = self.confirm_user_profile()  # Confirm the selected user profile

        try:
            self.taskStarted.emit(self.task_id)
            self.update_state("Initializing Browser")
            
            if self.session_id and self.session_id in self.session_manager.sessions:
                self.driver = self.session_manager.get_browser_session(self.session_id)
            else:
                self.session_id, self.driver = self.session_manager.create_browser_session(is_warm_up=False)

            # Navigate directly to the LinkedIn login page
            self.update_state("Navigating to LinkedIn Login")
            print(f"Selected Location ID: {self.selected_location_id}")
            login_system = LinkedInLoginSystem(self.session_manager, self.session_id)
            if login_system.login(user_profile.username, user_profile.password):
                self.update_state("Login Completed")
                jobs = Jobs(driver=self.driver, user_profile=user_profile, selected_location_id=self.selected_location_id, db_session=self.db_session)
                jobs.initiate_search(self.search_input)
                self.update_state("Search Initiated")
                jobs.process_results_page()

            else:
                self.update_state("Login Failed")

        finally:
            self.session_manager.mark_session_in_use(self.session_id, in_use=False)
            self.taskStopped.emit(self.task_id)
            self.update_state("Closing Browser")
            QThreadPool.globalInstance().start(lambda: self.close_browser_async())
            if self.db_session:
                self.db_session.close()

    def close_browser_async(self):
        self.session_manager.close_browser_session(self.session_id)
        self.update_state("Browser Closed")

    def stop_task(self):
        self._should_stop = True
        self.session_manager.release_browser_session(self.session_id)

    def pause_task(self):
        self.mutex.lock()
        self._is_paused = True
        self.mutex.unlock()

    def resume_task(self):
        self.mutex.lock()
        self._is_paused = False
        self.pause_condition.wakeAll()
        self.mutex.unlock()

    def update_state(self, new_state):
        self.state_manager.update_state(new_state)
        print(f"Emitting stateChanged signal for {self.task_id} with state {new_state}")
        self.stateChanged.emit(self.task_id, new_state)
