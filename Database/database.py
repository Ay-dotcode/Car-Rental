import sqlite3
from sqlite3 import Error

def create_connection(db_file):
    try:
        conn = sqlite3.connect(db_file)
        print("Connected to SQLite database successfully!")
        return conn
    except Error as e:
        print(f"SQLite connection error: {e}")
    return None

# Connect to SQLite database
db_file = "Database/carrental.db"
conn = create_connection(db_file)

if conn is not None:
    mycursor = conn.cursor()

    # Create tables if they don't exist
    mycursor.execute( # Create branch table
        """
    CREATE TABLE IF NOT EXISTS branch (
        branch_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL UNIQUE,
        location TEXT NOT NULL,
        contact TEXT
    );
    """)
    mycursor.execute( # Create car table
        """
    CREATE TABLE IF NOT EXISTS car (
        car_id INTEGER PRIMARY KEY AUTOINCREMENT,
        model TEXT NOT NULL,
        brand TEXT NOT NULL,
        available BOOLEAN NOT NULL DEFAULT 0,
        price_per_day REAL NOT NULL,
        branch_id INTEGER,
        FOREIGN KEY (branch_id) REFERENCES branch(branch_id) ON DELETE SET NULL
    );
    """)
    mycursor.execute( # Create customer table
        """
    CREATE TABLE IF NOT EXISTS customer (
        customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
        fullname TEXT NOT NULL,
        contact TEXT,
        email TEXT UNIQUE NOT NULL,
        drivers_license TEXT UNIQUE NOT NULL
    );
    """)
    mycursor.execute( # Create rentals table
        """
    CREATE TABLE IF NOT EXISTS rentals (
        rental_id INTEGER PRIMARY KEY AUTOINCREMENT,
        car_id INTEGER UNIQUE,
        customer_id INTEGER,
        rental_date DATE NOT NULL,
        return_date DATE,
        FOREIGN KEY (car_id) REFERENCES car(car_id) ON DELETE CASCADE,
        FOREIGN KEY (customer_id) REFERENCES customer(customer_id) ON DELETE CASCADE
    );
    """)

    conn.commit()
    mycursor.close()

    def fetch_car_data(search_query):
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute(f'''
            SELECT car.*, 
            customer.fullname AS customer_name
            FROM car
            LEFT JOIN rentals ON car.car_id = rentals.car_id
            LEFT JOIN customer ON rentals.customer_id = customer.customer_id
            GROUP BY car.car_id, customer.customer_id
            HAVING car.brand LIKE '%{search_query}%'
            OR car.model LIKE '%{search_query}%';
        ''')
        cars = cursor.fetchall()
        cursor.close()
        return cars
    def add_car(model, brand, price_per_day, branch_name):
        if not model or not brand or not price_per_day or not branch_name:
            print("All fields are required!")
            return

        cursor = conn.cursor()
        query = """
        INSERT INTO car (model, brand, price_per_day, branch_id, available)
        SELECT ?, ?, ROUND(?, 2), branch_id, 0
        FROM branch
        WHERE name = ?;
        """
        try:
            cursor.execute(query, (model, brand, price_per_day, branch_name))
            if cursor.rowcount > 0:
                conn.commit()
                print("Car added successfully!")
            else:
                print("Failed to add car. Branch name might be incorrect.")
        except Error as e:
            print(f"Error: {e}")
        finally:
            cursor.close()
    def add_branch(branch_name, location, contact):
        if not branch_name or not location or not contact:
            print("All fields are required!")
            return

        cursor = conn.cursor()
        try:
            query = """
            INSERT INTO branch (name, location, contact)
            VALUES (?, ?, ?);
            """
            cursor.execute(query, (branch_name, location, contact))
            conn.commit()
            print("Branch added successfully!")
        except Error as e:
            print(f"Error: {e}")
        finally:
            cursor.close()
    def get_car_by_id(car_id):
        conn.row_factory = sqlite3.Row
        mycursor = conn.cursor()
        try:
            
            query = """
                SELECT
                    car.*,
                    customer.fullname AS customer_name,
                    customer.contact AS customer_contact,
                    customer.drivers_license AS customer_license,
                    customer.email AS customer_email,
                    rentals.rental_date AS rental_date,
                    rentals.return_date AS expected_return_date,
                    branch.name AS branch_name,
                    branch.location AS branch_location,
                    branch.contact AS branch_contact,
                    car.price_per_day * (julianday(rentals.return_date) - julianday(rentals.rental_date)) AS total_cost
                FROM car
                LEFT JOIN rentals ON car.car_id = rentals.car_id
                LEFT JOIN customer ON rentals.customer_id = customer.customer_id
                LEFT JOIN branch ON car.branch_id = branch.branch_id
                WHERE car.car_id = ?
                GROUP BY
                    car.car_id, car.model, car.brand, car.price_per_day,
                    customer.fullname, customer.contact, customer.drivers_license, customer.email,
                    rentals.rental_date, rentals.return_date,
                    branch.name, branch.location, branch.contact;
                """
            mycursor.execute(query, (car_id,))

            car = mycursor.fetchone()
            
            if car:
                return dict(car)
            else:
                print(f"No car found with ID {car_id}")
                return None
        except sqlite3.Error as err:
            print(f"Get car error: {err}")
        finally:
            mycursor.close()
    def delete_car(car_id):
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM car WHERE car_id = ?", (car_id,))
            if cursor.rowcount > 0:
                conn.commit()
                print("Car deleted successfully!")
            else:
                print(f"No car found with ID {car_id}")
        except Error as e:
            print(f"Error: {e}")
        finally:
            cursor.close()
    def update_car(relation):
        cursor = conn.cursor()
        try:
            # Update car details
            update_car_query = """
            UPDATE car
            SET model = ?,
                brand = ?,
                price_per_day = ?,
                available = 0,
                branch_id = (SELECT branch_id FROM branch WHERE name = ?)
            WHERE car_id = ?;
            """
            cursor.execute(update_car_query, (
                relation.get('model'),
                relation.get('brand'),
                relation.get('price_per_day'),
                relation.get('branch_name'),
                relation.get('car_id')
            ))

            if not relation.get('customer_email'):
                # No customer provided, delete existing rental for the car
                delete_rental_query = """
                DELETE FROM rentals WHERE car_id = ?;
                """
                cursor.execute(delete_rental_query, (relation['car_id'],))

                # Mark the car as available
                update_availability_query = """
                UPDATE car SET available = 0 WHERE car_id = ?;
                """
                cursor.execute(update_availability_query, (relation['car_id'],))
            else:
                # Handle customer and rental updates
                customer_id = None
                find_customer_query = """
                SELECT customer_id FROM customer WHERE email = ?;
                """
                cursor.execute(find_customer_query, (relation['customer_email'],))
                result = cursor.fetchone()

                # Customer exists, update their details
                if result:
                    customer_id = result[0]
                    update_customer_query = """
                    UPDATE customer
                    SET fullname = ?,
                        contact = ?,
                        drivers_license = ?
                    WHERE customer_id = ?;
                    """
                    cursor.execute(update_customer_query, (
                        relation['customer_name'],
                        relation.get('customer_contact'),
                        relation.get('customer_license'),
                        customer_id
                    ))
                # Customer does not exist, insert a new one
                else:
                    insert_customer_query = """
                    INSERT INTO customer (fullname, contact, email, drivers_license)
                    VALUES (?, ?, ?, ?);
                    """
                    cursor.execute(insert_customer_query, (
                        relation['customer_name'],
                        relation.get('customer_contact'),
                        relation['customer_email'],
                        relation.get('customer_license')
                    ))
                    customer_id = cursor.lastrowid

                # Update or insert rental
                rental_date = relation.get('rental_date')
                return_date = relation.get('return_date')
                if rental_date and return_date and rental_date > return_date:
                    print("Error: Return date cannot be earlier than rental date.")
                    return

                delete_existing_rental_query = """
                DELETE FROM rentals WHERE car_id = ?;
                """
                cursor.execute(delete_existing_rental_query, (relation['car_id'],))

                insert_rental_query = """
                INSERT INTO rentals (car_id, customer_id, rental_date, return_date)
                VALUES (?, ?, ?, ?);
                """
                cursor.execute(insert_rental_query, (
                    relation['car_id'],
                    customer_id,
                    rental_date,
                    return_date
                ))

                # Mark the car as unavailable
                update_car_availability_query = """
                UPDATE car SET available = 1 WHERE car_id = ?;
                """
                cursor.execute(update_car_availability_query, (relation['car_id'],))

            conn.commit()
            print("Car updated successfully!")
        except Error as e:
            print(f"Error: {e}")
        finally:
            cursor.close()

else:
    print("Failed to create database connection.")
