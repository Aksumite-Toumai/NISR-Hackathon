import dash
from dash import dcc
from dash import html
import plotly.graph_objects as go
import pandas as pd


data = pd.read_excel("CPI.xlsm", sheet_name=None)

# Get the months
months = pd.to_datetime(data["Urban"]["Date"][1:]).dt.strftime("%b %Y")


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
    # Plot 3: CPI Yearly for Urban
    dcc.Graph(
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
                'title': 'CPI Yearly (Urban)',
                'xaxis': {
                    'ticktext': ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
                }
            }
        }
    ),
    # Plot 4: CPI Yearly for Rural
    dcc.Graph(
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
                    'ticktext': ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
                }
            }
        }
    ),
    # Plot 5: CPI Yearly for All Rwanda
    dcc.Graph(
        id='plot5',
        figure={
            'data': [
                {
                    'x': pd.to_datetime(data["All Rwanda"]["Date"][1:]).dt.strftime('%B').iloc[mask.values], 
                    'y': data["All Rwanda"]["GENERAL INDEX (CPI)"][1:].iloc[mask.values], 
                    'type': 'line', 
                    'name': str(year)
                }
                for year in pd.to_datetime(data["All Rwanda"]["Date"][1:]).dt.year.unique()
                for mask in [pd.to_datetime(data["All Rwanda"]["Date"][1:]).dt.year == year]
            ],
            'layout': {
                'title': 'CPI Yearly (All Rwanda)',
                'xaxis': {
                    'ticktext': ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
                }
            }
        }
    ),

])

# Run the Dash app
if __name__ == '__main__':
    app.run_server(debug=True)
