from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QPushButton, QTableWidget, 
                             QTableWidgetItem, QHeaderView, QHBoxLayout, QDialog)
from dialogs.task_config_dialog import TaskConfigDialog

# ActionButtonsWidget class
class ActionButtonsWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Play Button
        self.playButton = QPushButton("Play")
        self.playButton.clicked.connect(self.play_action)
        layout.addWidget(self.playButton)

        # Pause Button
        self.pauseButton = QPushButton("Pause")
        self.pauseButton.clicked.connect(self.pause_action)
        layout.addWidget(self.pauseButton)

        # Edit Button
        self.editButton = QPushButton("Edit")
        self.editButton.clicked.connect(self.edit_action)
        layout.addWidget(self.editButton)

        # Delete Button
        self.deleteButton = QPushButton("Delete")
        self.deleteButton.clicked.connect(self.delete_action)
        layout.addWidget(self.deleteButton)

        self.setLayout(layout)

    def play_action(self):
        # Define play action here
        pass

    def pause_action(self):
        # Define pause action here
        pass

    def edit_action(self):
        # Define edit action here
        pass

    def delete_action(self):
        # Define delete action here
        pass

# TaskScreen class
class TaskScreen(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout(self)

        self.add_task_button = QPushButton("Add Task")
        self.add_task_button.clicked.connect(self.open_task_config_dialog)
        self.layout.addWidget(self.add_task_button)

        self.tableWidget = QTableWidget()
        self.tableWidget.setRowCount(0)
        self.tableWidget.setColumnCount(3)
        headers = ["Task", "Status", "Actions"]
        self.tableWidget.setHorizontalHeaderLabels(headers)
        self.tableWidget.setShowGrid(False)
        self.tableWidget.verticalHeader().setVisible(False)
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.layout.addWidget(self.tableWidget)

    def open_task_config_dialog(self):
        dialog = TaskConfigDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            task_config = dialog.get_task_config()
            self.add_task_to_table(task_config)

    def add_task_to_table(self, task_config):
        row_count = self.tableWidget.rowCount()
        self.tableWidget.insertRow(row_count)
        self.tableWidget.setItem(row_count, 0, QTableWidgetItem(task_config))
        self.tableWidget.setItem(row_count, 1, QTableWidgetItem("Pending"))

        action_buttons = ActionButtonsWidget()
        self.tableWidget.setCellWidget(row_count, 2, action_buttons)
