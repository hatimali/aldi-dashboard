# First, you'll need to import the necessary libraries
import dash
from dash import html, dcc
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
from components.sidebar import create_sidebar

# Initialize your Dash app here
app = dash.Dash(__name__, 
                external_stylesheets=[dbc.themes.BOOTSTRAP,'https://use.fontawesome.com/releases/v5.8.1/css/all.css'],
                suppress_callback_exceptions=True)


# Automatically register all pages
from pages import home, table, graph


# Defome the layout of the app
app.layout = html.Div([
    dcc.Location(id="url"),
    create_sidebar(),
    html.Div(id="page-content") # Define the main content
])



# Callback to switch between pages/content
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

# Run the Dash app
if __name__ == '__main__':
    app.run_server(debug=True)
