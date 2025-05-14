import os
import pandas as pd


def load_data_into_df(file_name, fields):
    base_dir =  os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(base_dir, file_name)
    df = pd.read_csv(file_path, names=fields, header=None)
    return df
