from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QLabel, QPushButton, QWidget,
    QVBoxLayout, QHBoxLayout, QGridLayout, QSizePolicy, QLineEdit, QScrollArea
)
import sys
from PyQt6.QtGui import QIcon
from Pages.add_car import AddCarWindow
from Pages.details import CarDetailsWindow
from Pages.add_branch import AddBranchWindow
from MySql.database import fetch_car_data


class MainUI(QMainWindow):
    def __init__(self):
        super(MainUI, self).__init__()
        self.setWindowTitle("Car Rental")
        self.setWindowIcon(QIcon("./images/eul logo.ico"))
        self.setFixedSize(1100, 500)
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

        # Search and Filters Layout
        search_layout = QHBoxLayout()
        search_input = QLineEdit()
        search_input.setPlaceholderText("Search Input")
        search_input.setStyleSheet("""
                                    margin: 5px;
                                    margin-left: 180px;
                                    padding: 5px;
                                    border-radius: 5px;
                                    font-size: 18px
                                   """)
        search_input.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        filter_btn1 = QPushButton("Available")
        filter_btn1.setStyleSheet("margin: 10px; padding: 5px; border-radius: 5px;")
        filter_btn2 = QPushButton("Count")  
        filter_btn2.setStyleSheet("padding: 5px; border-radius: 5px;")
        

        search_layout.addWidget(search_input)
        search_layout.addWidget(filter_btn1)
        search_layout.addWidget(filter_btn2)

        # Scroll Area for Cards
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_content = QWidget()
        scroll_layout = QGridLayout(scroll_content)
        scroll_content.setLayout(scroll_layout)

        # List of cars with properties
        self.cars = [
            {"id": "001", "brand": "Toyota", "model": "Corolla", "available": True, "rent_count": "15", "price": 50, "customer_name": "John Doe"},
            {"id": "002", "brand": "Honda", "model": "Civic", "available": True, "rent_count": "20", "price": 45, "customer_name": "Jane Smith"},
            {"id": "003", "brand": "Ford", "model": "Fiesta", "available": True, "rent_count": "10", "price": 40, "customer_name": "Alice Johnson"},
            {"id": "004", "brand": "BMW", "model": "X5", "available": False, "rent_count": "5", "price": 100, "customer_name": ""},
            {"id": "005", "brand": "Mercedes", "model": "C-Class", "available": False, "rent_count": "8", "price": 90, "customer_name": ""},
            {"id": "006", "brand": "Audi", "model": "A4", "available": True, "rent_count": "12", "price": 80, "customer_name": "Diana Evans"},
            {"id": "007", "brand": "Toyota", "model": "Camry", "available": False, "rent_count": "18", "price": 60, "customer_name": ""},
            {"id": "008", "brand": "Honda", "model": "Accord", "available": True, "rent_count": "22", "price": 55, "customer_name": "Fiona Green"},
            {"id": "009", "brand": "Ford", "model": "Mustang", "available": True, "rent_count": "7", "price": 70, "customer_name": "George Harris"},
            {"id": "010", "brand": "BMW", "model": "M5", "available": True, "rent_count": "3", "price": 120, "customer_name": "Hannah Irving"},
            {"id": "011", "brand": "Mercedes", "model": "E-Class", "available": True, "rent_count": "9", "price": 95, "customer_name": "Ian Jackson"},
            {"id": "012", "brand": "Audi", "model": "A6", "available": True, "rent_count": "14", "price": 85, "customer_name": "Jackie King"},
        ]
        self.cars = fetch_car_data()

        # Create cards and populate with car data
        for index, car in enumerate(self.cars):
            card = self.create_car_card(car)
            row, col = divmod(index, 3)  # Arrange cards in 2 rows and 3 columns
            scroll_layout.addWidget(card, row, col)

        scroll_area.setWidget(scroll_content)

        # Add all sections to the main layout
        main_layout.addLayout(top_layout)
        main_layout.addLayout(search_layout)
        main_layout.addWidget(scroll_area)

        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

    def create_car_card(self, car):
        card_widget = QWidget()
        card_layout = QGridLayout()
        card_layout.setContentsMargins(20, 20, 20, 5)
        card_widget.setStyleSheet("border: 2px solid grey; border-radius: 10px;")

        # Top Labels
        count_label = QLabel(f"Times Rented: {car['rent_count']}")
        count_label.setStyleSheet("border: none; margin-left: 10px;")
        card_layout.addWidget(count_label, 0, 1)


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
            customer_label = QLabel("Car available")
        else:
            customer_label = QLabel(f"Customer: {car['customer_name']}")
        customer_label.setStyleSheet("border: none;")

        card_layout.addWidget(customer_label, 3, 0)

        # Price Button
        detail_button = QPushButton("Details")
        detail_button.setStyleSheet("border: none; margin: 10px; margin-top: 0px; font-size: 18px;")
        detail_button.clicked.connect(lambda: self.on_card_click(car))

        card_layout.addWidget(detail_button, 3, 1)

        card_widget.setLayout(card_layout)
        return card_widget

    def open_add_car_window(self):
        self.close_all_child_windows()
        self.add_car_window = AddCarWindow()
        self.child_windows.append(self.add_car_window)  # Track the window
        self.add_car_window.show()

    def open_add_branch_window(self):
        self.close_all_child_windows()
        self.add_branch_window = AddBranchWindow()
        self.child_windows.append(self.add_branch_window)  # Track the window
        self.add_branch_window.show()
    
    def on_card_click(self, car):
        self.close_all_child_windows()
        self.car_details_window = CarDetailsWindow(car)
        self.child_windows.append(self.car_details_window)  # Track the window to manage it later
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
    ui = MainUI()
    ui.show()
    with open("styles.qss", "r") as f:
        app.setStyleSheet(f.read())
    sys.exit(app.exec())