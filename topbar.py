from dash import html, dcc, Input, Output, callback   # type: ignore
import dash_bootstrap_components as dbc   # type: ignore
from config import translate
import data


lang_dropdown_btn = dcc.Dropdown(
    [
        {
            "label": html.Span(
                [
                    html.Img(src="/assets/en.png", height=20),
                    html.Span("English", style={'font-size': 15, 'padding-left': 10}),
                ], style={'align-items': 'center', 'justify-content': 'center'}
            ),
            "value": "en",
        },
        {
            "label": html.Span(
                [
                    html.Img(src="/assets/kwd.png", height=20),
                    html.Span("Kinyarwanda", style={'font-size': 15, 'padding-left': 10}),
                ], style={'align-items': 'center', 'justify-content': 'center'}
            ),
            "value": "rw",
        },
        {
            "label": html.Span(
                [
                    html.Img(src="/assets/fr.png", height=20),
                    html.Span("French", style={'font-size': 15, 'padding-left': 10}),
                ], style={'align-items': 'center', 'justify-content': 'center'}
            ),
            "value": "fr",
        },
    ],
    value="en",
    clearable=False,
    id="lang_dropdown_btn",
    style={'width': '150px'}
)


def topbar():
    navbar = dbc.Navbar(
        [
            html.Button([
                html.I(className="fa fa-bars")
            ], id="sidebarToggleTop", className="btn btn-link d-md-none rounded-circle mr-3"),

            # Topbar Search
            html.Form([
                html.Div([
                    dcc.Input(type="text", className="form-control bg-light border-0 small", placeholder="Search for..."),
                    html.Div([
                        html.Button([
                            html.I(className="fas fa-search fa-sm"),
                        ], className="btn btn-primary", type="button"),
                    ], className="input-group-append")
                ], className="input-group"),
            ], className="d-none d-sm-inline-block form-inline mr-auto ml-md-3 my-2 my-md-0 mw-100 navbar-search"),

            html.Div(className="topbar-divider d-none d-sm-block"),
            lang_dropdown_btn,
        ],
        color="white",
        className="navbar navbar-expand navbar-light bg-white topbar mb-4 static-top shadow",
        style={'margin': '0rem', 'margin-left': '1rem'}
    )
    return navbar


@callback(
    [
        Output("sidebar-text-view", "children"),
        Output("sidebar-text-machine", "children"),
        Output("sidebar-text-GDP", "children"),
        Output("sidebar-text-CPI", "children"),
        Output("sidebar-text-Home", "children"),
        Output("sidebar-text-Components", "children"),
        Output("sidebar-text-data", "children"),
        Output("sidebar-text-Dashboard", "children"),
        Output("sidebar-text-Overview", "children"),
        Output("sidebar-text-pivot", "children"),
        Output("sidebar-text-chat", "children"),
    ],
    [
        Input("lang_dropdown_btn", "value"),
        Input("sidebar-text-view", "children"),
        Input("sidebar-text-machine", "children"),
        Input("sidebar-text-GDP", "children"),
        Input("sidebar-text-CPI", "children"),
        Input("sidebar-text-Home", "children"),
        Input("sidebar-text-Components", "children"),
        Input("sidebar-text-data", "children"),
        Input("sidebar-text-Dashboard", "children"),
        Input("sidebar-text-Overview", "children"),
        Input("sidebar-text-pivot", "children"),
        Input("sidebar-text-chat", "children"),
    ],
)
def on_lang_change(selected_lang, *textes):
    translated_textes = [translate(text, to=selected_lang) for text in textes]
    data.CURRENT_LANG = selected_lang  # noqa
    return tuple(translated_textes)
