import dash
from dash import html

dash.register_page(__name__, path="/page1")

layout = html.Div([
    html.H1("Page 1"),
    html.P("Content for page 1.")
])
