from fastapi import FastAPI, Query

import uvicorn

from psycopg2 import connect

from dotenv import dotenv_values

import json

app = FastAPI()

db_config = json.loads(dotenv_values(".env").get("DB_CONFIG"))

connection = connect(**db_config)


@app.get("/search")
def search_item(term: str =  Query(...)):
    
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM nimble_table WHERE description ILIKE %s;", ('%' + term + '%',))

    result = cursor.fetchall()

    cursor.close()

    if not result:

        return "Not found"
    
    return {"RESULT": result}

if __name__=="__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
