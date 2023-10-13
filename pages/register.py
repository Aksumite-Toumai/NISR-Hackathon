import dash
from dash import html, dcc
import dash_bootstrap_components as dbc


dash.register_page(__name__)

layout = html.Section([
    html.Div([
        html.Div([
            html.Div([
                html.Div([
                    html.Div([
                        html.Div([
                            html.Div([
                                html.Div([
                                    html.Img(src="/assets/nisr_logo.png",
                                             style={"width": "200px"}, alt="nisr logo")
                                ], className="text-center"),
                                html.Form([
                                    html.P("Please enter your details"),
                                    html.Div([
                                        dcc.Input(
                                            type="text",
                                            id="username_create",
                                            className="form-control",
                                            placeholder="Username"
                                        ),
                                    ], className="form-outline mb-4"),
                                    html.Div([
                                        dcc.Input(
                                            type="password",
                                            id="pwd1",
                                            className="form-control",
                                            placeholder="Password"
                                        ),
                                    ], className="form-outline mb-4"),
                                    html.Div([
                                        dcc.Input(
                                            type="password",
                                            id="pwd2",
                                            className="form-control",
                                            placeholder="Repeat password"
                                        ),
                                    ], className="form-outline mb-4"),
                                    html.Div([
                                        dbc.Button("Register",
                                                   className="btn btn-primary btn-block fa-lg gradient-custom-2 mb-3",
                                                   type='button', id='create-btn',
                                                   style={'width': "160px", 'height': '50px', 'font': 'bold'}),
                                        html.Br(),
                                        html.Div(id='register-error-message'),
                                    ], className="text-center pt-1 mb-5 pb-1"),
                                    html.Div([
                                        html.P("Already have an account?", className="mb-0 me-2"),
                                        dcc.Link(children="Log in", href="/login", className="btn btn-outline-danger",
                                                 id='create-log-btn')
                                    ], className="d-flex align-items-center justify-content-center pb-4")
                                ])
                            ], className="card-body p-md-5 mx-md-4")
                        ], className="col-lg-6"),
                        html.Div([
                            html.Div([
                                html.H1("NISR Dashboard"),
                                html.H3("Registration", className="mb-4"),
                                html.P("Create your account to get access to the dashboard with full of functionalities..."),
                            ], className="text-white px-3 py-4 p-md-5 mx-md-4")
                        ], className="col-lg-6 d-flex align-items-center gradient-custom-2")
                    ], className="row g-0")
                ], className="card rounded-3 text-black")
            ], className="col-xl-10")
        ], className="row d-flex justify-content-center align-items-center h-100")
    ], className="container py-5 h-100")
], className="h-100 gradient-form", style={"background-color": '#eee'})

