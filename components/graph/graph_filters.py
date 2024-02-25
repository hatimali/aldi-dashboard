from dash import html, dcc
import dash_bootstrap_components as dbc


def get_graph_filters_2(df):
    # Add a DatePickerRange for selecting the date range
    date_picker_range = dcc.DatePickerRange(
        id='date-picker-range',
        min_date_allowed=df['Order Date'].min(),
        max_date_allowed=df['Order Date'].max(),
        start_date=df['Order Date'].min(),
        end_date=df['Order Date'].max(),
        display_format='MMM D, YYYY',
        className='date-picker-range custom-date-picker-range'
    )

    # Add a Dropdown for selecting granularity
    granularity_dropdown = dcc.Dropdown(
        id='granularity-dropdown',
        options=[
            {'label': 'Week', 'value': 'W'},
            {'label': 'Month', 'value': 'ME'},
            {'label': 'Quarter', 'value': 'Q'},
            {'label': 'Year', 'value': 'Y'}
        ],
        value='ME',  # Default to Month
        className='granularity-dropdown custom-granularity-dropdown'
    )

    color_category_dropdown = dcc.Dropdown(
    id='color-category-dropdown',
    options=[
        {'label': 'Segment', 'value': 'Segment'},
        {'label': 'Ship Mode', 'value': 'Delivery Mode'},
        {'label': 'Customer Name', 'value': 'Customer Name'},
        {'label': 'Category', 'value': 'Category'},
        {'label': 'Sub Category', 'value': 'Sub-Category'},
        {'label': 'Product Name', 'value': 'Product Name'},
    ],
    className='mb-2',
)


    return date_picker_range, granularity_dropdown, color_category_dropdown
