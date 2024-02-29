import pandas as pd

def preprocess_table_data(df):
    df['Order Date'] = pd.to_datetime(df['Order Date'])
    COLUMNS = ["Row ID", "Order ID", "Order Date", "Customer Name", "Product Name",
               "Segment", "Category", "Sub-Category", 
               "Country/Region", "State/Province", "City", "Profit"]
    
    df = df[[col for col in df.columns if col in COLUMNS]]
    return df