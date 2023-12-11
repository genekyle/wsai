from PyQt6.QtCore import QThreadPool
from task_management.task_worker import TaskWorker

class TaskManager:
    def __init__(self):
        self.thread_pool = QThreadPool()
        self.workers = {}  # Dictionary to store workers

    def start_task(self, task_id, task_orchestrator_class, task_config):
        # Create a worker for the task
        worker = TaskWorker(task_orchestrator_class, task_config)
        worker.signals.finished.connect(lambda: self.on_task_finished(task_id))
        worker.signals.error.connect(lambda e: self.on_task_error(task_id, e))

        # Store the worker reference
        self.workers[task_id] = worker

        # Start the worker in the thread pool
        self.thread_pool.start(worker)

    def stop_task(self, task_id):
        # Signal the worker to stop
        if task_id in self.workers:
            self.workers[task_id].stop()

    def on_task_finished(self, task_id):
        # Remove the worker from the dictionary
        if task_id in self.workers:
            del self.workers[task_id]

    def on_task_error(self, task_id, error):
        print(f"Error in task {task_id}: {error}")
        self.on_task_finished(task_id)
