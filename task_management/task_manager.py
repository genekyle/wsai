from PyQt6.QtCore import QObject, QThreadPool, pyqtSignal
import importlib
from task_management.task_worker import TaskWorker
from shared.shared_data import tasks_data
from automated_tasks.browser_session_manager import BrowserSessionManager
from db.DatabaseManager import Session  # Import Session

class TaskManager(QObject):
    taskStarted = pyqtSignal(str)
    taskStopped = pyqtSignal(str)
    tasksDataChanged = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.thread_pool = QThreadPool()
        self.workers = {}
        self.orchestrators = {}
        self.session_manager = BrowserSessionManager()
        self.db_session = Session()

    def start_task(self, task_id, task_name, task_config):
        module_name = f"automated_tasks.tasks.{task_name}.task_orchestrator"
        task_orchestrator_module = importlib.import_module(module_name)

        class_name = f"{task_name}Orchestrator"
        task_orchestrator_class = getattr(task_orchestrator_module, class_name)

        task_config['task_id'] = task_id

        session_id = task_config.get('session_id')
        session_in_use = False
        is_warm_up_session = False

        if session_id and session_id in self.session_manager.sessions:
            session_in_use = self.session_manager.sessions[session_id].get('in_use', False)
            is_warm_up_session = self.session_manager.sessions[session_id].get('is_warm_up', False)

        if not session_id or session_in_use or not is_warm_up_session:
            session_id, _ = self.session_manager.create_browser_session()
        else:
            self.session_manager.mark_session_in_use(session_id, in_use=True)

        task_orchestrator = task_orchestrator_class(task_config, self.session_manager, self.db_session, session_id)
        self.orchestrators[task_id] = task_orchestrator

        worker = TaskWorker(task_orchestrator, task_config)
        self.workers[task_id] = worker
        self.thread_pool.start(worker)

        self.taskStarted.emit(task_id)
                    
        tasks_data[task_id] = {
            "name": task_name,
            "status": "Running",
            "config": task_config
        }

        print(f"Task '{task_name}' with ID {task_id} started, using session ID {session_id}. Session in use: {session_in_use}, Is warm-up: {is_warm_up_session}")
        self.tasksDataChanged.emit()

    def stop_task(self, task_id):
        print(f"Stopping task with ID: {task_id}")
        if task_id in self.workers:
            worker = self.workers[task_id]
            worker.stop()

            if task_id in tasks_data:
                del tasks_data[task_id]
                print(f"Task {task_id} removed from tasks_data.")

            session_id = self.orchestrators[task_id].session_id
            self.session_manager.mark_session_in_use(session_id, in_use=False)

            self.tasksDataChanged.emit()
        else:
            print(f"No worker found for task ID: {task_id}")

    def stop_all_tasks(self):
        print("Stopping all running tasks.")
        for task_id in list(self.workers.keys()):
            self.stop_task(task_id)

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
            del tasks_data[task_id]
            print(f"Task {task_id} removed from tasks_data due to error.")

        self.on_task_finished(task_id)
