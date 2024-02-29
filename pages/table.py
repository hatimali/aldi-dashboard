import os
import dash
from dash import html, dcc, dash_table, callback, Input, Output, State
import numpy as np
# from dash.dependencies import Input, Output, State
import pandas as pd
import dash_bootstrap_components as dbc
from datetime import datetime as dt
from components.table.table_layout import generate_unique_options_for_dropdowns

# Assuming 'df' is your DataFrame and already loaded
from data.data_loader import load_data
from preprocess_data.preprocess_table_data import preprocess_table_data


PAGE_SIZE = 25
COLUMNS = ["Row ID", "Order ID", "Order Date", "Customer Name", "Product Name",
           "Segment", "Category", "Sub-Category", 
           "Country/Region", "State/Province", "City", "Profit"]


# df = get_dataframe()

# df = load_data()
if 'df' not in globals():
    print("Global found!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    global df
    df = load_data()  # Function to load the original data
    


df = preprocess_table_data(df)

# Register this file as a Dash page
dash.register_page(__name__)

# input_fields = get_table_input_fields(df)

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
        columns=[{"name": i, "id": i, "deletable": False, "selectable": True} for i in COLUMNS],
        # columns=[
        #     {"name": i, "id": i} for i in df.columns if i in ["Row ID", "Order ID", "Order Date", "Customer Name", "Segment", "Category", "Sub-Category", "Product Name", "Country/Region", "State/Province", "City", "Sale", "Profit", "Quantity"]
        # ],
        data=df.to_dict('records'),
        editable=True, # Make the table editable
        row_deletable=False, # Allow rows to be deleted
        page_size=PAGE_SIZE,
        filter_action="native",
        sort_action="native",
        sort_mode='multi',
        style_table={'maxHeight': '600px', 'overflowY': 'auto'},
        style_cell={
            'minWidth': '150px', 'width': '150px', 'maxWidth': '150px',
            'overflow': 'hidden',
            'textOverflow': 'ellipsis',
            'padding': '10px'
        },
        style_header={
            'backgroundColor': 'rgb(230, 230, 230)',
            'fontWeight': 'bold',
            'border': '1px solid black'
        },
        style_data_conditional=[
            {'if': {'row_index': 'odd'}, 'backgroundColor': 'rgb(248, 248, 248)'}
        ],
    ),
    dbc.Row([
        dbc.Col(dcc.Input(id='input-row-id', type='number', placeholder='Row ID', className='form-control')),
        dbc.Col(dcc.Input(id='input-order-id', type='text', placeholder='Order ID', className='form-control')),
        dbc.Col(dcc.DatePickerSingle(id='input-order-date', placeholder='Order Date', className='form-control-datepicker')),
        dbc.Col(dcc.Input(id='input-customer-name', type='text', placeholder='Customer Name', className='form-control')),
        dbc.Col(dcc.Input(id='input-product-name', type='text', placeholder='Product Name', className='form-control')),
        dbc.Col(dcc.Input(id='input-segment', type='text', placeholder='Segment', className='form-control')),
        dbc.Col(dcc.Input(id='input-category', type='text', placeholder='Category', className='form-control')),
        dbc.Col(dcc.Input(id='input-sub-category', type='text', placeholder='Sub-Category', className='form-control')),
        dbc.Col(dcc.Input(id='input-country-region', type='text', placeholder='Country/Region', className='form-control')),
        dbc.Col(dcc.Input(id='input-state-province', type='number', placeholder='State/Province', className='form-control')),
        dbc.Col(dcc.Input(id='input-city', type='text', placeholder='City', className='form-control')),
        # dbc.Col(dcc.Input(id='input-sale', type='text', placeholder='Sale', className='form-control')),
        dbc.Col(dcc.Input(id='input-profit', type='text', placeholder='Profit', className='form-control')),
        # dbc.Col(dcc.Input(id='input-quantity', type='text', placeholder='Quantity', className='form-control')),
    ], className="mb-3"),
    dbc.Button('Add Row', id='add-row-button', n_clicks=0, color="primary", className="me-1", size="lg"),

    html.Div(id='add-row-response', role='alert', style={'margin-top': '20px'})
])


@callback(
    Output('category-dropdown', 'options'),
    Output('category-dropdown', 'value'),
    Input('segment-dropdown', 'value')
)
def set_category_options(selected_segment):
    if selected_segment:
        filtered_df = df[df['Segment'] == selected_segment]
        category_options =  [{'label': i, 'value': i} for i in filtered_df['Category'].unique()]
        return category_options, None
    else:
        return [], None


