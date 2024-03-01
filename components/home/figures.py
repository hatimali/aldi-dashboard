from plotly.subplots import make_subplots
import plotly.express as px
import plotly.graph_objs as go

def create_pie_fig_by_segment(filtered_df_current_year, column):
    segmented_profit = filtered_df_current_year.groupby('Segment')[[column]].sum().reset_index()
    colors = ['#bbeaff', '#00005f', '#ff7800', '#55c3f0']
    fig = go.Figure(data=[
        go.Pie(
            labels=segmented_profit['Segment'],
            values=segmented_profit[column],
            hole=0.6,  # This creates a donut chart
            hoverinfo='label+percent',
            textinfo='percent', 
            marker=dict(colors=colors, line=dict(color='#55c3f0', width=1)),
        )
    ])
    
    fig.update_traces(textinfo='percent+label')
    fig.update_layout(title=f"{column} by Sgement", template="plotly_white")
    
    return fig


def create_year_by_year_comparision(monthly_data, selected_years, column):
    print("Year on Year comparision")
    print(monthly_data)

    current_year = selected_years[0] if selected_years else None
    previous_year = current_year - 1 if current_year else None

    # Calculate year-on-year growth
    # monthly_data['YoY Growth'] = (monthly_data[current_year] - monthly_data[previous_year]) / monthly_data[previous_year]
    monthly_data['YoY Growth'] = ((monthly_data[current_year] - monthly_data[previous_year]) / monthly_data[previous_year]) * 100  # Convert to percentage


    # Create a subplot with 2 y-axes
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    
    # Add the sales data as line charts
    fig.add_trace(
        go.Scatter(
            x=monthly_data.index, 
            y=monthly_data[previous_year], 
            name=f'{previous_year} {column}', 
            mode='lines+markers', 
            line=dict(color='#ff7800')
        )
    )
    fig.add_trace(
        go.Scatter(
            x=monthly_data.index, 
            y=monthly_data[current_year], 
            name=f'{current_year} {column}', 
            mode='lines+markers',
            line=dict(color='#00005f')
        )
    )

    # Add the year-on-year growth as a bar chart
    fig.add_trace(
        go.Bar(
            x=monthly_data.index, 
            y=monthly_data[current_year],
            text=monthly_data[current_year].round(),  # Display current year column on bars
            name='YoY Growth',
            marker_color='#55c3f0',
            hovertemplate='<b>Month:</b> %{x}<br>'+
                          '<b>YoY Growth:</b> %{y:.2f}%<br>'+
                          '<b>{column}:</b> %{text}<extra></extra>'),  # Custom hover info
        )

    # Update layout for a cleaner look
    fig.update_layout(
        title=f'Year over Year Comparison for {column}',
        xaxis_title='Month',
        yaxis_title=f'{column}',
        legend_title='Legend',
        template='plotly_white',
        barmode='group' # ensure bars are grouped by month if have multiple bars per month (not required)
    )

    # Set y-axes titles
    fig.update_yaxes(title_text=f"{column}", secondary_y=False)
    fig.update_yaxes(title_text="Year over Year Growth", secondary_y=True)

    return fig


