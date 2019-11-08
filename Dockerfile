FROM python:3.7

ARG WORKERS=4
ARG THREADS=4

COPY requirements.txt /opt/requirements.txt
RUN pip install -r /opt/requirements.txt

COPY src /opt/accident-risk-prediction/
COPY gunicorn.conf.py /gunicorn.conf.py

WORKDIR /opt/accident-risk-prediction
ENV PYTHONPATH /opt/accident-risk-prediction
CMD ["/usr/local/bin/gunicorn", "--config", "/gunicorn.conf.py",  "main:app"]
