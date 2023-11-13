import dash  # type: ignore
from dash import html, dcc, callback, Input, Output, ctx  # type: ignore
import dash_bootstrap_components as dbc  # type: ignore
from graphs import cpi, gdp, pivottable, view
import config


dash.register_page(__name__)

# the style arguments for the sidebar. We use position:fixed and a fixed width
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": "0rem",
    "left": "0rem",
    "bottom": "0rem",
    "width": "16rem",
    "padding": "2rem 1rem",
    "background-color": "white",
    "color": "#696969",
    "font": "bold",
}

# the styles for the main content position it to the right of the sidebar and
# add some padding.
CONTENT_STYLE = {
    "margin-left": "17rem",
    "margin-top": "0",
    "margin-right": "1rem",
    "padding": "0",
    "background-color": "#DCDCDC",
    "padding-top": "0.5rem",
}

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

search_bar = dbc.Row(
    [
        dbc.Col(dbc.Input(type="search", placeholder="Search"), width=3,),
        dbc.Col(
            dbc.Button(
                html.I(className="fa fa-search"), className="ms-2", n_clicks=0,
                style={'background-color': '#284fa1', "color": "white"},
            ),
            width=1,
        ),
        # dbc.Col(lang_dropdown_btn, width=4, className="d-flex justify-content-end",),
        dbc.Col(
            dcc.Link(children="Log out", href="/logout", className="btn btn-outline-danger btn-logout"),
            width=4,
            className="d-flex justify-content-end",
        ),
    ],
)


def layout():
    navbar = dbc.Navbar(
        search_bar,
        color="white",
        className="row card",
        style={'margin': '0rem'}
    )

    sidebar = html.Div(
        [
            html.H2([html.Img(className="aims_logo", src="assets/nisr_logo.png", style={'width': '150px'}), "Dashboard"],
                    className="display-8 row d-flex justify-content-center align-items-center"),
            html.Hr(),
            html.P([
                html.I(className="fa fa-file-excel fa-lg"),
                dbc.Label(config.translate_text("Excel Files"), style={'padding-left': '0.5rem'})
                ], style={'margin': '0rem', 'margin-left': '1rem', "color": "#284fa1"}),
            dbc.Nav(
                [
                    dbc.NavLink([config.translate_text("Consumer Price Index")],
                                href="#",
                                style={'color': "#696969"},
                                className="nav-link nav-home-link",
                                id="CPI"),
                    dbc.NavLink(config.translate_text("GDP National Accounts"),
                                href="#",
                                style={'color': "#696969"},
                                className="nav-link nav-home-link",
                                id="GDP")
                ],
                vertical=True,
                pills=True,
            ),
            # html.Hr(),
            # html.P([
            #     html.I(className="fa fa-microchip fa-lg"),
            #     dbc.Label(config.translate_text("Machine Learning"), style={'padding-left': '0.5rem'})
            #     ], style={'margin': '0rem', 'margin-left': '1rem', "color": "#284fa1"}),
            # dbc.Nav(
            #     [
            #         dbc.NavLink(config.translate_text("Supervised"),
            #                     href="#",
            #                     style={'color': "#696969"},
            #                     className="nav-link nav-home-link",
            #                     id="MLS"),
            #         dbc.NavLink(config.translate_text("Unsupervised"),
            #                     href="#",
            #                     style={'color': "#696969"},
            #                     className="nav-link nav-home-link",
            #                     id="MLU"),
            #     ],
            #     vertical=True,
            #     pills=True,
            # ),
            html.Hr(),
            html.P([
                html.I(className="fa fa-table fa-lg"),
                dbc.Label("Data", style={'padding-left': '0.5rem'})
                ], style={'margin': '0rem', 'margin-left': '1rem', "color": "#284fa1"}),
            dbc.Nav(
                [
                    dbc.NavLink(config.translate_text("View"),
                                href="#",
                                style={'color': "#696969"},
                                className="nav-link nav-home-link",
                                id="View-Data"),
                    dbc.NavLink(config.translate_text("Pivot Table"),
                                href="#",
                                style={'color': "#696969"},
                                className="nav-link nav-home-link",
                                id="Pivot-Table"),
                ],
                vertical=True,
                pills=True,
            ),
        ],
        style=SIDEBAR_STYLE,
    )

    content = html.Div(children=[], id="home-page-content", style={'background-color': '#DCDCDC', "margin-top": "0rem"})

    home = html.Div([navbar, content], style=CONTENT_STYLE)
    return html.Div([sidebar, home],
                    id="container", style={'background-color': '#DCDCDC', "margin-top": "0rem"})


# Function to render the home page
@callback([Output("home-page-content", "children")],
          [Input("CPI", "n_clicks"),
           Input("GDP", "n_clicks"),
           Input("View-Data", "n_clicks"),
           Input("Pivot-Table", "n_clicks"),])
def render_hone_page_content(btn1, btn2, btn4, btn5):
    button_clicked = ctx.triggered_id
    match button_clicked:
        case "GDP":
            return gdp.get_content()
        case "View-Data":
            return view.get_content()
        case "Pivot-Table":
            return pivottable.get_content()
        case _:
            return cpi.get_content()


@callback(
    [Output('url-home-lang', 'children'), Output('lang_dropdown_btn', 'value')],
    [Input('lang_dropdown_btn', 'value')]
)
def render_translate_text(lang):
    if lang:
        config.LANG = lang
        return layout(), lang
    return dash.no_update, dash.no_update
