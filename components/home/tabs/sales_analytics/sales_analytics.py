import plotly.express as px
import dash_bootstrap_components as dbc
from dash import html, dcc
from components.home.figures import create_fig_by_category_sub_category, create_geographical_map, create_pie_fig_by_segment, create_top_line_product_figure, create_year_by_year_comparision
from preprocess_data.calculate_dashboard_overview import calculate_monthly_sales_profit_data, calculate_sales_overview, calculate_top_product_with_sales


def get_sales_analytics_data(filtered_df, filtered_df_current_year, selected_years):
        preprocessed_data = calculate_sales_overview(filtered_df, selected_years)
        print(f"preprocessed_data: {preprocessed_data}")
        monthly_sales = calculate_monthly_sales_profit_data(filtered_df, selected_years, column='Sales')
        top_products = calculate_top_product_with_sales(filtered_df_current_year, selected_years)
        

        print("In get_sales_analytics_data()")
        # Generate the figures based on the filtered data
        fig1_bar_chart = create_fig_by_category_sub_category(filtered_df_current_year, column='Sales')
        fig2_pie_chart = create_pie_fig_by_segment(filtered_df_current_year, column='Sales')
        fig_year_by_year_comparision = create_year_by_year_comparision(monthly_sales, selected_years, column='Sales')
        fig_top_products = create_top_line_product_figure(top_products, column='Sales')
        fig_geogrpahical_map = create_geographical_map(filtered_df_current_year, column='Sales')

        # Continue to update other figures...

        container = dbc.Container(fluid=True, children=[
            # Overview cards
            dbc.Row([
                dbc.Col(dbc.Card(
                    className="card-one",
                    children=[
                        dbc.CardHeader("Current Year Sales", className='card-header'),
                        dbc.CardBody([
                            html.H4([
                                html.I(className="fa fa-money fa-icon"),
                                f"${preprocessed_data['sales_current_year']:,.0f}"
                            ], className='card-title'),
                        ])
                    ]), width=3),
                dbc.Col(dbc.Card(
                    className="card-two",
                    children=[
                        dbc.CardHeader("Previous Year Sales", className='card-header'),
                        dbc.CardBody([
                            html.H4([
                                html.I(className="fa fa-money fa-icon"),
                                f"${preprocessed_data['sales_previous_year']:,.0f}"
                            ], className='card-title'),
                        ])
                    ]), width=3),
                dbc.Col(dbc.Card(
                    className="card-three",
                    children=[
                        dbc.CardHeader("Avg. Sales Per Unit", className='card-header'),
                        dbc.CardBody([
                            html.H4([
                                html.I(className="fa fa-money fa-icon"),
                                f"${preprocessed_data['average_sales_per_unit']:,.0f}"
                            ], className='card-title'),
                        ])
                    ]), width=3),
                dbc.Col(dbc.Card(
                    className="card-four",
                    children=[
                        dbc.CardHeader("YoY Grwoth %", className='card-header'),
                        dbc.CardBody([
                            html.H4([
                                html.I(className="fa fa-money fa-icon"),
                                f"{preprocessed_data['yoy_growth_current_year'].iloc[0]:,.0f}%"
                            ], className='card-title'),
                        ])
                    ]), width=3),
            ]),
            # Graphs Section
            dbc.Row([
                dbc.Col(dcc.Graph(figure=fig1_bar_chart), width=12, md=4, lg=4),
                dbc.Col(dcc.Graph(figure=fig2_pie_chart), width=12, md=4, lg=4),
                dbc.Col(dcc.Graph(figure=fig_top_products), width=12, md=4, lg=4),
            ]),
            dbc.Row([
                dbc.Col(dcc.Graph(figure=fig_geogrpahical_map, responsive=True), width=6),
                dbc.Col(dcc.Graph(figure=fig_year_by_year_comparision, responsive=True), width=6),
            ]),
        ])
        
        return html.Div(container)

