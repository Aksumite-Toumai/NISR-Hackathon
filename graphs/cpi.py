import pandas as pd
from dash import dcc, html
import plotly.graph_objs as go
import os
import dash_bootstrap_components as dbc
import dash.dependencies as dd
from dash import callback
from config import CONFIG


DATASETS_PATH = os.environ.get("DATA_PATH")
CPI_PATH = os.path.join(DATASETS_PATH, "Consumer Price Index/CPI_time_series_November_2022.xls")


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


def generate_other_indices_plots(data_cleaned):
    graphs = []

    # 1. Local vs. Imported Goods Index
    local_goods = data_cleaned[data_cleaned["Unnamed: 3"] == "Local Goods Index"].iloc[0, 1:].values
    imported_goods = data_cleaned[data_cleaned["Unnamed: 3"] == "Imported Goods Index"].iloc[0, 1:].values

    graph1 = dcc.Graph(
        figure={
            'data': [
                go.Scatter(x=data_cleaned.columns[1:], y=local_goods, mode='lines', name="Local Goods Index"),
                go.Scatter(x=data_cleaned.columns[1:], y=imported_goods, mode='lines', name="Imported Goods Index")
            ],
            'layout': go.Layout(
                xaxis={'title': 'Date'},
                yaxis={'title': 'Index Value'},
                hovermode='closest',
                legend={'x': 0, 'y': 2, 'orientation': 'h'}

            )
        }, config=CONFIG
    )

    graphs.append(dbc.Card([
        dbc.CardHeader("Local vs. Imported Goods Index Over Time", style={"color": "white", 'font-size': 20},),
        dbc.CardBody(
            [
                html.Div([
                    graph1
                ])
            ], style={"padding": "0"},
        ),
    ], color="#284fa1", outline=False))

    # 2. Different Categories of Goods
    categories = [
        "Food and non-alcoholic beverages",
        "Housing, water, electricity, gas and other fuels",
        "Transport",
        "Furnishing, household equipment"
    ]

    graph2 = dcc.Graph(
        figure={
            'data': [
                go.Scatter(
                    x=data_cleaned.columns[1:],
                    y=data_cleaned[data_cleaned["Unnamed: 3"] == category].iloc[0, 1:].values,
                    mode='lines',
                    name=category
                ) for category in categories
            ],
            'layout': go.Layout(
                xaxis={'title': 'Date'},
                yaxis={'title': 'Index Value'},
                hovermode='closest',
                legend={'x': 0, 'y': 2, 'orientation': 'h'}
            )
        }, config=CONFIG
    )
    graphs.append(dbc.Card([
        dbc.CardHeader("Different Categories of Goods Over Time", style={"color": "white", 'font-size': 20},),
        dbc.CardBody(
            [
                html.Div([
                    graph2
                ])
            ], style={"padding": "0"},
        ),
    ], color="#284fa1", outline=False))

    # 3. Special Indices
    special_indices = [
        "Fresh Products(1) index",
        "Energy index",
        "General Index excluding fresh Products and energy(2)"
    ]

    graph3 = dcc.Graph(
        figure={
            'data': [
                go.Scatter(
                    x=data_cleaned.columns[1:],
                    y=data_cleaned[data_cleaned["Unnamed: 3"] == index].iloc[0, 1:].values,
                    mode='lines',
                    name=index
                ) for index in special_indices
            ],
            'layout': go.Layout(
                xaxis={'title': 'Date'},
                yaxis={'title': 'Index Value'},
                hovermode='closest',
                legend={'x': 0, 'y': 2, 'orientation': 'h'}
            )
        }, config=CONFIG
    )
    graphs.append(dbc.Card([
        dbc.CardHeader("Special Indices Over Time", style={"color": "white", 'font-size': 20},),
        dbc.CardBody(
            [
                html.Div([
                    graph3
                ])
            ], style={"padding": "0"},
        ),
    ], color="#284fa1", outline=False))

    return graphs


def get_dropdown_sheetnames():
    card_content = [
        dbc.CardHeader("Sheet Names", style={"color": "#284fa1", 'font-size': 20}),
        dbc.CardBody(
            [
                html.P("Select a sheet name:", className="card-title", style={"color": "#284fa1"}),
                dcc.Dropdown(
                    id='sheet-dropdown',
                    options=[
                            {
                                "label": html.Span(['Urban'], style={'color': 'black', 'font-size': 20}),
                                "value": "Urban",
                            },
                            {
                                "label": html.Span(['Rural'], style={'color': 'black', 'font-size': 20}),
                                "value": "Rural",
                            },
                            {
                                "label": html.Span(['All Rwanda'], style={'color': 'black', 'font-size': 20}),
                                "value": "All Rwanda",
                            },
                            {
                                "label": html.Span(['Other Indices'], style={'color': 'black', 'font-size': 20}),
                                "value": "Other_Indices",
                            },
                    ],
                    value='Urban',
                    clearable=False,
                ),
            ],
        ),
    ]
    return dbc.Card(card_content, color="white", style={"color": "#284fa1"})


