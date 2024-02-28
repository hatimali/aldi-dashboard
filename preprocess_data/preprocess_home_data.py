import pandas as pd

def preprocess_data(df):
    df['Order Date'] = pd.to_datetime(df['Order Date'])
    df['Year'] = df['Order Date'].dt.year
    df['Month'] = df['Order Date'].dt.strftime('%B')
    df['Sales'] = pd.to_numeric(df['Sales'])
    df['Profit'] = pd.to_numeric(df['Profit'])
    return df
