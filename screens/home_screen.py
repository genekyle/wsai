# screens/home_screen.py
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QLabel, QTableWidget, 
                             QTableWidgetItem, QSizePolicy, QHBoxLayout, QSpacerItem)
from shared.shared_data import tasks_data
import json

class HomeScreen(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)

        home_label = QLabel("Content of Home Screen", self)
        layout.addWidget(home_label)

        self.preview_table = QTableWidget()
        self.preview_table.setColumnCount(3)
        self.preview_table.setHorizontalHeaderLabels(["Task", "Status", "Config"])
        self.preview_table.setShowGrid(False)
        self.preview_table.setSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Maximum)

        preview_layout = QHBoxLayout()
        preview_layout.addWidget(self.preview_table)
        preview_layout.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))
        layout.addLayout(preview_layout)
        layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))

        self.update_preview_table()

    def update_preview_table(self):
        self.preview_table.setRowCount(len(tasks_data))
        for i, (task_id, task_info) in enumerate(tasks_data.items()):
            self.preview_table.setItem(i, 0, QTableWidgetItem(task_info["name"]))
            self.preview_table.setItem(i, 1, QTableWidgetItem(task_info["status"]))
            # Convert the config dictionary to a JSON string for display
            config_str = json.dumps(task_info.get("config", {}), indent=2)
            self.preview_table.setItem(i, 2, QTableWidgetItem(config_str))
