from dash import html
import dash_bootstrap_components as dbc
import os


DATASETS_PATH = os.environ.get("DATA_PATH")
GDP_PATH = os.path.join(DATASETS_PATH, "GDP National Accounts/R_GDP National Accounts 2022_r.xls")


def get_content():
    return [html.Div([
        dbc.Row(
            [
                dbc.Col(width=3),
                dbc.Col([
                    dbc.Card(
                        dbc.CardBody(
                            [
                                html.H5("Details", className="card-title", style={"color": "#284fa1", 'font-size': 20}),
                                html.P("", id="sheet_details", style={"color": "#696969"}),
                            ]
                        )
                    ),
                ], width=3),
                dbc.Col(width=3),
            ],
            className="mb-3 mt-2 py-0 px-0",
        ),
        html.Div(id="graphs-container", style={'background-color': '#DCDCDC', "margin-top": "0rem"})])
    ]
