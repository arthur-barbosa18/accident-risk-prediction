""" Module to extract all information from collection in mongo db """

import logging
from datetime import datetime
import random
from http import HTTPStatus
from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError
from accident_risk_prediction.repo.constants import (
    DATABASE_SERVER, DATABASE_PORT, CATEGORIES,
    CONDUTOR_TYPES, GENDER, VEHICLE_TYPE)

LOGGER = logging.getLogger(__name__)


WEEKDAY = {
    0: "segunda-feira",
    1: "terça-feira",
    2: "quarta-feira",
    3: "quinta-feira",
    4: "sexta-feira",
    5: "sábado",
    6: "domingo",
}


class FilterCoordinates:
    """ Class to select coordinates according with
    exogenous variables
    """

    def __init__(self):
        self.errors = []
        self.coordinates = []
        self.lat = []
        self.lng = []
        try:
            client = MongoClient(DATABASE_SERVER, DATABASE_PORT,
                                 serverSelectionTimeoutMS=10,
                                 connectTimeoutMS=20000)
            database = client.tcc
            accidents_db = database.accidents_db
            self.accident_data = [
                accident for accident in accidents_db.find(
                    {"weekday":  WEEKDAY.get(datetime.now().weekday())})
            ]
        except ServerSelectionTimeoutError as err:
            LOGGER.error(err)
            self.errors.append(
                {"code": HTTPStatus.INTERNAL_SERVER_ERROR,
                 "message": err._message})

    def filter_accident_data(self, person, vec):
        """ filter accident data
        person (dict): exogenous variables about person involved in accident
        vec (dict): exogenous variables about vehicle involved in accident
        return data of the accidents after all filters applied
        """
        accident_data_filtered = self.filter_person(person, self.accident_data)
        accident_data_filtered = self.filter_vec(vec, accident_data_filtered)

        return self.filter_locate(accident_data_filtered)

    def filter_person(self, person, sample):
        """ filter data by person variables """
        accident_data_filtered = []
        involved_type = self.validate_condutor(person.get("condutor", ""))
        gender = self.validate_gender(person.get("gender", ""))
        age = self.validate_age(person.get("age", ""))
        for accident in sample:
            for involved in accident["involveds"]:
                if (involved["gender"] in gender
                        and involved["involved_type"] in involved_type and
                        involved["age"] in age):
                    accident_data_filtered.append(accident)
        return accident_data_filtered

    def filter_vec(self, vec, sample):
        """ filter data by vehicle variables """
        accident_data_filtered = []
        vec_type = self.validate_vec_type(vec.get("vec_type", ""))
        vec_category = self.validate_vec_category(vec.get("vec_category", ""))
        for accident in sample:
            for vehicle in accident["vehicles"]:
                if vehicle["category"] in \
                        vec_category and vehicle["vehicle_type"] in vec_type:
                    accident_data_filtered.append(accident)
        return accident_data_filtered

    def filter_locate(self, sample):
        """ filter data by BH city local """
        for accident in sample:
            for locate in accident["public_places"]:
                for maps in locate["google_maps_info"]:
                    if "Belo Horizonte" in maps["formatted_address"]:
                        self.coordinates.append(maps["geometry"]["location"])
        return self.coordinates

    @classmethod
    def validate_condutor(cls, condutor):
        """ validate condutor types
        condutor (str)
        """
        if condutor:
            return ["condutor"]
        return CONDUTOR_TYPES

    @classmethod
    def validate_age(cls, age):
        """ validate involved age
        age (int)
        """
        if age:
            return [age]
        return [i for i in range(0, 100)]

    @classmethod
    def validate_gender(cls, gender):
        """ validate involved gender
        gender (str)
        """
        if gender:
            return [gender]
        return GENDER

    @classmethod
    def validate_vec_type(cls, vec_type):
        """ validate vehicle type
        vec_category (str)
        """
        if vec_type:
            return [vec_type]
        return VEHICLE_TYPE

    @classmethod
    def validate_vec_category(cls, vec_category):
        """ validate vehicle category
        vec_category (str)
        """
        if vec_category:
            return [vec_category]
        return CATEGORIES

    def create_coordinates(self, sample):
        """ Create coordinates array """
        if sample:
            total = 2000 / len(sample)

            coordinates = [item for item in sample if random.random() <= total]
            self.lat = [item["lat"] for item in coordinates]
            self.lng = [item["lng"] for item in coordinates]

    def main(self, person, vec):
        """ main function """
        if any(self.errors):
            return
        accident_data_filtered = self.filter_accident_data(person, vec)
        self.create_coordinates(accident_data_filtered)
