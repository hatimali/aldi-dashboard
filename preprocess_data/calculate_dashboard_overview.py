
def calculate_sales_overview(df, selected_year):
    # Preprocess the data
    try:
        current_year = int(selected_year[0])
        previous_year = current_year - 1

        df_current_year = df[(df['Year'] == current_year)]

        # Sales calculations
        sales_current_year = df_current_year['Sales'].sum()
        sales_previous_year = df[(df['Year'] == previous_year)]['Sales'].sum()
        #sales_percentage_increase = ((sales_current_year - sales_previous_year) / sales_previous_year) * 100 if sales_previous_year != 0 else float('nan')

        average_sales_per_unit = df_current_year['Sales'].sum() / df_current_year['Quantity'].sum()

        # calculate YOY growth with pct_change()
        annual_sales = df.groupby('Year')['Sales'].sum().reset_index()
        annual_sales['YoY Growth'] = (annual_sales['Sales'].pct_change()) * 100
        yoy_growth_current_year = annual_sales[annual_sales['Year'] == current_year]['YoY Growth']
        print(f"Year on Year growth: {yoy_growth_current_year}")
        
        preprocessed_data = {
            'sales_current_year': sales_current_year,
            'sales_previous_year': sales_previous_year,
            'average_sales_per_unit': average_sales_per_unit,
            'yoy_growth_current_year': yoy_growth_current_year,
        }

        return preprocessed_data
    except Exception as e:
        print(f"Error calculating sales overview: {e}")


def calculate_profit_overview(df, selected_year):
    # Preprocess the data
    try:
        current_year = int(selected_year[0])
        previous_year = selected_year[0] - 1

        # Profit calculations
        profit_current_year = df[df['Year'] == current_year]['Profit'].sum()
        profit_previous_year = df[df['Year'] == previous_year]['Profit'].sum()
        #profit_percentage_increase = ((profit_current_year - profit_previous_year) / profit_previous_year) * 100 if profit_previous_year != 0 else float('nan')

        # Total customers calculations
        # Assuming 'Customer ID' uniquely identifies customers
        # customers_current_year = df[df['Year'] == current_year]['Customer ID'].nunique()
        # customers_previous_year = df[df['Year'] == previous_year]['Customer ID'].nunique()
        # customers_percentage_increase = ((customers_current_year - customers_previous_year) / customers_previous_year) * 100 if customers_previous_year != 0 else float('nan')

        average_profit_per_unit = df[(df['Year'] == current_year)]['Profit'].sum() / df[(df['Year'] == current_year)]['Quantity'].sum()
        annual_profit = df.groupby('Year')['Profit'].sum().reset_index()
        annual_profit['YoY Growth'] = (annual_profit['Profit'].pct_change()) * 100
        yoy_growth_current_year = annual_profit[annual_profit['Year'] == current_year]['YoY Growth']

        preprocessed_data = {
            'profit_current_year': profit_current_year,
            'profit_previous_year': profit_previous_year,
            'average_profit_per_unit': average_profit_per_unit,
            'yoy_growth_current_year': yoy_growth_current_year,
        }
        
        return preprocessed_data
    except Exception as e:
        print(f"Error calculating profit overview: {e}")

def calculate_monthly_sales(df, selected_years):
    # Calculate monthly sales for current and previous years
    current_year = int(selected_years[0])
    previous_year = current_year - 1

    # Group by year and month
    monthly_sales = df.groupby(['Year', 'Month'])['Sales'].sum().unstack('Year')
    
    # Check if the previous year exists in the DataFrame
    if previous_year not in monthly_sales.columns:
        # If not, create a column for the previous year with zeros
        monthly_sales[previous_year] = 0


    monthly_sales = monthly_sales[[previous_year, current_year]]
    monthly_sales = monthly_sales.reindex(columns=sorted(monthly_sales.columns))

    return monthly_sales



def calculate_top_product_with_sales(df, selected_years):

    df = df[df['Order Date'].dt.year == int(selected_years[0])]
    top_products = df.groupby('Product Name')['Sales'].sum().nlargest(5).reset_index()
    # Calculate the total sales to find percentages.
    total_sales = top_products['Sales'].sum()

    # Add a new column for sales percentages.
    top_products['Sales Percent'] = (top_products['Sales'] / total_sales) * 100
    return top_products



def calculate_monthly_profit(df, selected_years):
    # Calculate monthly sales for current and previous years
    current_year = int(selected_years[0])
    previous_year = current_year - 1

    # Group by year and month
    monthly_profit = df.groupby(['Year', 'Month'])['Profit'].sum().unstack('Year')
    
    # Check if the previous year exists in the DataFrame
    if previous_year not in monthly_profit.columns:
        # If not, create a column for the previous year with zeros
        monthly_profit[previous_year] = 0

    monthly_profit = monthly_profit[[previous_year, current_year]]
    monthly_profit = monthly_profit.reindex(columns=sorted(monthly_profit.columns))

    return monthly_profit



def calculate_top_products_by_profit(df, selected_years):

    df = df[df['Order Date'].dt.year == int(selected_years[0])]
    top_products = df.groupby('Product Name')['Profit'].sum().nlargest(5).reset_index()
    # Calculate the total sales to find percentages.
    total_profit = top_products['Profit'].sum()

    # Add a new column for sales percentages.
    top_products['Profit Percent'] = (top_products['Profit'] / total_profit) * 100
    return top_products