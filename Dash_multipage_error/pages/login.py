import dash
from dash import html, dcc
import dash_bootstrap_components as dbc 


form = dbc.Form([
    dbc.Row(
        [
            dbc.Row([
                html.Center(html.H6("Email")),
            html.Center(dbc.Col(
                dbc.Input(type="username", placeholder="Enter email", id="uname-box"),
                className="me-3",width=5)),
            ]),
            dbc.Row([
                html.Center(html.H6("Password")),
            html.Center(dbc.Col(
                dbc.Input(type="password", placeholder="Enter password", id="pwd-box"),
                className="me-3",width=5,
            )),
            ]),
            dbc.Row([
                html.Center(dbc.Col(dbc.Button("Submit", color="primary", id="login-button"), width="auto"),)
            ])
        ],
        className="g-2",
    ),
    html.Center(html.Div(children="", id="output-state"))
])

# Login screen
layout = html.Div(
    [
       
        dcc.Link("Home", href="/"),
        form

        
    ]
)

dash.register_page(__name__, layout=layout)

"""
If you get this error message:
    dash.exceptions.NoLayoutException: No layout in module pages.login in dash.page_registry

Then register the page like this:

dash.register_page(__name__, layout=layout)

For more info see: https://github.com/AnnMarieW/dash-multi-page-app-demos/issues/1
"""