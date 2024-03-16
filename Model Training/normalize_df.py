import pandas as pd

def normalize_row(row):
    #Get the max value 
    row = (row - row.min()) / (row.max() - row.min())
    return row

def normalize_df(df):
    for index, row in df.iterrows():
        df.iloc[index] = normalize_row(row)
    return df