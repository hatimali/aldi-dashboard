import pandas as pd

# def prepare_data(df, df_returns):
    
#     df['Order Date'] = pd.to_datetime(df['Order Date'])
#     df['Year'] = df['Order Date'].dt.year
#     df['Month'] = df['Order Date'].dt.strftime('%B')
    
#     # Calculate Days to Ship as the difference between Dispatch Date and Order Date
#     df['Days to Ship'] = (df['Dispatch Date'] - df['Order Date']).dt.days

#     # Calculate Profit Ratio as Profit divided by Sales
#     df['Profit Ratio'] = df['Profit'] / df['Sales']
    
#     return df


def prepare_data(df, df_returns):
    # Convert Order Date to datetime
    df['Order Date'] = pd.to_datetime(df['Order Date'])
    df['Year'] = df['Order Date'].dt.year
    df['Month'] = df['Order Date'].dt.strftime('%B')

    # Calculate Days to Ship as the difference between Dispatch Date and Order Date
    df['Dispatch Date'] = pd.to_datetime(df['Dispatch Date'])
    df['Days to Ship'] = (df['Dispatch Date'] - df['Order Date']).dt.days

    # Calculate Profit Ratio as Profit divided by Sales
    df['Profit Ratio'] = df['Profit'] / df['Sales']

    # Add a column for Returns based on whether the Order ID is in the df_returns dataframe
    df['Returns'] = df['Order ID'].isin(df_returns['Order ID']).astype(int)
    # df['Returns'] = df['Order ID'].isin(df_returns['Order ID']).replace({True: 1, False: 0})

    # Add Year and Month columns for filtering purposes
    df['Year'] = df['Order Date'].dt.year
    df['Month'] = df['Order Date'].dt.strftime('%B')
    
    return df
