import dash  # type: ignore
from dash import html, dcc, Input, Output, callback  # type: ignore
import dash_bootstrap_components as dbc  # type: ignore
import numpy as np  # type: ignore
from data import GDP_EXCEL_FILE


dash.register_page(__name__)


pop_dropdown_years = dcc.Dropdown(
                    id='pop-year-dropdown',
                    options=[
                            {
                                "label": html.Span(year, style={'color': 'black', 'font-size': 12}),
                                "value": year,
                            } for year in GDP_EXCEL_FILE['Years'].values  # type: ignore
                    ],
                    value=2022,
                    clearable=False,
                    style={"border": "0.2"},
                ),
exchange_dropdown_years = dcc.Dropdown(
                id='exchange-year-dropdown',
                options=[
                        {
                            "label": html.Span(year, style={'color': 'black', 'font-size': 12}),
                            "value": year,
                        } for year in GDP_EXCEL_FILE['Years'].values  # type: ignore
                ],
                value=2022,
                clearable=False,
                style={"border": "0.2"},
            ),
popuplation_card = dbc.Card(
    [
        dbc.Row(
            [
                dbc.Col(
                    dbc.CardImg(
                        src="/assets/population.jpeg",
                        className="img-fluid mt-0 mb-0",
                        style={"height": "153px", "padding": "0", "margin": "0"},
                    ),
                    className="col-md-5",
                ),
                dbc.Col(
                    dbc.CardBody(
                        [
                            html.H4("Population", className="card-title"),
                            html.Span(pop_dropdown_years),
                            html.Small(
                                "Total population (millions): ",
                                className="card-text text-muted",
                            ),
                            html.Small(
                                id="pop-value",
                                className="card-text text-muted",
                            ),
                            html.Br(),
                            html.Small(
                                "Growth Rate: ",
                                className="card-text text-muted",
                            ),
                            html.Small(
                                id="pop-rate",
                                className="card-text text-muted",
                            ),
                        ]
                    ),
                    className="col-md-7",
                ),
            ],
            className="g-0 d-flex align-items-center",
            style={"padding": "0", "margin": "0"},
        )
    ],
    style={"maxWidth": "540px", "padding": "0"},
)
exchange_card = dbc.Card(
    [
        dbc.Row(
            [
                dbc.Col(
                    dbc.CardImg(
                        src="/assets/exchange.png",
                        className="img-fluid mt-0 mb-0",
                        style={"height": "153px", "padding": "0", "margin": "0"},
                    ),
                    className="col-md-5",
                ),
                dbc.Col(
                    dbc.CardBody(
                        [
                            html.H4("Exchange", className="card-title"),
                            html.Span(exchange_dropdown_years),
                            html.Small(
                                "Rwf per US dollar: ",
                                className="card-text text-muted",
                            ),
                            html.Small(
                                id="exchange-value",
                                className="card-text text-muted",
                            ),
                            html.Br(),
                            html.Small(
                                "Growth Rate: ",
                                className="card-text text-muted",
                            ),
                            html.Small(
                                id="exchange-rate",
                                className="card-text text-muted",
                            ),
                        ]
                    ),
                    className="col-md-7",
                ),
            ],
            className="g-0 d-flex align-items-center",
            style={"padding": "0", "margin": "0"},
        )
    ],
    style={"maxWidth": "540px", "padding": "0"},
)

dgp_2017_card = dbc.Card(
    [
        dbc.Row(
            [
                dbc.Col(
                    dbc.CardImg(
                        src="/assets/GDP.jpg",
                        className="img-fluid mt-0 mb-0",
                        style={"height": "153px", "padding": "0", "margin": "0"},
                    ),
                    className="col-md-5",
                ),
                dbc.Col(
                    dbc.CardBody(
                        [
                            html.H6("Constant 2017 prices, Billions RFW", className="card-title"),
                            html.Small(
                                GDP_EXCEL_FILE['Years'].values[-1],  # type: ignore
                                className="card-text text-muted",
                            ),
                            html.P(GDP_EXCEL_FILE['GDP at constant 2017 prices'].values[-1],  # type: ignore
                                    className="card-text",  # noqa
                                    style={"font": "bold", "font-size": 45, 'color': "#97d26f", "text-align": "right"}),  # noqa
                        ]
                    ),
                    className="col-md-7",
                ),
            ],
            className="g-0 d-flex align-items-center",
            style={"padding": "0", "margin": "0"},
        )
    ],
    style={"maxWidth": "540px", "padding": "0"},
)

