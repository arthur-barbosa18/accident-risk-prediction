from flask_restplus import fields
from jsonschema import validate


class NullableString(fields.String):
    __schema_type__ = ["string", "null"]
    __schema_example__ = "null or string"


class Schemas:
    def __init__(self, api=None):
        self.api = api

    # input_body = {
    #     "required": ["location"],
    #     "type": "object",
    #     "properties": {
    #         "location": {
    #             "required": ["lat", "lng"],
    #             "type": "object",
    #             "properties": {"lat": "number", "lng": "number"},
    #         },
    #         "person": {
    #             "type": "object",
    #             "properties": {
    #                 "gender": {"type": "string", "enum": ["M", "F"]},
    #                 "age": "number",
    #                 "condutor": "boolean",
    #             },
    #         },
    #         "vec": {
    #             "type": "object",
    #             "properties": {
    #                 "vec_type": {
    #                     "type": "string",
    #                     "enum": [
    #                         "NAO INFORMADO",
    #                         "AUTOMOVEL",
    #                         "BICICLETA",
    #                         "MICROONIBUS",
    #                         "CAMINHAO",
    #                         "TREM",
    #                         "CARRO DEAOTRATOR DEODAS",
    #                         "TRATOR DESTEIRAS",
    #                         "ESPECIAL",
    #                         "MOTOCICLETA",
    #                         "ONIBUS",
    #                         "CAMIONETA",
    #                         "TRACAO",
    #                         "CHARRETE",
    #                         "CARROCA",
    #                         "MOTONETA",
    #                         "CICLOMOTOR",
    #                         "CAMINHAO-TRATO",
    #                         "TRATOR MISTO",
    #                         "TRICICLO",
    #                         "REBOQUE EEMI",
    #                         "REBOQUE",
    #                         "MISTO",
    #                     ],
    #                 },
    #                 "category": {
    #                     "type": "string",
    #                     "enum": [
    #                         "NAO INFORMADO",
    #                         "PARTICULAR",
    #                         "APRENDIZAGEM",
    #                         "ALUGUEL",
    #                         "OFICIAL",
    #                         "MISSAO DIPLOMATICA",
    #                     ],
    #                 },
    #             },
    #         },
    #     },
    # }

    input_body = {
        "$schema": "http://json-schema.org/schema#",
        "type": "object",
        "properties": {
            "location": {
                "type": "object",
                "properties": {"lat": {"type": "number"}, "lng": {"type": "number"}},
                "required": ["lat", "lng"],
            },
            "person": {
                "type": "object",
                "properties": {
                    "age": {"type": "integer"},
                    "condutor": {"type": "boolean"},
                    "gender": {"type": "string", "enum": ["M", "F"]},
                },
                # "required": ["age", "condutor", "gender"],
            },
            "vec": {
                "type": "object",
                "properties": {
                    "vec_type": {
                        "type": "string",
                        "enum": [
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
                        ],
                    },
                    "category": {
                        "type": "string",
                        "enum": [
                            "NAO INFORMADO",
                            "PARTICULAR",
                            "APRENDIZAGEM",
                            "ALUGUEL",
                            "OFICIAL",
                            "MISSAO DIPLOMATICA",
                        ],
                    },
                },
                # "required": ["category", "vec_type"],
            },
        },
        "required": ["location", "person", "vec"],
    }

    def input_model(self):

        return self.api.model(
            "Input Body",
            {
                "duration": fields.Float(required=True, description="Duração do vídeo"),
                "timestamp": fields.Float(
                    required=True, description="Hora em timestamp que o vídeo foi criado"
                ),
            },
        )
