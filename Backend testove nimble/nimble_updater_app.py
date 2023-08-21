import requests

from celery import Celery
from celery.schedules import crontab

import logging

from dotenv import dotenv_values

from db_utils_nimble import update_table, create_table_and_first_filling


logging.basicConfig(filename="nimble_updater_app.log", level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

try:
    
    logging.info("'create_table_and_first_filling' func call...")

    create_table_and_first_filling()

    logging.info("Call the func 'create_table_and_first_filling' succeeded")

except Exception as e:

    logging.error(f"An error occured {e}")

headers = dotenv_values(".env").get("HEADERS")

try:

    logging.info("Requesting API...")

    r = requests.get("https://api.nimble.com/api/v1/contacts", headers=headers)

    if r.status_code == 200:
        
        logging.info(f"Request successful {r.status_code} ")
        
except Exception as e:

    logging.error(f"Request failed with an error: {e}")

app = Celery('tasks', broker="redis://localhost:6379/0")

logging.info("The launch Celery app")

@app.task
def update_user_data():

    data = r.json()



    for i in data["resources"]:
    
        try:

            logging.info("Checking the content of API request...")

            first_name = i.get("fields", {}).get("first name", [{}])[0].get("value", {})
            last_name = i.get("fields", {}).get("last name", [{}])[0].get("value", {})
            email = i.get("fields", {}).get("email", [{}])[0].get("value", {})
            description = i.get("fields", {}).get("description", [{}])[0].get("value", {})


            if first_name and last_name and email and description:
                
                logging.info("Content validation passed")

                logging.info("'update_table' call attempt")

                update_table(f_name=first_name, l_name=last_name, email=email, desc=description)

                logging.info("Function succeeded")

        except KeyError as e:
            
            logging.error(f"Validation failed an a error {e}")



    # first name/last name/email/description.

app.conf.beat_shedule = {
    "daily_task": {
        "task": "task.update_data_user",
        "schedule": crontab(minute=0, hour=0),
    }
}