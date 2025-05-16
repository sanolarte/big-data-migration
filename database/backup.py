from datetime import datetime
import json
import os

from sqlalchemy import text
import pandas as pd
from fastavro import writer, parse_schema

from connection import engine
from models import get_model_from_entity_name
from utils import generate_avro_schema_from_model

base_dir = os.path.dirname(os.path.abspath(__file__))
BACKUP_DIR = os.path.join(base_dir, "backups")


def backup(entity):
    model = get_model_from_entity_name(entity)
    if not model:
        return
    schema_dict = generate_avro_schema_from_model(model)
    parsed_schema = parse_schema(schema_dict)

    with engine.connect() as conn:
        df = pd.read_sql(text(f"SELECT * FROM `{entity}`"), conn)

    if df.empty:
        print(f"No data found in table {entity}.")
        return

    # Handle datetime fields
    datetime_cols = df.select_dtypes(include=["datetime64[ns]"]).columns
    for col in datetime_cols:
        df[col] = df[col].apply(
            lambda x: int(x.timestamp() * 1000) if pd.notnull(x) else None
        )
        df[col] = df[col].astype("Int64")  # Data type that supports None values

    rows = df.to_dict(orient="records")

    filename = f"{datetime.now().strftime('%Y%m%d%H%M%S')}_{entity}.avro"
    file_destination = os.path.join(BACKUP_DIR, filename)

    with open(file_destination, "wb") as out:
        writer(out, parsed_schema, rows)
    return file_destination


def restore(filename, entity):
    pass


backup("employees")
