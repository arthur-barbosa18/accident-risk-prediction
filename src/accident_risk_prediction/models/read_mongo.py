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


class Predict:
    def __init__(self):
        client = MongoClient("localhost", 27017)
        database = client.tcc
        revelante_data = database.revelante_data
        self.accident_data = [accident for accident in revelante_data.find({})]

    def filter_accident_data(self, person, vec, coordinates):



    def filter_person(self, person, sample):
        accident_data_filtered = []
        involved_type = validate_condutor(condutor)
        for accident in sample:
            for involved in accident_data['involveds']:
                if(involved['gender'] == person['sexo'] and involved['involed_type'] in involved_type and involved['age'] == person['idade']):
                    accident_data_filtered.append(accident)
        return accident_data_filtered

    def filter_vec(self, vec, sample):
        accident_data_filtered = []
        for accident in sample:
            for vehicle in accident_data['vehicles']:
                if(vehicle['category'] == vec['categoria'] and vehicle['vehicle_type'] == vec['tipo']):
                    accident_data_filtered.append(accident)
        return accident_data_filtered


    def filter_locate(self, coordinates):


    def validate_condutor(self, condutor):
        if(condutor):
            return ["condutor"]
        return ["nao condutor", "pedestre", "passageiro"]