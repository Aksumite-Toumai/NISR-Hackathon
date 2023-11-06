import dash
from dash import dcc
from dash import html
import plotly.graph_objects as go
import pandas as pd
import plotly.express as px


data = pd.read_excel("CPI_time_series_September_2023.xlsm", sheet_name=None)

# Get the months
months = pd.to_datetime(data["Urban"]["Date"][1:]).dt.strftime("%b %Y")

# years
years = sorted(pd.to_datetime(data["Urban"]["Date"][1:]).dt.year.unique())

app = dash.Dash(__name__)

app.layout = html.Div([

    # Plot 1: Urban vs. Rural vs. All Rwanda CPI
    dcc.Graph(
        id='plot1',
        figure={
            'data': [
                {'x': months, 'y': data["Urban"]["GENERAL INDEX (CPI)"][1:], 'type': 'line', 'name': 'Urban'},
                {'x': months, 'y': data["Rural"]["GENERAL INDEX (CPI)"][1:], 'type': 'line', 'name': 'Rural'},
                {'x': months, 'y': data["All Rwanda"]["GENERAL INDEX (CPI)"][1:], 'type': 'line', 'name': 'All Rwanda'}
            ],
            'layout': {
                'title': 'Urban vs. Rural vs. All Rwanda CPI',
                'xaxis': {
                    'tickangle': 45
                }
            }
        }
    ),
    # Plot 2: Urban vs. Rural vs. All Rwanda Weights
    dcc.Graph(
        id='plot2',
        figure={
            'data': [
                {'x': data["Urban"].columns[1:], 'y': data["Urban"].iloc[0, 1:], 'type': 'bar', 'name': 'Urban'},
                {'x': data["Rural"].columns[1:], 'y': data["Rural"].iloc[0, 1:], 'type': 'bar', 'name': 'Rural'},
                {'x': data["All Rwanda"].columns[1:], 'y': data["All Rwanda"].iloc[0, 1:], 'type': 'bar', 'name': 'All Rwanda'}
            ],
            'layout': {
                'title': 'Urban vs. Rural vs. All Rwanda Weights',
                'barmode': 'group'
            }
        }
    ),
    # year selection
    dcc.Dropdown(
        id='year-dropdown',
        options=[{'label': str(year), 'value': year} for year in years],
        value=years[-1],  # Default value is the latest year
        clearable=False
    ),
    dcc.Graph(id='combined-cpi-yearly-plot' # CPI monthly for selected year
    ),
    dcc.Graph(id='combined-cpi-monthly-change-plot' # CPI monthly change for selected year
    ),
    dcc.Graph(id='combined-cpi-monthly-change-histogram' # histogram of CPI values for selected year
    ),
    # CPI annual change
        dcc.Graph(
        id='cpi-annual-change',
        figure={
            'data': [
            {'x': data['Urban']['Date'][1:], 'y':data["Urban"]['GENERAL INDEX (CPI)'][1:].pct_change(periods=12) * 100, 'type': 'line', 'name': 'Urban'},
            {'x': data['Rural']['Date'][1:], 'y': data["Rural"]['GENERAL INDEX (CPI)'][1:].pct_change(periods=12) * 100, 'type': 'line', 'name': 'Rural'},
            {'x': data['All Rwanda']['Date'][1:], 'y': data["All Rwanda"]['GENERAL INDEX (CPI)'][1:].pct_change(periods=12) * 100, 'type': 'line', 'name': 'All Rwanda'}
            ],
            'layout': {
                'title': 'CPI Annual Change',
                'xaxis': {
                    'tickmode': 'linear',
                    'dtick': "M12",
                    'tickformat': "%Y"
                },
                'yaxis': {
                    'title': 'Annual Change (%)'
                }
            }
        }
    ),
    # CPI bar chart
        dcc.Dropdown(id='region-selector', options=[{'label': name, 'value': name} for name in ['Urban', 'Rural', 'All Rwanda']], value='Urban'),
        dcc.Graph(id='cpi-bar-chart')
])