# Raw indices plot
def get_raw_indice_plot(URBAN_DATA_CLEANED, items_list):
    card_content = [
        dbc.CardHeader("Indices Over Time", style={"color": "white", 'font-size': 20},),
        dbc.CardBody(
            [
                html.Div([
                    dcc.Graph(
                        id='raw-indices-graph',
                        figure={
                            'data': [
                                go.Scatter(
                                    x=URBAN_DATA_CLEANED.columns[2:],
                                    y=URBAN_DATA_CLEANED[URBAN_DATA_CLEANED["Unnamed: 3"] == item].iloc[:, 2:].values.flatten(),
                                    mode='lines',
                                    name=item
                                ) for item in items_list
                            ],
                            'layout': go.Layout(
                                xaxis={
                                    'title': 'Date',
                                    'tickvals': [URBAN_DATA_CLEANED.
                                                 columns[2:][i] for i in range(0, len(URBAN_DATA_CLEANED.columns[2:]), 12)],
                                    'ticktext': [str(year) for year in range(2009, 2023)]
                                },
                                yaxis={'title': 'Index Value'},
                                hovermode='closest',
                                legend={'x': 0, 'y': 2, 'orientation': 'h'}
                            )
                        }, config=CONFIG
                    )
                ])
            ], style={"padding": "0"},
        ),
    ]
    return dbc.Card(card_content, color="#284fa1", )


# Annual changes plot
def get_annual_change_plot(annual_changes, items_list):
    card_content = [
        dbc.CardHeader("Annual Changes Over Time", style={"color": "white", 'font-size': 20},),
        dbc.CardBody(
            [
                html.Div([
                    dcc.Graph(
                        id='annual-changes-graph',
                        figure={
                            'data': [
                                go.Scatter(
                                    x=annual_changes.columns[1:],
                                    y=annual_changes[annual_changes["Unnamed: 3"] == item].iloc[:, 1:].values.flatten() * 100,
                                    mode='lines',
                                    name=item
                                ) for item in items_list
                            ],
                            'layout': go.Layout(
                                xaxis={
                                    'title': 'Date',
                                    'tickvals': [annual_changes.
                                                 columns[1:][i] for i in range(0, len(annual_changes.columns[1:]), 12)],
                                    'ticktext': [str(year) for year in range(2009, 2023)]
                                },
                                yaxis={'title': 'Percentage Change'},
                                hovermode='closest',
                                legend={'x': 0, 'y': 2, 'orientation': 'h'}
                            )
                        }, style={"padding": "0"}, config=CONFIG
                    ),
                ], style={"padding": "0"},)
            ], style={"padding": "0"},
        ),
    ]
    return dbc.Card(card_content, color="#284fa1",)


# Monthly changes for "GENERAL INDEX (CPI)" plot
def get_monthly_change_general_index(monthly_changes_cpi):
    card_content = [
        dbc.CardHeader("Monthly changes for GENERAL INDEX (CPI)", style={"color": "white", 'font-size': 20},),
        dbc.CardBody(
            [
                html.Div([
                    dcc.Graph(
                        id='monthly-changes-cpi-graph',
                        figure={
                            'data': [
                                go.Scatter(
                                    x=monthly_changes_cpi.columns[1:],
                                    y=monthly_changes_cpi.iloc[0, 1:].values * 100,  # Multiply by 100 to get percentage
                                    mode='lines',
                                    name='GENERAL INDEX (CPI) Monthly Changes'
                                )
                            ],
                            'layout': go.Layout(
                                title='',
                                xaxis={
                                    'title': 'Date',
                                    'tickvals': [monthly_changes_cpi.\
                                                 columns[1:][i] for i in range(0, len(monthly_changes_cpi.columns[1:]), 12)],
                                    'ticktext': [str(year) for year in range(2009, 2023)]
                                },
                                yaxis={'title': 'Percentage Change'},
                                hovermode='closest',
                                legend={'x': 0, 'y': 2, 'orientation': 'h'}
                            )
                        }, style={"padding": "0"}, config=CONFIG
                    ),
                ], style={"padding": "0"},)
            ], style={"padding": "0"},
        ),
    ]
    return dbc.Card(card_content, color="#284fa1",)


# Plot for "GENERAL INDEX (CPI)" for Each Month Across Years
def get_change_across_years_general_index(cpi_yearly_pivot):
    card_content = [
        dbc.CardHeader("GENERAL INDEX (CPI) for Each Year Across Months", style={"color": "white", 'font-size': 20},),
        dbc.CardBody(
            [
                html.Div([
                    dcc.Graph(
                        id='cpi-yearly-across-months-graph',
                        figure={
                            'data': [
                                go.Scatter(
                                    x=cpi_yearly_pivot.index,
                                    y=cpi_yearly_pivot[month],
                                    mode='lines+markers',
                                    name=month
                                ) for month in cpi_yearly_pivot.columns
                            ],
                            'layout': go.Layout(
                                title='',
                                xaxis={'title': 'Year'},
                                yaxis={'title': 'GENERAL INDEX (CPI)'},
                                hovermode='closest',
                                legend={'title': 'Month', 'x': 0, 'y': 2, 'orientation': 'h'}
                            )
                        }, style={"padding": "0"}, config=CONFIG
                    )
                ], style={"padding": "0"},)
            ], style={"padding": "0"},
        ),
    ]
    return dbc.Card(card_content, color="#284fa1",)


