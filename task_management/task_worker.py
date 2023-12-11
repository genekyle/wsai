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
            self.task_orchestrator.execute()
        except Exception as e:
            self.signals.error.emit(e)
        finally:
            self.signals.finished.emit()

    def stop(self):
        if hasattr(self.task_orchestrator, 'stop_task'):
            self.task_orchestrator.stop_task()

    def is_stop_requested(self):
        return self._stop_requested
