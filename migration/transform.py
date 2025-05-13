def cleanse_data(df, mandatory_fields):
    df.dropna(subset=mandatory_fields, inplace=True)
    df.drop_duplicates(inplace=True)
    return df