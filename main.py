from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QLabel, QPushButton, QWidget,
    QVBoxLayout, QHBoxLayout, QGridLayout, QScrollArea, QLineEdit
)
import sys
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon
from Pages.add_car import AddCarWindow
from Pages.details import CarDetailsWindow
from Pages.add_branch import AddBranchWindow
from Database.database import fetch_car_data

class MainUI(QMainWindow):
    def __init__(self):
        super(MainUI, self).__init__()
        self.setWindowTitle("Car Rental")
        self.setFixedSize(1100, 460)
        self.child_windows = []  # List to track child windows

        # Main widget and layout
        central_widget = QWidget()
        main_layout = QVBoxLayout()

        # Top Layout with Title and Create Car Button
        top_layout = QHBoxLayout()
        title_label = QLabel("Car Rental")
        title_label.setStyleSheet("font-size: 40px; font-weight: bold; margin-left: 420px;")
        add_car_btn = QPushButton("+ Add Car")
        add_car_btn.clicked.connect(self.open_add_car_window)
        add_car_btn.setStyleSheet("font-size: 16px; padding: 7.5px; margin: 5px; border-radius: 5px;")
        add_branch_btn = QPushButton("+ Add Branch")
        add_branch_btn.setStyleSheet("font-size: 16px; padding: 7.5px; margin: 5px; border-radius: 5px;")
        add_branch_btn.clicked.connect(self.open_add_branch_window)

        top_layout.addWidget(title_label)
        top_layout.addStretch()
        top_layout.addWidget(add_car_btn)
        top_layout.addWidget(add_branch_btn)

        # Search Bar and Button
        search_layout = QHBoxLayout()
        search_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.search_bar = QLineEdit()
        self.search_bar.setFixedWidth(600)
        self.search_bar.setPlaceholderText("Search by model or brand...")
        self.search_bar.setStyleSheet("font-size: 16px; padding: 5px; border-radius: 5px;")
        self.search_bar.returnPressed.connect(lambda: self.update_car_cards(scroll_layout))
        search_button = QPushButton("Search")
        search_button.setFixedWidth(100)
        search_button.clicked.connect(lambda: self.update_car_cards(scroll_layout))
        search_button.setStyleSheet("font-size: 18px; padding: 5px; border-radius: 5px;")

        search_layout.addWidget(self.search_bar)
        search_layout.addWidget(search_button)

        # Scroll Area for Cards
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_content = QWidget()
        scroll_layout = QGridLayout(scroll_content)
        scroll_content.setLayout(scroll_layout)

        # Create initial car cards
        self.update_car_cards(scroll_layout)
        scroll_area.setWidget(scroll_content)

        # Add all sections to the main layout
        main_layout.addLayout(top_layout)
        main_layout.addLayout(search_layout)
        main_layout.addWidget(scroll_area)

        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

    def update_car_cards(self, scroll_layout):
        self.clear_car_cards(scroll_layout)

        search_query = self.search_bar.text()
        self.search_bar.clear()
        self.cars = fetch_car_data(search_query)

        # Add new cards to the layout
        for index, car in enumerate(self.cars):
            card = self.create_car_card(car)
            row, col = divmod(index, 3)  # Arrange cards in rows and columns
            alignment = Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft
            scroll_layout.addWidget(card, row, col, alignment)

    def create_car_card(self, car):
        card_widget = QWidget()
        card_layout = QGridLayout()
        card_widget.setFixedSize(340, 160)
        card_layout.setContentsMargins(20, 20, 20, 5)
        card_widget.setStyleSheet("border: 2px solid grey; border-radius: 10px;")

        # Brand and Model
        model_label = QLabel(f"Model: {car['model']}")
        model_label.setStyleSheet("border: none;")
        brand_label = QLabel(f"Name of Brand: {car['brand']}")
        brand_label.setStyleSheet("border: none;")

        card_layout.addWidget(model_label, 0, 0)
        card_layout.addWidget(brand_label, 1, 0)

        # Price and Customer
        price_label = QLabel(f"${car['price_per_day']}/day")
        price_label.setStyleSheet("border: none; font-size: 16px; text-decoration: underline;")
        card_layout.addWidget(price_label, 2, 0)

        if car['available']:
            customer_label = QLabel(f"Customer: {car['customer_name']}")
        else:
            customer_label = QLabel("Car available")
        customer_label.setStyleSheet("border: none;")

        card_layout.addWidget(customer_label, 3, 0)

        # Price Button
        detail_button = QPushButton("Details")
        detail_button.setStyleSheet("border: none; margin: 10px; margin-top: 0px; font-size: 18px;")
        detail_button.clicked.connect(lambda: self.on_card_click(car))

        card_layout.addWidget(detail_button, 3, 1)

        card_widget.setLayout(card_layout)
        return card_widget

    def clear_car_cards(self, scroll_layout):
        while scroll_layout.count():
            child = scroll_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

    def open_add_car_window(self):
        self.close_all_child_windows()
        self.add_car_window = AddCarWindow()
        self.add_car_window.car_added.connect(self.reload_data)  # Connect the signal
        self.child_windows.append(self.add_car_window)  # Track the window
        self.add_car_window.show()

    def open_add_branch_window(self):
        self.close_all_child_windows()
        self.add_branch_window = AddBranchWindow()
        self.child_windows.append(self.add_branch_window)  # Track the window
        self.add_branch_window.show()

    def reload_data(self):
        # Reload the car cards after adding a new car
        scroll_area = self.findChild(QScrollArea)
        scroll_content = scroll_area.widget()
        scroll_layout = scroll_content.layout()
        for i in range(scroll_layout.count()):
            widget = scroll_layout.itemAt(i).widget()
            if widget:
                widget.deleteLater()  # Remove old cards
        self.update_car_cards(scroll_layout)  # Reload the cards

    def on_card_click(self, car):
        self.close_all_child_windows()
        self.car_details_window = CarDetailsWindow(car['car_id'])
        self.car_details_window.details_closed.connect(self.reload_data)
        self.child_windows.append(self.car_details_window) 
        self.car_details_window.show()

    def close_all_child_windows(self):
        for window in self.child_windows:
            window.close()
        self.child_windows.clear()  # Clear the list after closing all windows

    def closeEvent(self, event):
        self.close_all_child_windows()
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("./Images/EUL logo.ico"))
    ui = MainUI()
    ui.show()
    with open("styles.qss", "r") as f:
        app.setStyleSheet(f.read())
    sys.exit(app.exec())
