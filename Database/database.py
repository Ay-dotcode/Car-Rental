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
    # Create a cursor object
    mycursor = conn.cursor()

    # Create tables
    create_branch_table = """
    CREATE TABLE IF NOT EXISTS branch (
        branch_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL UNIQUE,
        location TEXT NOT NULL,
        contact TEXT
    );
    """
    create_car_table = """
    CREATE TABLE IF NOT EXISTS car (
        car_id INTEGER PRIMARY KEY AUTOINCREMENT,
        model TEXT NOT NULL,
        brand TEXT NOT NULL,
        available BOOLEAN NOT NULL DEFAULT 1,
        price_per_day REAL NOT NULL,
        branch_id INTEGER,
        FOREIGN KEY (branch_id) REFERENCES branch(branch_id) ON DELETE SET NULL
    );
    """
    create_customer_table = """
    CREATE TABLE IF NOT EXISTS customer (
        customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
        fullname TEXT NOT NULL,
        contact TEXT,
        email TEXT UNIQUE NOT NULL,
        drivers_license TEXT UNIQUE NOT NULL
    );
    """
    create_rentals_table = """
    CREATE TABLE IF NOT EXISTS rentals (
        rental_id INTEGER PRIMARY KEY AUTOINCREMENT,
        car_id INTEGER,
        customer_id INTEGER,
        rental_date DATE NOT NULL,
        return_date DATE,
        total_cost REAL,
        FOREIGN KEY (car_id) REFERENCES car(car_id) ON DELETE CASCADE,
        FOREIGN KEY (customer_id) REFERENCES customer(customer_id) ON DELETE CASCADE
    );
    """

    # Execute table creation queries
    mycursor.execute(create_branch_table)
    mycursor.execute(create_car_table)
    mycursor.execute(create_customer_table)
    mycursor.execute(create_rentals_table)
    conn.commit()

    def fetch_car_data():
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute('''
            SELECT car.*, 
            customer.fullname AS customer_name
            FROM car
            LEFT JOIN rentals ON car.car_id = rentals.car_id
            LEFT JOIN customer ON rentals.customer_id = customer.customer_id
            GROUP BY car.car_id, customer.customer_id;
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
        SELECT ?, ?, ROUND(?, 2), branch_id, 1
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

    mycursor.close()
else:
    print("Failed to create database connection.")