from dash import html, dcc

def get_table_input_fields(df):
    # Define input fields for the properties you want to be able to add

    input_fields = html.Div([
        dcc.Input(id='input-row-id', type='number', placeholder='Row ID'),
        dcc.Input(id='input-order-id', type='text', placeholder='Order ID'),
        dcc.Input(id='input-order-date', type='text', placeholder='Order Date'),
        dcc.Input(id='input-customer-name', type='text', placeholder='Customer Name'),
        dcc.Input(id='input-segment', type='text', placeholder='Segment'),
        dcc.Input(id='input-category', type='text', placeholder='Category'),
        dcc.Input(id='input-sub-category', type='text', placeholder='Sub-Category'),
        dcc.Input(id='input-product-name', type='text', placeholder='Product Name'),
        dcc.Input(id='input-country-region', type='text', placeholder='Country/Region'),
        dcc.Input(id='input-state-province', type='number', placeholder='State/Province'),
        dcc.Input(id='input-city', type='text', placeholder='City'),
        dcc.Input(id='input-sale', type='text', placeholder='Sale'),
        dcc.Input(id='input-profit', type='text', placeholder='Profit'),
        dcc.Input(id='input-quantity', type='text', placeholder='Quantity'),
        html.Button('Add Row', id='add-row-button', n_clicks=0),
    ], style={'height': 50})

    return input_fields

def generate_unique_options_for_dropdowns(df):
    country_options = [{'label': country, 'value': country} for country in df['Country/Region'].unique()]
    segment_options = [{'label': segment, 'value': segment} for segment in df['Segment'].unique()]
    
    dropdown_options = {
        'country_options': country_options,
        'segment_options': segment_options,

    }
    return dropdown_options