from celery import Celery
from celery.schedules import crontab

from dotenv import dotenv_values

from api_requests import update_db_from_api

from db_utils import create_table_and_first_filling, table_exists


app = Celery('tasks', broker=dotenv_values(".env").get("BROKER_URL"))


if not table_exists():

    create_table_and_first_filling()
    update_db_from_api()


@app.task
def perform_update():
    
    try:

        update_db_from_api()

        return "SUCCESS"
    
    except Exception as e:

        return {"FAILED": e}


app.conf.beat_schedule = {

    "daily_task": {

        "task": "tasks.perform_update",
        "schedule": crontab(minute=0, hour=0),

    }

}