from psycopg2 import errors, connect

import csv

from dotenv import dotenv_values

import json


db_params = json.loads(dotenv_values(".env").get("DB_CONFIG"))


def create_table_and_first_filling():
        
    connection = connect(**db_params)

    cursor = connection.cursor()

    connection.autocommit = True

    create_table = """  CREATE TABLE IF NOT EXISTS nimble_table (

                        id serial PRIMARY KEY, 

                        first_name varchar(50), 

                        last_name varchar(50), 

                        email varchar(150) UNIQUE, 

                        description TEXT

                        ); """


    cursor.execute(create_table)

    with open("contact.csv", "r", encoding="UTF-8") as file_csv:
        reader = csv.reader(file_csv)       
    
        for i in list(reader)[1:]:      
            
            try:
                
                insert_query = "INSERT INTO nimble_table (first_name, last_name, email, description) VALUES (%s, %s, %s, %s)"       

                cursor.execute(insert_query, (i[0], i[1], i[2], i[3]))

            except errors.UniqueViolation:

                pass

    cursor.close()
    connection.close()
    

def update_table(f_name, l_name, email, desc):
    
    connection = connect(**db_params)

    cursor = connection.cursor()

    connection.autocommit = True

    update_data_table = "INSERT INTO nimble_table (first_name, last_name, email, description) VALUES (%s, %s, %s, %s)"

    try:    
        
        cursor.execute(update_data_table, (f_name, l_name, email, desc))
    
    except errors.UniqueViolation:
        pass
    
    cursor.close()
    connection.close()


def table_exists():

    connection = connect(**db_params)

    cursor = connection.cursor()

    table_name = "nimble_table"

    cursor.execute(f"SELECT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = '{table_name}')")

    response = cursor.fetchone()[0]

    if response:

        return True
    
    return False