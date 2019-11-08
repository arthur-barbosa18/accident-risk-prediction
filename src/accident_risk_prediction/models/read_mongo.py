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
import random
import numpy as np


logger = logging.getLogger(__name__)


class FilterCoordinates:
    def __init__(self):
        self.errors = []
        try:
            client = MongoClient("localhost", 27017)
            database = client.tcc
            revelante_data = database.revelante_data
            self.accident_data = [accident for accident in revelante_data.find({})]
        except Exception as err:
            logger.error(err)
            self.errors.append({"code": HTTPStatus.INTERNAL_SERVER_ERROR, "message": err.message})

    def filter_accident_data(self, person, vec):
        accident_data_filtered = self.filter_person(person, self.accident_data)
        accident_data_filtered = self.filter_vec(vec, accident_data_filtered)
        return self.filter_locate(accident_data_filtered)

    def filter_person(self, person, sample):
        accident_data_filtered = []
        involved_type = validate_condutor(condutor)
        for accident in sample:
            for involved in accident["involveds"]:
                if (
                    involved["gender"] == person["sexo"]
                    and involved["involed_type"] in involved_type
                    and involved["age"] == person["idade"]
                ):
                    accident_data_filtered.append(accident)
        return accident_data_filtered

    def filter_vec(self, vec, sample):
        accident_data_filtered = []
        for accident in sample:
            for vehicle in accident["vehicles"]:
                if (
                    vehicle["category"] == vec["categoria"]
                    and vehicle["vehicle_type"] == vec["tipo"]
                ):
                    accident_data_filtered.append(accident)
        return accident_data_filtered

    def filter_locate(self, sample):
        self.coordinates = []
        for accident in sample:
            for locate in accident["public_places"]:
                for maps in locate["google_maps_info"]:
                    if "Belo Horizonte" in maps["formatted_address"]:
                        self.coordinates.append(maps["geometry"]["location"])

    def validate_condutor(self, condutor):
        if condutor:
            return ["condutor"]
        return ["nao condutor", "pedestre", "passageiro"]

    def create_coordinates(self, sample):
        total = 2000 / len(sample)
        coordinates = [item for item in sample if random.random() <= total]
        self.lat = [item["lat"] for item in coordinates]
        self.lng = [item["lng"] for item in coordinates]

    def main(self, person, vec):
        if any(self.errors):
            return
        accident_data_filtered = self.filter_accident_data(person, vec)
        self.create_coordinates(accident_data_filtered)
