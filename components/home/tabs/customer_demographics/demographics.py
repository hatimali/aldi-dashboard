
import plotly.express as px
import dash_bootstrap_components as dbc
from dash import html, dcc
import plotly.graph_objs as go
from plotly.subplots import make_subplots
from components.home.tabs.customer_demographics.figures import create_delivery_mode_pie_chart, create_profit_sales_figure, create_top_profitable_state_fig, create_top_valuable_customers_fig, top_customers_with_max_product_purchased
from preprocess_data.calculate_demographics_overview import calculate_demographic_overview


def get_demographics_data(filtered_df, filtered_df_current_year, selected_years):
    preprocessed_data = calculate_demographic_overview(filtered_df_current_year, selected_years)
    print(f"demographic_overview: {preprocessed_data}")
    print("In get_demographics_data()")
    # Generate the figures based on the filtered data
    region_profit_sales_fig = create_profit_sales_figure(filtered_df_current_year)
    top_valuable_customers_fig = create_top_valuable_customers_fig(filtered_df_current_year)
    top_profitable_states_fig = create_top_profitable_state_fig(filtered_df_current_year)
    top_active_customers = top_customers_with_max_product_purchased(filtered_df_current_year)

    # Initial pie chart for 'Sales by Delivery Mode'
    delivery_mode_pie_chart_figure = create_delivery_mode_pie_chart(filtered_df_current_year, 'Sales')
    # Add the toggle buttons and pie chart to the layout
    toggle_buttons = dcc.RadioItems(
        id='toggle-delivery-mode',
        options=[
            {'label': 'Sales', 'value': 'Sales'},
            {'label': 'Profit', 'value': 'Profit'}
        ],
        value='Sales',  # default selected value
        labelStyle={'display': 'inline-block', 'margin-right': '20px'},
        className='my-3'  # Add margin for spacing (Bootstrap class)
    )

    container = dbc.Container(fluid=True, children=[
        # Navbar - already defined outside of this function
        # Overview cards
        dbc.Row([
            dbc.Col(dbc.Card(
                className="card-one",
                children=[
                    dbc.CardHeader("Total Customers", className='card-header'),
                    dbc.CardBody([
                        html.H4([
                            html.I(className="fa fa-money fa-icon"),  # Icon with Font Awesome class
                            f"{preprocessed_data['customers_current_year']:,.0f}"  # Display total sales
                        ], className='card-title'),
                    ])
                ]), width=3),
            dbc.Col(dbc.Card(
                className="card-two",
                children=[
                    dbc.CardHeader("Total Orders", className='card-header'),
                    dbc.CardBody([
                        html.H4([
                            html.I(className="fa fa-money fa-icon"),  # Icon with Font Awesome class
                            f"{preprocessed_data['orders_current_year']:,.0f}"  # Display total sales
                        ], className='card-title'),
                    ])
                ]), width=3),
            dbc.Col(dbc.Card(
                className="card-three",
                children=[
                    dbc.CardHeader("Total Products", className='card-header'),
                    dbc.CardBody([
                        html.H4([
                            html.I(className="fa fa-money fa-icon"),  # Icon with Font Awesome class
                            f"{preprocessed_data['products_current_year']:,.0f}"  # Display total sales
                        ], className='card-title'),
                    ])
                ]), width=3),
            dbc.Col(dbc.Card(
                className="card-four",
                children=[
                    dbc.CardHeader("Avg. Sales Per State", className='card-header'),
                    dbc.CardBody([
                        html.H4([
                            html.I(className="fa fa-money fa-icon"),  # Icon with Font Awesome class
                            f"{preprocessed_data['average_sales_per_state']:,.0f}"  # Display total sales
                        ], className='card-title'),
                    ])
                ]), width=3),
        ]),
        # Graphs Section
        dbc.Row([
            dbc.Col(dcc.Graph(figure=region_profit_sales_fig), width=4, md=4, lg=4),
            dbc.Col(dcc.Graph(figure=top_valuable_customers_fig), width=4, md=4, lg=4),
            dbc.Col(dcc.Graph(figure=top_profitable_states_fig), width=4, md=4, lg=4),
        ]),
        dbc.Row([
            dbc.Col([
                toggle_buttons,
                dcc.Graph(id='delivery-mode-pie-chart', figure=delivery_mode_pie_chart_figure),
                # ... Placeholders for other figures if necessary ...
            ], width=4),
            dbc.Col(dcc.Graph(figure=top_active_customers), width=4, md=4, lg=4),
        ]),
    ])
    
    return html.Div(container)

