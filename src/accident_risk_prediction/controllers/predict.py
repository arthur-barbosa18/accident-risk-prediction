""" Module to class Predict """

import json
import logging
from http import HTTPStatus
import numpy as np
from jsonschema import Draft7Validator
from accident_risk_prediction.repo.schemas import INPUT_BODY
from accident_risk_prediction.repo.extract_data import FilterCoordinates
from accident_risk_prediction.repo.calculate_kde import calculate_kde

LOGGER = logging.getLogger(__name__)


class Predict:

    """ Class responsible by handling all operations to
    generate accident risk prediction of Belo Horizonte city
    """

    def __init__(self, body=None):
        self.risk = None
        self.kde = None
        self.coordinates = None
        self.estimate = None
        self.errors = []
        if body:
            body = json.loads(body)
            self.validate_body(body)
            if not any(self.errors):
                self.person, self.vec, self.location = (
                    body["person"],
                    body["vec"],
                    body["location"],
                )

    def calculate_kde(self):
        """ Calculate kernel density estimation 2d """
        try:
            self.kde = calculate_kde(
                self.coordinates.lat, self.coordinates.lng)
        except BaseException as err:
            self.errors.append(err)

    def filter_coordinates(self):
        """ Responsible by filter coordinates according
        with exogenous variables about vehicle,
        gender, weekday, conductor age, etc
        """
        self.coordinates = FilterCoordinates()
        self.coordinates.main(self.person, self.vec)

    def calculate_predict(self):
        """ Calculate the risk accident prediction """
        if (any(self.coordinates.lat) and any(self.coordinates.lng)
                and len(self.coordinates.lat) == len(self.coordinates.lng)):
            values = np.vstack([self.coordinates.lat, self.coordinates.lng])
            max_value = self.kde(values).max()

            self.estimate = self.kde(
                [self.location["lat"], self.location["lng"]])[0]
            return self.estimate / max_value
        err_msg = "There are no one accident with this profile"
        LOGGER.error(err_msg)
        self.errors.append(err_msg)
        return False

    def to_rank(self):
        """ Define a rank to calculated probability of accident risk """
        accident_probability = self.calculate_predict()
        if accident_probability:
            self.risk = round(accident_probability, 2)
            if self.risk <= 0.1:
                return "Pífio"
            if self.risk <= 0.2:
                return "Muito Baixo"
            if self.risk <= 0.4:
                return "Baixo"
            if self.risk <= 0.6:
                return "Mediano"
            if self.risk <= 0.8:
                return "Alto"
            if self.risk <= 1:
                return "Muito Alto"
        return None

    def validate_body(self, body):
        """ Validate input data from request """
        for err in Draft7Validator(INPUT_BODY).iter_errors(body):
            self.errors.append(err)
            LOGGER.error(err)

    def main(self):
        """ Main function """

        if any(self.errors):
            return {"code": HTTPStatus.UNPROCESSABLE_ENTITY,
                    "errors": str(self.errors)}
        self.filter_coordinates()
        if any(self.coordinates.errors):
            return {"code": HTTPStatus.BAD_REQUEST, "errors": str(self.errors)}
        self.calculate_kde()
        if any(self.errors):
            return {"code": HTTPStatus.INTERNAL_SERVER_ERROR,
                    "errors": str(self.errors)}
        risk = self.to_rank()
        if not risk and any(self.errors):
            return {"code": HTTPStatus.INTERNAL_SERVER_ERROR,
                    "errors": str(self.errors)}

        return {
            "code": HTTPStatus.OK,
            "message":
            "Seu indice de sofrer acidente no ponto {} é {} e igual a {}\
            ".format(
                self.location, risk, self.risk
            ).strip(),
        }
