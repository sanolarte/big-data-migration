import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pandas as pd

from fields import get_fields, get_mandatory_fields
from extract import load_data_into_df
from transform import cleanse_data
from database.connection import engine, run_query, run_duplicate_precheck
from database.queries import build_insert_query


def load_data(file_location, entity):
    fields = get_fields(entity)
    mandatory_fields = get_mandatory_fields(entity)

    if fields:
        df = load_data_into_df(file_location, fields)
        
        cleansed_df = cleanse_data(df, mandatory_fields)

        cleansed_df["imported_from"] = "file"

        
    cleansed_df.to_sql(
        name=f"stg_{entity}", # Load to staging table
        con=engine,
        if_exists='replace',
        index=False
    )

    # run a precheck for duplicate entity_ids
    duplicates = run_duplicate_precheck(entity, fields)

    if duplicates:
        print("There are duplicates!!")
    else:
        string_query = build_insert_query(entity, fields)
        run_query(string_query)


load_data("departments.csv", "departments")