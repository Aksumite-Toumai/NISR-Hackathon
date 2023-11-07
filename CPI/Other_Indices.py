import dash
from dash import html, dcc
import plotly.express as px
import pandas as pd

data = pd.read_excel("CPI_time_series_September_2023.xlsm", sheet_name=None)

# data for sheet "Other_Indices" and remove the first row
Other_Indices_data = data["Other_Indices"].iloc[1:, :]
Other_Indices_data['Date'] = pd.to_datetime(Other_Indices_data['Date'])
Other_Indices_data = Other_Indices_data.sort_values(by='Date')

# data frame for box plots
cpi_data_melted = Other_Indices_data.melt(id_vars=['Date'], var_name='Index', value_name='Value')

# heatmap data frame
cpi_data_heatmap = Other_Indices_data.copy()
cpi_data_heatmap['Year'] = cpi_data_heatmap['Date'].dt.year
cpi_data_heatmap['Month'] = cpi_data_heatmap['Date'].dt.strftime('%b')  # Month abbreviation
heatmap_data_local = cpi_data_heatmap.pivot('Year', 'Month', 'Local Goods Index')
heatmap_data_imported = cpi_data_heatmap.pivot('Year', 'Month', 'Imported Goods Index')
month_order = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
heatmap_data_local = heatmap_data_local[month_order]
heatmap_data_imported = heatmap_data_imported[month_order]

# Initialize the Dash app
app = dash.Dash(__name__)

# Ctime series line plots
fig_line_local_imported = px.line(Other_Indices_data, x='Date', y=[col for col in Other_Indices_data.columns if col in ['Local Goods Index', 'Imported Goods Index']],
                                 title='CPI Time Series Indices (Local Goods Index vs Imported Goods Index)')
fig_line_fresh_energy = px.line(Other_Indices_data, x='Date', y=[col for col in Other_Indices_data.columns if col in
                                ['Fresh Products(1) index', 'Energy index', 'General Index excluding fresh Products and energy(2)']],
                                title='CPI Time Series Indices (Fresh vs Energy vs Excluding Fresh and Energy)')

# heatmap plots
fig_heatmap_local = px.imshow(heatmap_data_local, text_auto=True, aspect="auto", title='Monthly Heatmap of Local Goods Index')
fig_heatmap_imported = px.imshow(heatmap_data_imported, text_auto=True, aspect="auto", title='Monthly Heatmap of Imported Goods Index')

# box plot
fig_box = px.box(cpi_data_melted, x='Index', y='Value', title='Box Plot of CPI Indices')

app.layout = html.Div([
    html.H1("CPI Dashboard"),
    dcc.Graph(figure=fig_line_local_imported),
    dcc.Graph(figure=fig_line_fresh_energy),
    dcc.Graph(figure=fig_heatmap_local),
    dcc.Graph(figure=fig_heatmap_imported),
    dcc.Graph(figure=fig_box)
])

if __name__ == '__main__':
    app.run_server(debug=True)
