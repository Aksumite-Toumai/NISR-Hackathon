import dash  # type: ignore
from dash import html


dash.register_page(__name__)

layout = html.Div([
    html.H1('This is our Login page'),
    html.Div('This is our Login page content.'),
])
