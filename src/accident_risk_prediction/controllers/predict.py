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
from accident_risk_prediction.models.read_mongo import FilterCoordinates
from accident_risk_prediction.models.calculate_kde import CalculateKDE
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
                logger.error(err)

            if not any(self.errors):
                self.person, self.vec, self.weather, self.location = (
                    newBody["person"],
                    newBody["vec"],
                    # newBody["weather"],
                    newBody["location"],
                )

    def calculate_kde(self):
        self.kde = CalculateKDE(self.coordinates.lat, self.coordinates.lng).main()

    def filter_coordinates(self):
        self.coordinates = FilterCoordinates(self.person, self.vec)

    def calculate_predict(self):
        values = np.vstack([self.coordinates.lat, self.coordinates.lng])
        max_value = self.kde(values).max()
        self.estimate = self.kde([self.location["lat"], self.location["lng"]])
        return self.estimate / max_value

    def to_rank(self):
        if self.calculate_predict() <= 0.2:
            return "Muito Baixo"
        elif self.calculate_predict() <= 0.4:
            return "Baixo"
        elif self.calculate_predict() <= 0.6:
            return "Moderado"
        elif self.calculate_predict() <= 0.8:
            return "Alto"
        elif self.calculate_predict() <= 1:
            return "Muito Alto"

    def validate_body(self, body):
        return Draft7Validator(Schemas.input_body).iter_errors(body)

    def main(self):
        self.filter_coordinates()
        if any(self.coordinates.errors) or any(self.errors):
            self.errors.append(self.coordinates.errors)
            return {"code": HTTPStatus.BAD_REQUEST, "errors": self.errors}
        self.calculate_kde()
        self.calculate_predict()
        return {
            "code": HttpStatus.OK,
            "message": "Seu indice de sofrer acidente em Belo Horizonte é {}".format(
                self.to_rank()
            ),
        }
