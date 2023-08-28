# Launch beat
celery -A tasks beat --loglevel=info
# Launch worker
celery -A tasks worker --loglevel=info
# Clear queue
celery -A tasks purge

# How search by api
http://127.0.0.1:8000/search?term='your_text'


# Let`s run it

# Preparing the enviroment
python3.10 -m venv venv && 
source venv/bin/activate && 
pip install -r requirements.txt

# Running the app to load data from csv and after daily update from api
celery -A tasks beat --loglevel=info && celery -A tasks worker --loglevel=info

# Search engine api launch
python my_api.py

# Launch api for table search
http://127.0.0.1:8000/search?term='your_text'

# Example
http://127.0.0.1:8000/search?term=Arnold