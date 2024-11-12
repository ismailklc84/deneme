import dash
from dash import html

dash.register_page(__name__, path="/page2")

layout = html.Div([
    html.H1("Page 2"),
    html.P("Content for page 2.")
])
