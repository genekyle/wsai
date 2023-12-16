from PyQt6.QtCore import QObject, QThreadPool, pyqtSignal
from .state_manager import CheckEmailsStateManager
from automated_tasks.subtasks.initialize_browser import initialize_browser
from automated_tasks.subtasks.navigate_to import navigate_to
from automated_tasks.subtasks.close_browser import close_browser
import time

class CheckEmailsOrchestrator(QObject):
    taskStarted = pyqtSignal(str)
    taskStopped = pyqtSignal(str)
    stateChanged = pyqtSignal(str, str)  # New signal for state changes

    def __init__(self, config):
        super().__init__()
        self.config = config
        self.task_id = config.get('task_id')  # Store the task_id
        self.state_manager = CheckEmailsStateManager()
        self.driver = None
        self._should_stop = False

    def execute(self):
        try:
            self.taskStarted.emit(self.task_id)
            self.update_state("Initializing Browser")
            self.driver = initialize_browser()  # Initialize the WebDriver here

            while not self._should_stop:
                self.update_state("Navigating to Email Service")
                navigate_to(self.driver, self.config['url'])

                # Break operation for stop signal
                time.sleep(2)
                if self._should_stop:
                    break

                # Additional logic...

            self.update_state("Completed")
        finally:
            self.taskStopped.emit(self.task_id)
            if self.driver:
                self.update_state("Closing Browser")
                QThreadPool.globalInstance().start(lambda: self.close_browser_async())

    
    def close_browser_async(self):
        close_browser(self.driver)
        self.driver = None
        self.update_state("Browser Closed")

    def stop_task(self):
        self._should_stop = True
        if self.driver:
            QThreadPool.globalInstance().start(self.driver.quit)

    def update_state(self, new_state):
        self.state_manager.update_state(new_state)
        print(f"Emitting stateChanged signal for {self.task_id} with state {new_state}")
        self.stateChanged.emit(self.task_id, new_state)
   


    # Removed start_task method, as it seems unnecessary
