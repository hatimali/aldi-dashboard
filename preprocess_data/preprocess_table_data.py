import pandas as pd

def preprocess_table_data(df):
    df['Order Date'] = pd.to_datetime(df['Order Date'])
    COLUMNS = ["Row ID", "Order ID", "Order Date", "Customer Name", 
           "Segment", "Category", "Sub-Category", "Product Name", 
           "Country/Region", "State/Province", "City", "Sale", "Profit", "Quantity"]

    df = df[[col for col in df.columns if col in COLUMNS]]
    return df