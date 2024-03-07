import dash
from dash import html, dcc
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
from components.sidebar import create_sidebar
from logger_config import setup_logging
setup_logging()


app = dash.Dash(__name__, 
                external_stylesheets=[dbc.themes.BOOTSTRAP,'https://use.fontawesome.com/releases/v5.8.1/css/all.css'],
                suppress_callback_exceptions=True)


from pages import home, table, graph


app.layout = html.Div([
    dcc.Location(id="url"),
    create_sidebar(),
    html.Div(id="page-content")
])


@app.callback(
    Output("page-content", "children"),
    [Input("url", "pathname")]
)
def render_page_content(pathname):
    if pathname == "/":
        return home.layout

    elif pathname == "/table":
        return table.layout
        
    elif pathname == "/graph":
        return graph.layout
    else:
        return html.Div("Page Not Found!!")


if __name__ == '__main__':
    app.run_server(debug=True)
