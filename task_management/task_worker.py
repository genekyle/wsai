from PyQt6.QtCore import QRunnable, pyqtSignal, QObject

class WorkerSignals(QObject):
    finished = pyqtSignal()
    error = pyqtSignal(Exception)

class TaskWorker(QRunnable):
    def __init__(self, task_orchestrator_class, task_config):
        super(TaskWorker, self).__init__()
        self.signals = WorkerSignals()
        self.task_orchestrator = task_orchestrator_class(task_config)
        self._stop_requested = False

    def run(self):
        try:
            # Execute the task
            self.task_orchestrator.execute()

            # If a stop was requested during execution, handle any additional clean-up if needed
            if self._stop_requested:
                self.handle_stop_request()
        except Exception as e:
            self.signals.error.emit(e)
        finally:
            self.signals.finished.emit()

    def stop(self):
        # Mark stop as requested
        self._stop_requested = True

        # If the task is currently running, call its stop_task method
        if hasattr(self.task_orchestrator, 'stop_task'):
            self.task_orchestrator.stop_task()

    def handle_stop_request(self):
        # Implement any additional clean-up required when a stop is requested
        pass

    def is_stop_requested(self):
        return self._stop_requested
