from PyQt6.QtWidgets import QDialog, QVBoxLayout, QComboBox, QPushButton, QHBoxLayout, QLabel, QWidget

class TaskConfigDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Configure Task")
        self.layout = QVBoxLayout()

        self.task_selector = QComboBox()
        self.task_selector.addItems(["Task 1", "Task 2", "Task 3"])
        self.task_selector.currentIndexChanged.connect(self.update_config_options)
        self.layout.addWidget(self.task_selector)

        self.config_options_container = QWidget()
        self.config_options_layout = QVBoxLayout()
        self.config_options_container.setLayout(self.config_options_layout)
        self.layout.addWidget(self.config_options_container)

        self.buttons_layout = QHBoxLayout()
        self.submit_button = QPushButton("Submit")
        self.submit_button.clicked.connect(self.accept)
        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.clicked.connect(self.reject)
        self.buttons_layout.addWidget(self.submit_button)
        self.buttons_layout.addWidget(self.cancel_button)
        self.layout.addLayout(self.buttons_layout)

        self.setLayout(self.layout)
        self.update_config_options()

    def update_config_options(self):
        for i in reversed(range(self.config_options_layout.count())): 
            widget = self.config_options_layout.takeAt(i).widget()
            if widget is not None:
                widget.deleteLater()

        task = self.task_selector.currentText()
        if task == "Task 1":
            self.config_options_layout.addWidget(QLabel("Config for Task 1"))
            # Add more widgets as needed...
        elif task == "Task 2":
            self.config_options_layout.addWidget(QLabel("Config for Task 2"))
            # Add more widgets as needed...
        # ... Handle other tasks similarly ...

    def get_task_config(self):
        return self.task_selector.currentText()
