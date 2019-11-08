#!/bin/bash

source ./src/venv/bin/activate
export PYTHONPATH=$(pwd)/src
export HOST=localhost
#exec gunicorn -b 0.0.0.0:5000 app:app
#exec gunicorn -b 0.0.0.0:5000 app:app
pytest --cov tests 