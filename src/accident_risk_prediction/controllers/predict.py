import requests
import json
import sys
from jsonschema import validate
import os
from os.path import join, dirname
import logging
import json
from datetime import datetime
from http import HTTPStatus
from jsonschema import validate, Draft7Validator
from accident_risk_prediction.models.Schemas import Schemas
from pymongo import MongoClient
from scipy import stats, integrate
import random
import numpy as np
import seaborn as sns

logger = logging.getLogger(__name__)


class Predict:
    def __init__(self, body=None):
        if body:
            newBody = json.loads(body)
            self.errors = []
            for err in self.validate_body(newBody):
                self.errors.append(err)

            if not any(self.errors):
                self.person, self.vec, self.weather, self.location = (
                    newBody["person"],
                    newBody["vec"],
                    # newBody["weather"],
                    newBody["location"],
                )

    def calculate_kde(self):
        pass

    def filter_database(self):
        pass

    def calculate_predict(self):
        pass

    def to_rank(self):
        pass

    def delete_list_videos():
        conn = redis.Redis(host=os.environ.get("HOST"), port=6379)
        conn.delete("duration")
        conn.delete("timestamp")
        del conn
        return {"body": {}, "code": HTTPStatus.NO_CONTENT}

    def validate_body(self, body):

        return Draft7Validator(Schemas.input_video).iter_errors(body)

    def set_list_videos(self):
        try:
            conn = redis.Redis(host=os.environ.get("HOST"), port=6379)
            duration = {}
            duration[str(len(conn.hgetall("duration")) + 1)] = self.duration
            timestamp = {}
            timestamp[str(len(conn.hgetall("timestamp")) + 1)] = self.timestamp
            conn.hmset("duration", duration)
            conn.hmset("timestamp", timestamp)
            del conn
        except Exception as err:
            raise (err)

    def validate_timestamp(self, timestamp):

        return timestamp / (10 ** len(str(timestamp)[10:])) >= (
            datetime.timestamp(datetime.now()) - 60
        )

    def create_statistics(self, statistics, duration):
        statistics["sum_duration"] = statistics["sum_duration"] + duration
        statistics["count_videos"] = statistics["count_videos"] + 1
        statistics["avg_duration"] = statistics["sum_duration"] / statistics["count_videos"]
        statistics["max_duration"] = (
            duration if duration > statistics["max_duration"] else statistics["max_duration"]
        )
        statistics["min_duration"] = (
            duration if duration < statistics["min_duration"] else statistics["min_duration"]
        )
        return statistics

    def save_video(self):
        try:
            if len(self.errors) > 0:
                messages = []
                code = HTTPStatus.UNPROCESSABLE_ENTITY
                logger.error(self.errors)
                for err in self.errors:

                    messages.append(err.message)

                    if "required" in err.message:
                        code = HTTPStatus.PRECONDITION_FAILED

                return {"code": code, "message": messages}
            self.set_list_videos()
            if self.validate_timestamp(self.timestamp):
                logger.info({"message": "Video salvo com sucesso"})
                return {"code": HTTPStatus.CREATED, "message": "Video salvo com sucesso"}
            logger.info(
                {"message": "Video com timestamp mais antigo que 60 segundos da hora atual"}
            )
            return {"code": HTTPStatus.NO_CONTENT}
        except Exception as err:
            logger.error(err)
            return {"code": HTTPStatus.INTERNAL_SERVER_ERROR, "message": err.message}

    def get_statistics(self):
        try:
            message = None
            statistics = {
                "sum_duration": 0,
                "avg_duration": 0,
                "max_duration": 0,
                "min_duration": float("inf"),
                "count_videos": 0,
            }
            conn = redis.Redis(host=os.environ.get("HOST"), port=6379)

            list_duration = [
                float(duration) for duration in list(conn.hgetall("duration").values())
            ]
            list_timestamp = [
                int(timestamp) for timestamp in list(conn.hgetall("timestamp").values())
            ]
            for index in range(0, (len(list_duration))):
                if self.validate_timestamp(list_timestamp[index]):

                    statistics = self.create_statistics(statistics, list_duration[index])

            if statistics["sum_duration"] == 0:
                message = "Não há videos para estatísticas serem geradas!"
            del conn
            return {"code": HTTPStatus.OK, "statistics": message or statistics}
        except Exception as err:
            logger.error(err)
            return {"code": HTTPStatus.INTERNAL_SERVER_ERROR, "message": err.message}
