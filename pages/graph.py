import dash
from dash import dcc, html, Input, Output, callback, State
import pandas as pd
import plotly.express as px
from components.graph.graph_filters import get_graph_filters_2
import dash_bootstrap_components as dbc
from data.data_loader import load_data, load_data_for_graph
from preprocess_data.preprocess_graph_data import prepare_data
from dash.exceptions import PreventUpdate

df, df_returns = load_data_for_graph()
df = prepare_data(df, df_returns)

date_picker_range, granularity_dropdown, color_category_dropdown  = get_graph_filters_2(df)

# Register this file as a Dash page
dash.register_page(__name__)


# Define the layout for the Graph page
layout = html.Div([
    dbc.Container([
        dbc.Row([
            dbc.Col(width=1),
            dbc.Col(html.Div([
                html.Label("Select Date Range", className='filter-label'),
                date_picker_range
            ]), width=5),
            dbc.Col(html.Div([
                html.Label("Granularity", className='filter-label'),
                granularity_dropdown
            ]), width=5),
            dbc.Col(width=1),
        ],  className='filter-bar'),
        dbc.Row([
            dbc.Col(width=1),
            dbc.Col(html.Div([
                html.Label("Select Metric", className='filter-label'),
                dcc.Dropdown(
                    id='metric-dropdown',
                    clearable=False,
                    options=[
                        {'label': 'Days to Ship', 'value': 'Days to Ship'},
                        {'label': 'Discount', 'value': 'Discount'},
                        {'label': 'Profit', 'value': 'Profit'},
                        {'label': 'Profit Ratio', 'value': 'Profit Ratio'},
                        {'label': 'Quantity', 'value': 'Quantity'},
                        {'label': 'Returns', 'value': 'Returns'},
                        {'label': 'Sales', 'value': 'Sales'},
                    ],
                    value='Sales'  # Default value
                ),
            ]), md=3),
            dbc.Col(width=3),
            dbc.Col(html.Div([
                html.Label("Select X Axis", className='filter-label'),
                dcc.Dropdown(
                    id='xaxis-dropdown',
                    options=[{'label': prop, 'value': prop} for prop in df.columns if prop in ['Days to Ship', 'Discount', 'Profit', 'Profit Ratio', 'Quantity', 'Returns', 'Sales']],
                    value='Profit',  # Default value
                ),
            ]), md=3),
        ]),
        dbc.Row([
            dbc.Col(html.Div([
            ]), md=3),
            dbc.Col(width=4),
            dbc.Col(html.Div([
                html.Label("Select Y Axis", className='filter-label'),
                dcc.Dropdown(
                    id='yaxis-dropdown',
                    options=[{'label': prop, 'value': prop} for prop in df.columns if prop in ['Days to Ship', 'Discount', 'Profit', 'Profit Ratio', 'Quantity', 'Returns', 'Sales']],
                    value='Sales',  # Default value
                ),
            ]), md=3),
        ]),
        dbc.Row([
            dbc.Col(html.Div([
            ]), md=3),
            dbc.Col(width=4),
            dbc.Col(html.Div([
                html.Label("Select Category", className='filter-label'),
                color_category_dropdown
            ]), md=3),
        ]),
        dbc.Row([
            dbc.Col(html.Div([
                dcc.Graph(id='timeline-graph', style={'height': '650px'})
            ]), md=6),
            dbc.Col(html.Div([
                dcc.Graph(id='bubble-chart', style={'height': '650px'})
            ]), md=6),
        ], align="start"),  # This ensures that the row starts from the same point
    ], fluid=True)
])


