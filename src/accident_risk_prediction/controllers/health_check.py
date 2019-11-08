import requests
import json
import sys
from jsonschema import validate
import os
from os.path import join, dirname
import requests
import logging
from http import HTTPStatus
import redis

logger = logging.getLogger(__name__)

dotenv_path = join(dirname(__file__), ".env")


class HealthCheck:
    def __init__(self):
        pass

    def conn_redis(self):
        try:
            conn = redis.Redis(host=os.environ.get("HOST"), port=6379)
            del conn
            self.response = {"code": HTTPStatus.OK, "message": "Redis OK"}
            logger.info(self.response)
        except Exception as err:
            self.response = {"code": HTTPStatus.INTERNAL_SERVER_ERROR, "message": "Redis NOT OK"}
            logger.error(err)

    def main(self):
        self.conn_redis()
        return self.response
