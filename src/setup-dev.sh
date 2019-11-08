#!/bin/bash

source src/test_samba/venv/bin/activate
export PYTHONPATH=$(pwd)/src
export HOST=localhost
#exec gunicorn -b 0.0.0.0:5000 app:app
#exec gunicorn -b 0.0.0.0:5000 app:app
python3 src/main.py