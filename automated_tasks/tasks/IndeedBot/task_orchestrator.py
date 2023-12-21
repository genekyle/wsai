from PyQt6.QtCore import QObject, QThreadPool, pyqtSignal
from .state_manager import IndeedBotStateManager
from automated_tasks.subtasks.navigate_to import navigate_to
from automated_tasks.browser_session_manager import BrowserSessionManager
import time

class IndeedBotOrchestrator(QObject):
    taskStarted = pyqtSignal(str)
    taskStopped = pyqtSignal(str)
    stateChanged = pyqtSignal(str, str)  # New signal for state changes

    def __init__(self, config, session_manager: BrowserSessionManager, session_id):
        super().__init__()
        self.config = config
        self.task_id = config.get('task_id')
        self.state_manager = IndeedBotStateManager()
        self.session_manager = session_manager
        self.session_id = session_id
        self._should_stop = False

    def execute(self):
        try:
            self.taskStarted.emit(self.task_id)
            self.update_state("Initializing Browser")
            # Check if the session ID corresponds to an existing session
            if self.session_id and self.session_id in self.session_manager.sessions:
                self.driver = self.session_manager.get_browser_session(self.session_id)
            else:
                # If no valid session ID, create a new session
                self.session_id, self.driver = self.session_manager.create_browser_session(is_warm_up=False)

            while not self._should_stop:
                self.update_state("Navigating to Email Service")
                navigate_to(self.session_manager, self.session_id, self.config['url'])
                
                # Break operation for stop signal
                time.sleep(2)
                if self._should_stop:
                    print("_should_stop triggered at execution")
                    break

                # Additional task-specific logic can be added here

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
