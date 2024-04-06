import pandas as pd
import os
global_df = None


def load_data():
    file_path = 'data\Sample - EU Superstore.xls'
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"No such file: {file_path}. Current directory: {os.getcwd()}")
    
    df =  pd.read_excel(file_path, sheet_name='Orders', engine='xlrd')
    return df


def load_data_for_graph():
    """
    Load the dataset into a Pandas DataFrame.

    Parameters:
    - filepath: str, path to the dataset file.

    Returns:
    - DataFrame containing the loaded dataset.
    """
    file_path = os.getcwd()+'\data\Sample - EU Superstore.xls'
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"No such file: {file_path}. Current directory: {os.getcwd()}")
    
    
    df =  pd.read_excel(file_path, sheet_name='Orders', engine='xlrd')
    df_returns = pd.read_excel(file_path, sheet_name='Returns', engine='xlrd')
    return df, df_returns