@app.callback(
    dash.dependencies.Output('combined-cpi-yearly-plot', 'figure'),
    [dash.dependencies.Input('year-dropdown', 'value')]
)
def update_graph(selected_year):
    mask_urban = pd.to_datetime(data["Urban"]["Date"][1:]).dt.year == selected_year
    mask_rural = pd.to_datetime(data["Rural"]["Date"][1:]).dt.year == selected_year
    mask_all_rwanda = pd.to_datetime(data["All Rwanda"]["Date"][1:]).dt.year == selected_year
    
    return {
        'data': [
            {
                'x': pd.to_datetime(data["Urban"]["Date"][1:]).dt.strftime('%B').iloc[mask_urban.values],
                'y': data["Urban"]["GENERAL INDEX (CPI)"][1:].iloc[mask_urban.values],
                'type': 'line',
                'name': 'Urban'
            },
            {
                'x': pd.to_datetime(data["Rural"]["Date"][1:]).dt.strftime('%B').iloc[mask_rural.values],
                'y': data["Rural"]["GENERAL INDEX (CPI)"][1:].iloc[mask_rural.values],
                'type': 'line',
                'name': 'Rural'
            },
            {
                'x': pd.to_datetime(data["All Rwanda"]["Date"][1:]).dt.strftime('%B').iloc[mask_all_rwanda.values],
                'y': data["All Rwanda"]["GENERAL INDEX (CPI)"][1:].iloc[mask_all_rwanda.values],
                'type': 'line',
                'name': 'All Rwanda'
            }
        ],
        'layout': {
            'title': f'CPI Monthly for {selected_year}',
            'xaxis': {
                'ticktext': ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
            }
        }
    }

@app.callback(
    dash.dependencies.Output('combined-cpi-monthly-change-plot', 'figure'),
    [dash.dependencies.Input('year-dropdown', 'value')]
)
def update_monthly_change_graph(selected_year):
    mask_urban = pd.to_datetime(data["Urban"]["Date"][1:]).dt.year == selected_year
    mask_rural = pd.to_datetime(data["Rural"]["Date"][1:]).dt.year == selected_year
    mask_all_rwanda = pd.to_datetime(data["All Rwanda"]["Date"][1:]).dt.year == selected_year
    
    monthly_change_urban = data["Urban"]["GENERAL INDEX (CPI)"][1:].pct_change() * 100
    monthly_change_rural = data["Rural"]["GENERAL INDEX (CPI)"][1:].pct_change() * 100
    monthly_change_all_rwanda = data["All Rwanda"]["GENERAL INDEX (CPI)"][1:].pct_change() * 100
    
    return {
        'data': [
            {
                'x': pd.to_datetime(data["Urban"]["Date"][1:]).dt.strftime('%B').iloc[mask_urban.values],
                'y': monthly_change_urban.iloc[mask_urban.values],
                'type': 'line',
                'name': 'Urban'
            },
            {
                'x': pd.to_datetime(data["Rural"]["Date"][1:]).dt.strftime('%B').iloc[mask_rural.values],
                'y': monthly_change_rural.iloc[mask_rural.values],
                'type': 'line',
                'name': 'Rural'
            },
            {
                'x': pd.to_datetime(data["All Rwanda"]["Date"][1:]).dt.strftime('%B').iloc[mask_all_rwanda.values],
                'y': monthly_change_all_rwanda.iloc[mask_all_rwanda.values],
                'type': 'line',
                'name': 'All Rwanda'
            }
        ],
        'layout': {
            'title': f'CPI Monthly Change for {selected_year}',
            'xaxis': {
                'ticktext': ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
            },
            'yaxis': {
                'title': 'Monthly Change (%)'
            }
        }
    }

@app.callback(
    dash.dependencies.Output('combined-cpi-monthly-change-histogram', 'figure'),
    [dash.dependencies.Input('year-dropdown', 'value')]
)

def update_cpi_histogram(selected_year):
    mask_urban = pd.to_datetime(data["Urban"]["Date"][1:]).dt.year == selected_year
    mask_rural = pd.to_datetime(data["Rural"]["Date"][1:]).dt.year == selected_year
    mask_all_rwanda = pd.to_datetime(data["All Rwanda"]["Date"][1:]).dt.year == selected_year

    cpi_urban = data["Urban"]["GENERAL INDEX (CPI)"][1:][mask_urban]
    cpi_rural = data["Rural"]["GENERAL INDEX (CPI)"][1:][mask_rural]
    cpi_all_rwanda = data["All Rwanda"]["GENERAL INDEX (CPI)"][1:][mask_all_rwanda]

    cpi_data = pd.DataFrame({'Urban': cpi_urban, 'Rural': cpi_rural, 'All Rwanda': cpi_all_rwanda}).reset_index(drop=True)

    long_format_data = cpi_data.melt(var_name='Region', value_name='CPI')

    fig = px.histogram(long_format_data, x='CPI', color='Region', barmode='overlay')

    fig.update_layout(title=f'CPI Values for {selected_year}', xaxis_title='CPI', yaxis_title='Count')

    return fig


# Callback to update the bar chart based on the selected region
@app.callback(
    dash.dependencies.Output('cpi-bar-chart', 'figure'),
    [dash.dependencies.Input('region-selector', 'value')]
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
    fig.update_layout(title=f'Monthly CPI Values by Year - {selected_region}', xaxis={'title': 'Year'}, yaxis_title='CPI')
    return fig

# Run the Dash app
if __name__ == '__main__':
    app.run_server(debug=True)
