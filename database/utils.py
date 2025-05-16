from sqlalchemy import Integer, String, Float, Boolean, DateTime, Date
import json


def sqlalchemy_to_avro_type(sqlalchemy_type):
    if isinstance(sqlalchemy_type, Integer):
        return "int"
    elif isinstance(sqlalchemy_type, String):
        return "string"
    elif isinstance(sqlalchemy_type, DateTime):
        return {"type": "long", "logicalType": "timestamp-millis"}
    else:
        return "string"  # Default


def generate_avro_schema_from_model(model):
    fields = []
    for column in model.__table__.columns:
        avro_type = sqlalchemy_to_avro_type(column.type)
        if column.nullable:
            avro_type = ["null", avro_type]
        fields.append({"name": column.name, "type": avro_type})

    schema = {
        "type": "record",
        "name": model.__name__,
        # "namespace": f"{model}.avro",
        "fields": fields,
    }
    return schema
