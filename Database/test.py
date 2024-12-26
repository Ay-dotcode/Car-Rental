try:
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

    # Example usage
    # add_branch("Downtown Branch", "123 Main St", "123-456-7890")
    # add_car("Toyota", "Corolla", 50.00, "Downtown Branch")
    # print("\nAll Cars:")
    # get_all_cars()
    # print("\nCar Details by ID:")
    # get_car_by_id(1)
    # print("\nTesting update with multiple fields for car_id = 1")
    # update_car_by_id(car_id=1, price_per_day=75.00)
    # update_car_by_id(
    #     car_id=1,
    #     model="Mazda 4",
    #     brand="Mazda",
    #     price_per_day=70.00,
    #     customer_fullname="Jane Smith",
    #     customer_contact="555-987-6543",
    #     customer_license="A98765XYZ",
    #     customer_email="janesmith@example.com",
    #     rental_date="2024-12-22",
    #     return_date="2024-12-27",
    #     branch_name="Westside Branch",
    #     branch_location="789 Westside Ave",
    #     branch_contact="555-555-5555"
    # )
    print("\nCar Details by ID:")
    get_car_by_id(1)



except mysql.connector.Error as err:
    print(f"Error: {err}")
except Exception as e:
    print(f"Unexpected error: {e}")
finally:
    if mydb.is_connected():
        mycursor.close()
        mydb.close()
        print("Database connection closed")