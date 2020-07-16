""" Module to store schemas """

INPUT_BODY = {
    "$schema": "http://json-schema.org/schema#",
    "type": "object",
    "properties": {
        "location": {
            "type": "object",
            "properties": {"lat": {"type": "number"},
                           "lng": {"type": "number"}},
            "required": ["lat", "lng"],
        },
        "person": {
            "type": "object",
            "properties": {
                "age": {"type": "integer"},
                "condutor": {"type": "boolean"},
                "gender": {"type": "string", "enum": ["M", "F"]},
            },
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
        },
    },
    "required": ["location", "person", "vec"],
}
