import dash
from dash import html, dcc, callback, Input, Output
import dash_bootstrap_components as dbc
from components.home.filters import get_filters
from components.home.tabs.customer_demographics.demographics import get_demographics_data
from components.home.tabs.customer_demographics.figures import create_delivery_mode_pie_chart
from components.home.tabs.profit_analytics.profit_analytics import get_profit_analytics_data
from components.home.tabs.sales_analytics.sales_analytics import get_sales_analytics_data
from data.data_loader import load_data
from dash.exceptions import PreventUpdate
from preprocess_data.preprocess_home_data import preprocess_data
import logging
logger = logging.getLogger()

# Register this file as a Dash page
dash.register_page(__name__ , path='/')


df = load_data()
df = preprocess_data(df)

filters = get_filters(df)

layout = html.Div([
    dbc.Tabs(
        [
                dbc.Tab(label="Sales Analytics", tab_id="tab-1", tabClassName="text-center", labelClassName="h5 mb-0"),
                dbc.Tab(label="Profit Analytics", tab_id="tab-2", tabClassName="text-center", labelClassName="h5 mb-0"),
                dbc.Tab(label="Customer Demographics", tab_id="tab-3", tabClassName="text-center", labelClassName="h5 mb-0"),
        ],
        id="tabs",
        active_tab="tab-1",
        className="nav-justified",
    ),
    filters,
    html.Div(id="tab-content")
])


@callback(
    Output("tab-content", "children"),
    [Input("tabs", "active_tab"),
     Input("year-filter", "value"),
     Input("segment-filter", "value")]
)
def update_home_content(active_tab, selected_years, selected_segments):
    print(f"Active Tab: {active_tab}, Selected Years: {selected_years}, Selected Segments: {selected_segments}")
    if active_tab is None:
        print("Active tab is None, raising PreventUpdate")
        raise PreventUpdate

    print(f"Current Year: {selected_years[0]}, Previous Year: {selected_years[0] - 1}")
    current_year = selected_years[0] if selected_years else None
    previous_year = current_year - 1 if current_year else None


    filtered_df = df.loc[(df['Year'] >= previous_year) & (df['Year'] <= current_year) & (df['Segment'].isin(selected_segments))]
    
    filtered_df_current_year = filtered_df[(filtered_df['Year'] == current_year)]

    if active_tab == "tab-1":
        logger.info('Tab1')
        return get_sales_analytics_data(filtered_df, filtered_df_current_year, selected_years)
    elif active_tab == "tab-2":
        logger.info('Tab2')
        return get_profit_analytics_data(filtered_df, filtered_df_current_year, selected_years)
    else:
        logger.info('Tab3')
        return get_demographics_data(filtered_df, filtered_df_current_year, selected_years)



@callback(
    Output('delivery-mode-pie-chart', 'figure'),
    [Input('toggle-delivery-mode', 'value'),
     Input('year-filter', 'value'),
     Input('segment-filter', 'value')]
)
def update_delivery_mode_pie_chart(toggle_value, selected_years, selected_segments):

    filtered_df_current_year = df[(df['Year'].isin(selected_years)) & (df['Segment'].isin(selected_segments))]

    return create_delivery_mode_pie_chart(filtered_df_current_year, toggle_value)