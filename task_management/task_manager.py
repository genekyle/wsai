# task_manager/task_worker.py

from PyQt6.QtCore import QRunnable, pyqtSignal

class TaskWorker(QRunnable):
    finished = pyqtSignal()
    error = pyqtSignal(Exception)

    def __init__(self, task_function, *args, **kwargs):
        super(TaskWorker, self).__init__()
        self.task_function = task_function
        self.args = args
        self.kwargs = kwargs

    def run(self):
        try:
            self.task_function(*self.args, **self.kwargs)
        except Exception as e:
            self.error.emit(e)
        finally:
            self.finished.emit()
