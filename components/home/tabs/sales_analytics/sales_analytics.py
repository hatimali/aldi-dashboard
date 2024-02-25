import plotly.express as px
import dash_bootstrap_components as dbc
from dash import html, dcc
from preprocess_data.calculate_dashboard_overview import calculate_monthly_sales, calculate_sales_overview, calculate_top_product_with_sales


def get_sales_analytics_data(filtered_df, filtered_df_current_year, selected_years):
        preprocessed_data = calculate_sales_overview(filtered_df, selected_years)
        print(f"preprocessed_data: {preprocessed_data}")
        monthly_sales = calculate_monthly_sales(filtered_df, selected_years)
        top_products = calculate_top_product_with_sales(filtered_df, selected_years)
        

        print("In get_sales_analytics_data()")
        # Generate the figures based on the filtered data
        fig1_bar_chart = px.bar(filtered_df_current_year, x='Sub-Category', y='Sales', color='Category', title='Sales by Category and Sub-Category')
        fig2_pie_chart = px.pie(filtered_df_current_year, values='Sales', names='Segment', title='Sales by Segment')
        
        print("*************************************")
        print(monthly_sales.index)
        print("*********************************")
        
        fig3_line_chart = px.line(monthly_sales, x=monthly_sales.index, y=monthly_sales.columns,
            labels={'value': 'Sales', 'variable': 'Year'})
        
        fig_top_products = px.bar(top_products, 
            x='Sales', 
            y='Product Name', 
            text='Sales Percent',
            title='Top 5 Selling Products')

        # Update the layout and the traces for a better look
        fig_top_products.update_traces(texttemplate='%{text:.2s}%', textposition='outside')
        fig_top_products.update_layout(showlegend=False)
        fig_top_products.update_layout(
            xaxis_title="Product Name",
            yaxis_title="Sales",
            title={
                'text': "Top 5 Selling Products",
                'y':0.9,
                'x':0.5,
                'xanchor': 'center',
                'yanchor': 'top'},
            title_font=dict(size=25),
            autosize=True,
            margin=dict(l=50, r=50, b=100, t=100, pad=4),
        )


        # Continue to update other figures...

        # fig_sales_comparison = px.line(
        #     df.groupby(['Order Date', 'Year'])['Sales'].sum().reset_index(),
        #     x='Order Date', y='Sales', color='Year',
        #     labels={'Sales': 'Total Sales', 'Order Date': 'Date'},
        #     title='Sales Comparison'
        # )

        container = dbc.Container(fluid=True, children=[
            # Navbar - already defined outside of this function
            # Overview cards
            dbc.Row([
                dbc.Col(dbc.Card(
                    className="card-sales",  # Apply custom CSS class for styling
                    children=[
                        dbc.CardHeader("Current Year Sales", className='card-header'),
                        dbc.CardBody([
                            html.H4([
                                html.I(className="fa fa-money fa-icon"),  # Icon with Font Awesome class
                                f"${preprocessed_data['sales_current_year']:,.0f}"  # Display total sales
                            ], className='card-title'),
                        ])
                    ]), width=3),
                dbc.Col(dbc.Card(
                    className="card-orders",  # Apply custom CSS class for styling
                    children=[
                        dbc.CardHeader("Previous Year Sales", className='card-header'),
                        dbc.CardBody([
                            html.H4([
                                html.I(className="fa fa-money fa-icon"),  # Icon with Font Awesome class
                                f"${preprocessed_data['sales_previous_year']:,.0f}"  # Display total sales
                            ], className='card-title'),
                        ])
                    ]), width=3),
                dbc.Col(dbc.Card(
                    className="card-profit",  # Apply custom CSS class for styling
                    children=[
                        dbc.CardHeader("Avg. Sales Per Unit", className='card-header'),
                        dbc.CardBody([
                            html.H4([
                                html.I(className="fa fa-money fa-icon"),  # Icon with Font Awesome class
                                f"${preprocessed_data['average_sales_per_unit']:,.0f}"  # Display total sales
                            ], className='card-title'),
                        ])
                    ]), width=3),
                dbc.Col(dbc.Card(
                    className="card-customers",  # Apply custom CSS class for styling
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
                dbc.Col(dcc.Graph(figure=fig_top_products), width=12, md=4, lg=4),
            ]),
            dbc.Row([
                dbc.Col(dcc.Graph(figure=fig3_line_chart), width=12),
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