# Callback for updating Bubble Chart and Dropdowns
@callback(
    [Output('bubble-chart', 'figure'),
     Output('xaxis-dropdown', 'options'),
     Output('yaxis-dropdown', 'options')],
    [Input('date-picker-range', 'start_date'), 
     Input('date-picker-range', 'end_date'),
     Input('granularity-dropdown', 'value'),
     Input('xaxis-dropdown', 'value'),
     Input('yaxis-dropdown', 'value'),
     Input('color-category-dropdown', 'value')],
    [State('xaxis-dropdown', 'options'),
     State('yaxis-dropdown', 'options')]
)
def update_bubble_chart(start_date, end_date, granularity, xaxis_prop, yaxis_prop, color_prop, xaxis_options, yaxis_options):
    
    print(f"Start date: {start_date}")
    print(f"End date: {end_date}")
    filtered_df = df.loc[(df['Order Date'] >= pd.to_datetime(start_date)) & (df['Order Date'] <= pd.to_datetime(end_date))]

    if granularity == 'ME':
        filtered_df['Order Date'] = filtered_df['Order Date'].dt.strftime('%Y-%m')
    elif granularity == 'W':
        filtered_df['Order Date'] = filtered_df['Order Date'].dt.strftime('%Y-%U')
    elif granularity == 'Q':
        filtered_df['Order Date'] = filtered_df['Order Date'].dt.to_period('Q').astype(str)
    elif granularity == 'Y':
        filtered_df['Order Date'] = filtered_df['Order Date'].dt.to_period('Y').astype(str)

    if color_prop:
        grouped_df = filtered_df.groupby('Order Date').agg({
            xaxis_prop: 'sum',
            yaxis_prop: 'sum',
            color_prop: 'first'  # or any other logic to assign a segment to the bin
        }).reset_index()
    else:
        grouped_df = filtered_df.groupby('Order Date').agg({
            xaxis_prop: 'sum',
            yaxis_prop: 'sum'
        }).reset_index()

    all_options = [
        {'label': 'Days to Ship', 'value': 'Days to Ship'},
        {'label': 'Discount', 'value': 'Discount'},
        {'label': 'Profit', 'value': 'Profit'},
        {'label': 'Profit Ratio', 'value': 'Profit Ratio'},
        {'label': 'Quantity', 'value': 'Quantity'},
        {'label': 'Returns', 'value': 'Returns'},
        {'label': 'Sales', 'value': 'Sales'}
    ]
    
    xaxis_options = [option for option in all_options if option['value'] != yaxis_prop]
    yaxis_options = [option for option in all_options if option['value'] != xaxis_prop]

    scatter_kwargs = {
        'x': xaxis_prop,
        'y': yaxis_prop,
        'hover_name': 'Order Date',
        'title': f'{xaxis_prop} vs {yaxis_prop}',
        'labels': {xaxis_prop: xaxis_prop, yaxis_prop: yaxis_prop},
    }

    if color_prop:
        scatter_kwargs['color'] = color_prop

    fig = px.scatter(grouped_df, **scatter_kwargs)
    fig.update_layout(transition_duration=500, template='plotly_white')

    return fig, xaxis_options, yaxis_options



@callback(
    Output('timeline-graph', 'figure'),
    [Input('date-picker-range', 'start_date'), 
     Input('date-picker-range', 'end_date'),
     Input('granularity-dropdown', 'value'),
     Input('metric-dropdown', 'value')]
)
def update_graph(start_date, end_date, granularity, selected_metric):

    print(f"Start date: {start_date}")
    print(f"End date: {end_date}")
    filtered_df = df.loc[(df['Order Date'] >= pd.to_datetime(start_date)) & (df['Order Date'] <= pd.to_datetime(end_date))]
    
    filtered_df.set_index('Order Date', inplace=True)

    if granularity == 'W':
        filtered_df = filtered_df.resample('W')[selected_metric].sum().reset_index()
    elif granularity == 'ME':
        filtered_df = filtered_df.resample('ME')[selected_metric].sum().reset_index()
    elif granularity == 'Q':
        filtered_df = filtered_df.resample('QE')[selected_metric].sum().reset_index()
    elif granularity == 'Y':
        filtered_df = filtered_df.resample('YE')[selected_metric].sum().reset_index()

    filtered_df = filtered_df.sort_values('Order Date')


    fig = px.line(filtered_df, x='Order Date', y=selected_metric, title=f'{selected_metric} Over Time')

    fig.update_layout(xaxis_title='Order Date', yaxis_title=selected_metric, template='plotly_white')


    return fig
