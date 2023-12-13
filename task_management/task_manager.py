from PyQt6.QtCore import QObject, QThreadPool, pyqtSignal
import importlib
from task_management.task_worker import TaskWorker

class TaskManager(QObject):  # Inherit from QObject
    taskStarted = pyqtSignal(str)  # Signal for when a task starts
    taskStopped = pyqtSignal(str)  # Signal for when a task stops

    def __init__(self):
        super(TaskManager, self).__init__()  # Initialize the QObject base class
        self.thread_pool = QThreadPool()
        self.workers = {}

    def start_task(self, task_id, task_name, task_config):
        # Dynamically import the task orchestrator class
        module_name = f"automated_tasks.tasks.{task_name}.task_orchestrator"
        task_orchestrator_module = importlib.import_module(module_name)
        class_name = f"{task_name}Orchestrator"
        task_orchestrator_class = getattr(task_orchestrator_module, class_name)
        task_config['task_id'] = task_id  # Add this line to ensure task_id is in the config

        # Instantiate the orchestrator and create a worker for the task
        task_orchestrator = task_orchestrator_class(task_config)
        worker = TaskWorker(task_orchestrator_class, task_config) 
        self.taskStarted.emit(task_id)  # Emit the taskStarted signal

        worker.signals.finished.connect(lambda: self.on_task_finished(task_id))
        worker.signals.error.connect(lambda e: self.on_task_error(task_id, e))

        task_orchestrator.taskStarted.connect(lambda task_id=task_id: self.on_task_started(task_id))
        task_orchestrator.taskStopped.connect(lambda task_id=task_id: self.on_task_stopped(task_id))

        # Store the worker reference
        self.workers[task_id] = worker

        # Start the worker in the thread pool
        self.thread_pool.start(worker)

    def stop_task(self, task_id):
        if task_id in self.workers:
            worker = self.workers[task_id]
            worker.stop()
            # Do not delete the worker here, as it's still completing the stop process


    def on_task_finished(self, task_id):
        if task_id in self.workers:
            del self.workers[task_id]
            self.taskStopped.emit(task_id)

    def on_task_error(self, task_id, error):
        print(f"Error in task {task_id}: {error}")
        self.on_task_finished(task_id)