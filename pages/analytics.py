from dash import html, dcc
import dash_bootstrap_components as dbc
import dash


dash.register_page(__name__)

layout = html.Div(
    id="page-top",
    children=[
        html.Div(
            id="wrapper",
            children=[
                html.Ul(
                    className="navbar-nav sidebar sidebar-dark accordion",
                    id="accordionSidebar",
                    children=[
                        html.A(
                            className="sidebar-brand d-flex align-items-center justify-content-center",
                            href="/home",
                            children=[
                                html.Div(
                                    className="sidebar-brand-icon",
                                    children=html.Img(
                                        className="aims_logo",
                                        src="assets/nisr_logo.png",
                                        style={'width': '50px'}
                                    )
                                ),
                                html.Div(
                                    className="sidebar-brand-text mx-3",
                                    children="AIMS Rwanda"
                                )
                            ]
                        ),
                        html.Hr(
                            className="sidebar-divider my-0",
                        ),
                        html.Li(
                            className="nav-item active",
                            children=[
                                dcc.Link(
                                    className="nav-link", href="index_page",
                                    children=[
                                        html.Span("DASHBOARD")
                                    ]
                                )
                            ]
                        ),
                        html.Hr(
                            className="sidebar-divider",
                        ),
                        html.Div(
                            className="sidebar-heading",
                            children="Personal Information"
                        ),
                        html.Li(
                            className="nav-item",
                            children=[
                                 html.A(
                                    className="nav-link collapsed", href="#", **{'data-toggle': "collapse"}, **{'data-target': "#collapseTwo"},
                                    **{'aria-expanded': "true"}, **{'aria-controls': "collapseTwo"},
                                    children=html.Span("CONTACTS")
                                ),
                                html.Div(
                                    id="collapseTwo", className="collapse",**{'aria-labelledby':"headingTwo"},**{'data-parent':"#accordionSidebar"},
                                    children=html.Div(
                                        className="bg-white py-2 collapse-inner rounded",
                                        children=[
                                            html.H6(
                                                className="collapse-header", children="See:"
                                            ),
                                            dcc.Link(
                                                className="collapse-item", href="/Student_profiles", children="Students",
                                            ),
                                            dcc.Link(
                                                className="collapse-item", href="#", children="Tutors",
                                            ),
                                            dcc.Link(
                                                className="collapse-item", href="#", children="Lecturers",
                                            )
                                        ]
                                    )
                                )
                            ]
                        ),
                        html.Hr(className="sidebar-divider"),
                        html.Div("Phases",className="sidebar-heading"),
                        html.Li(
                            className="nav-item",
                            children=[
                                html.A(
                                    className="nav-link collapsed", href="#", **{'data-toggle':"collapse"}, **{'data-target':"#collapseUtilities"},
                                    **{'aria-expanded':"true"}, **{'aria-controls':"collapseUtilities"},
                                    children=html.Span("SKILL PHASE")
                                ),
                                html.Div(
                                    id="collapseUtilities", className="collapse", **{'aria-labelledby':"headingUtilities"},
                                    **{'data-parent':"#accordionSidebar"},
                                    children=html.Div(
                                        className="bg-white py-2 collapse-inner rounded",
                                        children=[
                                            html.H6("See:",
                                                className="collapse-header",
                                            ),
                                            dcc.Link(
                                                className="collapse-item", href="/Skillphase_1", children="Block 1",
                                            ),
                                            dcc.Link(
                                                className="collapse-item", href="/Skillphase_2", children="Block 2",
                                            ),
                                            dcc.Link(
                                                className="collapse-item", href="/Skillphase_3", children="Block 3",
                                            ),
                                        ]
                                    )
                                )
                            ]
                        ),
                        html.Li(
                            className="nav-item",
                            children=[
                                html.A(
                                    className="nav-link collapsed", href="#", **{'data-toggle':"collapse"}, **{'data-target':"#collapseUtilities1"},
                                    **{'aria-expanded':"true"}, **{'aria-controls':"collapseUtilities1"},
                                    children=html.Span("REVIEW PHASE")
                                ),
                                html.Div(
                                    id="collapseUtilities1", className="collapse", **{'aria-labelledby':"headingUtilities"},
                                    **{'data-parent':"#accordionSidebar"},
                                    children=html.Div(
                                        className="bg-white py-2 collapse-inner rounded",
                                        children=[
                                            html.H6("See:",
                                                className="collapse-header",
                                            ),
                                            dcc.Link(
                                                className="collapse-item", href="/Reviewphase_1", children="Block 1",
                                            ),
                                            dcc.Link(
                                                className="collapse-item", href="/Reviewphase_2", children="Block 2",
                                            ),
                                            dcc.Link(
                                                className="collapse-item", href="/Reviewphase_3", children="Block 3",
                                            ),
                                            dcc.Link(
                                                className="collapse-item", href="/Reviewphase_4", children="Block 4",
                                            ),
                                            dcc.Link(
                                                className="collapse-item", href="/Reviewphase_5", children="Block 5",
                                            ),
                                            dcc.Link(
                                                className="collapse-item", href="/Reviewphase_6", children="Block 6",
                                            ),
                                        ]
                                    )
                                )
                            ]
                        ),
                        html.Li(
                            className="nav-item",
                            children=dcc.Link(
                                className="nav-link", href="/Research",
                                children=html.Span('RESEARCH PHASE')
                            )
                        ),
                        html.Hr(className="sidebar-divider"),
                        html.Div("Stats",className="sidebar-heading"),
                        html.Li(
                            className="nav-item",
                            children=dcc.Link(
                                className="nav-link", href="/GeneralStatistics",
                                children=html.Span('General Statistics'.upper())
                            )
                        )
                    ]
                ),
                # END OF SIDEBAR

                html.Div(
                    id="content-wrapper", className="d-flex flex-column",
                    children=html.Div(
                        id="content",
                        children=[
                            
                            html.Nav(
                                className="navbar navbar-expand navbar-light bg-white topbar mb-4 static-top shadow",
                                children=[
                                   dbc.Button(
                                       id="sidebarToggleTop", className="btn btn-link d-md-none rounded-circle mr-3",
                                       children=html.I(className="fa fa-bars")
                                   ),
                                   dbc.Form(
                                       className="d-none d-sm-inline-block form-inline mr-auto ml-md-3 my-2 my-md-0 mw-100 navbar-search",
                                       children=html.Div(
                                           className="input-group",
                                           children=[
                                               dcc.Input(
                                                   type="text", className="form-control bg-light border-0 small", placeholder="Search for...",
                            
                                               ),
                                               html.Div(
                                                   className="input-group-append",
                                                   children=html.Button(
                                                       className="btn btn-primary", type="button",
                                                       children=html.I(className="fas fa-search fa-sm")
                                                   )
                                               )
                                           ]
                                       )
                                   ),
                                   #------------- TopBar NavBar
                                   html.Ul(
                                       className="navbar-nav ml-auto",
                                       children=[
                                           #<!-- Nav Item - Search Dropdown (Visible Only XS) -->
                                           html.Li(
                                               className="nav-item dropdown no-arrow d-sm-none",
                                               children=[
                                                   html.A(
                                                       className="nav-link dropdown-toggle", href="#", id="searchDropdown", role="button",
                                                        **{'data-toggle':"dropdown"}, **{'aria-haspopup':"true"}, **{'aria-expanded':"false"},
                                                        children=html.I(className="fas fa-search fa-fw")
                                                   ),

                                                # <!-- Dropdown - Messages -->
                                                html.Div(
                                                    className="dropdown-menu dropdown-menu-right p-3 shadow animated--grow-in",
                                                    **{'aria-labelledby':"searchDropdown"},
                                                    children=html.Div(
                                                        className="form-inline mr-auto w-100 navbar-search",
                                                        children=html.Div(
                                                            className="input-group",
                                                            children=[
                                                                dcc.Input(
                                                                    type="text", className="form-control bg-light border-0 small",
                                             placeholder="Search for..."
                                                                ),
                                                                html.Div(
                                                                     className="input-group-append",
                                                                     children=html.Button(
                                                                         className="btn btn-primary", type="button",
                                                                         children=html.I(className="fas fa-search fa-sm")
                                                                     )
                                                                )
                                                            ]
                                                        )
                                                    )
                                                )   
                                               ]
                                           ),

                                           # <!-- Nav Item - Alerts -->
                                           html.Li(
                                               className="nav-item dropdown no-arrow mx-1",
                                               children=[
                                                   html.A(
                                                       className="nav-link dropdown-toggle", href="#", id="alertsDropdown", role="button",
                                                **{'data-toggle':"dropdown"}, **{'aria-haspopup':"true"}, **{'aria-expanded':"false"},
                                                        children=[
                                                            html.I(className="fas fa-bell fa-fw"),
                                                            #  <!-- Counter - Alerts -->
                                                            html.Span(
                                                                className="badge badge-danger badge-counter",
                                                                children =""#str(app.alert_counter) + '+',
                                                            )
                                                        ]
                                                   ),
                                                   # <!-- Dropdown - Alerts -->
                                                   html.Div(
                                                        className="dropdown-list dropdown-menu dropdown-menu-right shadow animated--grow-in",
                                                        children=[
                                                            html.H6('Notification Center',className="dropdown-header", id='dropha'),
                                                            html.A(
                                                                className="dropdown-item d-flex align-items-center" ,href="#",
                                                                children=[
                                                                    html.Div(
                                                                        className="mr-3",
                                                                        children=[
                                                                            html.Div(
                                                                                className="icon-circle bg-primary",
                                                                                children=html.I(className="fas fa-file-alt text-white")
                                                                            )
                                                                        ]
                                                                    ),
                                                                    html.Div(
                                                                        children=[
                                                                            html.Div('Date Here', className="small text-gray-500"),
                                                                            'Some information'
                                                                        ]
                                                                    )
                                                                ]
                                                            ),
                                                            html.A(
                                                                className="dropdown-item d-flex align-items-center" ,href="#",
                                                                children=[
                                                                    html.Div(
                                                                        className="mr-3",
                                                                        children=[
                                                                            html.Div(
                                                                                className="icon-circle bg-primary",
                                                                                children=html.I(className="fas fa-file-alt text-white")
                                                                            )
                                                                        ]
                                                                    ),
                                                                    html.Div(
                                                                        children=[
                                                                            html.Div('Date Here', className="small text-gray-500"),
                                                                            'Some information'
                                                                        ]
                                                                    )
                                                                ]
                                                            ),
                                                            html.A("Show All",className="dropdown-item text-center small text-gray-500", href="#"),


                                                        ]
                                                   )
                                               ]
                                           ),
                                        #<!-- Nav Item - Messages -->
                                        html.Li(
                                        className="nav-item dropdown no-arrow mx-1",
                                        
                                        children=[
                                            html.A(
                                                className="nav-link dropdown-toggle", href="#", id="messagesDropdown", role="button",
                                                **{'data-toggle':"dropdown"}, **{'aria-haspopup':"true"}, **{'aria-expanded':"false"},
                                                children=[
                                                    html.I(className="fas fa-envelope fa-fw"),
                                                    html.Span("", className="badge badge-danger badge-counter")
                                                ]
                                            ),

                                            # <!-- Dropdown - Messages -->
                                            html.Div(
                                            className="dropdown-list dropdown-menu dropdown-menu-right shadow animated--grow-in",
                                            children=[
                                                html.H6("Message Center", className="dropdown-header", id='droph6'),
                                                html.A(
                                                    className="dropdown-item d-flex align-items-center",
                                                    href="#",
                                                    children=[
                                                        html.Div(
                                                            className="dropdown-list-image mr-3",
                                                            children=[
                                                                html.Img(className="rounded-circle", src="assets/img/undraw_profile_1.svg",
                                                                alt="..."),
                                                                html.Div(className="status-indicator bg-success")
                                                            ]
                                                        ),
                                                        html.Div(
                                                            className="font-weight-bold",
                                                            children =[ html.Div(
                                                                className="text-truncate",
                                                                children="Here, we will insert message..."
                                                            ),
                                                            html.Div(className="small text-gray-500",
                                                                children='M 20min'
                                                            )
                                                            ]
                                                        )
                                                    ]
                                                ),
                                                html.A(
                                                    className="dropdown-item d-flex align-items-center",
                                                    href="#",
                                                    children=[
                                                        html.Div(
                                                            className="dropdown-list-image mr-3",
                                                            children=[
                                                                html.Img(className="rounded-circle", src="assets/img/undraw_profile_2.svg",
                                                                alt="..."),
                                                                html.Div(className="status-indicator")
                                                            ]
                                                        ),
                                                        html.Div(
                                                            children =[ html.Div(
                                                                className="text-truncate",
                                                                children="Here, we will insert message..."
                                                            ),
                                                            html.Div(className="small text-gray-500",
                                                                children='Az. 1d'
                                                            )
                                                            ]
                                                        )
                                                    ]
                                                ), 
                                                html.A(
                                                    className="dropdown-item d-flex align-items-center",
                                                    href="#",
                                                    children=[
                                                        html.Div(
                                                            className="dropdown-list-image mr-3",
                                                            children=[
                                                                html.Img(className="rounded-circle", src="https://source.unsplash.com/Mv9hjnEUHR4/60x60",
                                                                alt="..."),
                                                                html.Div(className="status-indicator bg-warning")
                                                            ]
                                                        ),
                                                        html.Div(
                                                            children =[ html.Div(
                                                                className="text-truncate",
                                                                children="Here, we will insert message..."
                                                            ),
                                                            html.Div(className="small text-gray-500",
                                                                children='A 20min'
                                                            )
                                                            ]
                                                        )
                                                    ]
                                                ),
                                                html.A(
                                                    children="Read More Messages",
                                                    className="dropdown-item text-center small text-gray-500", href="#",
                                                )   
                                            
                                            ]
                                            )
                                        ]
                                        )   

                                       ]
                                   ),

                                   html.Div(className="topbar-divider d-none d-sm-block"),
                                   # <!-- Nav Item - User Information -->
                                   html.Li(
                                      className="nav-item dropdown no-arrow", 
                                      children=[
                                          html.A(
                                              className="nav-link dropdown-toggle", href="#", id="userDropdown", role="button",
                                                **{'data-toggle':"dropdown"}, **{'aria-haspopup':"true"}, **{'aria-expanded':"false"},
                                               children=[
                                                   html.Span(
                                                      className="mr-2 d-none d-lg-inline text-gray-600 small",
                                                      children="Hove Kouevi."
                                                   ),
                                                   html.Img(
                                                       className="img-profile rounded-circle",
                                                        src="assets/img/Tutor/Hove Kouevi.jpg"
                                                   )
                                               ] 
                                          ),

                                          #  <!-- Dropdown - User Information -->
                                          html.Div(
                                            className="dropdown-menu dropdown-menu-right shadow animated--grow-in",
                                            children=[
                                                html.A(
                                                    className="dropdown-item", href="#",
                                                    children=[
                                                        html.I(className="fas fa-user fa-sm fa-fw mr-2 text-gray-400"),
                                                        "Profile",
                                                    ]
                                                ),
                                                html.A(
                                                    className="dropdown-item", href="#",
                                                    children=[
                                                        html.I(className="fas fa-cogs fa-sm fa-fw mr-2 text-gray-400"),
                                                        "Setting",
                                                    ]
                                                ),
                                                html.Div(className="dropdown-divider"),
                                                dcc.Link(href='/login',  className="dropdown-item", 
                                                children=[
                                                        html.I(className="fas fa-sign-out-alt fa-sm fa-fw mr-2 text-gray-400"),
                                                        "Logout",
                                                    ]
                                                ),
                                                 html.A(
                                                     id='logout',
                                                    className="dropdown-item", href="/login", **{'data-toggle':"modal"} ,**{'data-target':"#logoutModal"},
                                                    children=[
                                                        html.I(className="fas fa-sign-out-alt fa-sm fa-fw mr-2 text-gray-400"),
                                                        "Logout",
                                                    ]
                                                ),
                                            ]
                                          )
                                      ]
                                   )
                                ]
                            ),
                            # <!-- End of Topbar -->

                            # -- Begin Page Content -->
                            html.Div(
                                className="container-fluid",
                                children=[
                                    dcc.Location(id='url_home', refresh=False),
                                    html.Div(
                                        id="page-admin-content"
                        
                                    )
                                ]
                            )
                        ]
                    )
                )


            ]
        )
    ]
)
