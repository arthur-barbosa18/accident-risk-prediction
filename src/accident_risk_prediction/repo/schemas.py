""" Module to store schemas """

from accident_risk_prediction.repo.constants import (VEHICLE_TYPE,
                                                     CATEGORIES, GENDER)

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
                "gender": {"type": "string", "enum": GENDER},
            },
        },
        "vec": {
            "type": "object",
            "properties": {
                "vec_type": {
                    "type": "string",
                    "enum": VEHICLE_TYPE,
                },
                "category": {
                    "type": "string",
                    "enum": CATEGORIES,
                },
            },
        },
    },
    "required": ["location", "person", "vec"],
}
