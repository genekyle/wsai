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
        self.stop_requested = False
        self.driver = None

    def execute(self):
        try:
            self.state_manager.update_state("Initializing Browser")
            self.driver = initialize_browser()

            if self.stop_requested:
                return

            self.state_manager.update_state("Navigating to Email Service")
            navigate_to(self.driver, self.config['url'])

            time.sleep(2)  # Simulate task duration

            if self.stop_requested:
                return

            self.state_manager.update_state("Task Completed")
        finally:
            if self.driver:
                self.driver.quit()
                self.state_manager.update_state("Browser Closed")

    def stop_task(self):
        self.stop_requested = True
        if self.driver:
            self.driver.quit()
