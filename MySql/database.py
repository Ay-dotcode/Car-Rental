import mysql.connector

try:
    print("Attempting to connect to the database...")
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Owozz",
        database="carrental"
    )
    if mydb.is_connected():
        print("Database connected successfully!")
except mysql.connector.Error as e:
    print(f"Database connection error: {e}")
except Exception as ex:
    print(f"An unexpected error occurred: {ex}")

mycursor = mydb.cursor()

# create tables
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

def fetch_car_data():
    cursor = mydb.cursor(dictionary=True)
    cursor.execute('''
        SELECT car.*, 
            customer.fullname AS customer_name, 
            COUNT(rentals.rental_id) AS rent_count
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

    mycursor = mydb.cursor()
    query = """
    INSERT INTO car (model, brand, price_per_day, branch_id, available)
    SELECT %s, %s, ROUND(%s, 2), branch_id, TRUE
    FROM branch
    WHERE name = %s;
    """
    try:
        mycursor.execute(query, (model, brand, price_per_day, branch_name))
        mydb.commit()
        print("Car added successfully!") 
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        mycursor.close()

    
mycursor.close()    