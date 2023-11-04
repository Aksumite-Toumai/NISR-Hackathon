import dash  # type: ignore
import os  # type: ignore
from dash import Dash, html, dcc, Input, Output, State
import dash_bootstrap_components as dbc  # type: ignore
from flask import Flask
import logging
import db
import auth


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s]: %(message)s",
    handlers=[
        logging.FileHandler("app.log"),
        logging.StreamHandler()
    ]
)


# Initialize Flask app
FLASK_APP = Flask(__name__, instance_relative_config=True)
FLASK_APP.config.from_mapping(
    SECRET_KEY=os.environ.get('SECRET_KEY'),
    DATABASE=os.path.join(FLASK_APP.instance_path, 'nisr.sqlite'),
)

# Initialize the flask server with the database
db.init_app(FLASK_APP)

css2 = "assets/vendor/fontawesome-free/css/all.min.css"
# script1 = "assets/vendor/jquery/jquery.min.js"
# script2 = "assets/vendor/bootstrap/js/bootstrap.bundle.min.js"
# script3 = "assets/vendor/jquery-easing/jquery.easing.min.js"
# script5 = "assets/vendor/chart.js/Chart.min.js"

# Initialize Dash app within the Flask app
external_stylesheets = ['/assets/css/bootstrap.min.css', '/assets/style.css', css2]
external_scripts = ['/assets/js/bootstrap.min.js']

DASH_APP = Dash(__name__,
                server=FLASK_APP,
                use_pages=True,
                external_stylesheets=[dbc.themes.SOLAR, "/assets/style.css"],
                external_scripts=external_scripts,
                prevent_initial_callbacks='initial_duplicate',
                suppress_callback_exceptions=True)

# Dash App main layout to display the pages
DASH_APP.layout = html.Div([
    dcc.Location(id='url', refresh=True),
    dash.page_container
], style={'background-color': '#DCDCDC'})


# Function to render the main page based on the url
@DASH_APP.callback(Output("url", "pathname"), [Input("url", "pathname")])
def render_page_content(pathname):
    if pathname == '/register':
        return '/register'
    url = auth.login_required()
    if url is None:
        if pathname == '/logout':
            return auth.logout()
        return pathname
    return '/home'


# Create user callback
@DASH_APP.callback([Output("register-error-message", "children"),
                    Output("register-error-message", "style")],
                   [Input("create-btn", "n_clicks"),
                    State("username_create", "value"),
                    State("pwd1", "value"),
                    State("pwd2", "value")])
def register_user(n_clicks, username, pwd1, pwd2):

    if n_clicks is not None:
        error = []
        if username is None or username == '' or username.strip() == ' ':
            error.append("Enter your username")
        if pwd1 is None or pwd1 == '' or pwd1.strip() == ' ':
            error.append("Enter your password")
        if pwd1 != pwd2:
            error.append("Passwords don't match.")

        if len(error) > 0:
            return " and ".join(error), {'color': 'red'}

        error = auth.register(username=username, password=pwd1)

        if error is None:
            return 'Successfull', {'color': 'green'}
        return error, {'color': 'red'}
    return '', {}


# Create user callback
@DASH_APP.callback([Output("login-error-message", "children"),
                    Output("login-error-message", "style"),
                    Output("url", "pathname", allow_duplicate=True)],
                   [Input("login-btn", "n_clicks"),
                    State("username_login", "value"),
                    State("pwd_login", "value")])
def login_user(n_clicks, username, pwd):

    if n_clicks is not None:
        error = []
        if username is None or username == '' or username.strip() == ' ':
            error.append("Enter your username")
        if pwd is None or pwd == '' or pwd.strip() == ' ':
            error.append("Enter your password")

        if len(error) > 0:
            return " and ".join(error), {'color': 'red'}

        error = auth.login(username=username, password=pwd)

        if error is None:
            auth.load_logged_in_user()
            return 'Successfull', {'color': 'green'}, '/home'
        return error, {'color': 'red'}, '/login'
    return '', {}, '/login'


# Run the app
if __name__ == '__main__':
    DASH_APP.run_server(port=8889, debug=True)
