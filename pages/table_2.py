import dash
from dash.exceptions import PreventUpdate
from dash import html, dcc, dash_table, callback, Input, Output, State
# from dash.dependencies import Input, Output, State
import pandas as pd
import dash_bootstrap_components as dbc
from datetime import datetime as dt
from components.table.table_layout import generate_unique_options_for_dropdowns, get_table_input_fields

# Assuming 'df' is your DataFrame and already loaded
from data.data_loader import load_data
from preprocess_data.preprocess_table_data import preprocess_table_data

global original_df

PAGE_SIZE = 25
COLUMNS = ["Row ID", "Order ID", "Order Date", "Customer Name", 
           "Segment", "Category", "Sub-Category", "Product Name", 
           "Country/Region", "State/Province", "City", "Sale", "Profit", "Quantity"]

original_df = load_data()

df = preprocess_table_data(original_df)

# df.loc[len(df)] = [None] * len(df.columns) 
# Register this file as a Dash page
dash.register_page(__name__)

input_fields = get_table_input_fields(df)

dropdown_options = generate_unique_options_for_dropdowns(df)

layout = html.Div([
    dbc.Row([
        dbc.Col(
            dcc.Dropdown(
                id='segment-dropdown',
                options=dropdown_options['segment_options'],
                value=None,
                placeholder="Select a Segment",
                className='mb-3'
            ), width={"size": 4}
        ),
        dbc.Col(
            dcc.Dropdown(
                id='category-dropdown',
                placeholder="Select a Category",
                className='mb-3'
            ), width={"size": 4}
        ),
        dbc.Col(
            dcc.Dropdown(
                id='sub-category-dropdown',
                placeholder="Select a Sub Category",
                className='mb-3'
            ), width={"size": 4}
        ),
    ]),
    dbc.Row([
        dbc.Col(
            dcc.Dropdown(
                id='country-dropdown',
                options=dropdown_options['country_options'],
                value=None,
                placeholder="Select a Country",
                className='mb-3'
            ), 
            width=4
        ),
        dbc.Col(
            dcc.Dropdown(
                id='state-dropdown',
                placeholder="Select a State",
                className='mb-3'
            ), 
            width=4
        ),
        dbc.Col(
            dcc.Dropdown(
                id='city-dropdown',
                placeholder="Select a City",
                className='mb-3'
            ), 
            width=4
        ),
    ]),
    dbc.Row([
        dbc.Col(
            dcc.DatePickerRange(
                id='date-picker-range',
                min_date_allowed=df['Order Date'].min(),
                max_date_allowed=df['Order Date'].max(),
                start_date=dt(2022, 1, 1),  # Default or dynamically set based on your data
                end_date=dt(2022, 12, 31),
                className='mb-3',
            ),
        ),
    ]),
    dbc.Row([
        dbc.Col(
            dcc.Dropdown(
                id='row-dropdown',
                options=[
                    {'label': '5 rows', 'value': 5},
                    {'label': '10 rows', 'value': 10},
                    {'label': '25 rows', 'value': 25},
                    {'label': '50 rows', 'value': 50},
                ],
                value=PAGE_SIZE,  # Default value
                className='mb-3',
                style={'width':'35%'},
            ),
        ),
    ]),
    dash_table.DataTable(
        id='datatable',
        columns=[{"name": i, "id": i, "deletable": True, "selectable": True} for i in df.columns],
        # columns=[
        #     {"name": i, "id": i} for i in df.columns if i in ["Row ID", "Order ID", "Order Date", "Customer Name", "Segment", "Category", "Sub-Category", "Product Name", "Country/Region", "State/Province", "City", "Sale", "Profit", "Quantity"]
        # ],
        data=df.to_dict('records'),
        editable=True, # Make the table editable
        row_deletable=True, # Allow rows to be deleted
        page_size=PAGE_SIZE,
        filter_action="native",
        sort_action="native",
    ),
    dbc.Row([
        dbc.Col(dcc.Input(id='input-row-id', type='number', placeholder='Row ID', className='form-control'), width=1),
        dbc.Col(dcc.Input(id='input-order-id', type='text', placeholder='Order ID', className='form-control'), width=1),
        dbc.Col(dcc.DatePickerSingle(id='input-order-date', placeholder='Order Date', className='form-control'), width=1),
        dbc.Col(dcc.Input(id='input-customer-name', type='text', placeholder='Customer Name', className='form-control'), width=1),
        dbc.Col(dcc.Input(id='input-segment', type='text', placeholder='Segment', className='form-control'), width=1),
        dbc.Col(dcc.Input(id='input-category', type='text', placeholder='Category', className='form-control'), width=1),
        dbc.Col(dcc.Input(id='input-sub-category', type='text', placeholder='Sub-Category', className='form-control'), width=1),
        dbc.Col(dcc.Input(id='input-product-name', type='text', placeholder='Product Name', className='form-control'), width=1),
        dbc.Col(dcc.Input(id='input-country-region', type='text', placeholder='Country/Region', className='form-control'), width=1),
        dbc.Col(dcc.Input(id='input-state-province', type='number', placeholder='State/Province', className='form-control'), width=1),
        dbc.Col(dcc.Input(id='input-city', type='text', placeholder='City', className='form-control'), width=1),
        dbc.Col(dcc.Input(id='input-sale', type='text', placeholder='Sale', className='form-control'), width=1),
        dbc.Col(dcc.Input(id='input-profit', type='text', placeholder='Profit', className='form-control'), width=1),
        dbc.Col(dcc.Input(id='input-quantity', type='text', placeholder='Quantity', className='form-control'), width=1),
    ], className="mb-3"),
    html.Button('Add Row', id='add-row-button', n_clicks=0),
    html.Div(id='add-row-response'), # for adding response
    # dbc.Alert(id='add-row-alert', dismissable=True, is_open=False),
])


