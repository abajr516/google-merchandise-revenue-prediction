import json
import pandas as pd
from pandas import json_normalize
import os

PROTECTED_COLUMNS = ['totals.transactionRevenue']

def load_df(csv_path, nrows=None):
    '''
    Source: https://www.kaggle.com/julian3833/1-quick-start-read-csv-and-flatten-json-fields/notebook
    '''
    
    JSON_COLUMNS = ['device', 'geoNetwork', 'totals', 'trafficSource']
    
    df = pd.read_csv(csv_path, 
                     converters={column: json.loads for column in JSON_COLUMNS}, 
                     dtype={'fullVisitorId': 'str'}, # Important!!
                     nrows=nrows)
    
    for column in JSON_COLUMNS:
        column_as_df = json_normalize(df[column])
        column_as_df.columns = [f"{column}.{subcolumn}" for subcolumn in column_as_df.columns]
        df = df.drop(column, axis=1).merge(column_as_df, right_index=True, left_index=True)
    print(f"Loaded {os.path.basename(csv_path)}. Shape: {df.shape}")
    return df


def get_missing_value_report(df):
    """
    Return a DataFrame of percent-missing per column, sorted
    descending. Used to decide the drop column threshold.
    """
    percent_missing = df.isnull().sum() * 100 / len(df)
    report = pd.DataFrame({
        "column_name": df.columns,
        "percent_missing": percent_missing.values,
    }).sort_values("percent_missing", ascending=False)
    return report.reset_index(drop=True)


def drop_high_missing_columns(df, threshold=80, protect=PROTECTED_COLUMNS):
    """
    Drop columns missing more than `threshold` percent of values,
    except columns in `protect` (e.g. the revenue target, where
    "missing" means $0, not unusable).
    """
    report = get_missing_value_report(df)
    to_drop = [
        row.column_name for row in report.itertuples()
        if row.percent_missing > threshold and row.column_name not in protect
    ]
    if to_drop:
        print(f"Dropping {len(to_drop)} columns (>{threshold}% missing): {to_drop}")
    return df.drop(columns=to_drop)













def clean_data_final(csv_path):
    '''
    Input: csv path
    Output: the cleaned dataset that automatically saves as a csv in data/processed
    THIS IS STILL A WIP
    '''
    df = load_df(csv_path)
    df = drop_high_missing_columns(df)
    
    
    
    
    
