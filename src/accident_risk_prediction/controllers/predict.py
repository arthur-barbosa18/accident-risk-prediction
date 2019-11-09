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
                self.person, self.vec, self.location = (
                    newBody["person"],
                    newBody["vec"],
                    newBody["location"],
                )

    def calculate_kde(self):
        try:
            self.kde = CalculateKDE(self.coordinates.lat, self.coordinates.lng).main()
        except Exception as err:
            self.error.append(err)

    def filter_coordinates(self):
        self.coordinates = FilterCoordinates()
        self.coordinates.main(self.person, self.vec)

    def calculate_predict(self):
        values = np.vstack([self.coordinates.lat, self.coordinates.lng])
        max_value = self.kde(values).max()

        self.estimate = self.kde([self.location["lat"], self.location["lng"]])[0]
        return self.estimate / max_value

    def to_rank(self):
        self.risk = round(self.calculate_predict(), 2)
        if self.risk <= 0.1:
            return "Pífio"
        elif self.risk <= 0.2:
            return "Muito Baixo"
        elif self.risk <= 0.4:
            return "Baixo"
        elif self.risk <= 0.6:
            return "Mediano"
        elif self.risk <= 0.8:
            return "Alto"
        elif self.risk <= 1:
            return "Muito Alto"

    def validate_body(self, body):
        return Draft7Validator(Schemas.input_body).iter_errors(body)

    def main(self):
        if any(self.errors):
            return {"code": HTTPStatus.UNPROCESSABLE_ENTITY, "errors": str(self.errors)}
        self.filter_coordinates()
        if any(self.coordinates.errors):
            return {"code": HTTPStatus.BAD_REQUEST, "errors": str(self.errors)}
        self.calculate_kde()
        if any(self.errors):
            return {"code": HTTPStatus.INTERNAL_SERVER_ERROR, "errors": str(self.errors)}
        self.calculate_predict()
        return {
            "code": HTTPStatus.OK,
            "message": "Seu indice de sofrer acidente no ponto {} é {} e igual a {}".format(
                self.location, self.to_rank(), self.risk
            ),
        }
