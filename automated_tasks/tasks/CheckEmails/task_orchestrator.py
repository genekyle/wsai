from PyQt6.QtCore import QObject, QThreadPool, pyqtSignal, QMutex, QWaitCondition
from .state_manager import CheckEmailsStateManager
from automated_tasks.subtasks.navigate_to import navigate_to
from automated_tasks.browser_session_manager import BrowserSessionManager
import time

class CheckEmailsOrchestrator(QObject):
    taskStarted = pyqtSignal(str)
    taskStopped = pyqtSignal(str)
    stateChanged = pyqtSignal(str, str)  # New signal for state changes

    def __init__(self, config, session_manager: BrowserSessionManager, session_id):
        super().__init__()
        self.config = config
        self.task_id = config.get('task_id')
        self.state_manager = CheckEmailsStateManager()
        self.session_manager = session_manager
        self.session_id = session_id
        self._should_stop = False
        self._is_paused = False
        self.pause_condition = QWaitCondition()
        self.mutex = QMutex()

    def execute(self):
        self.session_manager.mark_session_in_use(self.session_id, in_use=True)
        try:
            self.taskStarted.emit(self.task_id)
            self.update_state("Initializing Browser")
            
            if self.session_id and self.session_id in self.session_manager.sessions:
                self.driver = self.session_manager.get_browser_session(self.session_id)
            else:
                self.session_id, self.driver = self.session_manager.create_browser_session(is_warm_up=False)

            while not self._should_stop:
                self.mutex.lock()
                while self._is_paused:
                    self.pause_condition.wait(self.mutex)
                self.mutex.unlock()

                self.update_state("Navigating to Email Service")
                navigate_to(self.session_manager, self.session_id, self.config['url'])
                print("sleeping pretending to be complex equation")
                time.sleep(2)
                print("sleeping...")
                time.sleep(1)
                if self._should_stop:
                    break   

            self.update_state("Completed")
        finally:
            self.session_manager.mark_session_in_use(self.session_id, in_use=False)
            self.taskStopped.emit(self.task_id)
            self.update_state("Closing Browser")
            QThreadPool.globalInstance().start(lambda: self.close_browser_async())

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