dgp_current_card = dbc.Card(
    [
        dbc.Row(
            [
                dbc.Col(
                    dbc.CardImg(
                        src="/assets/gdp.jpg",
                        className="img-fluid mt-0 mb-0",
                        style={"height": "153px", "padding": "0", "margin": "0"},
                    ),
                    className="col-md-5",
                ),
                dbc.Col(
                    dbc.CardBody(
                        [
                            html.H6("Current prices, Billions RFW", className="card-title"),
                            html.Small(
                                GDP_EXCEL_FILE['Years'].values[-1],  # type: ignore
                                className="card-text text-muted",
                            ),
                            html.P(GDP_EXCEL_FILE['GDP at current prices'].values[-1],  # type: ignore
                                    className="card-text",  # noqa
                                    style={"font": "bold", "font-size": 45, 'color': "#419b3c", "text-align": "right"}),  # noqa
                        ]
                    ),
                    className="col-md-7",
                ),
            ],
            className="g-0 d-flex align-items-center",
            style={"padding": "0", "margin": "0"},
        )
    ],
    style={"maxWidth": "540px", "padding": "0"},
)


def layout():
    return html.Div([
        html.Div(
            html.H1("Dashboard > Overview", className="h3 mb-0 text-gray-800"),
            className="d-sm-flex align-items-center justify-content-between mb-4",
        ),
        dbc.Row(
            [

                dbc.Col(popuplation_card, width=3),
                dbc.Col(exchange_card, width=3),
                dbc.Col(dgp_2017_card, width=3),
                dbc.Col(dgp_current_card, width=3),
            ],
            className="mb-3 mt-2 py-0 px-0",
        ),
        dbc.Row(
            [
                dbc.Container(
                    [
                        html.H1("Welcome to the NISR Hackathon Dashboard", className="display-4"),
                        html.P("This dashboard showcases statistical data visualizations generated using Python. "
                               "Explore the various features to gain insights into the provided datasets.", className="lead"),

                        html.H2("Key Features", className="mt-4"),
                        html.Ul([
                            html.Li(["Interactive visualizations of NISR datasets:",
                                    html.Ul([
                                        html.Li("GDP National Accounts"),
                                        html.Li("Consumer Price Index"),
                                        # Add more features as needed
                                    ], className="list-styled"),]),
                            html.Li("Data exploration tools and filters."),
                            html.Li("Insights and trends analysis."),
                            # Add more features as needed
                        ], className="list-styled"),

                        html.P("To get started, use the sidebar navigation to explore different sections of the dashboard.",
                               className="mt-3 font-italic text-muted"),
                    ],
                    fluid=True  # Use a fluid layout for a full-width container
                )
            ],
            className="mb-3 py-0 px-0 mt-4",
        ),
    ])


@callback(
    [Output("pop-value", "children"), Output("pop-rate", "children")],
    [
        Input("pop-year-dropdown", "value"),
    ],
)
def gdp_pop_year_dropdown_on_change(items_value):
    data = GDP_EXCEL_FILE[['Years', 'Total population (millions)']]
    data['rate'] = data['Total population (millions)'].pct_change()
    value = data[data['Years'] == items_value]['Total population (millions)'].values[0]
    rate = np.round(data[data['Years'] == items_value]['rate'].values[0], 2)*100
    return [value], [f"{rate}%"]


@callback(
    [Output("exchange-value", "children"), Output("exchange-rate", "children")],
    [
        Input("exchange-year-dropdown", "value"),
    ],
)
def gdp_exchange_year_dropdown_on_change(items_value):
    data = GDP_EXCEL_FILE[['Years', 'Exchange rate: Rwf per US dollar']]
    data['rate'] = data['Exchange rate: Rwf per US dollar'].pct_change()
    value = data[data['Years'] == items_value]['Exchange rate: Rwf per US dollar'].values[0]
    rate = np.round(data[data['Years'] == items_value]['rate'].values[0], 2)*100
    return [value], [f"{rate}%"]
