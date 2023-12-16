from PyQt6.QtCore import QRunnable, pyqtSignal, QObject

class WorkerSignals(QObject):
    finished = pyqtSignal()
    error = pyqtSignal(Exception)

class TaskWorker(QRunnable):
    def __init__(self, task_orchestrator, task_config):
        super(TaskWorker, self).__init__()
        self.signals = WorkerSignals()
        self.task_orchestrator = task_orchestrator  # Already an instance, no need to instantiate
        self._stop_requested = False

    def run(self):
        try:
            self.task_orchestrator.execute()
            if self._stop_requested:
                self.handle_stop_request()
        except Exception as e:
            self.signals.error.emit(e)
        finally:
            self.signals.finished.emit()

    def stop(self):
        self._stop_requested = True
        if hasattr(self.task_orchestrator, 'stop_task'):
            self.task_orchestrator.stop_task()

    def handle_stop_request(self):
        pass

    def is_stop_requested(self):
        return self._stop_requested
