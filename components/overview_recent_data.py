# File: No longer used
import pandas as pd
from dash import html, dcc
from data.data_loader import load_data
import plotly.graph_objs as go



def calculate_monthly_profit_ratio(data):
    data['Order Date'] = pd.to_datetime(data['Order Date'])
    data.set_index('Order Date', inplace=True)
    monthly_data = data[['Sales', 'Profit']].resample('ME').sum()

    # Calculate profit ratio
    monthly_data['Profit Ratio'] = (monthly_data['Profit'] / monthly_data['Sales']) * 100

    graph = dcc.Graph(
        id='profit-ratio-over-time',
        figure={
            'data': [
                go.Scatter(
                    x=monthly_data.index,  # Your DataFrame's datetime index or date column
                    y=monthly_data['Profit Ratio'],  # The column containing the profit ratio
                    mode='lines+markers',  # Line chart with markers at each data point
                    name='Profit Ratio'
                )
            ],
            'layout': go.Layout(
                title='Profit Ratio Over Time',
                xaxis={'title': 'Date'},
                yaxis={'title': 'Profit Ratio (%)'},
                margin={'l': 40, 'b': 40, 't': 40, 'r': 10},
                hovermode='closest'
            )
        }
    )
    return graph


def create_overview_recent_data(data):
    data = load_data()
    # Load the dataset    
    # Ensure 'Order Date' is in datetime format and calculate the most recent date
    data['Order Date'] = pd.to_datetime(data['Order Date'])
    most_recent_order_date = data['Order Date'].max()
    
    # Filter data for the most recent date
    recent_data = data[data['Order Date'] == most_recent_order_date]
    
    # Calculate total sales and profit for the most recent data
    total_sales_recent = recent_data['Sales'].sum()
    total_profit_recent = recent_data['Profit'].sum()
    
    # Calculate profit ratio
    profit_ratio_recent = (total_profit_recent / total_sales_recent) * 100 if total_sales_recent else 0
    
    # Create a simple HTML layout to display the insights
    layout = html.Div([
        html.H3('Most Recent Data Overview'),
        html.P(f'Total Sales on {most_recent_order_date.date()}: €{total_sales_recent:.2f}'),
        html.P(f'Total Profit on {most_recent_order_date.date()}: €{total_profit_recent:.2f}'),
        html.P(f'Profit Ratio: {profit_ratio_recent:.2f}%')
    ])
    
    return layout
