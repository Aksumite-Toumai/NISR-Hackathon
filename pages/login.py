import dash
from dash import html, dcc


dash.register_page(__name__)

layout = html.Section([
    dcc.Location(id='url_login', refresh=False),
    dcc.Location(id='url_create', refresh=True),
    html.Div([
        html.Div([
            html.Div([
                html.Div([
                    html.Div([
                        html.Div([
                            html.Div([
                                # html.Div([
                                #     dcc.Dropdown([
                                #         {"label": html.Span(['English'],
                                #                             style={'color': '#284fa1', 'font-size': 15}), "value": "en"},
                                #         {"label": html.Span(['Kinyarwanda'],
                                #                             style={'color': '#284fa1', 'font-size': 15}), "value": "rw"},
                                #         {"label": html.Span(['French'],
                                #                             style={'color': '#284fa1', 'font-size': 15}), "value": "fr"}
                                #                   ],
                                # value='en', clearable=False, style={"width": "125px"})], className="row"),
                                html.Div([
                                    html.Img(src="/assets/nisr_logo.png",
                                             style={"width": "285px"}, alt="nisr logo")
                                ], className="text-center"),
                                html.Form([
                                    html.P("Please login to your account"),
                                    html.Div([
                                        dcc.Input(
                                            type="text",
                                            id="username_login",
                                            className="form-control",
                                            placeholder="Username"
                                        ),
                                    ], className="form-outline mb-4"),
                                    html.Div([
                                        dcc.Input(
                                            type="password",
                                            id="pwd_login",
                                            className="form-control",
                                            placeholder="Password"
                                        ),
                                    ], className="form-outline mb-4"),
                                    html.Div([
                                        html.Button("Log in",
                                                    className="btn btn-primary btn-block fa-lg gradient-custom-2 mb-3",
                                                    type='button', id='login-btn',
                                                    style={'width': "160px", 'height': '50px', 'font': 'bold'}),
                                        html.Br(),
                                        html.Div(id='login-error-message'),
                                        html.Br(),
                                        html.A('Forgot password?', className="text-muted", href="#!")
                                    ], className="text-center pt-1 mb-5 pb-1"),
                                    # html.Div([
                                    #     html.P("Don't have an account?", className="mb-0 me-2"),
                                    #     html.Button("Create new", className="btn btn-outline-danger", type="button",
                                    # id='create-btn')
                                    # ], className="d-flex align-items-center justify-content-center pb-4")
                                ])
                            ], className="card-body p-md-5 mx-md-4")
                        ], className="col-lg-6"),
                        html.Div([
                            html.Div([
                                html.H1("NISR Dashboard"),
                                html.H3("Data Analytics", className="mb-4"),
                                html.H5("Mission Statement"),
                                html.P("To assume the leading role in improving capacity to use information for evidence based\
                                       decision-making by coordinating national effort to collect and archive reliable data, to\
                                       analyze, document and disseminate data within an integrated and sustainable framework"),
                            ], className="text-white px-3 py-4 p-md-5 mx-md-4")
                        ], className="col-lg-6 d-flex align-items-center gradient-custom-2")
                    ], className="row g-0")
                ], className="card rounded-3 text-black")
            ], className="col-xl-10")
        ], className="row d-flex justify-content-center align-items-center h-100")
    ], className="container py-5 h-100")
], className="h-100 gradient-form", style={"background-color": '#eee'})
