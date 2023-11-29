from dash import html, callback, Output, Input, dcc  # type: ignore
import dash_bootstrap_components as dbc  # type: ignore
import dash  # type: ignore
import pandas as pd  # type: ignore
from config import CONFIG
import plotly.express as px  # type: ignore
from data import CPI_EXCEL_FILE


dash.register_page(__name__)

data = CPI_EXCEL_FILE

# Get the months
months = pd.to_datetime(data["Urban"]["Date"][1:]).dt.strftime("%b %Y")  # type: ignore

# years
years = sorted(pd.to_datetime(data["Urban"]["Date"][1:]).dt.year.unique())  # type: ignore

graphs = []

# Plot 1: Urban vs. Rural vs. All Rwanda CPI
graph1 = dcc.Graph(
    id='plot1',
    figure={
        'data': [
            {'x': months, 'y': data["Urban"]["GENERAL INDEX (CPI)"][1:], 'type': 'line', 'name': 'Urban'},  # type: ignore
            {'x': months, 'y': data["Rural"]["GENERAL INDEX (CPI)"][1:], 'type': 'line', 'name': 'Rural'},  # type: ignore
            {'x': months, 'y': data["All Rwanda"]["GENERAL INDEX (CPI)"][1:], 'type': 'line', 'name': 'All Rwanda'}  # type: ignore  # noqa
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
    dbc.CardHeader(dbc.Col("Urban vs. Rural vs. All Rwanda CPI", className="figCard"), className="figTitle"),
    dbc.CardBody(
        [
            html.Div([
                graph1
            ])
        ], style={"padding": "0"},
    ),
], outline=False))

# Plot 2: Urban vs. Rural vs. All Rwanda Weights
graph2 = dcc.Graph(
    id='plot2',
    figure={
        'data': [
            {'x': data["Urban"].columns[1:], 'y': data["Urban"].iloc[0, 1:], 'type': 'bar', 'name': 'Urban'},  # type: ignore
            {'x': data["Rural"].columns[1:], 'y': data["Rural"].iloc[0, 1:], 'type': 'bar', 'name': 'Rural'},  # type: ignore
            {'x': data["All Rwanda"].columns[1:], 'y': data["All Rwanda"].iloc[0, 1:], 'type': 'bar', 'name': 'All Rwanda'}  # type: ignore  # noqa
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
    dbc.CardHeader(dbc.Col("Urban vs. Rural vs. All Rwanda Weights", className="figCard"), className="figTitle"),
    dbc.CardBody(
        [
            html.Div([
                graph2
            ])
        ], style={"padding": "0"},
    ),
], outline=False))

# Plot 3: CPI Yearly for Urban
graph3 = dcc.Graph(id='combined-cpi-yearly-plot', config=CONFIG)

