import pandas as pd

def preprocess_data(df):
    df['Order Date'] = pd.to_datetime(df['Order Date'])
    df['Year'] = df['Order Date'].dt.year
    df['Month'] = df['Order Date'].dt.strftime('%B')

    return df
