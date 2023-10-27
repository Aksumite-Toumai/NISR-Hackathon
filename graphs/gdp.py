from dash import html, dcc
import dash_bootstrap_components as dbc
import os
import pandas as pd
import logging
import plotly.graph_objects as go
from dash import callback, Output, Input
import plotly.express as px


# datasets main directory
DATASETS_PATH = os.environ.get("DATA_PATH")

# GDP file path
GDP_PATH = os.path.join(DATASETS_PATH, "GDP National Accounts/R_GDP National Accounts 2022_r.xls")

# read the GDP excel file
GDP_EXCEL_FILE = None
if os.path.exists(GDP_PATH):
    GDP_EXCEL_FILE = pd.read_excel(GDP_PATH, sheet_name='Table A', skiprows=2,
                                   usecols=lambda x: True if 'Unnamed:' not in str(x) else False)
    GDP_EXCEL_FILE = GDP_EXCEL_FILE.dropna()
    GDP_EXCEL_FILE = GDP_EXCEL_FILE.set_index("Years")
    GDP_EXCEL_FILE = GDP_EXCEL_FILE.T.reset_index()
    GDP_EXCEL_FILE.columns = [col.strip() for col in GDP_EXCEL_FILE.columns]

    # Rename the column
    GDP_EXCEL_FILE = GDP_EXCEL_FILE.rename(columns={'index': 'Years'})
    logging.info('GDP file loaded...')


def get_gdp_at_current_price(y):
    data = pd.read_excel(GDP_PATH, sheet_name='Table A', skiprows=22, header=None)
    data = data.iloc[:4, 3:20]
    data_cleaned = data.dropna(how='all')
    data_cleaned.columns = ["sector"] + [2007+i for i in range(16)]
    return data_cleaned.to_dict()


def get_proportions_of_gdp_by_sectors():
    dropdown_years = dcc.Dropdown(
                    id='gdp-by-sectors-year-dropdown',
                    options=[
                            {
                                "label": html.Span(year, style={'color': 'black', 'font-size': 20}),
                                "value": year,
                            } for year in GDP_EXCEL_FILE['Years']
                    ],
                    value=2022,
                    clearable=False,
                ),

    content = dbc.Card([
        dbc.CardHeader([
            "Proportion of GDP by Sectors - At Current Prices", html.Hr(),
            html.Div(dropdown_years)], style={"color": "white", 'font-size': 20},),
        dbc.CardBody(
            [
                html.Div([
                  dcc.Graph(id='donut-gdp-by-sector-fig')
                ])
            ], style={"padding": "0"},
        ),
    ], color="#284fa1", outline=False)

    return content


def get_proportions_of_gdp_constant_2017_by_sectors():
    dropdown_years = dcc.Dropdown(
                    id='gdp_constant_2017-by-sectors-year-dropdown',
                    options=[
                            {
                                "label": html.Span(year, style={'color': 'black', 'font-size': 20}),
                                "value": year,
                            } for year in GDP_EXCEL_FILE['Years']
                    ],
                    value=2022,
                    clearable=False,
                ),

    content = dbc.Card([
        dbc.CardHeader([
            "Proportion of GDP by Sectors - At Constant 2017 Prices", html.Hr(),
            html.Div(dropdown_years)], style={"color": "white", 'font-size': 20},),
        dbc.CardBody(
            [
                html.Div([
                  dcc.Graph(id='donut-gdp_constant_2017-by-sector-fig')
                ])
            ], style={"padding": "0"},
        ),
    ], color="#284fa1", outline=False)

    return content


