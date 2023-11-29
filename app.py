from dash import Dash, html, dcc  # type: ignore
import dash_bootstrap_components as dbc  # type: ignore
import logging
import dash  # type: ignore
import dash_auth  # type: ignore
from topbar import topbar
from sidebar import sidebar


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s]: %(message)s",
    handlers=[
        logging.FileHandler("app.log"),
        logging.StreamHandler()
    ]
)


# Keep this out of source code repository - save in a file or a database
VALID_USERNAME_PASSWORD_PAIRS = {
    'test': 'test'
}

# Create the dash app
DASH_APP = Dash(__name__,
                use_pages=True,
                external_stylesheets=[dbc.themes.BOOTSTRAP,
                                      "assets/vendor/fontawesome-free/css/all.min.css",
                                      "/assets/style.css",
                                      "/assets/css/sb-admin-2.min.css",
                                      "/assets/home.css"
                                      ])

auth = dash_auth.BasicAuth(
    DASH_APP,
    VALID_USERNAME_PASSWORD_PAIRS
)


# Home page design
content = html.Div(
    id="wrapper",
    children=[
        dcc.Location(id="url", refresh=False, pathname="/home"),
        # sidebar
        sidebar(),

        # Content Wrapper
        html.Div(
            [
                # Main Content
                html.Div([
                    # Topbar
                    topbar(),

                    # Begin Page Content
                    html.Div([dash.page_container], className="container-fluid")

                ], id="content")
            ],
            id="content-wrapper",
            className="d-flex flex-column",
        )
    ]
)

# Dash App main layout to display the pages
DASH_APP.layout = html.Div([
    content,
], id="page-top", className="py-2")


# Update page to change the language

# Run the app
if __name__ == '__main__':
    DASH_APP.run_server(host='localhost', port=8888, debug=True)
