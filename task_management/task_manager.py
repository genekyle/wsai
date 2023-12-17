from PyQt6.QtCore import QObject, QThreadPool, pyqtSignal
import importlib
from task_management.task_worker import TaskWorker
from shared.shared_data import tasks_data


class TaskManager(QObject):
    taskStarted = pyqtSignal(str)
    taskStopped = pyqtSignal(str)
    tasksDataChanged = pyqtSignal()  # New signal


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
                
        tasks_data[task_id] = {
            "name": task_name,
            "status": "Running",
            "config": task_config
        }

        print("Task started, emitting tasksDataChanged signal.")
        self.tasksDataChanged.emit()  # Emit signal after starting a task


    def stop_task(self, task_id):
        print(f"Stopping task with ID: {task_id}")
        if task_id in self.workers:
            worker = self.workers[task_id]
            worker.stop()

            # Remove the task from tasks_data if it exists
            if task_id in tasks_data:
                del tasks_data[task_id]
                print(f"Task {task_id} removed from tasks_data.")

            # Emit the signal to indicate tasks data has changed
            self.tasksDataChanged.emit()
        else:
            print(f"No worker found for task ID: {task_id}")

    def stop_all_tasks(self):
        """
        Stop all running tasks.
        """
        print("Stopping all running tasks.")
        for task_id in list(self.workers.keys()):  # Iterate over a copy of the keys
            self.stop_task(task_id)

        # Optionally, wait for all tasks to finish if needed
        self.thread_pool.waitForDone()
            
    def get_orchestrator(self, task_id):
        orchestrator = self.orchestrators.get(task_id, None)
        print(f"Retrieving orchestrator for task {task_id}: {orchestrator}")
        return orchestrator
    
    def on_task_finished(self, task_id):
        if task_id in self.workers:
            del self.workers[task_id]
            if task_id in tasks_data:
                del tasks_data[task_id]
                print(f"Task {task_id} removed from tasks_data after completion.")

            self.taskStopped.emit(task_id)
            self.tasksDataChanged.emit()

    def on_task_error(self, task_id, error):
        print(f"Error in task {task_id}: {error}")
        if task_id in self.workers and task_id in tasks_data:
            # Optionally, you can update tasks_data with error details
            # tasks_data[task_id]["status"] = "Error"
            del tasks_data[task_id]
            print(f"Task {task_id} removed from tasks_data due to error.")

        self.on_task_finished(task_id)