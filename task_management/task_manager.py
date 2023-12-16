from PyQt6.QtCore import QObject, QThreadPool, pyqtSignal
import importlib
from task_management.task_worker import TaskWorker

class TaskManager(QObject):
    taskStarted = pyqtSignal(str)
    taskStopped = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.thread_pool = QThreadPool()
        self.workers = {}
        self.orchestrators = {}  # Store references to orchestrators

    def start_task(self, task_id, task_name, task_config):
        module_name = f"automated_tasks.tasks.{task_name}.task_orchestrator"
        task_orchestrator_module = importlib.import_module(module_name)
        class_name = f"{task_name}Orchestrator"
        task_orchestrator_class = getattr(task_orchestrator_module, class_name)
        task_config['task_id'] = task_id

        task_orchestrator = task_orchestrator_class(task_config)
        self.orchestrators[task_id] = task_orchestrator  # Instantiate and store first
        print(f"Instantiating orchestrator for task {task_id}")

        worker = TaskWorker(task_orchestrator, task_config)
        self.workers[task_id] = worker

        self.thread_pool.start(worker)
        self.taskStarted.emit(task_id)

    def stop_task(self, task_id):
        print(f"Stopping task with ID: {task_id}")
        # Check if the task_id is in self.workers
        if task_id in self.workers:
            worker = self.workers[task_id]
            worker.stop()
        else:
            print(f"No worker found for task ID: {task_id}")
            
    def get_orchestrator(self, task_id):
        orchestrator = self.orchestrators.get(task_id, None)
        print(f"Retrieving orchestrator for task {task_id}: {orchestrator}")
        return orchestrator
    
    def on_task_finished(self, task_id):
        if task_id in self.workers:
            del self.workers[task_id]
            self.taskStopped.emit(task_id)

    def on_task_error(self, task_id, error):
        print(f"Error in task {task_id}: {error}")
        self.on_task_finished(task_id)