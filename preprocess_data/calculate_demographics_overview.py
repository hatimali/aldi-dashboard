def calculate_demographic_overview(df, selected_year):
    # Preprocess the data
    try:
        # current_year = int(selected_year[0])
        # df = df[(df['Year'] == current_year)]

        # customers calculations len(orders_data['Customer ID'].unique())
        customers_current_year = df['Customer ID'].nunique()

        # orders calculations
        orders_current_year = df['Order ID'].nunique()

        # products calculations
        products_current_year = df['Product ID'].nunique()

        # Calculate average sales per state
        average_sales_per_state = df.groupby('State/Province')['Sales'].mean().reset_index()

        # calculate average order value
        sales_current_year = df['Sales'].sum()
        total_orders_current_year = df['Order ID'].nunique()
        average_order_value_current_year = sales_current_year/total_orders_current_year


        # Average Sales per Order
        #This is calculated by summing all sales for each order and then taking the average of these sums.
        average_sales_per_order = df.groupby('Order ID')['Sales'].sum().mean()

        # Average Sales per Product
         #This is calculated by summing all sales for each product and then taking the average of these sums.
        average_sales_per_product = df.groupby('Product ID')['Sales'].sum().mean()
       
        # Average sales per state
        average_sales_per_state = df.groupby('State/Province')['Sales'].sum().mean()
        average_profit_per_state = df.groupby('State/Province')['Profit'].sum().mean()

        preprocessed_data = {
            'customers_current_year': customers_current_year,
            'orders_current_year': orders_current_year,
            'products_current_year': products_current_year,
            'average_sales_per_state': average_sales_per_state,
            'average_profit_per_state': average_profit_per_state,
        }

        print(f"Preprocessed data: {preprocessed_data}")
        return preprocessed_data
    except Exception as e:
        print(f"Error calculating sales overview: {e}")
