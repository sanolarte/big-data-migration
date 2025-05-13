import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pandas as pd

from fields import get_fields, get_mandatory_fields
from extract import load_data_into_df
from transform import cleanse_data
from database.connection import engine


def load_data(file_location, entity):
    fields = get_fields(entity)
    mandatory_fields = get_mandatory_fields(entity)

    if fields:
        df = load_data_into_df(file_location, fields)
        
        cleansed_df = cleanse_data(df, mandatory_fields)

        cleansed_df["imported_from"] = "file"

        
    cleansed_df.to_sql(
        name=entity,       # Target table name
        con=engine,
        if_exists='append',  # Options: 'fail', 'replace', 'append'
        index=False
    )



load_data("jobs.csv", "jobs")