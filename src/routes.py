from flask import Flask, request
from flask_restplus import Api, Resource, reqparse
from accident_risk_prediction.controllers.predict import Predict

# from accident_risk_prediction.controllers.health_check import HealthCheck
from accident_risk_prediction.models.Schemas import Schemas
import werkzeug
from http import HTTPStatus
import sys

app = Flask(__name__)
api = Api(
    app,
    version="1.0",
    title="PREDICT RISK ACCIDENT AT BH",
    description="PREDICT RISK ACCIDENT AT BH",
    doc="/api/v1/swagger",
)

ns = api.namespace("api/v1", description="TCC")
# input_model = Schemas(api).input_model()


# input_model = Schemas(api).input_model()


@ns.route("/predict-accident")
class Predict(Resource):
    @ns.doc("TCC")
    # @ns.expect(input_model)
    @ns.response(code=HTTPStatus.OK, description="Ok")
    @ns.response(code=HTTPStatus.INTERNAL_SERVER_ERROR, description="Internal Server Error")
    @ns.response(code=HTTPStatus.UNPROCESSABLE_ENTITY, description="Unprocessable Entity")
    @ns.response(code=HTTPStatus.PRECONDITION_FAILED, description="Precondition Failed")
    def post(self):

        response = Predict(request.data).main()
        code = response["code"]
        del response["code"]
        return response, code

    # @ns.response(code=HTTPStatus.NO_CONTENT, description="No Content")
    # def delete(self):
    #     response = Videos.delete_list_videos()
    #     return response["body"], response["code"]


# @ns.route("/healthy")
# class Health(Resource):
#     @ns.response(code=HTTPStatus.OK, description="REDIS OK")
#     @ns.response(code=HTTPStatus.INTERNAL_SERVER_ERROR, description="REDIS NOT OK")
#     @ns.doc("get to health check")
#     def get(self):
#         response = HealthCheck().main()
#         return response["message"], response["code"]
