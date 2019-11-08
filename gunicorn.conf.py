#!/usr/bin/env python
import os

bind = "0.0.0.0:80"
max_requests = 1000
max_requests_jitter = 100
preload_app = True
pythonpath = "/opt/test-samba/src"
# statsd_host = os.environ.get("STATSD_HOST", "localhost:8125")
# statsd_prefix = "test-samba"
os.environ["HOST"] = "redis"
threads = os.environ.get("GUNICORN_THREADS", 4)
timeout = 10
worker_class = "gthread"
worker_tmp_dir = "/dev/shm"
workers = os.environ.get("GUNICORN_WORKERS", 4)
