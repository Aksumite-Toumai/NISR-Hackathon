import pandas as pd  # type: ignore
from dash import dcc, html, callback, Output, Input  # type: ignore
import os
import dash_bootstrap_components as dbc  # type: ignore
from config import CONFIG
import logging


# Path to datasets main folder
DATASETS_PATH = ""
CPI_PATH = "CPI.xlsm"

# read the CPI excel file
CPI_EXCEL_FILE = None
if os.path.exists(CPI_PATH):
    CPI_EXCEL_FILE = pd.read_excel(CPI_PATH, sheet_name=None)
    logging.info('CPI file loaded...')


# read metadata
def read_metadata(sheet_name):
    data = pd.read_excel(CPI_PATH, sheet_name=sheet_name)
    metadata = data.iloc[:3, 3].dropna().tolist()
    return metadata


# Function to load the data based on the sheet name
def load_data(sheet_name):
    data = pd.read_excel(CPI_PATH, sheet_name=sheet_name, skiprows=3)
    data = data.iloc[:, 3:]  # Skip the first 3 columns
    data_cleaned = data.dropna(how='all')
    items_list = data_cleaned["Unnamed: 3"].unique().tolist()
    return data_cleaned, items_list


def generate_other_indices_plots():
    graphs = []
    data = CPI_EXCEL_FILE

    # Get the months
    months = pd.to_datetime(data["Urban"]["Date"][1:]).dt.strftime("%b %Y")

    # years
    years = sorted(pd.to_datetime(data["Urban"]["Date"][1:]).dt.year.unique())

    # Plot 1: Urban vs. Rural vs. All Rwanda CPI
    graph1 = dcc.Graph(
        id='plot1',
        figure={
            'data': [
                {'x': months, 'y': data["Urban"]["GENERAL INDEX (CPI)"][1:], 'type': 'line', 'name': 'Urban'},
                {'x': months, 'y': data["Rural"]["GENERAL INDEX (CPI)"][1:], 'type': 'line', 'name': 'Rural'},
                {'x': months, 'y': data["All Rwanda"]["GENERAL INDEX (CPI)"][1:], 'type': 'line', 'name': 'All Rwanda'}
            ],
            'layout': {
                'title': '',
                'xaxis': {
                    'tickangle': 45
                },
                'paper_bgcolor': 'rgb(243, 243, 243)',
                'plot_bgcolor': 'rgb(243, 243, 243)',
            }
        },
        config=CONFIG
    )

    graphs.append(dbc.Card([
        dbc.CardHeader("Urban vs. Rural vs. All Rwanda CPI", style={"color": "white", 'font-size': 20},),
        dbc.CardBody(
            [
                html.Div([
                    graph1
                ])
            ], style={"padding": "0"},
        ),
    ], color="#284fa1", outline=False))

    # Plot 2: Urban vs. Rural vs. All Rwanda Weights
    graph2 = dcc.Graph(
        id='plot2',
        figure={
            'data': [
                {'x': data["Urban"].columns[1:], 'y': data["Urban"].iloc[0, 1:], 'type': 'bar', 'name': 'Urban'},
                {'x': data["Rural"].columns[1:], 'y': data["Rural"].iloc[0, 1:], 'type': 'bar', 'name': 'Rural'},
                {'x': data["All Rwanda"].columns[1:], 'y': data["All Rwanda"].iloc[0, 1:], 'type': 'bar', 'name': 'All Rwanda'}
            ],
            'layout': {
                'title': '',
                'barmode': 'group',
                'paper_bgcolor': 'rgb(243, 243, 243)',
                'plot_bgcolor': 'rgb(243, 243, 243)',
            }
        }, config=CONFIG
    )
    graphs.append(dbc.Card([
        dbc.CardHeader("Urban vs. Rural vs. All Rwanda Weights", style={"color": "white", 'font-size': 20},),
        dbc.CardBody(
            [
                html.Div([
                    graph2
                ])
            ], style={"padding": "0"},
        ),
    ], color="#284fa1", outline=False))

    # Plot 3: CPI Yearly for Urban
    graph3 = dcc.Graph(id='combined-cpi-yearly-plot')

    graphs.append(dbc.Card([
        dbc.CardHeader([
            dbc.Row(
                [
                    dbc.Col(html.Span(id='cpi-year-title')),
                    dbc.Col([
                        # year selection
                        dcc.Dropdown(
                            id='cpi-year-dropdown',
                            options=[
                                {
                                    "label": html.Span(year, style={'color': 'black'}),
                                    "value": year,
                                } for year in years
                            ],
                            value=years[-1],  # Default value is the latest year
                            clearable=False
                        ),
                    ])
                ]
            )
        ], style={"color": "white", 'font-size': 20},),
        dbc.CardBody(
            [
                html.Div([
                    graph3
                ])
            ], style={"padding": "0"},
        ),
    ], color="#284fa1", outline=False))

    # Plot 4: CPI Yearly for Rural
    graph4 = dcc.Graph(id='combined-cpi-monthly-change-plot')

    graphs.append(dbc.Card([
        dbc.CardHeader([
            dbc.Row(
                [
                    dbc.Col(html.Span(id='cpi-year-title-2')),
                    dbc.Col([
                        # year selection
                        dcc.Dropdown(
                            id='cpi-year-dropdown-2',
                            options=[
                                {
                                    "label": html.Span(year, style={'color': 'black'}),
                                    "value": year,
                                } for year in years
                            ],
                            value=years[-1],  # Default value is the latest year
                            clearable=False
                        ),
                    ])
                ]
            )
        ], style={"color": "white", 'font-size': 20},),
        dbc.CardBody(
            [
                html.Div([
                    graph4
                ])
            ], style={"padding": "0"},
        ),
    ], color="#284fa1", outline=False))

    return graphs


