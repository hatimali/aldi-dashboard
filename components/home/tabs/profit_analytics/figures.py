# from plotly.subplots import make_subplots
# import plotly.express as px
# import plotly.graph_objs as go

# def create_pie_fig_by_segment(filtered_df_current_year, column):
#     segmented_profit = filtered_df_current_year.groupby('Segment')[[column]].sum().reset_index()
#     colors = ['#bbeaff', '#00005f', '#ff7800', '#55c3f0']  # Define your custom colors
#     fig = go.Figure(data=[
#         go.Pie(
#             labels=segmented_profit['Segment'],
#             values=segmented_profit[column],
#             hole=0.6,  # This creates a donut chart
#             hoverinfo='label+percent',  # Show label and percentage on hover
#             textinfo='percent',  # Show only the percentage in the chart
#             marker=dict(colors=colors, line=dict(color='#55c3f0', width=1)),
#         )
#     ])
    
#     fig.update_traces(textinfo='percent+label')
#     fig.update_layout(title=f"{column} by Sgement", template="plotly_white")
    
#     return fig


# def create_fig_by_category_sub_category(filtered_df_current_year, column):

#     filtered_df_current_year = filtered_df_current_year.groupby(['Sub-Category', 'Category'])[column].sum().reset_index()
#     print("create_Profit_by_category_sub_category")
#     print(filtered_df_current_year)
#     filtered_df_current_year['Percentage of Total Profit'] = (
#         filtered_df_current_year[column] / filtered_df_current_year[column].sum()) * 100

#     # Sort the DataFrame based on the column (Profit/ Sales) within each 'Category' group
#     filtered_df_current_year.sort_values(by=['Category', column], ascending=[True, False], inplace=True)

#     category_colors = {
#         'Furniture': '#bbeaff',
#         'Office Supplies': '#00005f', 
#         'Technology': '#ff7800'
#     }
    
#     # Create the grouped bar chart
#     fig = px.bar(
#         filtered_df_current_year,
#         x='Sub-Category',
#         y=column,
#         color='Category',
#         title=f'{column} by Category and Sub-Category',
#         text=filtered_df_current_year[column].apply(lambda x: f"${x:,.2f}"),
#         category_orders={'Sub-Category': filtered_df_current_year['Sub-Category'].unique()},
#         # color_discrete_sequence=px.colors.qualitative.Safe, # color blind friendly color palete
#         color_discrete_map=category_colors,
#         labels={f'Percentage of Total {column}': f'% of Total {column}', column: f'{column} (USD)'},
        
#     )

#     # Enhance layout for better readability and interactivity
#     fig.update_layout(
#         # hovermode='closest',
#         xaxis=dict(title='Sub-Category', type='category'),
#         yaxis=dict(title=column, tickprefix='$'),
#         plot_bgcolor='rgba(0,0,0,0)',
        
#     )

#     # Add interactive features
#     fig.update_layout(
#         xaxis={'categoryorder':'total descending'},
#         legend_title_text='Category',
#         legend=dict(
#             orientation='h',
#             yanchor='bottom',
#             y=1.02,
#             xanchor='right',
#             x=1
#         )
#     )

#     return fig