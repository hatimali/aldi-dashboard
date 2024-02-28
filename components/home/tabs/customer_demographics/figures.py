import dash
import plotly.graph_objs as go
from plotly.subplots import make_subplots
import plotly.express as px
import pandas as pd


# Tab 3 Filters Start
def create_profit_sales_figure(df):
    
    df_agg = df[['Sales', 'Profit', 'Region']].groupby('Region').sum().reset_index()

    # Sort the dataframe by region for consistent plotting
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
        autosize=True,
        template="plotly_white"
    )

    # Create the figure using both traces
    fig = go.Figure(data=[trace_sales, trace_profit], layout=layout)
    
    return fig


def create_top_valuable_customers_fig(df):
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
            textposition='inside',  # Position text outside the bar
            marker_color='#55c3f0'
        )
    ]
    layout=go.Layout(
        title='Top 10 Customers with most Profit',
        xaxis={'title': 'Profit'},
        yaxis={'title': 'Customer Name', 'categoryorder': 'total ascending'},  # Sort y-axis in ascending order of total
        margin={'l': 150, 'r': 50, 't': 50, 'b': 50},  # Adjust margins to accommodate longer customer names
        autosize=True,
        template="plotly_white"
    )

    fig = go.Figure(data=fig_data, layout=layout)
    return fig

def create_top_profitable_state_fig(df):
    df_agg = df[['State/Province', 'Profit']].groupby('State/Province').sum().reset_index()
    df_agg.sort_values(by='Profit', ascending=False, inplace=True)
    top_5_states = df_agg.head(5)

    print("Top 5 Profitable States")
    print(top_5_states)
    fig_data=[
        go.Bar(
            x=top_5_states['Profit'],
            y=top_5_states['State/Province'],
            orientation='h',
            text=top_5_states['Profit'].round(2),  # Display profit on each bar
            textposition='inside',  # Position text outside the bar
            marker_color='#55c3f0'
        )
    ]
    layout=go.Layout(
        title='Top 5 Profitable States',
        xaxis={'title': 'Profit'},
        yaxis={'title': 'States/Province', 'categoryorder': 'total ascending'},  # Sort y-axis in ascending order of total
        margin={'l': 150, 'r': 50, 't': 50, 'b': 50},  # Adjust margins to accommodate longer customer names
        autosize=True,
        template="plotly_white"
    )

    fig = go.Figure(data=fig_data, layout=layout)
    return fig


def create_delivery_mode_pie_chart(df_current_year, value='Sales'):
    delivery_summary = df_current_year.groupby('Delivery Mode')[['Sales', 'Profit']].sum().reset_index()
    colors = ['#bbeaff', '#00005f', '#ff7800', '#55c3f0']  # Define your custom colors
    fig = go.Figure(data=[
        go.Pie(
            labels=delivery_summary['Delivery Mode'],
            values=delivery_summary[value],
            hole=0.6,  # This creates a donut chart
            hoverinfo='label+percent',  # Show label and percentage on hover
            textinfo='percent',  # Show only the percentage in the chart
            marker=dict(colors=colors, line=dict(color='#55c3f0', width=1)),
        )
    ])
    
    fig.update_traces(textinfo='percent+label')
    fig.update_layout(title=f"{value} by Delivery Mode", template="plotly_white")
    
    return fig

def top_performing_products(df_current_year):
    df = df_current_year.groupby('Product ID')[['Sales', 'Quantity']].sum().reset_index()

    df['Average Sales per Unit'] = df['Sales'] / df['Quantity']

    # Sort the DataFrame by 'Average Sales per Unit' to find the top-performing products
    df_sorted = df.sort_values(by='Average Sales per Unit', ascending=False)

    # Create a bar chart
    fig = go.Figure(data=[
        go.Bar(
            x=df_sorted['Product Name'],
            y=df_sorted['Average Sales per Unit'],
            marker_color='indianred'  # You can customize the color
        )
    ])

    # Update the layout to add titles and adjust other aesthetic elements
    fig.update_layout(
        title='Top Performing Products by Average Sales per Unit',
        xaxis_title='Product Name',
        yaxis_title='Average Sales per Unit',
        template='plotly_white'  # Choose a template that fits your dashboard's theme
    )

    # Assuming you're using this in a Dash app, you would return this figure where needed
    return fig


def top_customers_with_max_product_purchased(df_current_year):
    # Group the data by 'Customer Name' and count the number of products purchased
    customer_product_counts = df_current_year.groupby('Customer Name')['Product Name'].count().reset_index()

    # Sort the customers based on the count in descending order
    top_customers = customer_product_counts.sort_values(by='Product Name', ascending=False)

    # Slice the DataFrame to get the top 10 customers
    top_10_customers = top_customers.head(10)

    # Ensure the customers are sorted correctly in the figure
    top_10_customers = top_10_customers.sort_values(by='Product Name', ascending=True)

    fig_data=[
        go.Bar(
            x=top_10_customers['Product Name'],
            y=top_10_customers['Customer Name'],
            orientation='h',
            text=top_10_customers['Product Name'],
            textposition='inside',  # Position text inside the bar
            marker_color='#55c3f0'
        )
    ]

    # Create a bar chart with Plotly
    fig = go.Figure(data=fig_data)

    # Update the layout of the figure for custom binning on the x-axis
    fig.update_layout(
        title="Top 10 Customers by Number of Products Purchased",
        xaxis=dict(
            title="Total Products Purchased",
            tickvals=[0, 10, 20],  # Set custom ticks based on desired bins
            ticktext=['0-10', '10-20', '20+']  # Set custom text for bins
        ),
        yaxis_title="Customer Name",
        template="plotly_white",
        autosize=True
    )

    return fig
