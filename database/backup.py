from datetime import datetime
import json
import os

from sqlalchemy import text
import pandas as pd
from fastavro import writer, parse_schema, reader

from database.connection import engine
from database.models import get_model_from_entity_name, Employee, Job, Department
from database.utils import generate_avro_schema_from_model
from migration.exceptions import (
    InvalidModelError,
    EmptyDataFrameError,
    DuplicateDataError,
    EmptyAvroFile,
    IncompatibleAvroFileError,
)
from migration.load import load_df_into_table
from migration.fields import get_fields

base_dir = os.path.dirname(os.path.abspath(__file__))
BACKUP_DIR = os.path.join(base_dir, "backups")


def backup(entity):
    model = get_model_from_entity_name(entity)
    if not model:
        raise InvalidModelError()
    schema_dict = generate_avro_schema_from_model(model)
    parsed_schema = parse_schema(schema_dict)

    with engine.connect() as conn:
        df = pd.read_sql(text(f"SELECT * FROM `{entity}`"), conn)

    if df.empty:
        print(f"No data found in table {entity}.")
        raise EmptyDataFrameError(
            "Schema name in Avro file differs from the entity name passed in the request"
        )

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
    with open(filename, "rb") as file:
        file_reader = reader(file)
        schema_name = file_reader.schema["name"]
        records = [record for record in file_reader]

    if not records:
        raise EmptyAvroFile()

    if entity != schema_name:
        import pdb

        pdb.set_trace()
        raise IncompatibleAvroFileError(
            "Name in Avro file's schema differs from the entity to be restored"
        )

    fields = get_fields(schema_name)
    df = pd.DataFrame(records)
    result, validation = load_df_into_table(df, schema_name, fields)
    if validation == "duplicates":
        raise DuplicateDataError(
            "Trying to insert records that already exist in destination table",
            result,
            schema_name,
        )
    elif validation == "OK":
        return result