def get_content():
    graphs = generate_other_indices_plots()
    content = html.Div([
        dbc.Row(
            [
                dbc.Col(graphs[0], width=6),
                dbc.Col(graphs[1], width=6),
            ],
            className="mb-3 py-0 px-0",
        ),
        dbc.Row(
            [
                dbc.Col(graphs[2], width=6),
                dbc.Col(graphs[3], width=6),
            ],
            className="mb-3 py-0 px-0",
        ),
        dbc.Row(
            [
                dbc.Col(width=6),
            ],
            className="mb-3 py-0 px-0",
        ),
    ])
    return [html.Div([
        dbc.Row(
            [
                dbc.Col(width=3),
                dbc.Col(width=3),
                dbc.Col(width=3),
            ],
            className="mb-3 mt-2 py-0 px-0",
        ),
        html.Div([content], id="graphs-container", style={'background-color': '#DCDCDC', "margin-top": "0rem"})])
    ]


@callback(
        [Output('combined-cpi-yearly-plot', 'figure'),
         Output('cpi-year-title', 'children')],
        [Input('cpi-year-dropdown', 'value')]
)
def update_graph(selected_year):
    mask_urban = pd.to_datetime(CPI_EXCEL_FILE["Urban"]["Date"][1:]).dt.year == selected_year
    mask_rural = pd.to_datetime(CPI_EXCEL_FILE["Rural"]["Date"][1:]).dt.year == selected_year
    mask_all_rwanda = pd.to_datetime(CPI_EXCEL_FILE["All Rwanda"]["Date"][1:]).dt.year == selected_year

    graph = {
        'data': [
            {
                'x': pd.to_datetime(CPI_EXCEL_FILE["Urban"]["Date"][1:]).dt.strftime('%B').iloc[mask_urban.values],
                'y': CPI_EXCEL_FILE["Urban"]["GENERAL INDEX (CPI)"][1:].iloc[mask_urban.values],
                'type': 'line',
                'name': 'Urban'
            },
            {
                'x': pd.to_datetime(CPI_EXCEL_FILE["Rural"]["Date"][1:]).dt.strftime('%B').iloc[mask_rural.values],
                'y': CPI_EXCEL_FILE["Rural"]["GENERAL INDEX (CPI)"][1:].iloc[mask_rural.values],
                'type': 'line',
                'name': 'Rural'
            },
            {
                'x': pd.to_datetime(CPI_EXCEL_FILE["All Rwanda"]["Date"][1:]).dt.strftime('%B').iloc[mask_all_rwanda.values],
                'y': CPI_EXCEL_FILE["All Rwanda"]["GENERAL INDEX (CPI)"][1:].iloc[mask_all_rwanda.values],
                'type': 'line',
                'name': 'All Rwanda'
            }
        ],
        'layout': {
            'title': '',
            'xaxis': {
                'ticktext': ['January', 'February', 'March', 'April', 'May',
                             'June', 'July', 'August', 'September', 'October', 'November', 'December']
            },
            'paper_bgcolor': 'rgb(243, 243, 243)',
            'plot_bgcolor': 'rgb(243, 243, 243)',
        }
    }
    title = f'CPI Monthly for {selected_year}'
    return graph, title


