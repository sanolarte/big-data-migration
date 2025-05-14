import sys
import os

import pandas as pd

from migration.fields import get_fields, get_mandatory_fields, get_foreign_keys
from migration.extract import load_data_into_df
from migration.transform import cleanse_data
from migration.exceptions import DuplicateDataError
from database.connection import engine, run_query, run_duplicate_precheck
from database.queries import build_insert_query


def load_data(file_location, entity):
    fields = get_fields(entity)
    mandatory_fields = get_mandatory_fields(entity)

    if not fields:
        return
    
    df = load_data_into_df(file_location, fields)
    
    cleansed_df = cleanse_data(df, fields, mandatory_fields)

    cleansed_df["imported_from"] = "file"

    # Load data into staging table
    cleansed_df.to_sql(
        name=f"stg_{entity}",
        con=engine,
        if_exists='replace',
        index=False
    )

    # Run a precheck for duplicate entity_ids
    duplicates = run_duplicate_precheck(entity, fields)

    if duplicates:
        formatted_duplicates = [record[0] for record in duplicates]
        raise DuplicateDataError("Trying to insert records that already exist in destination table", formatted_duplicates, entity)
    else:
        foreign_keys = get_foreign_keys(entity)
        # If there are no duplicates, insert data into actual table
        string_query = build_insert_query(entity, fields, foreign_keys)
        result = run_query(string_query)
        return result.rowcount
