from PyQt6.QtWidgets import (
    QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QGridLayout, QLineEdit
)
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtGui import QIntValidator
from MySql.database import add_branch

class AddBranchWindow(QWidget):
    window_closed = pyqtSignal()

    def __init__(self):
        super(AddBranchWindow, self).__init__()
        self.setWindowTitle("Add Branch")
        self.setFixedSize(550, 210)

        # Main layout
        main_layout = QVBoxLayout()

        # Grid layout for input fields
        grid_layout = QGridLayout()
        grid_layout.setSpacing(10)
        grid_layout.setContentsMargins(20, 0, 20, 0)

        # Input fields
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Branch Name")
        self.location_input = QLineEdit()
        self.location_input.setPlaceholderText("Location")
        self.contact_input = QLineEdit()
        self.contact_input.setPlaceholderText("Contact No")
        self.contact_input.setValidator(QIntValidator())

        grid_layout.addWidget(QLabel("Branch Name:"), 0, 0)
        grid_layout.addWidget(self.name_input, 0, 1)
        grid_layout.addWidget(QLabel("Location:"), 1, 0)
        grid_layout.addWidget(self.location_input, 1, 1)
        grid_layout.addWidget(QLabel("Contact No:"), 2, 0)
        grid_layout.addWidget(self.contact_input, 2, 1)

        main_layout.addLayout(grid_layout)

        # Buttons
        button_layout = QHBoxLayout()
        self.cancel_btn = QPushButton("Cancel")
        self.cancel_btn.clicked.connect(self.close)
        self.add_btn = QPushButton("Add Branch")
        self.add_btn.clicked.connect(self.on_add_branch_button_click)
        self.cancel_btn.setStyleSheet("margin: 5px 20px; padding: 5px 5px; font-size: 20px; border-radius: 2px;")
        self.add_btn.setStyleSheet("margin: 5px 20px; padding: 5px 5px; font-size: 20px; border-radius: 2px;")

        button_layout.addWidget(self.cancel_btn)
        button_layout.addWidget(self.add_btn)

        main_layout.addLayout(button_layout)

        self.setLayout(main_layout)

    def on_add_branch_button_click(self):
        branch_name = self.name_input.text()
        location = self.location_input.text()
        contact = self.contact_input.text()

        add_branch(branch_name, location, contact)
        self.window_closed.emit()

        self.close()

    def closeEvent(self, event):
        self.window_closed.emit()
        event.accept()