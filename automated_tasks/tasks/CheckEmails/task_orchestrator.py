from PyQt6.QtCore import QObject
from .state_manager import CheckEmailsStateManager
from automated_tasks.subtasks.initialize_browser import initialize_browser
from automated_tasks.subtasks.navigate_to import navigate_to
from automated_tasks.subtasks.close_browser import close_browser
import time

class CheckEmailsOrchestrator(QObject):
    def __init__(self, config):
        super().__init__()
        self.config = config
        self.state_manager = CheckEmailsStateManager()
        self.driver = None
        self._should_stop = False

    def execute(self):
        try:
            self.state_manager.update_state("Initializing Browser")
            self.driver = initialize_browser()

            while not self._should_stop:
                self.state_manager.update_state("Navigating to Email Service")
                navigate_to(self.driver, self.config['url'])

                # Break the operation into smaller steps to frequently check for stop signal
                for _ in range(10):
                    time.sleep(0.5)
                    if self._should_stop:
                        return  # Exit the method if stopping is requested

                # Add additional email checking logic here...

            self.state_manager.update_state("Completed")
        finally:
            if self.driver:
                self.state_manager.update_state("Closing Browser")
                close_browser(self.driver)
                self.state_manager.update_state("Browser Closed")

    def stop_task(self):
        self._should_stop = True
