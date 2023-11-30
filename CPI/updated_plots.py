import dash
from dash import dcc
from dash import html
import plotly.graph_objects as go
import pandas as pd
import plotly.express as px
from dash.dependencies import Input, Output


data = pd.read_excel("CPI_time_series_September_2023.xlsm", sheet_name=None)

# Get the months
months = pd.to_datetime(data["Urban"]["Date"][1:]).dt.strftime("%b %Y")

# years
years = sorted(pd.to_datetime(data["Urban"]["Date"][1:]).dt.year.unique())

app = dash.Dash(__name__)

app.layout = html.Div([

    # Plot 1: Urban vs. Rural vs. All Rwanda CPI
     dcc.RadioItems(
        id='plot-selection',
        options=[
            {'label': 'All CPI', 'value': 'current'},
            {'label': 'Average CPI', 'value': 'average'}
        ],
        value='current'
    ),
    dcc.Graph(id='dynamic-plot'),
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
    # plot 3
  # Year selection for cpi monthly, cpi monthly change and cpi histogram
    dcc.Dropdown(
        id='year-dropdown',
        options=[{'label': str(year), 'value': year} for year in years],
        value=years[-1],  # Default value is the latest year
        clearable=False
    ),

    # Radio button for cpi monthly, cpi monthly change and cpi histogram
    dcc.RadioItems(
        id='graph-type-selection',
        options=[
            {'label': 'CPI Monthly', 'value': 'cpi_monthly'},
            {'label': 'CPI Monthly Change', 'value': 'cpi_monthly_change'},
            {'label': 'CPI Histogram', 'value': 'cpi_histogram'}
        ],
        value='cpi_monthly'
    ),
    # plot 4
    # cpi monthly, cpi monthly change and cpi histogram

    dcc.Graph(id='combined-cpi-graph'),
    # CPI annual change
    dcc.Graph(
        id='cpi-annual-change',
        figure={
            'data': [
                # Urban
                {'x': [date for date in data['Urban']['Date'][1:]], 
                'y': [value for value in data["Urban"]['GENERAL INDEX (CPI)'][1:].pct_change(periods=12) * 100], 
                'type': 'line', 'name': 'Urban'},

                # Rural
                {'x': [date for date in data['Rural']['Date'][1:]], 
                'y': [value for value in data["Rural"]['GENERAL INDEX (CPI)'][1:].pct_change(periods=12) * 100], 
                'type': 'line', 'name': 'Rural'},

                # All Rwanda
                {'x': [date for date in data['All Rwanda']['Date'][1:]], 
                'y': [value for value in data["All Rwanda"]['GENERAL INDEX (CPI)'][1:].pct_change(periods=12) * 100], 
                'type': 'line', 'name': 'All Rwanda'}
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
    )
    ,
    # CPI bar chart
        dcc.Dropdown(id='region-selector', options=[{'label': name, 'value': name} for name in ['Urban', 'Rural', 'All Rwanda']], value='Urban'),
        dcc.Graph(id='cpi-bar-chart')
])

# computer yearly average CPI
def compute_yearly_average(data, category):
    data_filtered = data[category][1:]
    data_filtered['Date'] = pd.to_datetime(data_filtered['Date'])

    # Group by year
    yearly_data = data_filtered.groupby(data_filtered['Date'].dt.year).mean()
    return yearly_data


# callback for average CPI plot and All CPI plot
@app.callback(
    Output('dynamic-plot', 'figure'),
    [Input('plot-selection', 'value')]
)
def all_n_average(plot_type):
    if plot_type == 'average':
        # Compute yearly averages
        urban_avg = compute_yearly_average(data, "Urban")
        rural_avg = compute_yearly_average(data, "Rural")
        all_rwanda_avg = compute_yearly_average(data, "All Rwanda")

        # Create the average CPI plot
        average_cpi_plot = {
            'data': [
                {'x': urban_avg.index, 'y': urban_avg['GENERAL INDEX (CPI)'], 'type': 'line', 'name': 'Urban Average'},
                {'x': rural_avg.index, 'y': rural_avg['GENERAL INDEX (CPI)'], 'type': 'line', 'name': 'Rural Average'},
                {'x': all_rwanda_avg.index, 'y': all_rwanda_avg['GENERAL INDEX (CPI)'], 'type': 'line', 'name': 'All Rwanda Average'}
            ],
            'layout': {
                'title': 'Average CPI per Year',
                'xaxis': {'title': 'Year', 'tickangle': 45},
                'yaxis': {'title': 'Average CPI'}
            }
        }
        return average_cpi_plot
    else:
        # Urban vs. Rural vs. All Rwanda CPI plot
        return {
            'data': [
                {'x': months, 'y': data["Urban"]["GENERAL INDEX (CPI)"][1:], 'type': 'line', 'name': 'Urban'},
                {'x': months, 'y': data["Rural"]["GENERAL INDEX (CPI)"][1:], 'type': 'line', 'name': 'Rural'},
                {'x': months, 'y': data["All Rwanda"]["GENERAL INDEX (CPI)"][1:], 'type': 'line', 'name': 'All Rwanda'}
            ],
            'layout': {
                'title': 'Urban vs. Rural vs. All Rwanda CPI',
                'xaxis': {'tickangle': 45}
            }
        }

# cpi monthly
def CPI_Monthly(selected_year):
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

# cpi monthly change
def CPI_monthly_change(selected_year):
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

# cpi histogram
def CPI_histogram(selected_year):
    mask_urban = pd.to_datetime(data["Urban"]["Date"][1:]).dt.year == selected_year
    mask_rural = pd.to_datetime(data["Rural"]["Date"][1:]).dt.year == selected_year
    mask_all_rwanda = pd.to_datetime(data["All Rwanda"]["Date"][1:]).dt.year == selected_year

    cpi_urban = data["Urban"]["GENERAL INDEX (CPI)"][1:][mask_urban]
    cpi_rural = data["Rural"]["GENERAL INDEX (CPI)"][1:][mask_rural]
    cpi_all_rwanda = data["All Rwanda"]["GENERAL INDEX (CPI)"][1:][mask_all_rwanda]

    cpi_data = pd.DataFrame({'Urban': cpi_urban, 'Rural': cpi_rural, 'All Rwanda': cpi_all_rwanda}).reset_index(drop=True)

    long_format_data = cpi_data.melt(var_name='Region', value_name='CPI')

    fig = px.histogram(long_format_data, x='CPI', color='Region', barmode='overlay')

    fig.update_layout(
            title={
                'text': f'CPI Values for {selected_year}',
                'x': 0.5,  # Center the title
                'xanchor': 'center'
            },
            xaxis_title='CPI',
            yaxis_title='Count',
            plot_bgcolor='white',
            xaxis={'showgrid': True},
            yaxis={'showgrid': True},
            paper_bgcolor='white', 
            font=dict(size=12),
        )
    return fig

# call back for cpi monthly, cpi monthly change and cpi histogram
@app.callback(
    dash.dependencies.Output('combined-cpi-graph', 'figure'),
    [dash.dependencies.Input('year-dropdown', 'value'),
     dash.dependencies.Input('graph-type-selection', 'value')]
)
def monthly__mnthlychange(selected_year, graph_type):
    if graph_type == 'cpi_monthly':
        # Code to generate the 'CPI Monthly' plot for the selected year
        return CPI_Monthly(selected_year)

    elif graph_type == 'cpi_monthly_change':
        # Code to generate the 'CPI Monthly Change' plot for the selected year
        return CPI_monthly_change(selected_year)

    elif graph_type == 'cpi_histogram':
        # Code to generate the 'CPI Histogram' for the selected year
        return CPI_histogram(selected_year)



# Callback to update the bar chart based on the selected region
@app.callback(
    dash.dependencies.Output('cpi-bar-chart', 'figure'),
    [dash.dependencies.Input('region-selector', 'value')]
)
def all_cpi_bar_chart(selected_region):
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
