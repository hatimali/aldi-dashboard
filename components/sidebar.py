# components/sidebar.py
from dash import html
import dash_bootstrap_components as dbc

def create_sidebar():
    return html.Div(
            children=[
                html.H4("Dash", className="display-4"),
                html.Hr(),
                dbc.Nav(
                    [
                        dbc.NavLink([html.I(className="fa fa-home"), " Home"], href="/", active="exact"),
                        dbc.NavLink([html.I(className="fa fa-table"), " Table Page"], href="/table", active="exact"),
                        dbc.NavLink([html.I(className="fas fa-chart-bar"), " Graph Page"], href="/graph", active="exact"),
                    ],
                    vertical=True,
                    pills=True,
                ),
            ],className="sidebar"
        )