# callback(
#     Output('datatable', 'data'),
#     Input('add-row-button', 'n_clicks'),
#     State('datatable', 'data')
# )
# def add_empty_row(n_clicks, rows):
#     if n_clicks > 0:
#         new_row = {col_id: "" for col_id in df.columns}  # Create an empty row
#         rows.append(new_row)  # Append it to the existing data
#     return rows



@callback(
    Output('category-dropdown', 'options'),
    Input('segment-dropdown', 'value')
)
def set_category_options(selected_segment):
    if selected_segment:
        filtered_df = df[df['Segment'] == selected_segment]
        return [{'label': i, 'value': i} for i in filtered_df['Category'].unique()]
    else:
        return []


@callback(
    Output('sub-category-dropdown', 'options'),
    [Input('category-dropdown', 'value'),
     State('segment-dropdown', 'value')]
)
def set_sub_category_options(selected_category, selected_segment):
    if selected_segment and selected_category:
        filtered_df = df[(df['Segment'] == selected_segment) & (df['Category'] == selected_category)]
        return [{'label': i, 'value': i} for i in filtered_df['Sub-Category'].unique()]
    else:
        return []


@callback(
    Output('state-dropdown', 'options'),
    Input('country-dropdown', 'value')
)
def set_state_options(selected_country):
    if selected_country:
        filtered_df = df[df['Country/Region'] == selected_country]
        return [{'label': i, 'value': i} for i in filtered_df['State/Province'].unique()]
    else:
        return []


@callback(
    Output('city-dropdown', 'options'),
    Input('state-dropdown', 'value')
)
def set_city_options(selected_state):
    if selected_state:
        filtered_df = df[df['State/Province'] == selected_state]
        return [{'label': i, 'value': i} for i in filtered_df['City'].unique()]
    else:
        return []

