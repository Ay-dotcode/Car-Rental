import mysql.connector

try:
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Owozz",
        port="3306",
        database="Carrental"
)


    if mydb.is_connected():
        print("Successfully connected to the database")

    mycursor = mydb.cursor()

    # commands to create tables that you would
    # need to run only once
    create_branch_table = """
    CREATE TABLE IF NOT EXISTS branch (
        branch_id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        location VARCHAR(255) NOT NULL,
        contact VARCHAR(20)
    );
    """
    create_car_table = """
    CREATE TABLE IF NOT EXISTS car (
        car_id INT AUTO_INCREMENT PRIMARY KEY,
        model VARCHAR(255) NOT NULL,
        brand VARCHAR(255) NOT NULL,
        available BOOLEAN NOT NULL DEFAULT TRUE,
        price_per_day DECIMAL(10, 2) NOT NULL,
        branch_id INT,
        FOREIGN KEY (branch_id) REFERENCES branch(branch_id) ON DELETE SET NULL
    );
    """
    create_customer_table = """
    CREATE TABLE IF NOT EXISTS customer (
        customer_id INT AUTO_INCREMENT PRIMARY KEY,
        fullname VARCHAR(255) NOT NULL,
        contact VARCHAR(20),
        email VARCHAR(255) UNIQUE NOT NULL,
        drivers_license VARCHAR(50) UNIQUE NOT NULL
    );
    """
    create_rentals_table = """
    CREATE TABLE IF NOT EXISTS rentals (
        rental_id INT AUTO_INCREMENT PRIMARY KEY,
        car_id INT,
        customer_id INT,
        rental_date DATE NOT NULL,
        return_date DATE,
        total_cost DECIMAL(10, 2),
        FOREIGN KEY (car_id) REFERENCES car(car_id) ON DELETE CASCADE,
        FOREIGN KEY (customer_id) REFERENCES customer(customer_id) ON DELETE CASCADE
    );
    """

    # run table creation queries
    mycursor.execute(create_branch_table)
    mycursor.execute(create_car_table)
    mycursor.execute(create_customer_table)
    mycursor.execute(create_rentals_table)
  
    print("Tables created successfully")

    def add_branch(name, location, contact):
        try:
            query = "INSERT INTO branch (name, location, contact) VALUES (%s, %s, %s)"
            values = (name, location, contact)
            mycursor.execute(query, values)
            mydb.commit()
            print(f"Branch '{name}' added successfully.")
        except mysql.connector.Error as err:
            print(f"Error: {err}")
    def add_car(brand, model, price_per_day, branch_name):
        try:
            # Find the branch_id from the branch name
            branch_query = "SELECT branch_id FROM branch WHERE name = %s"
            mycursor.execute(branch_query, (branch_name,))
            branch = mycursor.fetchone()
            if not branch:
                print(f"Branch '{branch_name}' does not exist.")
                return

            branch_id = branch[0]

            # Insert the car into the needed table
            car_query = """
            INSERT INTO car (model, brand, available, price_per_day, branch_id)
            VALUES (%s, %s, %s, %s, %s)
            """
            values = (model, brand, True, price_per_day, branch_id)
            mycursor.execute(car_query, values)
            mydb.commit()
            print(f"Car '{brand} {model}' added to branch '{branch_name}' successfully.")
        except mysql.connector.Error as err:
            print(f"Error: {err}")
    def get_all_cars(): #returns car_id, model, brand, price_per_day, current_customer, times_rented
        try:
            query = """
            SELECT 
                car.car_id, 
                car.model, 
                car.brand, 
                car.price_per_day, 
                COALESCE(customer.fullname, 'Available') AS current_customer, 
                COUNT(rentals.rental_id) AS times_rented
            FROM car
            LEFT JOIN rentals ON car.car_id = rentals.car_id
            LEFT JOIN customer ON rentals.customer_id = customer.customer_id AND rentals.return_date IS NULL
            GROUP BY car.car_id, car.model, car.brand, car.price_per_day, current_customer;
            """
            mycursor.execute(query)
            cars = mycursor.fetchall()
            if cars:
                for car in cars:
                    print(car)
            else:
                print("No cars found.")
        except Exception as e:
            print(f"Error: {e}")
    def get_car_by_id(car_id):
        try:
            query = """
            SELECT 
                car.car_id, 
                car.model, 
                car.brand, 
                car.price_per_day, 
                customer.fullname AS current_customer, 
                customer.contact AS customer_contact,
                customer.drivers_license AS customer_license,
                customer.email AS customer_email,
                active_rental.rental_date AS rental_date,
                active_rental.return_date AS expected_return_date,
                branch.name AS branch_name,
                branch.location AS branch_location,
                branch.contact AS branch_contact,
                COUNT(all_rentals.rental_id) AS times_rented
            FROM car
            LEFT JOIN (
                SELECT rental_id, car_id, customer_id, rental_date, return_date
                FROM rentals
                WHERE return_date >= CURDATE() OR return_date IS NULL
                ORDER BY rental_date DESC
                LIMIT 1
            ) active_rental ON car.car_id = active_rental.car_id
            LEFT JOIN rentals all_rentals ON car.car_id = all_rentals.car_id
            LEFT JOIN customer ON active_rental.customer_id = customer.customer_id
            LEFT JOIN branch ON car.branch_id = branch.branch_id
            WHERE car.car_id = %s
            GROUP BY 
                car.car_id, car.model, car.brand, car.price_per_day,
                customer.fullname, customer.contact, customer.drivers_license, customer.email,
                active_rental.rental_date, active_rental.return_date,
                branch.name, branch.location, branch.contact;
            """
            mycursor.execute(query, (car_id,))
            car = mycursor.fetchone()

            if car:
                car_dict = {
                    "car_id": car[0],
                    "model": car[1],
                    "brand": car[2],
                    "price_per_day": car[3],
                    "current_customer": car[4],
                    "customer_contact": car[5],
                    "customer_license": car[6],
                    "customer_email": car[7],
                    "rental_date": car[8],
                    "expected_return_date": car[9],
                    "branch_name": car[10],
                    "branch_location": car[11],
                    "branch_contact": car[12],
                    "times_rented": car[13]
                }
                print({k: v for k, v in car_dict.items() if v is not None})
            else:
                print(f"No car found with ID {car_id}")
        except mysql.connector.Error as err:
            print(f"Error: {err}")
    def update_car_by_id(car_id, model=None, brand=None, price_per_day=None, 
                        customer_fullname=None, customer_contact=None, customer_email=None, 
                        customer_license=None, rental_date=None, return_date=None, 
                        branch_name=None, branch_location=None, branch_contact=None):
        try:
            # this is to update a car details if provided
            if any([model, brand, price_per_day]):
                update_fields = []
                values = []
                
                if model:
                    update_fields.append("model = %s")
                    values.append(model)
                if brand:
                    update_fields.append("brand = %s")
                    values.append(brand)
                if price_per_day:
                    update_fields.append("price_per_day = %s")
                    values.append(price_per_day)
                    
                if update_fields:
                    car_update_query = f"""
                    UPDATE car
                    SET {', '.join(update_fields)}
                    WHERE car_id = %s
                    """
                    values.append(car_id)
                    mycursor.execute(car_update_query, tuple(values))

            # this is for handling customer details if any customer information is provided
            if any([customer_fullname, customer_contact, customer_email, customer_license]):
                if customer_email:  # Email is required to identify/create customer
                    # Check if customer exists
                    customer_query = "SELECT customer_id FROM customer WHERE email = %s"
                    mycursor.execute(customer_query, (customer_email,))
                    customer = mycursor.fetchone()

                    if customer:
                        # this is for updating existing customer with provided fields
                        update_fields = []
                        values = []
                        
                        if customer_fullname:
                            update_fields.append("fullname = %s")
                            values.append(customer_fullname)
                        if customer_contact:
                            update_fields.append("contact = %s")
                            values.append(customer_contact)
                        if customer_license:
                            update_fields.append("drivers_license = %s")
                            values.append(customer_license)
                            
                        if update_fields:
                            customer_update_query = f"""
                            UPDATE customer
                            SET {', '.join(update_fields)}
                            WHERE customer_id = %s
                            """
                            values.append(customer[0])
                            mycursor.execute(customer_update_query, tuple(values))
                        customer_id = customer[0]
                    else:
                        # query to insert a new customer if not found
                        customer_query = """
                        INSERT INTO customer (fullname, contact, email, drivers_license)
                        VALUES (%s, %s, %s, %s)
                        """
                        mycursor.execute(customer_query, (
                            customer_fullname,
                            customer_contact,
                            customer_email,
                            customer_license
                        ))
                        customer_id = mycursor.lastrowid

                    # query for rental information if rental date is provided
                    if rental_date:
                        rental_query = """
                        INSERT INTO rentals (car_id, customer_id, rental_date, return_date)
                        VALUES (%s, %s, %s, %s)
                        """
                        mycursor.execute(rental_query, (car_id, customer_id, rental_date, return_date))

            # this is to handle branch details if any branch information is provided
            if any([branch_name, branch_location, branch_contact]):
                update_fields = []
                values = []
                
                if branch_name:
                    update_fields.append("name = %s")
                    values.append(branch_name)
                if branch_location:
                    update_fields.append("location = %s")
                    values.append(branch_location)
                if branch_contact:
                    update_fields.append("contact = %s")
                    values.append(branch_contact)
                    
                if update_fields:
                    branch_query = f"""
                    UPDATE branch
                    SET {', '.join(update_fields)}
                    WHERE branch_id = (SELECT branch_id FROM car WHERE car_id = %s)
                    """
                    values.append(car_id)
                    mycursor.execute(branch_query, tuple(values))

            mydb.commit()
            print("Car details updated successfully.")
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            mydb.rollback()

except mysql.connector.Error as err:
    print(f"Error: {err}")
except Exception as e:
    print(f"Unexpected error: {e}")
# finally:
#     if mydb.is_connected():
#         mycursor.close()
#         mydb.close()
#         print("Database connection closed")