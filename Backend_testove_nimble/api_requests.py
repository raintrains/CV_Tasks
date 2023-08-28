import requests

from dotenv import dotenv_values

import json

from db_utils import update_table


headers = json.loads(dotenv_values(".env").get("HEADERS"))
api_nimble = dotenv_values(".env").get("API")


def update_db_from_api():

    r = requests.get(api_nimble, headers=headers)

    if r.status_code == 200:
        
        data = r.json()

        for i in data["resources"]:
 
            first_name = i.get("fields", {}).get("first name", [{}])[0].get("value", {})
            last_name = i.get("fields", {}).get("last name", [{}])[0].get("value", {})
            email = i.get("fields", {}).get("email", [{}])[0].get("value", {})
            description = i.get("fields", {}).get("description", [{}])[0].get("value", {})

            if first_name and last_name and email and description:

                update_table(f_name=first_name, l_name=last_name, email=email, desc=description)

            else:

                print("Some of the fields are empty")

    else:

        print(f"Request failed with an error: {r.status_code}")