graphs.append(dbc.Card([
    dbc.CardHeader([
        dbc.Row(
            [
                dbc.Col(id='cpi-year-title', className="figCard"),
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
    ], className="figTitle"),
    dbc.CardBody(
        [
            html.Div([
                graph3
            ])
        ], style={"padding": "0"},
    ),
], outline=False))

# Plot 4: CPI Yearly for Rural
graph4 = dcc.Graph(id='combined-cpi-monthly-change-plot', config=CONFIG)

graphs.append(dbc.Card([
    dbc.CardHeader([
        dbc.Row(
            [
                dbc.Col(id='cpi-year-title-2', className="figCard"),
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
    ], className="figTitle"),
    dbc.CardBody(
        [
            html.Div([
                graph4
            ])
        ], style={"padding": "0"},
    ),
], outline=False))

graph5 = dcc.Graph(id='combined-cpi-monthly-change-histogram', config=CONFIG)
graphs.append(dbc.Card([
    dbc.CardHeader([
        dbc.Row(
            [
                dbc.Col("CPI Values", id='cpi-year-title-3', className="figCard"),
                dbc.Col([
                    # year selection
                    dcc.Dropdown(
                        id='cpi-year-dropdown-3',
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
    ], className="figTitle"),
    dbc.CardBody(
        [
            html.Div([
                graph5
            ])
        ], style={"padding": "0"},
    ),
], outline=False))

graph6 = dcc.Graph(id='cpi-bar-chart', config=CONFIG)
regions = ['Urban', 'Rural', 'All Rwanda']
graphs.append(dbc.Card([
    dbc.CardHeader([
        dbc.Row(
            [
                dbc.Col("Monthly CPI Values by Year", id='cpi-year-title-6', className="figCard"),
                dbc.Col([
                    # year selection
                    dcc.Dropdown(
                        id='cpi-region-selector-dropdown',
                        options=[
                            {
                                "label": html.Span(region, style={'color': 'black'}),
                                "value": region,
                            } for region in regions
                        ],
                        value=regions[0],  # Default value is the latest year
                        clearable=False
                    ),
                ])
            ]
        )
    ], className="figTitle"),
    dbc.CardBody(
        [
            html.Div([
                graph6
            ])
        ], style={"padding": "0"},
    ),
], outline=False))


# Render the CPI content
def layout():
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
                dbc.Col(graphs[4], width=5),
                dbc.Col(graphs[5], width=7),
            ],
            className="mb-3 py-0 px-0",
        ),
    ])

    return [html.Div([
        html.Div(
            html.H1("Dashboard > Consumer Price Index", className="h5 mb-0 text-gray-800"),
            className="d-sm-flex align-items-center justify-content-between mb-4",
        ),
        html.Div([content], id="graphs-container")])]


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


@callback(
    Output('combined-cpi-monthly-change-histogram', 'figure'),
    [Input('cpi-year-dropdown-3', 'value')]
)
def update_cpi_histogram(selected_year):
    data = CPI_EXCEL_FILE
    mask_urban = pd.to_datetime(data["Urban"]["Date"][1:]).dt.year == selected_year
    mask_rural = pd.to_datetime(data["Rural"]["Date"][1:]).dt.year == selected_year
    mask_all_rwanda = pd.to_datetime(data["All Rwanda"]["Date"][1:]).dt.year == selected_year

    cpi_urban = data["Urban"]["GENERAL INDEX (CPI)"][1:][mask_urban]
    cpi_rural = data["Rural"]["GENERAL INDEX (CPI)"][1:][mask_rural]
    cpi_all_rwanda = data["All Rwanda"]["GENERAL INDEX (CPI)"][1:][mask_all_rwanda]

    cpi_data = pd.DataFrame({'Urban': cpi_urban, 'Rural': cpi_rural, 'All Rwanda': cpi_all_rwanda}).reset_index(drop=True)

    long_format_data = cpi_data.melt(var_name='Region', value_name='CPI')

    fig = px.histogram(long_format_data, x='CPI', color='Region', barmode='overlay')

    fig.update_layout(title='', xaxis_title='CPI', yaxis_title='Count')

    return fig


# Callback to update the bar chart based on the selected region
@callback(
    Output('cpi-bar-chart', 'figure'),
    [Input('cpi-region-selector-dropdown', 'value')]
)
def update_cpi_chart(selected_region):
    sheet_data = data[selected_region].iloc[1:]
    sheet_data['Date'] = pd.to_datetime(sheet_data['Date'])
    sheet_data['Year'] = sheet_data['Date'].dt.year
    sheet_data['MonthName'] = sheet_data['Date'].dt.strftime('%b')
    sheet_data['CPI'] = sheet_data.iloc[:, 1]
    sheet_data.sort_values(by='Date', inplace=True)
    pivot_data = sheet_data.pivot_table(index='Year', columns='MonthName', values='CPI', aggfunc='mean')
    pivot_data.reset_index(inplace=True)
    month_order = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    pivot_data = pivot_data.reindex(columns=['Year'] + month_order)
    fig = px.bar(pivot_data, x='Year', y=month_order, barmode='group')
    fig.update_layout(title='', xaxis={'title': 'Year'}, yaxis_title='CPI')
    return fig
    # long_format_data = cpi_data.melt(var_name='Region', value_name='CPI')

    # fig = px.histogram(long_format_data, x='CPI', color='Region', barmode='overlay')

    # fig.update_layout(title='', xaxis_title='CPI', yaxis_title='Count')

    # return fig


# Callback to update the bar chart based on the selected region
# @callback(
#     Output('cpi-bar-chart', 'figure'),
#     [Input('cpi-region-selector-dropdown', 'value')]
# )
# def update_cpi_chart_2(selected_region):
#     data = CPI_EXCEL_FILE
#     sheet_data = data[selected_region].iloc[1:]
#     sheet_data['Date'] = pd.to_datetime(sheet_data['Date'])
#     sheet_data['Year'] = sheet_data['Date'].dt.year
#     sheet_data['MonthName'] = sheet_data['Date'].dt.strftime('%b')
#     sheet_data['CPI'] = sheet_data.iloc[:, 1]
#     sheet_data.sort_values(by='Date', inplace=True)
#     pivot_data = sheet_data.pivot_table(index='Year', columns='MonthName', values='CPI', aggfunc='mean')
#     pivot_data.reset_index(inplace=True)
#     month_order = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
#     pivot_data = pivot_data.reindex(columns=['Year'] + month_order)
#     fig = px.bar(pivot_data, x='Year', y=month_order, barmode='group')
#     fig.update_layout(title='', xaxis={'title': 'Year'}, yaxis_title='CPI')
#     return fig
