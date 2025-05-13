import pandas as pd


def load_data_into_df(file_location, fields):
    df = pd.read_csv(file_location, names=fields, header=None)
    import pdb; pdb.set_trace()
    print("hello!")
    return df



