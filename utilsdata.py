import pandas as pd
import numpy as np

def find_rows(df, col_name, val_l):
    '''fast method for finding rows in a dataframe whose values for a given column is in a given 
    list. Based on this:
    https://stackoverflow.com/a/31296878 '''
    mask = np.in1d(df[col_name].values, val_l) #vs code says to use isin, not is1d, for new code
    return df[mask]

def val_from_row(row_df, col_name_s):
    return row_df[col_name_s].values[0]

def moving_average(npa, w):
    return np.convolve(npa, np.ones(w), 'valid') / w
