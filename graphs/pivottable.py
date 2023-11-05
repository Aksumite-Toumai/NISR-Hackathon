import dash_pivottable  # type: ignore
from dash import html, dcc, callback, Input, Output, State  # type: ignore
import os
import dash_bootstrap_components as dbc  # type: ignore
import pandas as pd  # type: ignore
import numpy as np  # type: ignore
from graphs import gdp  # type: ignore
from typing import List


DATASETS_PATH = ""
DATASETS = {
    "Consumer Price Index": "CPI_time_series_November_2022.xls",
    "GDP National Accounts": "R_GDP National Accounts 2022_r.xls",
}
CURRENT_DATA: List = []
OPTIONS: List = []


# Create the dropdown button to select a dataset
def get_dropdown_datasets():
    card_content = [
        dbc.CardHeader("Datasets", style={"color": "#284fa1", 'font-size': 20}),
        dbc.CardBody(
            [
                html.P("Select a dataset:", className="card-title", style={"color": "#284fa1"}),
                dcc.Dropdown(
                    id='dataset-dropdown',
                    options=[
                            {
                                "label": html.Span(['Consumer Price Index'], style={'color': 'black', 'font-size': 20}),
                                "value": "Consumer Price Index",
                            },
                            {
                                "label": html.Span(['GDP National Accounts'], style={'color': 'black', 'font-size': 20}),
                                "value": "GDP National Accounts",
                            },
                    ],
                    value='Consumer Price Index',
                    clearable=False,
                ),
            ],
        ),
    ]
    return dbc.Card(card_content, color="white", style={"color": "#284fa1"})


# Create the dropdown button to select a Sheet Name
def get_dropdown_dataset_sheet_names():
    card_content = [
        dbc.CardHeader("Sheets", style={"color": "#284fa1", 'font-size': 20}),
        dbc.CardBody(
            [
                html.P("Select a sheet name:", className="card-title", style={"color": "#284fa1"}),
                dcc.Dropdown(
                    id='sheetnames-dropdown',
                    clearable=False,
                ),
            ],
        ),
    ]
    return dbc.Card(card_content, color="white", style={"color": "#284fa1"})


def get_content():
    pivot_table = dbc.Col(
        id="pivotTlayout",
        style={'background-color': '#DCDCDC', "margin-top": "0rem"},
        width=9
    )

    return [html.Div([
        dbc.Row(
            [
                dbc.Col(get_dropdown_datasets(), width=3),
                dbc.Col(get_dropdown_dataset_sheet_names(), width=3),
                dbc.Col(width=3),
            ],
            className="mb-3 mt-2 py-0 px-0",
        ),
        html.Hr(),
        dbc.Row(pivot_table, className="mb-3 mt-2 py-0 px-0", style={'background-color': '#DCDCDC', "margin-top": "0rem"})])
    ]


# Function to find the list of sheetnames
@callback([Output("sheetnames-dropdown", "options")],
          [Input("dataset-dropdown", "value")])
def render_sheetnames_content(val):
    path = os.path.join(DATASETS_PATH, DATASETS[val])
    excel_file = pd.ExcelFile(path)
    OPTIONS = [
                {
                    "label": html.Span([sh], style={'color': 'black', 'font-size': 20}),
                    "value": sh,
                } for sh in excel_file.sheet_names
            ]
    return [OPTIONS]


# Function to render the pivot page
@callback([Output("pivotTlayout", "children")],
          [Input("sheetnames-dropdown", "value"), State("dataset-dropdown", "value")])
def render_pivot_page_content(val1, val2):
    data = np.vstack([gdp.GDP_EXCEL_FILE.columns, gdp.GDP_EXCEL_FILE.values])
    if val2 == "Consumer Price Index":
        # path = os.path.join(DATASETS_PATH, DATASETS[val2])
        # df = pd.read_excel(path, val1, skiprows=3, header=None)
        # items_list = ['date'] + df[3].unique().tolist()
        # data = df.iloc[:, 4:]  # Skip the first 3 columns
        # data_cleaned = data.dropna(how='all').T

        # d = pd.DataFrame({
        #     'Category': items_list,
        #     'Value': data_cleaned.values.tolist()
        # })

        pivot_table = dash_pivottable.PivotTable(
            data=data,
        )
        return [html.Div(pivot_table)]
    else:
        pivot_table = dash_pivottable.PivotTable(
            data=data
        )
        return [html.Div(pivot_table)]
