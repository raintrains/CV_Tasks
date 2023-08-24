# Run it in the terminal

# Launch beat
celery -A tasks beat --loglevel=info
# Launch worker
celery -A tasks worker --loglevel=info
# Clear queue
celery -A tasks purge