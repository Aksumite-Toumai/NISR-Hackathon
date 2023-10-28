from dash import html, dcc, dash_table
import dash_bootstrap_components as dbc
from dash import callback, Output, Input
from graphs import gdp


def get_dropdown_sheetnames():
    card_content = [
        dbc.CardHeader("Datasets", style={"color": "#284fa1", 'font-size': 20}),
        dbc.CardBody(
            [
                html.P("Select a dataset:", className="card-title", style={"color": "#284fa1"}),
                dcc.Dropdown(
                    id='view-dataset-dropdown',
                    options=[
                            {
                                "label": html.Span(['GDP National Accounts'], style={'color': 'black', 'font-size': 20}),
                                "value": "GDP",
                            },
                            {
                                "label": html.Span(['Consumer Price Index'], style={'color': 'black', 'font-size': 20}),
                                "value": "CPI",
                            },
                    ],
                    value='GDP',
                    clearable=False,
                ),
            ],
        ),
    ]
    return dbc.Card(card_content, color="white", style={"color": "#284fa1"})


def get_content():
    table = dash_table.DataTable(
        data=gdp.GDP_EXCEL_FILE.to_dict('records'),
        sort_action='native',
        filter_action='native',
        filter_options={"placeholder_text": "Filter column..."},
        style_header={
            'backgroundColor': '#284fa1',
            'color': 'white',
            'fontWeight': 'bold'
        },
        # style_data={
        #     'backgroundColor': 'rgb(50, 50, 50)',
        #     'color': 'white'
        #  },
        columns=[
            {"name": i, "id": i} for i in gdp.GDP_EXCEL_FILE.columns
        ],
    )
    return [html.Div([
        dbc.Row(
            [
                dbc.Col(get_dropdown_sheetnames(), width=3),
                dbc.Col(),
                dbc.Col(),
            ],
            className="mb-3 mt-2 py-0 px-0",
        ),
        html.Div([table],
                 id="graphs-container",
                 style={'background-color': '#DCDCDC', "margin-top": "0rem", "overflow": "scroll"})])
    ]