def create_geographical_map(df, column):
    country_to_code = {
        'United Kingdom': 'GBR',
        'France': 'FRA',
        'Germany': 'DEU',
        'Italy': 'ITA',
        'Spain': 'ESP',
        'Netherlands': 'NLD',
        'Sweden': 'SWE',
        'Belgium': 'BEL',
        'Austria': 'AUT',
        'Ireland': 'IRL',
        'Portugal': 'PRT',
        'Finland': 'FIN',
        'Denmark': 'DNK',
        'Norway': 'NOR',
        'Switzerland': 'CHE'
    }
    custom_colorscale = [
        [0.0, "#c6e2f0"],  # Lighter shade
        [0.2, "#9ecdee"],
        [0.4, "#76b8ec"],
        [0.6, "#4ea3ea"],
        [0.8, "#268ee9"],
        [1.0, "#0079e7"],   # Darker shade
        [1.0, "#00005f"],   # Darker shade
    ]
    print(f"Geographical Map {column}")
    if 'ISO Alpha-3' in df.columns:
        df = df.drop('ISO Alpha-3', axis=1)
    
    # df['ISO Alpha-3'] = df['Country/Region'].map(country_to_code)

    # df.loc[:, 'ISO Alpha-3'] = df['Country/Region'].map(country_to_code)
    df_new = df.copy()
    df_new.loc[:, 'ISO Alpha-3'] = df_new['Country/Region'].apply(lambda x: country_to_code.get(x, None))
    df_new = df_new.groupby(['Country/Region', 'ISO Alpha-3'])[column].sum().reset_index()

    print(df_new)
    fig = go.Figure(data=go.Choropleth(
        locations=df_new['ISO Alpha-3'],  # Spatial coordinates
        z=df_new[column].astype(float),  # Data to be color-coded
        text=df_new['Country/Region'] + f'<br>{column}: ' + df_new[column].astype(str),  # Text that will appear on the map
        hoverinfo='text',  # Show custom text on hover
        colorscale=custom_colorscale,
        autocolorscale=False,
        reversescale=False,
        marker_line_color='darkgray',
        marker_line_width=0.5,
        colorbar_title=f'{column} in USD',
    ))

    fig.update_layout(
        title_text=f'Geographic {column} Performance',
        geo=dict(
            showframe=False,
            showcoastlines=False,
            projection_type='equirectangular',
            lataxis=dict(range=[40, 65]),  # Latitude range for Central-Western Europe
            lonaxis=dict(range=[-10, 30]),  # Longitude range for Central-Western Europe
        ),
        margin=dict(l=0, r=0, t=25, b=25),
    )

    return fig


def create_fig_by_category_sub_category(filtered_df_current_year, column):

    filtered_df_current_year = filtered_df_current_year.groupby(['Sub-Category', 'Category'])[column].sum().reset_index()
    print("create_Profit_by_category_sub_category")
    print(filtered_df_current_year)
    filtered_df_current_year['Percentage of Total Profit'] = (
        filtered_df_current_year[column] / filtered_df_current_year[column].sum()) * 100

    # Sort the DataFrame based on the column (Profit/ Sales) within each 'Category' group
    filtered_df_current_year.sort_values(by=['Category', column], ascending=[True, False], inplace=True)

    category_colors = {
        'Furniture': '#bbeaff',
        'Office Supplies': '#00005f', 
        'Technology': '#ff7800'
    }
    
    # Create the grouped bar chart
    fig = px.bar(
        filtered_df_current_year,
        x='Sub-Category',
        y=column,
        color='Category',
        title=f'{column} by Category and Sub-Category',
        text=filtered_df_current_year[column].apply(lambda x: f"${x:,.2f}"),
        category_orders={'Sub-Category': filtered_df_current_year['Sub-Category'].unique()},
        # color_discrete_sequence=px.colors.qualitative.Safe, # color blind friendly color palete
        color_discrete_map=category_colors,
        labels={f'Percentage of Total {column}': f'% of Total {column}', column: f'{column} (USD)'},
        
    )

    # Enhance layout for better readability and interactivity
    fig.update_layout(
        # hovermode='closest',
        xaxis=dict(title='Sub-Category', type='category'),
        yaxis=dict(title=column, tickprefix='$'),
        plot_bgcolor='rgba(0,0,0,0)',
        
    )

    # Add interactive features
    fig.update_layout(
        xaxis={'categoryorder':'total descending'},
        legend_title_text='Category',
        legend=dict(
            orientation='h',
            yanchor='bottom',
            y=1.02,
            xanchor='right',
            x=1
        )
    )

    return fig


def create_top_line_product_figure(top_products, column):
    label = 'Selling' if column == "Sales" else "Profitable"
    fig_top_products = px.bar(top_products, 
        x=f'{column}', 
        y='Product Name', 
        text=f'{column} Percent',
        title='Top 5 Selling Products')

    # Update the layout and the traces for a better look
    fig_top_products.update_traces(texttemplate='%{text:.0f}%', textposition='inside')
    fig_top_products.update_layout(showlegend=False)
    fig_top_products.update_layout(
        xaxis_title=f"{column}",
        yaxis_title="Product Name",
        title={
            'text': f"Top 5 {label} Products",
            'y':0.9,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'},
        # title_font=dict(size=25),
        autosize=True,
        template="plotly_white",
        margin=dict(l=50, r=50, b=100, t=100, pad=4),
    )
    fig_top_products.update_traces(marker_color='#55c3f0')
    return fig_top_products
