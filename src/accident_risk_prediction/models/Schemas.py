from flask_restplus import fields
from jsonschema import validate


class NullableString(fields.String):
    __schema_type__ = ["string", "null"]
    __schema_example__ = "null or string"


class Schemas:
    def __init__(self, api=None):
        self.api = api

    input_body = {
        "required": ["location"],
        "type": "object",
        "properties": {
            "location": {
                "required": ["lat", "lng"],
                "type": "object",
                "properties": {"lat": "number", "lng": "number"},
            },
            "person": {
                "required": ["gender", "age", "condutor"],
                "type": "object",
                "properties": {"gender": "string", "age": "number", "condutor": "boolean"},
            },
            "vec": {
                "required": ["category", "vec_type"],
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
            },
        },
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
