import plotly.graph_objs as go
from plotly.subplots import make_subplots
import plotly.express as px
import pandas as pd

def create_profit_sales_figure_2(df):
    # Sort the dataframe by region for consistent plotting

    df['Sales'] = pd.to_numeric(df['Sales'])
    df['Profit'] = pd.to_numeric(df['Profit'])
    df_agg = df[['Sales', 'Profit', 'Region']].groupby('Region').sum().reset_index()

    df_agg.sort_values('Region', inplace=True)
    

    # Create traces for the Sales and Profit
    trace_sales = go.Bar(
        x=df_agg['Region'],
        y=df_agg['Sales'],
        name='Sales',
        marker_color='#55c3f0', # dark blue
        text=df_agg['Sales'].round(),
        textposition='auto',
    )
    
    trace_profit = go.Bar(
        x=df_agg['Region'],
        y=df_agg['Profit'],
        name='Profit',
        marker_color='#ff7800', # orange
        text=df_agg['Profit'].round(),
        textposition='auto',
    )
    
    layout = go.Layout(
        title='Sales and Profit by Region',
        barmode='stack',
        xaxis={'title': 'Region'},
        yaxis={'title': 'Amount'},
        autosize=True
    )

    # Create the figure using both traces
    fig = go.Figure(data=[trace_sales, trace_profit], layout=layout)
    
    return fig

def create_profit_sales_figure(df):
    df['Sales'] = pd.to_numeric(df['Sales'])
    df['Profit'] = pd.to_numeric(df['Profit'])

    # df_agg = df[['Sales', 'Profit', 'Region']].groupby('Region').sum().reset_index()
    df_agg = df[['Sales', 'Profit', 'Region']].groupby('Region').sum().reset_index()

    figure=px.bar(df_agg,
                  x='Region', 
                  y=['Profit', 'Sales'], 
                  barmode='group', 
                  title='Profit and Sales by Region')
    
    return figure


def create_top_valuable_customers(df):
    df['Profit'] = pd.to_numeric(df['Profit'])
    df_agg = df[['Customer ID', 'Customer Name', 'Profit']].groupby(['Customer ID', 'Customer Name']).sum().reset_index()
    
    # df_agg.sort_values('Customer ID', inplace=True)
    df_agg.sort_values(by='Profit', ascending=False, inplace=True)

    top_10_customers = df_agg.head(10)

    print("Create Top Valuable customers")
    print(top_10_customers)

    fig_data=[
        go.Bar(
            x=top_10_customers['Profit'],
            y=top_10_customers['Customer Name'],
            orientation='h',
            text=top_10_customers['Profit'].round(2),  # Display profit on each bar
            textposition='outside',  # Position text outside the bar
            marker_color='#55c3f0'
        )
    ]
    layout=go.Layout(
        title='Top 10 Valuable Customers by Profit',
        xaxis={'title': 'Profit'},
        yaxis={'title': 'Customer Name', 'categoryorder': 'total ascending'},  # Sort y-axis in ascending order of total
        margin={'l': 150, 'r': 50, 't': 50, 'b': 50},  # Adjust margins to accommodate longer customer names
        autosize=True
    )

    fig = go.Figure(data=fig_data, layout=layout)
    return fig