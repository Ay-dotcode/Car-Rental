from PyQt6.QtWidgets import (
    QWidget, QLabel, QPushButton, QHBoxLayout, QGridLayout, QLineEdit, QSpinBox
)
from datetime import datetime
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtGui import QIntValidator

class CarDetailsWindow(QWidget):
    window_closed = pyqtSignal()

    def __init__(self, car):
        super().__init__()
        self.setWindowIcon(QIcon("./images/eul logo.ico"))
        self.setWindowTitle(f"{car['brand']} {car['model']} - Details")
        if car['customer_name']:
            self.setFixedSize(470, 370)
        else:
            self.setFixedSize(470, 250)

        layout = QGridLayout()
        layout.setSpacing(10)

        # Car Details
        brand_label = QLabel(f"Brand Name: {car['brand']}")
        model_label = QLabel(f"Model Name: {car['model']}")
        price_label = QLabel(f"Price: ${car['price']}/day")
        times_rented_label = QLabel(f"Times Rented: {car['rent_count']}")
        availability_label = QLabel(f"Status: {'Available' if not car['customer_name'] else 'Rented by ' + car['customer_name']}")

        layout.addWidget(brand_label, 0, 0)
        layout.addWidget(model_label, 0, 1)
        layout.addWidget(price_label, 1, 0)
        layout.addWidget(times_rented_label, 1, 1)
        layout.addWidget(availability_label, 2, 1)

        if car['customer_name']:
            # Customer Details
            contact_label = QLabel(f"Customer Contact: 'N/A'")
            email_label = QLabel(f"Customer Email:  'N/A'")
            license_label = QLabel(f"Customer License:  'N/A'")

            layout.addWidget(contact_label, 3, 0)
            layout.addWidget(email_label, 4, 0)
            layout.addWidget(license_label, 5, 0)
     
            # Rental Details
            rented_date_label = QLabel(f"Rented Date:  'N/A'")
            return_date_label = QLabel(f"Expected Return Date: 'N/A'")
            total_cost_label = QLabel("Total Cost: N/A")

            layout.addWidget(rented_date_label, 4, 1)
            layout.addWidget(return_date_label, 5, 1)
            layout.addWidget(total_cost_label, 6, 1)

        # Branch Details
        branch_label = QLabel(f"Branch: 'N/A'")
        branch_contact_label = QLabel(f"Branch Contact: 'N/A'")
        branch_location_label = QLabel(f"Branch Location: 'N/A'")

        layout.addWidget(branch_label, 7, 0)
        layout.addWidget(branch_contact_label, 8, 0)
        layout.addWidget(branch_location_label, 9, 0)

        # Buttons
        button_layout = QHBoxLayout()
        button_layout.addStretch()  # Add stretch to push buttons to the right

        delete_button = QPushButton("Delete")
        edit_button = QPushButton("Edit")
        edit_button.clicked.connect(self.enable_edit_mode)
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
        self.price_input = QLineEdit(str(self.car['price']))
        self.price_input.setValidator(QIntValidator())
        self.times_rented_input = QSpinBox()
        self.times_rented_input.setRange(0, 1000)
        self.times_rented_input.setValue(int(self.car['rent_count']))
        # self.times_rented_input.setValidator(QIntValidator())

        # Set fixed width for input fields
        input_width = 200
        self.model_input.setFixedWidth(input_width)
        self.brand_input.setFixedWidth(input_width)
        self.price_input.setFixedWidth(input_width // 2)
        self.times_rented_input.setFixedWidth(input_width // 2)

        layout.addWidget(QLabel("Brand Name:"), 0, 0)
        layout.addWidget(self.brand_input, 0, 1)
        layout.addWidget(QLabel("Model Name:"), 0,  2)
        layout.addWidget(self.model_input, 0, 3)
        layout.addWidget(QLabel("Price:"), 1, 0)
        layout.addWidget(self.price_input, 1, 1)
        layout.addWidget(QLabel("Times Rented:"), 1, 2)
        layout.addWidget(self.times_rented_input, 1, 3)

        # Customer Details
        self.customer_name = QLineEdit(self.car.get('customer_name', 'N/A') if self.car.get('customer_name') else '')
        self.contact_input = QLineEdit(self.car.get('customer_contact', 'N/A') if self.car.get('customer_contact') else '')
        self.email_input = QLineEdit(self.car.get('customer_email', 'N/A') if self.car.get('customer_email') else '')
        self.license_input = QLineEdit(self.car.get('customer_license', 'N/A') if self.car.get('customer_license') else '')
        self.contact_input.setValidator(QIntValidator())

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
        self.rented_date_input = QLineEdit(self.car.get('rented_date', 'N/A') if self.car.get('rented_date') else '')
        self.return_date_input = QLineEdit(self.car.get('return_date', 'N/A') if self.car.get('return_date') else '')

        # Set fixed width for input fields
        self.rented_date_input.setFixedWidth(input_width)
        self.return_date_input.setFixedWidth(input_width)

        layout.addWidget(QLabel("Rented Date:"), 4, 0)
        layout.addWidget(self.rented_date_input, 4, 1)
        layout.addWidget(QLabel("Expected Return Date:"), 4, 2)
        layout.addWidget(self.return_date_input, 4, 3)


        # Branch Details
        self.branch_input = QLineEdit(self.car.get('branch', 'N/A') if self.car.get('branch') else '')
        self.branch_contact_input = QLineEdit(self.car.get('branch_contact', 'N/A') if self.car.get('branch_contact') else '')
        self.branch_location_input = QLineEdit(self.car.get('branch_location', 'N/A') if self.car.get('branch_location') else '')
        self.branch_contact_input.setValidator(QIntValidator())
    
        # Set fixed width for input fields
        self.branch_input.setFixedWidth(input_width)
        self.branch_contact_input.setFixedWidth(input_width)
        self.branch_location_input.setFixedWidth(input_width)

        layout.addWidget(QLabel("Branch Name:"), 5, 0)
        layout.addWidget(self.branch_input, 5, 1)
        layout.addWidget(QLabel("Branch Contact:"), 5, 2)
        layout.addWidget(self.branch_contact_input, 5, 3)
        layout.addWidget(QLabel("Branch Location:"), 6, 0)
        layout.addWidget(self.branch_location_input, 6, 1)
                
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
        layout.addLayout(button_layout, 7, 2, 1, 2)

    def save_details(self):
        # Update the car object with the new input values
        self.car['brand'] = self.brand_input.text()
        self.car['model'] = self.model_input.text()
        self.car['price'] = float(self.price_input.text())
        self.car['rent_count'] = int(self.times_rented_input.text())
        self.car['customer_name'] = None if self.availability_input.text() == 'Available' else self.availability_input.text().replace('Rented by ', '')

        self.close()

        self.total_cost_input = QLineEdit(self.car.get('total_cost', 'N/A') if self.car.get('total_cost') else '')
    
    def closeEvent(self, event):
        self.window_closed.emit()
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