# create macro-economic aggregates content
def macro_economic_aggregates_content():
    gdp_current_price_inline_radioitems = html.Div(
        [
            dbc.RadioItems(
                options=[
                    {"label": "price", "value": 1},
                    {"label": "growth rate", "value": 2},
                ],
                value=1,
                id="gdp_at_current_price-radioitems-inline-input",
                inline=True,
            ),
        ]
    )
    gdp_current_price_card = dbc.Card([
        dbc.CardHeader([
            dbc.Col("GDP at current prices",),
            dbc.Col(
                gdp_current_price_inline_radioitems, className="d-flex justify-content-end class",
            )
        ], style={"color": "white", 'font-size': 20},),
        dbc.CardBody(
            [
                html.Div([
                    dcc.Graph(id='gdp_at_current_price_fig')
                ])
            ], style={"padding": "0"},
        ),
    ], color="#284fa1", outline=False)

    gdp_constant_2017_price_inline_radioitems = html.Div(
        [
            dbc.RadioItems(
                options=[
                    {"label": "price", "value": 1},
                    {"label": "growth rate", "value": 2},
                ],
                value=1,
                id="gdp_constant_2017_price-radioitems-inline-input",
                inline=True,
            ),
        ]
    )
    gdp_constant_price_2017_card = dbc.Card([
        dbc.CardHeader([
            dbc.Col("GDP at constant 2017 prices",),
            dbc.Col(
                gdp_constant_2017_price_inline_radioitems, className="d-flex justify-content-end class",
            )
        ], style={"color": "white", 'font-size': 20},),
        dbc.CardBody(
            [
                html.Div([
                    dcc.Graph(id='gdp_constant_2017_price_fig')
                ])
            ], style={"padding": "0"},
        ),
    ], color="#284fa1", outline=False)

    content = html.Div([
        dbc.Row([
            dbc.Col(gdp_current_price_card, width=6),
            dbc.Col(gdp_constant_price_2017_card, width=6),
        ], className="mb-3 mt-2"),
        dbc.Row(
            [
                dbc.Col(get_proportions_of_gdp_by_sectors(), width=5),
                dbc.Col(get_proportions_of_gdp_constant_2017_by_sectors(), width=5),
                dbc.Col(),
            ],
            className="mb-3 mt-2",
        ),
    ])
    return content


def get_content():
    tabs = (" Macro-Economic Aggregates",
            "GDP by Kind of Activity at Current Price",
            "GDP by Kind of Activity at constant 2017 prices",
            "GDP by Kind of Activity Deflators",
            "Expenditure on GDP")
    return [html.Div([
        dbc.Row([
            dbc.Card(
                [
                    dbc.CardHeader(
                        dbc.Tabs(
                            [
                                dbc.Tab(label=tab, tab_id=tab,
                                        activeTabClassName="fw-bold fst-italic",
                                        label_style={"color": "#284fa1", "font": "bold", 'font-size': 17}) for tab in tabs
                            ],
                            id="card-tabs",
                            active_tab=tabs[0],
                        )
                    ),
                    dbc.CardBody(html.Div(id="card-content", className="card-text")),
                ], style={'background-color': '#DCDCDC', 'border': 'none'}
            )
        ], className="mb-2 mt-2 py-0 px-0",),
        html.Div(id="graphs-container-GDP", style={'background-color': '#DCDCDC', "margin-top": "0rem"})])
    ]


@callback(
    Output("card-content", "children"), [Input("card-tabs", "active_tab")]
)
def tab_content(active_tab):
    return macro_economic_aggregates_content()


@callback(
    Output("gdp_at_current_price_fig", "figure"),
    [
        Input("gdp_at_current_price-radioitems-inline-input", "value"),
    ],
)
def gdp_at_current_price_fig_on_change(radio_items_value):
    if radio_items_value == 1:
        fig = px.scatter(GDP_EXCEL_FILE, x="Years", y="GDP at current prices", color="GDP at current prices",
                         size='GDP at current prices', hover_data=['GDP at current prices'])
        # Remove the x-label and y-label
        fig.update_layout(xaxis_title=None, yaxis_title=None, legend_title_text="Prices (RWF Billions)")
    else:
        data = GDP_EXCEL_FILE[['Years', 'GDP at current prices']]
        data['Growth Rate'] = data['GDP at current prices'].pct_change()
        # Calculate the growth rate as percentages and format them as strings
        data["Growth Rate (Percentage)"] = (data["Growth Rate"] * 100).round(1).astype(str) + '%'

        # Create the line plot with markers and text labels
        fig = px.line(data, x="Years", y="Growth Rate", markers=True, text="Growth Rate (Percentage)")

        # Customize the text labels
        fig.update_traces(marker=dict(size=10), textposition="top center")
        # Increase the size of the figure
        fig.update_layout(xaxis_title=None, xaxis={'type': 'category'})
    return fig


