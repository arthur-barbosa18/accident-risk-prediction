""" Routes """
# pylint: disable=no-self-use

from http import HTTPStatus
from flask import Flask, request
from flask_restplus import Api, Resource
from accident_risk_prediction.repo.schemas import INPUT_BODY
from accident_risk_prediction.controllers.predict import Predict
from accident_risk_prediction.controllers.health_check import conn_mongo
from accident_risk_prediction.controllers.handle_logs import conf_logging

# from accident_risk_prediction.controllers.health_check import HealthCheck
conf_logging()

APP = Flask(__name__)
API = Api(
    APP,
    version="1.0",
    title="PREDICT RISK ACCIDENT AT BH",
    description="PREDICT RISK ACCIDENT AT BH",
    doc="/api/v1/swagger",
)


NAMESPACE = API.namespace("api/v1", description="TCC")


@NAMESPACE.route("/predict-accident")
class PredictAccident(Resource):
    """ Class to /predict-accident handle requests """
    @NAMESPACE.doc("TCC")
    @NAMESPACE.expect(API.schema_model("data", INPUT_BODY))
    @NAMESPACE.response(code=HTTPStatus.OK, description="Ok")
    @NAMESPACE.response(code=HTTPStatus.INTERNAL_SERVER_ERROR,
                        description="Internal Server Error")
    @NAMESPACE.response(code=HTTPStatus.UNPROCESSABLE_ENTITY,
                        description="Unprocessable Entity")
    @NAMESPACE.response(code=HTTPStatus.PRECONDITION_FAILED,
                        description="Precondition Failed")
    def post(self):
        """ dsadsad """
        response = Predict(request.data).main()
        code = response["code"]
        del response["code"]
        return response, code


@NAMESPACE.route("/healthy")
class Health(Resource):
    """ Clas to handle /healthy requests """
    @NAMESPACE.response(code=HTTPStatus.OK,
                        description="REDIS OK")
    @NAMESPACE.response(code=HTTPStatus.INTERNAL_SERVER_ERROR,
                        description="REDIS NOT OK")
    @NAMESPACE.doc("get to health check")
    def get(self):
        """ Get method http to verify if all is ok with the api """
        response = conn_mongo()
        return response["message"], response["code"]
