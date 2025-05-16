import pandas as pd


def cleanse_data(df, fields, mandatory_fields):
    df.dropna(subset=mandatory_fields, inplace=True)
    df.drop_duplicates(inplace=True)
    df = format_dates(df, fields)
    return df


def format_dates(df, fields):
    date_fields = [field for field in fields if "date" in field]
    for field in date_fields:
        df[field] = pd.to_datetime(df[field], errors="coerce")
    return df
