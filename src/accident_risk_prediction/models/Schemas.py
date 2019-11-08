from flask_restplus import fields
from jsonschema import validate


class NullableString(fields.String):
    __schema_type__ = ["string", "null"]
    __schema_example__ = "null or string"


class Schemas:
    def __init__(self, api=None):
        self.api = api

    input_video = {
        "required": ["duration", "timestamp"],
        "type": "object",
        "properties": {
            "duration": {"type": "number"},
            "timestamp": {"type": "number"},
        },
    }

    def input_model(self):

        return self.api.model(
            "Input Video",
            {
                "duration": fields.Float(
                    required=True, description="Duração do vídeo"
                ),
                "timestamp": fields.Float(
                    required=True,
                    description="Hora em timestamp que o vídeo foi criado",
                ),
            },
        )
