""" Module to software health check """

import logging
from http import HTTPStatus
from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError
from accident_risk_prediction.repo.constants import \
    DATABASE_SERVER, DATABASE_PORT

LOGGER = logging.getLogger(__name__)


def conn_mongo():
    """ Check Mongodb connection """
    try:
        client = MongoClient(DATABASE_SERVER, DATABASE_PORT,
                             serverSelectionTimeoutMS=10,
                             connectTimeoutMS=20000)
        LOGGER.info(client.server_info())
        response = {"code": HTTPStatus.OK, "message": "Mongodb connection OK"}
        LOGGER.info(response)
        return response
    except ServerSelectionTimeoutError as err:
        response = {
            "code": HTTPStatus.INTERNAL_SERVER_ERROR,
            "message": "Mongodb connection NOT OK"}
        LOGGER.error(err)
        return response
