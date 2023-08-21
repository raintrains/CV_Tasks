from psycopg2 import errors, connect

import logging

import csv

from dotenv import dotenv_values


logging.basicConfig(filename="db_utils_nimble.log", level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

db_params = dotenv_values(".env").get("DB_CONFIG")


def create_table_and_first_filling():

    logging.info("Starting func create table and first filling...")

    try:
        
        logging.info("Connecting to db...")

        connection = connect(**db_params)

        logging.info("Successfully conected")

    except errors.OperationalError as e:

        logging.error(f"Connection error {e}")
    

    cursor = connection.cursor()

    connection.autocommit = True

    create_table = """  CREATE TABLE IF NOT EXISTS nimble_table (

                        id serial PRIMARY KEY, 

                        first_name varchar(50), 

                        last_name varchar(50), 

                        email varchar(150) UNIQUE, 

                        description TEXT

                        ); """

    try:

        logging.info("Creation table...")

        cursor.execute(create_table)

        logging.info("Table has been created")

    except errors.OperationalError as e:

        logging.error(f"Base creation error: {e}")

    logging.info("Opening a csv file")

    with open("contact.csv", "r", encoding="UTF-8") as file_csv:
        reader = csv.reader(file_csv)

        for i in list(reader)[1:]:
        
            try:

                logging.info("Adding data to a table...")

                insert_query = "INSERT INTO nimble_table (first_name, last_name, email, description) VALUES (%s, %s, %s, %s)"

                cursor.execute(insert_query, (i[0], i[1], i[2], i[3]))
                
                logging.info("Added successfully")

            except errors.UniqueViolation as e:

                logging.error(f"Addition error {e}")
                
    cursor.close()
    connection.close()


def update_table(f_name, l_name, email, desc):
    
    logging.info("Starting the table update function...")

    try:
        
        logging.info("Connecting to db...")

        connection = connect(**db_params)

        logging.info("Successfully conected")

    except errors.OperationalError as e:

        logging.error(f"Connection error {e}")

    cursor = connection.cursor()

    connection.autocommit = True

    update_data_table = "INSERT INTO nimble_table (first_name, last_name, email, description) VALUES (%s, %s, %s, %s)"

    try:

        logging.info("Data update...")
        
        cursor.execute(update_data_table, (f_name, l_name, email, desc))

        logging.info("Data updated")

    except errors.UniqueViolation as e:

        logging.error(f"Update error {e}")

    cursor.close()
    connection.close()

