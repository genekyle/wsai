from PyQt6.QtCore import QObject
from .state_manager import CheckEmailsStateManager
# Import the function directly
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
        self.stop_requested = False


    def execute(self):
        try:
            while not self.stop_requested:
                self.state_manager.update_state("Initializing Browser")
                self.driver = initialize_browser()  # This should now work correctly

                self.state_manager.update_state("Navigating to Email Service")
                navigate_to(self.driver, self.config['url'])

                time.sleep(2.5)  # Wait for a bit to visually confirm the browser is open

                self.state_manager.update_state("Completed")
        finally:
            # Clean up resources
            if self.driver:
                self.driver.quit()
    
    def stop_task(self):
        self.stop_requested = True