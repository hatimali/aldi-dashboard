import plotly.express as px
import dash_bootstrap_components as dbc
from dash import html, dcc
from preprocess_data.calculate_dashboard_overview import calculate_monthly_profit, calculate_profit_overview, calculate_top_products_by_profit

def get_profit_analytics_data(filtered_df, filtered_df_current_year, selected_years):
    preprocessed_data = calculate_profit_overview(filtered_df, selected_years)
    print(f"preprocessed_data profit: {preprocessed_data}")
    monthly_profit = calculate_monthly_profit(filtered_df, selected_years)
    print(f"monthly_profit: {monthly_profit}")
    top_products = calculate_top_products_by_profit(filtered_df, selected_years)

    print(f"top_products: {top_products}")
    # Generate the figures based on the filtered data
    fig1_bar_chart = px.bar(filtered_df_current_year, x='Sub-Category', y='Profit', color='Category', title='Profit by Category and Sub-Category')
    fig2_pie_chart = px.pie(filtered_df_current_year, values='Profit', names='Segment', title='Profit by Segment')    
    fig3_top_products = px.bar(top_products, 
        x='Profit', 
        y='Product Name', 
        text='Profit Percent',
        title='Top 5 Profitable Products')

    # Update the layout and the traces for a better look
    fig3_top_products.update_traces(texttemplate='%{text:.2s}%', textposition='outside')
    fig3_top_products.update_layout(showlegend=False)
    fig3_top_products.update_layout(
        xaxis_title="Product Name",
        yaxis_title="Profit",
        title={
            'text': "Top 5 Profitable Products",
            'y':0.9,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'},
        title_font=dict(size=25),
        autosize=True,
        margin=dict(l=50, r=50, b=100, t=100, pad=4),
    )

    fig4_line_chart = px.line(monthly_profit, x=monthly_profit.index, y=monthly_profit.columns,
    labels={'value': 'Profit', 'variable': 'Year'})



    # Continue to update other figures...

    # fig_sales_comparison = px.line(
    #     df.groupby(['Order Date', 'Year'])['Profit'].sum().reset_index(),
    #     x='Order Date', y='Profit', color='Year',
    #     labels={'Profit': 'Total Profit', 'Order Date': 'Date'},
    #     title='Profit Comparison'
    # )

    container = dbc.Container(fluid=True, children=[
        # Navbar - already defined outside of this function
        # Overview cards
        dbc.Row([
            dbc.Col(dbc.Card(
                className="card-sales",  # Apply custom CSS class for styling
                children=[
                    dbc.CardHeader("Current Year Profit", className='card-header'),
                    dbc.CardBody([
                        html.H4([
                            html.I(className="fa fa-money fa-icon"),  # Icon with Font Awesome class
                            f"${preprocessed_data['profit_current_year']:,.0f}"  # Display total sales
                        ], className='card-title'),
                    ])
                ]), width=3),
            dbc.Col(dbc.Card(
                className="card-sales",  # Apply custom CSS class for styling
                children=[
                    dbc.CardHeader("Previous Year Profit", className='card-header'),
                    dbc.CardBody([
                        html.H4([
                            html.I(className="fa fa-money fa-icon"),  # Icon with Font Awesome class
                            f"${preprocessed_data['profit_previous_year']:,.0f}"  # Display total sales
                        ], className='card-title'),
                    ])
                ]), width=3),
            dbc.Col(dbc.Card(
                className="card-sales",  # Apply custom CSS class for styling
                children=[
                    dbc.CardHeader("Avg. Profit Per Unit", className='card-header'),
                    dbc.CardBody([
                        html.H4([
                            html.I(className="fa fa-money fa-icon"),  # Icon with Font Awesome class
                            f"${preprocessed_data['average_profit_per_unit']:,.0f}"  # Display total sales
                        ], className='card-title'),
                    ])
                ]), width=3),
            dbc.Col(dbc.Card(
                className="card-sales",  # Apply custom CSS class for styling
                children=[
                    dbc.CardHeader("YoY Grwoth %", className='card-header'),
                    dbc.CardBody([
                        html.H4([
                            html.I(className="fa fa-money fa-icon"),  # Icon with Font Awesome class
                            f"{preprocessed_data['yoy_growth_current_year'].iloc[0]:,.0f}"  # Display total sales
                        ], className='card-title'),
                    ])
                ]), width=3),
        ]),
        # Graphs Section
        dbc.Row([
            dbc.Col(dcc.Graph(figure=fig1_bar_chart), width=12, md=4, lg=4),
            dbc.Col(dcc.Graph(figure=fig2_pie_chart), width=12, md=4, lg=4),
            dbc.Col(dcc.Graph(figure=fig3_top_products), width=12, md=4, lg=4),
        ]),
        dbc.Row([
            dbc.Col(dcc.Graph(figure=fig4_line_chart), width=12),
            # ... Add placeholders for fig4 and fig5
        ]),
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

