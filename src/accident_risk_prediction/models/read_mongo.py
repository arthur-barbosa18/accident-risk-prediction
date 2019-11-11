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
from accident_risk_prediction.models.Schemas import Schemas
from pymongo import MongoClient
import random
import numpy as np


logger = logging.getLogger(__name__)


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
    def __init__(self):
        self.errors = []
        try:
            client = MongoClient("localhost", 27017)
            database = client.tcc
            revelante_data = database.revelante_data
            weekday = WEEKDAY.get(datetime.now().weekday())
            self.accident_data = [
                accident for accident in revelante_data.find({"weekday": weekday})
            ]
        except Exception as err:
            logger.error(err)
            self.errors.append({"code": HTTPStatus.INTERNAL_SERVER_ERROR, "message": err.message})

    def filter_accident_data(self, person, vec):
        accident_data_filtered = self.filter_person(person, self.accident_data)
        accident_data_filtered = self.filter_vec(vec, accident_data_filtered)

        return self.filter_locate(accident_data_filtered)

    def filter_person(self, person, sample):
        accident_data_filtered = []
        involved_type = self.validate_condutor(person.get("condutor", ""))
        gender = self.validate_gender(person.get("gender", ""))
        age = self.validate_age(person.get("age", ""))
        for accident in sample:
            for involved in accident["involveds"]:
                if (
                    involved["gender"] in gender
                    and involved["involved_type"] in involved_type
                    and involved["age"] in age
                ):
                    accident_data_filtered.append(accident)
        return accident_data_filtered

    def filter_vec(self, vec, sample):
        accident_data_filtered = []
        vec_type = self.validate_vec_type(vec.get("vec_type", ""))
        vec_category = self.validate_vec_category(vec.get("vec_category", ""))
        for accident in sample:
            for vehicle in accident["vehicles"]:
                if vehicle["category"] in vec_category and vehicle["vehicle_type"] in vec_type:
                    accident_data_filtered.append(accident)
        return accident_data_filtered

    def filter_locate(self, sample):
        self.coordinates = []
        for accident in sample:
            for locate in accident["public_places"]:
                for maps in locate["google_maps_info"]:
                    if "Belo Horizonte" in maps["formatted_address"]:
                        self.coordinates.append(maps["geometry"]["location"])
        return self.coordinates

    def validate_condutor(self, condutor):
        if condutor:
            return ["condutor"]
        return ["nao condutor", "pedestre", "passageiro"]

    def validate_age(self, age):
        if age:
            return [age]
        return [i for i in range(0, 100)]

    def validate_gender(self, gender):
        if gender:
            return [gender]
        return ["M", "F"]

    def validate_vec_type(self, vec_type):
        if vec_type:
            return [vec_type]
        return [
            "NAO INFORMADO",
            "AUTOMOVEL",
            "BICICLETA",
            "MICROONIBUS",
            "CAMINHAO",
            "TREM",
            "CARRO DEAOTRATOR DEODAS",
            "TRATOR DESTEIRAS",
            "ESPECIAL",
            "MOTOCICLETA",
            "ONIBUS",
            "CAMIONETA",
            "TRACAO",
            "CHARRETE",
            "CARROCA",
            "MOTONETA",
            "CICLOMOTOR",
            "CAMINHAO-TRATO",
            "TRATOR MISTO",
            "TRICICLO",
            "REBOQUE EEMI",
            "REBOQUE",
            "MISTO",
        ]

    def validate_vec_category(self, vec_category):
        if vec_category:
            return [vec_category]
        return [
            "NAO INFORMADO",
            "PARTICULAR",
            "APRENDIZAGEM",
            "ALUGUEL",
            "OFICIAL",
            "MISSAO DIPLOMATICA",
        ]

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