@callback(
    [Output('datatable', 'data'), Output('datatable', 'page_size'), Output('add-row-response', 'children')],
    [Input('sub-category-dropdown', 'value'), Input('segment-dropdown', 'value'), 
     Input('category-dropdown', 'value'), Input('country-dropdown', 'value'), 
     Input('state-dropdown', 'value'), Input('city-dropdown', 'value'), 
     Input('row-dropdown', 'value'), Input('date-picker-range', 'start_date'), 
     Input('date-picker-range', 'end_date'), Input('add-row-button', 'n_clicks')],
    [State('datatable', 'data'), State('input-row-id', 'value'), 
     State('input-order-id', 'value'), State('input-order-date', 'value'), 
     State('input-customer-name', 'value'), State('input-segment', 'value'), 
     State('input-category', 'value'), State('input-sub-category', 'value'), 
     State('input-product-name', 'value'), State('input-country-region', 'value'), 
     State('input-state-province', 'value'), State('input-city', 'value'), 
     State('input-sale', 'value'), State('input-profit', 'value'), 
     State('input-quantity', 'value')]
)
def update_table_content(selected_sub_category, selected_segment, selected_category, selected_country, 
                         selected_state, selected_city, selected_size, start_date, end_date, n_clicks, rows,
                         input_row_id, input_order_id, input_order_date, input_customer_name, input_segment, 
                         input_category, input_sub_category, input_product_name, input_country_region, 
                         input_state_province, input_city, input_sale, input_profit, input_quantity):
    
    ctx = dash.callback_context
    filtered_df = df
    if ctx.triggered:
        trigger_id = ctx.triggered[0]['prop_id'].split('.')[0]
        print("First logic for filteres")
        if trigger_id == 'add-row-button':
            print("Add button clicked!!!!")
            # Handle add row logic
            if n_clicks > 0:
                print("Add button clicked again!!!!")
                print(f"ROW IDS: {rows}")
                # Check if the Row ID already exists
                existing_ids = {row['Row ID'] for row in rows}
                print(existing_ids)

                print(f"Input Row ID: {input_row_id}")
                if input_row_id in existing_ids:
                    print("This Row ID already being used, please try again!")
                    return rows, selected_size, "Error: This Row ID already being used, please try again!"

                # Create the new row dictionary
                new_row = {
                    'Row ID': input_row_id,
                    'Order ID': input_order_id,
                    'Order Date': input_order_date,
                    'Customer Name': input_customer_name,
                    'Segment': input_segment,
                    'Category': input_category,
                    'Sub-Category': input_sub_category,
                    'Product Name': input_product_name,
                    'Country/Region': input_country_region,
                    'State/Province': input_state_province,
                    'City': input_city,
                    'Sale': input_sale,
                    'Profit': input_profit,
                    'Quantity': input_quantity
                }

                # Append the new row to the existing rows
                rows.append(new_row)

                # Save updated DataFrame to CSV (Optional)
                pd.DataFrame(rows).to_excel('updated_superstore_data.csv', index=False)
                print("save it to file")

    # Handle case where no inputs have been triggered
    if start_date and end_date:
        filtered_df = filtered_df[
            (filtered_df['Order Date'] >= pd.to_datetime(start_date)) & 
            (filtered_df['Order Date'] <= pd.to_datetime(end_date))
        ]
    if selected_segment:
        filtered_df = filtered_df[filtered_df['Segment'] == selected_segment]
    if selected_category:
        filtered_df = filtered_df[filtered_df['Category'] == selected_category]
    if selected_sub_category:
        filtered_df = filtered_df[filtered_df['Sub-Category'] == selected_sub_category]
    if selected_country:
        filtered_df = filtered_df[filtered_df['Country/Region'] == selected_country]
    if selected_state:
        filtered_df = filtered_df[filtered_df['State/Province'] == selected_state]
    if selected_city:
        filtered_df = filtered_df[filtered_df['City'] == selected_city]
    


    return filtered_df.to_dict('records'), selected_size, "Success!"
