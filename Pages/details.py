from PyQt6.QtWidgets import (
    QWidget, QLabel, QPushButton, QHBoxLayout, QGridLayout, QLineEdit
)
from PyQt6.QtCore import pyqtSignal, QRegularExpression
from PyQt6.QtGui import QIntValidator, QDoubleValidator, QRegularExpressionValidator
from Database.database import get_car_by_id, delete_car, update_car

class CarDetailsWindow(QWidget):
    details_closed = pyqtSignal()

    def __init__(self, car_id):
        self.car = get_car_by_id(car_id)
        super().__init__()
        self.setWindowTitle(f"{self.car['brand']} {self.car['model']} - Details")
        if self.car['available']:
            self.setFixedSize(600, 370)
        else:
            self.setFixedSize(600, 250)

        layout = QGridLayout()
        layout.setSpacing(10)

        # self.Car Details
        brand_label = QLabel(f"Brand Name: {self.car['brand']}")
        model_label = QLabel(f"Model Name: {self.car['model']}")
        price_label = QLabel(f"Price: ${self.car['price_per_day']}/day")
        availability_label = QLabel(f"Status: {'Available' if not self.car['customer_name'] else 'Rented by ' + self.car['customer_name']}")

        layout.addWidget(brand_label, 0, 0)
        layout.addWidget(model_label, 1, 0)
        layout.addWidget(price_label, 1, 1)
        layout.addWidget(availability_label, 2, 1)

        if self.car['available']:
            # Customer Details
            email_label = QLabel(f"Customer Email: {self.car['customer_email']}")
            contact_label = QLabel(f"Customer Contact: {self.car['customer_contact']}")
            license_label = QLabel(f"Customer License:  {self.car['customer_license']}")

            layout.addWidget(email_label, 3, 0, 1, 2)
            layout.addWidget(contact_label, 4, 0)
            layout.addWidget(license_label, 5, 0)
     
            # Rental Details
            rented_date_label = QLabel(f"Rented Date: {self.car['rental_date']}")
            return_date_label = QLabel(f"Return Date: {self.car['expected_return_date']}")
            total_cost_label = QLabel(f"Total Cost: {self.car['total_cost']}")

            layout.addWidget(rented_date_label, 4, 1)
            layout.addWidget(return_date_label, 5, 1)
            layout.addWidget(total_cost_label, 6, 1)

        # Branch Details
        branch_label = QLabel(f"Branch Name: {self.car['branch_name']}")
        branch_contact_label = QLabel(f"Branch Contact: {self.car['branch_contact']}")
        branch_location_label = QLabel(f"Branch Location: {self.car['branch_location']}")

        layout.addWidget(branch_label, 7, 0)
        layout.addWidget(branch_contact_label, 8, 0)
        layout.addWidget(branch_location_label, 9, 0)

        # Buttons
        button_layout = QHBoxLayout()
        button_layout.addStretch()  # Add stretch to push buttons to the right

        delete_button = QPushButton("Delete")
        delete_button.clicked.connect(lambda: self.delete_car_btn(car_id))
        edit_button = QPushButton("Edit")
        edit_button.clicked.connect(lambda: self.enable_edit_mode())
        ok_button = QPushButton("Ok")
        ok_button.clicked.connect(self.close)

        # Set fixed width for buttons
        button_width = 100
        delete_button.setFixedWidth(button_width)
        edit_button.setFixedWidth(button_width)
        ok_button.setFixedWidth(button_width)

        delete_button.setStyleSheet("padding: 5px 10px; font-size: 20px; border-radius: 5px;")
        edit_button.setStyleSheet("padding: 5px 10px; font-size: 20px; border-radius: 5px;")
        ok_button.setStyleSheet("margin: 5px; padding: 5px 10px; font-size: 20px; border-radius: 5px;")
        
        button_layout.addWidget(edit_button)
        button_layout.addWidget(ok_button)
        button_layout.addWidget(delete_button)
        
        layout.addLayout(button_layout, 10, 0, 1, 2)

        self.setLayout(layout)

    def delete_car_btn(self, car_id):
        delete_car(car_id)
        self.close()

    def enable_edit_mode(self):
        layout = self.layout()
        self.setFixedSize(750, 310)
        self.setGeometry(200, 200, 800, 310)

        # Clear the current layout
        for i in reversed(range(layout.count())):
            widget = layout.itemAt(i).widget()
            if widget is not None:
                widget.deleteLater()
        self.remove_button_layout()

        # Create input fields for car details
        self.model_input = QLineEdit(self.car['model'])
        self.brand_input = QLineEdit(self.car['brand'])
        self.price_input = QLineEdit(str(self.car['price_per_day']))
        self.price_input.setValidator(QDoubleValidator(0.0, 9999.99, 2))

        # Set fixed width for input fields
        input_width = 200
        self.model_input.setFixedWidth(input_width)
        self.brand_input.setFixedWidth(input_width)
        self.price_input.setFixedWidth(input_width // 2)

        layout.addWidget(QLabel("Brand Name:"), 0, 0)
        layout.addWidget(self.brand_input, 0, 1)
        layout.addWidget(QLabel("Model Name:"), 0, 2)
        layout.addWidget(self.model_input, 0, 3)
        layout.addWidget(QLabel("Price/day:"), 1, 2)
        layout.addWidget(self.price_input, 1, 3)

        # Customer Details
        self.customer_name = QLineEdit(self.car.get('customer_name', 'N/A') if self.car.get('customer_name') else '')
        self.contact_input = QLineEdit(self.car.get('customer_contact', 'N/A') if self.car.get('customer_contact') else '')
        self.email_input = QLineEdit(self.car.get('customer_email', 'N/A') if self.car.get('customer_email') else '')
        self.license_input = QLineEdit(self.car.get('customer_license', 'N/A') if self.car.get('customer_license') else '')
        self.contact_input.setValidator(QIntValidator())

        # Email validator
        email_regex = QRegularExpression(r"^[\w\.-]+@[\w\.-]+\.\w+$")
        email_validator = QRegularExpressionValidator(email_regex)
        self.email_input.setValidator(email_validator)

        # Set fixed width for input fields
        self.customer_name.setFixedWidth(input_width)
        self.contact_input.setFixedWidth(input_width)
        self.email_input.setFixedWidth(input_width)
        self.license_input.setFixedWidth(input_width)
        
        layout.addWidget(QLabel("Customer Name:"), 2, 0)
        layout.addWidget(self.customer_name, 2, 1)
        layout.addWidget(QLabel("Customer Contact:"), 2, 2)
        layout.addWidget(self.contact_input, 2, 3)
        layout.addWidget(QLabel("Customer Email:"), 3, 0)
        layout.addWidget(self.email_input, 3, 1)
        layout.addWidget(QLabel("Customer License:"), 3, 2)
        layout.addWidget(self.license_input, 3, 3)

        # Rental Details
        self.rented_date_input = QLineEdit(self.car.get('rental_date', 'N/A') if self.car.get('rental_date') else '')
        self.return_date_input = QLineEdit(self.car.get('expected_return_date', 'N/A') if self.car.get('expected_return_date') else '')

        # Set input mask for date fields to accept YYYY-MM-DD format
        self.rented_date_input.setInputMask("0000-00-00")
        self.return_date_input.setInputMask("0000-00-00")

        # Set fixed width for input fields
        self.rented_date_input.setFixedWidth(input_width)
        self.return_date_input.setFixedWidth(input_width)

        layout.addWidget(QLabel("Rented Date:"), 4, 0)
        layout.addWidget(self.rented_date_input, 4, 1)
        layout.addWidget(QLabel("Expected Return Date:"), 4, 2)
        layout.addWidget(self.return_date_input, 4, 3)


        # Branch Details
        self.branch_input = QLineEdit(self.car['branch_name'])
        self.branch_contact_input = QLineEdit(self.car.get('branch_contact', 'N/A') if self.car.get('branch_contact') else '')
        self.branch_location_input = QLineEdit(self.car.get('branch_location', 'N/A') if self.car.get('branch_location') else '')
        self.branch_contact_input.setValidator(QIntValidator())
    
        # Set fixed width for input fields
        self.branch_input.setFixedWidth(input_width)
        self.branch_contact_input.setFixedWidth(input_width)
        self.branch_location_input.setFixedWidth(input_width)

        layout.addWidget(QLabel("Branch Name:"), 5, 0)
        layout.addWidget(self.branch_input, 5, 1)
                
        # Update buttons
        button_layout = QHBoxLayout()
        save_button = QPushButton("Save")
        save_button.clicked.connect(self.save_details)
        cancel_button = QPushButton("Cancel")
        cancel_button.clicked.connect(self.close)

        save_button.setStyleSheet("padding: 5px 10px; font-size: 20px; border-radius: 5px;")
        cancel_button.setStyleSheet("margin: 5px; padding: 5px 10px; font-size: 20px; border-radius: 5px;")

        button_layout.addWidget(save_button)
        button_layout.addWidget(cancel_button)
        layout.addLayout(button_layout, 6, 2, 1, 2)

    def save_details(self):
        email = self.email_input.text()
        email_regex = QRegularExpression(r"^[\w\.-]+@[\w\.-]+\.\w+$") # must contain @ and a domain
        if not email_regex.match(email).hasMatch():
            print(f"Invalid email: {email}")
            return  # Stop further execution if the email is invalid

        relation = {
            'car_id': self.car['car_id'],
            'brand': self.brand_input.text(),
            'model': self.model_input.text(),
            'price_per_day': self.price_input.text(),
            'customer_name': self.customer_name.text(),
            'customer_contact': self.contact_input.text(),
            'customer_email': email,
            'customer_license': self.license_input.text(),
            'rental_date': self.rented_date_input.text(),
            'return_date': self.return_date_input.text(),
            'branch_name': self.branch_input.text(),
            'branch_contact': self.branch_contact_input.text(),
            'branch_location': self.branch_location_input.text()
        }
        update_car(relation)

        self.close()
  
    def closeEvent(self, event):
        self.details_closed.emit() # Emit the signal to update the main window
        event.accept()

    def remove_button_layout(self):
        layout = self.layout()
        
        # Iterate over the items in the layout to find the button_layout
        for i in reversed(range(layout.count())):
            item = layout.itemAt(i)
            if isinstance(item, QHBoxLayout):
                # Remove all widgets inside the button layout
                for j in reversed(range(item.count())):
                    widget = item.itemAt(j).widget()
                    if widget is not None:
                        widget.deleteLater()  # Delete the button widget
                
                # Remove the button_layout itself
                layout.removeItem(item)
                item.deleteLater()
                break  # Stop after finding and deleting the button_layout
