from PyQt6.QtCore import QObject, QThreadPool, pyqtSignal
from .state_manager import CheckEmailsStateManager
from automated_tasks.subtasks.initialize_browser import initialize_browser
from automated_tasks.subtasks.navigate_to import navigate_to
from automated_tasks.subtasks.close_browser import close_browser
import time

class CheckEmailsOrchestrator(QObject):
    taskStarted = pyqtSignal(str)
    taskStopped = pyqtSignal(str)

    def __init__(self, config):
        super().__init__()
        self.config = config
        self.task_id = config.get('task_id')  # Store the task_id

        self.state_manager = CheckEmailsStateManager()
        self.driver = None
        self._should_stop = False

    def execute(self):
        try:
            self.taskStarted.emit(self.task_id)  # Use stored task_id
            self.state_manager.update_state("Initializing Browser")
            self.driver = initialize_browser()
            
            while not self._should_stop:
                self.state_manager.update_state("Navigating to Email Service")
                navigate_to(self.driver, self.config['url'])

                # Here, break the operation into smaller checks for stop signal
                time.sleep(2)  # Example: Pause for a second
                if self._should_stop:
                    break  # Exit the loop if stop signal is received

                # Add additional email checking logic here...
                # Remember to check self._should_stop periodically

            self.state_manager.update_state("Completed")
        finally:
            self.taskStopped.emit(self.task_id)  # Use stored task_id
            if self.driver:
                self.state_manager.update_state("Closing Browser")
                QThreadPool.globalInstance().start(lambda: self.close_browser_async())
    
    def close_browser_async(self):
        close_browser(self.driver)
        self.driver = None
        self.state_manager.update_state("Browser Closed")

    def stop_task(self):
        self._should_stop = True
        if self.driver:
            QThreadPool.globalInstance().start(self.driver.quit)

    def start_task(self, task_id, task_name, task_config):
        task_config['task_id'] = task_id