@callback(
        [Output('combined-cpi-monthly-change-plot', 'figure'),
         Output('cpi-year-title-2', 'children')],
        [Input('cpi-year-dropdown-2', 'value')]
)
def update_monthly_change_graph(selected_year):
    mask_urban = pd.to_datetime(CPI_EXCEL_FILE["Urban"]["Date"][1:]).dt.year == selected_year
    mask_rural = pd.to_datetime(CPI_EXCEL_FILE["Rural"]["Date"][1:]).dt.year == selected_year
    mask_all_rwanda = pd.to_datetime(CPI_EXCEL_FILE["All Rwanda"]["Date"][1:]).dt.year == selected_year
    monthly_change_urban = CPI_EXCEL_FILE["Urban"]["GENERAL INDEX (CPI)"][1:].pct_change() * 100
    monthly_change_rural = CPI_EXCEL_FILE["Rural"]["GENERAL INDEX (CPI)"][1:].pct_change() * 100
    monthly_change_all_rwanda = CPI_EXCEL_FILE["All Rwanda"]["GENERAL INDEX (CPI)"][1:].pct_change() * 100

    graph = {
        'data': [
            {
                'x': pd.to_datetime(CPI_EXCEL_FILE["Urban"]["Date"][1:]).dt.strftime('%B').iloc[mask_urban.values],
                'y': monthly_change_urban.iloc[mask_urban.values],
                'type': 'line',
                'name': 'Urban'
            },
            {
                'x': pd.to_datetime(CPI_EXCEL_FILE["Rural"]["Date"][1:]).dt.strftime('%B').iloc[mask_rural.values],
                'y': monthly_change_rural.iloc[mask_rural.values],
                'type': 'line',
                'name': 'Rural'
            },
            {
                'x': pd.to_datetime(CPI_EXCEL_FILE["All Rwanda"]["Date"][1:]).dt.strftime('%B').iloc[mask_all_rwanda.values],
                'y': monthly_change_all_rwanda.iloc[mask_all_rwanda.values],
                'type': 'line',
                'name': 'All Rwanda'
            }
        ],
        'layout': {
            'title': "",
            'xaxis': {
                'ticktext': ['January', 'February', 'March', 'April', 'May', 'June',
                             'July', 'August', 'September', 'October', 'November', 'December']
            },
            'yaxis': {
                'title': 'Monthly Change (%)'
            },
            'paper_bgcolor': 'rgb(243, 243, 243)',
            'plot_bgcolor': 'rgb(243, 243, 243)',
        }
    }
    title = f'CPI Monthly Change for {selected_year}'
    return graph, title
