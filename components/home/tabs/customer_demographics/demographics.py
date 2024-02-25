
import plotly.express as px
import dash_bootstrap_components as dbc
from dash import html, dcc
import plotly.graph_objs as go
from plotly.subplots import make_subplots
from components.home.tabs.customer_demographics.figures import create_profit_sales_figure_2, create_top_valuable_customers
from preprocess_data.calculate_demographics_overview import calculate_demographic_overview


def get_demographics_data(filtered_df, filtered_df_current_year, selected_years):
    preprocessed_data = calculate_demographic_overview(filtered_df_current_year, selected_years)
    print(f"demographic_overview: {preprocessed_data}")
    #monthly_sales = calculate_monthly_sales(filtered_df, selected_years)
    #top_products = calculate_top_product_with_sales(filtered_df, selected_years)
    

    print("In get_demographics_data()")
    # Generate the figures based on the filtered data

    profit_sales_fig = create_profit_sales_figure_2(filtered_df_current_year)
    top_valuable_customers_fig = create_top_valuable_customers(filtered_df_current_year)
    

    container = dbc.Container(fluid=True, children=[
        # Navbar - already defined outside of this function
        # Overview cards
        dbc.Row([
            dbc.Col(dbc.Card(
                className="card-sales",  # Apply custom CSS class for styling
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
                className="card-sales",  # Apply custom CSS class for styling
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
                className="card-sales",  # Apply custom CSS class for styling
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
                className="card-sales",  # Apply custom CSS class for styling
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
            dbc.Col(dcc.Graph(figure=profit_sales_fig), width=4, md=4, lg=4),
            dbc.Col(dcc.Graph(figure=top_valuable_customers_fig), width=4, md=4, lg=4),
            dbc.Col(dcc.Graph(figure=profit_sales_fig), width=4, md=4, lg=4),
        ]),
        # dbc.Row([
        #     dbc.Col(dcc.Graph(figure=fig3_line_chart), width=12),
        #     # ... Add placeholders for fig4 and fig5
        # ]),

        # dbc.Row([
        #     dbc.Col(dcc.Graph(figure=fig_sales_comparison), width=12),
        #     # ... Repeat for other overview cards
        # ]),
        

        # Top 5 Selling Products and Sales Mapping by Country
        # dbc.Row([
        #     dbc.Col(html.Div([
        #         html.H5('Top 5 Selling Products'),
        #         # Add a table or list group for Top 5 Selling Products
        #     ]), width=12, md=6, lg=6),
        #     dbc.Col(dcc.Graph(figure=fig2), width=12, md=6, lg=6),  # Placeholder for fig6
        # ]),
        # ... Continue for the rest of your layout as per the sections
    ])
    
    return html.Div(container)

