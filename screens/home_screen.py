from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QTableWidget, \
                           QTableWidgetItem, QSizePolicy, QHBoxLayout, QSpacerItem
from shared.shared_data import tasks_data, TASK_DISPLAY_NAMES
from db.DatabaseManager import IndeedUserProfile
import json

class HomeScreen(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)

        home_label = QLabel("Content of Home Screen", self)
        layout.addWidget(home_label)
    
        self.preview_table = QTableWidget()
        self.preview_table.setColumnCount(2)  # Set to 2 columns
        self.preview_table.setHorizontalHeaderLabels(["Task", "Status"])
        self.preview_table.setShowGrid(False)
        self.preview_table.setSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Maximum)

        preview_layout = QHBoxLayout()
        preview_layout.addWidget(self.preview_table)
        preview_layout.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))
        layout.addLayout(preview_layout)
        layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))

        self.update_preview_table()

    def update_preview_table(self):
        # Clear the table first
        self.preview_table.setRowCount(0)

        # Repopulate the table with updated tasks data
        for i, (task_id, task_info) in enumerate(tasks_data.items()):
            task_name_display = TASK_DISPLAY_NAMES.get(task_info["name"], task_info["name"])
            self.preview_table.insertRow(i)
            self.preview_table.setItem(i, 0, QTableWidgetItem(task_name_display))
            self.preview_table.setItem(i, 1, QTableWidgetItem(task_info["status"]))

            # Prepare configuration for serialization
            config = task_info.get("config", {})
            if 'user_profile' in config and isinstance(config['user_profile'], IndeedUserProfile):
                config['user_profile'] = vars(config['user_profile'])  # Convert UserProfile to dict

            config_str = json.dumps(config, indent=2, default=str)  # Use default=str to handle non-serializable types
            self.preview_table.setItem(i, 2, QTableWidgetItem(config_str))
