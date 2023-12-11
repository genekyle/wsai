from PyQt6.QtCore import QThreadPool
from task_management.task_worker import TaskWorker
import importlib

class TaskManager:
    def __init__(self):
        self.thread_pool = QThreadPool()
        self.workers = {}

    def start_task(self, task_id, task_name, task_config):
        # Dynamically import the task orchestrator class
        module_name = f"automated_tasks.tasks.{task_name}.task_orchestrator"
        task_orchestrator_module = importlib.import_module(module_name)
        class_name = f"{task_name}Orchestrator"
        task_orchestrator_class = getattr(task_orchestrator_module, class_name)

        # Instantiate the orchestrator and create a worker for the task
        task_orchestrator = task_orchestrator_class(task_config)
        worker = TaskWorker(task_orchestrator_class, task_config)  # Corrected here
        worker.signals.finished.connect(lambda: self.on_task_finished(task_id))
        worker.signals.error.connect(lambda e: self.on_task_error(task_id, e))

        # Store the worker reference
        self.workers[task_id] = worker

        # Start the worker in the thread pool
        self.thread_pool.start(worker)

    def stop_task(self, task_id):
        if task_id in self.workers:
            self.workers[task_id].stop()

    def on_task_finished(self, task_id):
        if task_id in self.workers:
            del self.workers[task_id]

    def on_task_error(self, task_id, error):
        print(f"Error in task {task_id}: {error}")
        self.on_task_finished(task_id)