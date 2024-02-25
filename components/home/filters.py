from dash import html, dcc
import dash_bootstrap_components as dbc
def get_filters(df):
    years = sorted(df['Year'].unique())
    year_slider = dcc.RangeSlider(
        id='year-filter',
        min=min(years),
        max=max(years),
        value=[max(years)],
        marks={str(year): str(year) for year in years},
        step=None,  # This makes the slider snap to the provided marks
        allowCross=False,  # Prevents the user from selecting a range in reverse order
        className='year-slider',
        persistence=True,  # Remember the selected value on page refresh
        persistence_type='session',  # Persist selected value within the user's session
    )
    segment_filter = dcc.Dropdown(
        id='segment-filter',
        options=[{'label': segment, 'value': segment} for segment in df['Segment'].unique()],
        value=df['Segment'].unique(),  # Set the default value to include all segments
        multi=True,  # Allow selecting multiple segments
        className='segment-dropdown',
        persistence=True,  # Remember the selected value on page refresh
        persistence_type='session',  # Persist selected value within the user's session
    )

    return html.Div([
        dbc.Row([
            dbc.Col(html.Div([
                html.Label("Year", className='filter-label'),
                year_slider
            ]), lg=9, md=8, sm=12, className='year-filter-container'),
            dbc.Col(html.Div([
                html.Div('Segment', className='filter-label'),
                segment_filter
            ]), lg=3, md=4, sm=12, className='segment-filter-container', align='end'),
        ]),
        ], className='filter-bar')
