#!/bin/sh

# Start the Django application in the background
python /uemarketplace/manage.py runserver 0.0.0.0:8000 &

# Start Nginx in the foreground
nginx -g "daemon off;"