@callback(
    Output('sub-category-dropdown', 'options'),
    Output('sub-category-dropdown', 'value'),
    [Input('category-dropdown', 'value'),
     State('segment-dropdown', 'value')]
)
def set_sub_category_options(selected_category, selected_segment):
    if selected_segment and selected_category:
        filtered_df = df[(df['Segment'] == selected_segment) & (df['Category'] == selected_category)]
        sub_category_options = [{'label': i, 'value': i} for i in filtered_df['Sub-Category'].unique()]
        return sub_category_options, None
    else:
        return [], None


@callback(
    Output('state-dropdown', 'options'),
    Output('state-dropdown', 'value'),
    Input('country-dropdown', 'value')
)
def set_state_options(selected_country):
    if selected_country:
        filtered_df = df[df['Country/Region'] == selected_country]
        state_options = [{'label': i, 'value': i} for i in filtered_df['State/Province'].unique()]
        return state_options, None
    else:
        return [], None


@callback(
    Output('city-dropdown', 'options'),
    Output('city-dropdown', 'value'),
    Input('state-dropdown', 'value')
)
def set_city_options(selected_state):
    if selected_state:
        filtered_df = df[df['State/Province'] == selected_state]
        city_options =  [{'label': i, 'value': i} for i in filtered_df['City'].unique()]
        return city_options, None
    else:
        return [], None

@callback(
    [Output('datatable', 'data'), Output('datatable', 'page_size'), Output('add-row-response', 'children')],
    [Input('sub-category-dropdown', 'value'), Input('segment-dropdown', 'value'), 
     Input('category-dropdown', 'value'), Input('country-dropdown', 'value'), 
     Input('state-dropdown', 'value'), Input('city-dropdown', 'value'), 
     Input('row-dropdown', 'value'), Input('date-picker-range', 'start_date'), 
     Input('date-picker-range', 'end_date'), Input('add-row-button', 'n_clicks')],
    [State('datatable', 'data'), State('input-row-id', 'value'), 
     State('input-order-id', 'value'), State('input-order-date', 'value'), 
     State('input-customer-name', 'value'), State('input-product-name', 'value'),
     State('input-segment', 'value'), State('input-category', 'value'), 
     State('input-sub-category', 'value'), State('input-country-region', 'value'), 
     State('input-state-province', 'value'), State('input-city', 'value'), 
     State('input-profit', 'value')]
)
def update_table_content(selected_sub_category, selected_segment, selected_category, selected_country, 
                         selected_state, selected_city, selected_size, start_date, end_date, n_clicks, rows,
                         input_row_id, input_order_id, input_order_date, input_customer_name, input_product_name, 
                         input_segment, input_category, input_sub_category, input_country_region, 
                         input_state_province, input_city, input_profit):
    
    ctx = dash.callback_context
    if ctx.triggered:
        trigger_id = ctx.triggered[0]['prop_id'].split('.')[0]

        if trigger_id == 'add-row-button' and n_clicks > 0:
            # Validate inputs
            print("Validating Input")
            if not all([input_row_id, input_order_id, input_customer_name, input_product_name]):
                return df.to_dict('records'), selected_size, dbc.Alert("Error adding row. The required fields include Row ID, Order ID, Order Date, Customer Name, Product Name.", color="info", is_open=True, 
                       style={"width": "100%", "text-align": "center", "fontSize": "20px"})
            

            row_ids = [item['Row ID'] for item in rows]
            # Check for duplicate Row ID
            if input_row_id in row_ids:
                return df.to_dict('records'), selected_size, dbc.Alert("Error duplicate ID. Please add unique ID.", color="danger", is_open=True, 
                       style={"width": "100%", "text-align": "center", "fontSize": "20px"})
            

            # Create the new row dictionary
            new_row = {
                'Row ID': input_row_id,
                'Order ID': input_order_id,
                'Order Date': pd.to_datetime(input_order_date) if input_order_date else np.nan,
                'Customer Name': input_customer_name,
                'Product Name': input_product_name,
                'Segment': input_segment,
                'Category': input_category,
                'Sub-Category': input_sub_category,
                'Country/Region': input_country_region,
                'State/Province': input_state_province,
                'City': input_city,
                # 'Sale': input_sale,
                'Profit': input_profit,
                # 'Quantity': input_quantity
            }

            df.loc[len(df)] = new_row
            rows.append(new_row)

            # Save to Excel
            file_name = os.getcwd()+'\data\Table - EU Superstore.xlsx'
            df_test = pd.DataFrame(rows, columns=COLUMNS)  
            # df_test.to_excel('TEST.xls')
            with pd.ExcelWriter(file_name) as writer:
                df_test.to_excel(writer, sheet_name='Orders', index=False)

            print("save it to file")
            # Update response
            return df.to_dict('records'), selected_size, dbc.Alert(
                "Row Added Successfully!", 
                color="success", 
                is_open=True, 
                style={"width": "100%", "text-align": "center", "fontSize": "20px"})

    filtered_df = df.copy()
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
    

    return filtered_df.to_dict('records'), selected_size, ''