# # Plot for "GENERAL INDEX (CPI)" for Each Year Across Months
def get_change_across_month_general_index(cpi_monthly_pivot):
    card_content = [
        dbc.CardHeader("GENERAL INDEX (CPI) for Each Month Across Years", style={"color": "white", 'font-size': 20},),
        dbc.CardBody(
            [
                html.Div([
                    dcc.Graph(
                        id='cpi-monthly-across-years-graph',
                        figure={
                            'data': [
                                go.Scatter(
                                    x=cpi_monthly_pivot.index,
                                    y=cpi_monthly_pivot[year],
                                    mode='lines+markers',
                                    name=str(year)
                                ) for year in cpi_monthly_pivot.columns
                            ],
                            'layout': go.Layout(
                                xaxis={'title': 'Month'},
                                yaxis={'title': 'GENERAL INDEX (CPI)'},
                                hovermode='closest',
                                legend={'title': 'Year', 'x': 0, 'y': 2, 'orientation': 'h'},
                            )
                        }, config=CONFIG
                    ),
                ])
            ], style={"padding": "0"},
        ),
    ]
    return dbc.Card(card_content, color="#284fa1", outline=False)


@callback(
    [dd.Output('graphs-container', 'children'), dd.Output('sheet_details', 'children')],
    [dd.Input('sheet-dropdown', 'value')]
)
def update_cpi_graphs(sheet_name):
    data_cleaned, items_list = load_data(sheet_name)
    details = []
    for d in read_metadata(sheet_name):
        details.append(d)
        details.append(html.Br())

    if sheet_name == "Other_Indices":
        graphs = generate_other_indices_plots(data_cleaned)
        content = html.Div([
            dbc.Row(
                [
                    dbc.Col(graphs[0]),
                    dbc.Col(graphs[1]),
                ],
                className="mb-3 py-0 px-0",
            ),
            dbc.Row(
                [
                    dbc.Col(graphs[2]),
                    dbc.Col(graphs[2]),
                ],
                className="mb-3 py-0 px-0",
            ),
            dbc.Row(
                [
                    dbc.Col(graphs[2]),
                ],
                className="mb-3 py-0 px-0",
            ),
        ])
        return content, details
    # Calculate annual changes (year-over-year percentage change)
    annual_changes = data_cleaned.set_index("Unnamed: 3").iloc[:, 2:].transpose().pct_change(12).transpose().reset_index()

    # Calculate month-over-month changes for "GENERAL INDEX (CPI)"
    monthly_changes_cpi = data_cleaned[data_cleaned["Unnamed: 3"] == "GENERAL INDEX (CPI)"].iloc[:, 2:].transpose().\
        pct_change().transpose().reset_index()

    # Process the data for the "GENERAL INDEX (CPI)" plots
    cpi_data_raw = data_cleaned[data_cleaned["Unnamed: 3"] == "GENERAL INDEX (CPI)"]
    cpi_data = cpi_data_raw.iloc[:, 2:].transpose()
    cpi_data.index = pd.to_datetime(cpi_data.index)
    cpi_data['Year'] = cpi_data.index.year
    cpi_data['Month'] = cpi_data.index.strftime('%B')
    cpi_monthly_pivot = cpi_data.pivot(index='Month', columns='Year', values=cpi_data.columns[0])
    cpi_yearly_pivot = cpi_data.pivot(index='Year', columns='Month', values=cpi_data.columns[0])

    content = html.Div([
        dbc.Row(
            [
                dbc.Col(get_raw_indice_plot(data_cleaned, items_list)),
                dbc.Col(get_annual_change_plot(annual_changes, items_list)),
            ],
            className="mb-3 py-0 px-0",
        ),
        dbc.Row(
            [
                dbc.Col(get_monthly_change_general_index(monthly_changes_cpi)),
                dbc.Col(get_change_across_years_general_index(cpi_yearly_pivot)),
            ],
            className="mb-3 py-0 px-0",
        ),
        dbc.Row(
            [
                dbc.Col(get_change_across_month_general_index(cpi_monthly_pivot)),
            ],
            className="mb-3 py-0 px-0",
        ),
    ])

    # Return the list of graphs
    return content, details


def get_content():
    return [html.Div([
        dbc.Row(
            [
                dbc.Col(get_dropdown_sheetnames(), width=3),
                dbc.Col([
                    dbc.Card(
                        dbc.CardBody(
                            [
                                html.H5("Sheet Details", className="card-title", style={"color": "#284fa1", 'font-size': 20}),
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
