#!/bin/bash

source src/venv/bin/activate
export PYTHONPATH=$(pwd)/src
export HOST=localhost
#docker run -d -p 6379:6379 redis:latest
#exec gunicorn -b 0.0.0.0:5000 app:app
#exec gunicorn -b 0.0.0.0:5000 app:app
python3 src/main.py