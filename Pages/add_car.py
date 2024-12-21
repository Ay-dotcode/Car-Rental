from PyQt6.QtWidgets import (
    QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QGridLayout, QLineEdit
)

from PyQt6.QtGui import QIcon
from PyQt6.QtCore import pyqtSignal


class AddCarWindow(QWidget):
    window_closed = pyqtSignal()

    def __init__(self):
        super(AddCarWindow, self).__init__()
        self.setWindowTitle("Add Car")
        self.setFixedSize(550, 250)

        # Main layout
        main_layout = QVBoxLayout()

        # Grid layout for input fields
        grid_layout = QGridLayout()
        grid_layout.setSpacing(10)
        grid_layout.setContentsMargins(20, 0, 20, 0)

        # Input fields
        self.brand_input = QLineEdit()
        self.brand_input.setPlaceholderText("Brand")
        self.model_input = QLineEdit()
        self.model_input.setPlaceholderText("Model")
        self.price_input = QLineEdit()
        self.price_input.setPlaceholderText("Price per day")
        self.branch_input = QLineEdit()
        self.branch_input.setPlaceholderText("Branch name")

        grid_layout.addWidget(QLabel("Brand:"), 0, 0)
        grid_layout.addWidget(self.brand_input, 0, 1)
        grid_layout.addWidget(QLabel("Model:"), 1, 0)
        grid_layout.addWidget(self.model_input, 1, 1)

        grid_layout.addWidget(QLabel("Price per day:"), 2, 0)
        grid_layout.addWidget(self.price_input, 2, 1)
        grid_layout.addWidget(QLabel("Branch name:"), 3, 0)
        grid_layout.addWidget(self.branch_input, 3, 1)

        main_layout.addLayout(grid_layout)

        brand = self.brand_input.text()
        model = self.model_input.text()
        price = self.price_input.text()
        branch = self.branch_input.text

        # Buttons
        button_layout = QHBoxLayout()
        self.cancel_btn = QPushButton("Cancel")
        self.cancel_btn.clicked.connect(self.close)
        self.add_btn = QPushButton("Add Car")
        # self.add_btn.clicked.connect()
        self.cancel_btn.setStyleSheet("margin: 5px 20px; padding: 5px 5px; font-size: 20px; border-radius: 2px;")
        self.add_btn.setStyleSheet("margin: 5px 20px; padding: 5px 5px; font-size: 20px; border-radius: 2px;")

        button_layout.addWidget(self.cancel_btn)
        button_layout.addWidget(self.add_btn)

        main_layout.addLayout(button_layout)

        self.setLayout(main_layout)

    def closeEvent(self, event):
        self.window_closed.emit()
        event.accept()