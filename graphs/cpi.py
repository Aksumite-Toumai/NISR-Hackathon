import pandas as pd
from dash import dcc, html
import os
import dash_bootstrap_components as dbc
from config import CONFIG
import logging


DATASETS_PATH = os.environ.get("DATA_PATH")
CPI_PATH = os.path.join(DATASETS_PATH, "Consumer Price Index/CPI.xlsm")

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
    data = CPI_EXCEL_FILE.copy()

    # Get the months
    months = pd.to_datetime(data["Urban"]["Date"][1:]).dt.strftime("%b %Y")

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
    graph3 = dcc.Graph(
        id='plot3',
        figure={
            'data': [
                {
                    'x': pd.to_datetime(data["Urban"]["Date"][1:]).dt.strftime('%B').iloc[mask.values],
                    'y': data["Urban"]["GENERAL INDEX (CPI)"][1:].iloc[mask.values],
                    'type': 'line',
                    'name': str(year)
                }
                for year in pd.to_datetime(data["Urban"]["Date"][1:]).dt.year.unique()
                for mask in [pd.to_datetime(data["Urban"]["Date"][1:]).dt.year == year]
            ],
            'layout': {
                'title': '',
                'xaxis': {
                    'ticktext': ['January', 'February', 'March', 'April', 'May', 'June', 'July',
                                 'August', 'September', 'October', 'November', 'December']
                },
                'paper_bgcolor': 'rgb(243, 243, 243)',
                'plot_bgcolor': 'rgb(243, 243, 243)',
            }
        }, config=CONFIG
    )

    graphs.append(dbc.Card([
        dbc.CardHeader("CPI Yearly (Urban)", style={"color": "white", 'font-size': 20},),
        dbc.CardBody(
            [
                html.Div([
                    graph3
                ])
            ], style={"padding": "0"},
        ),
    ], color="#284fa1", outline=False))

    # Plot 4: CPI Yearly for Rural
    graph4 = dcc.Graph(
        id='plot4',
        figure={
            'data': [
                {
                    'x': pd.to_datetime(data["Rural"]["Date"][1:]).dt.strftime('%B').iloc[mask.values],
                    'y': data["Rural"]["GENERAL INDEX (CPI)"][1:].iloc[mask.values],
                    'type': 'line',
                    'name': str(year)
                }
                for year in pd.to_datetime(data["Rural"]["Date"][1:]).dt.year.unique()
                for mask in [pd.to_datetime(data["Rural"]["Date"][1:]).dt.year == year]
            ],
            'layout': {
                'title': 'CPI Yearly (Rural)',
                'xaxis': {
                    'ticktext': ['January', 'February', 'March', 'April', 'May', 'June',
                                 'July', 'August', 'September', 'October', 'November', 'December']
                },
                'paper_bgcolor': 'rgb(243, 243, 243)',
                'plot_bgcolor': 'rgb(243, 243, 243)',
            }
        },
        config=CONFIG
    )
    graphs.append(dbc.Card([
        dbc.CardHeader("CPI Yearly (Rural)", style={"color": "white", 'font-size': 20},),
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
