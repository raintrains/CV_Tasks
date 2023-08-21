from psycopg2 import connect, errors

from dotenv import dotenv_values

db_params = dotenv_values(".env").get("DB_CONFIG")


def create_and_db_filling():

    connection = connect(**db_params)

    cursor = connection.cursor()

    connection.autocommit = True

    cursor.execute("CREATE TABLE IF NOT EXISTS numbers (id serial PRIMARY KEY, phone_numbers varchar(50) UNIQUE);")


    with open("numbers.txt", "r", encoding="UTF-8") as numbers:
        numbers = [number.rstrip("\n").lstrip("+").replace(" ", "") for number in numbers]

    try:
        for number in numbers:

            insert_query = "INSERT INTO numbers (phone_numbers) VALUES (%s);"

            cursor.execute(insert_query, (f"{number}", ))

    except errors.UniqueViolation:
        pass

    cursor.close()

    connection.close()
    

def user_query(query):

    connection = connect(**db_params)

    cursor = connection.cursor()

    placeholders = ", ".join(["%s"] * len(query))

    select_query = f"SELECT phone_numbers FROM numbers WHERE phone_numbers IN ({placeholders}) ;"

    cursor.execute(select_query, query)
    
    response = [number[0] for number in cursor.fetchall()]

    cursor.close()
    connection.close()

    return response[:10]
