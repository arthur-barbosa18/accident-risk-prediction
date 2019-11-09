import requests
import json
import sys
from jsonschema import validate
import os
from os.path import join, dirname
import logging
from scipy import stats, integrate

import json
from datetime import datetime
from http import HTTPStatus
from accident_risk_prediction.models.Schemas import Schemas
from pymongo import MongoClient
import random
import numpy as np


logger = logging.getLogger(__name__)


class CalculateKDE:
    def __init__(self, lat, lng):
        self.lat, self.lng = lat, lng

    def main(self):
        try:
            values = np.vstack([self.lat, self.lng])
            self.kernel = stats.gaussian_kde(values)
            import ipdb

            ipdb.set_trace()  # breakpoint f38a82a6 //

            return self.kernel
        except Exception as err:
            logger.error(err)
            return {"code": HTTPStatus.INTERNAL_SERVER_ERROR, "message": err}