@callback(
    Output("gdp_constant_2017_price_fig", "figure"),
    [
        Input("gdp_constant_2017_price-radioitems-inline-input", "value"),
    ],
)
def gdp_constant_2017_price_fig_on_change(radio_items_value):
    if radio_items_value == 1:
        fig = px.scatter(GDP_EXCEL_FILE, x="Years", y="GDP at constant 2017 prices", color="GDP at constant 2017 prices",
                         size='GDP at constant 2017 prices', hover_data=['GDP at constant 2017 prices'])
        # Remove the x-label and y-label
        fig.update_layout(xaxis_title=None, yaxis_title=None, legend_title_text="Prices (RWF Billions)")
    else:
        data = GDP_EXCEL_FILE[['Years', 'GDP at constant 2017 prices']]
        data['Growth Rate'] = data['GDP at constant 2017 prices'].pct_change()
        # Calculate the growth rate as percentages and format them as strings
        data["Growth Rate (Percentage)"] = (data["Growth Rate"] * 100).round(1).astype(str) + '%'

        # Create the line plot with markers and text labels
        fig = px.line(data, x="Years", y="Growth Rate", markers=True, text="Growth Rate (Percentage)")

        # Customize the text labels
        fig.update_traces(marker=dict(size=10), textposition="bottom right")
        # Increase the size of the figure
        fig.update_layout(xaxis_title=None, xaxis={'type': 'category'})
    return fig


@callback(
    Output("donut-gdp-by-sector-fig", "figure"),
    [
        Input("gdp-by-sectors-year-dropdown", "value"),
    ],
)
def gdp_by_sector_year_dropdown_on_change(radio_items_value):
    labels = ["Agriculture", "Industry", "Services", "Adjustments"]
    data = GDP_EXCEL_FILE[GDP_EXCEL_FILE['Years'] == radio_items_value][labels]
    values = list(data.values[0])
    total = GDP_EXCEL_FILE[GDP_EXCEL_FILE['Years'] == radio_items_value]['GDP at current prices'].values[0]

    # Create a smaller pie chart (the "hole" in the donut)
    fig = px.pie(values=values, names=labels, hole=0.6)

    # Create a larger pie chart to overlay the smaller one (the outer "ring")
    fig2 = px.pie(values=[total], names=["GDP at current prices"], hole=0.97)
    # fig2.update_traces(marker=dict(color='white'))

    # Combine the two charts to create the donut chart
    fig.add_traces(fig2.data)
    # # Use `hole` to create a donut-like pie chart
    # fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.6)])
    fig.update_layout(annotations=[dict(text=f"{total} (RWF Billions)", font_size=15, showarrow=False,)])
    return fig


@callback(
    Output("donut-gdp_constant_2017-by-sector-fig", "figure"),
    [
        Input("gdp_constant_2017-by-sectors-year-dropdown", "value"),
    ],
)
def gdp_contant_2017_by_sector_year_dropdown_on_change(radio_items_value):
    labels = ["Agriculture", "Industry", "Services", "Adjustments"]
    data = GDP_EXCEL_FILE[GDP_EXCEL_FILE['Years'] == radio_items_value][labels]
    values = list(data.values[0])
    total = GDP_EXCEL_FILE[GDP_EXCEL_FILE['Years'] == radio_items_value]['GDP at constant 2017 prices'].values[0]

    # Create a smaller pie chart (the "hole" in the donut)
    fig = px.pie(values=values, names=labels, hole=0.6)

    # Create a larger pie chart to overlay the smaller one (the outer "ring")
    fig2 = px.pie(values=[total], names=["GDP at constant 2017 prices"], hole=0.97)

    # Combine the two charts to create the donut chart
    fig.add_traces(fig2.data)

    # Use `hole` to create a donut-like pie chart
    fig.update_layout(annotations=[dict(text=f"{total} (RWF Billions)", font_size=15, showarrow=False,)])
    return fig
