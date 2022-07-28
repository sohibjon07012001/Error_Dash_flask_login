import base64
import datetime
import io
import calendar
import dash
from dash.dependencies import Input, Output, State
from dash import dcc, html, dash_table, callback, Dash
import dash_bootstrap_components as dbc
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import plotly.tools as tls
import plotly.offline as py
import dash_pivottable
from pages.login import layout as login
from flask_login import current_user

dash.register_page(__name__, title='upload dataset page',)



def parse_contents(contents, filename, date):
    content_type, content_string = contents.split(',')

    decoded = base64.b64decode(content_string)

    try:
        if '.csv' in filename:
            # Assume that the user uploaded a CSV file
            df = pd.read_csv(
                io.StringIO(decoded.decode('utf-8')))
            return df
        elif '.xls' in filename:
            # Assume that the user uploaded an excel file
            df = pd.read_excel(io.BytesIO(decoded))
            return df
        elif '.xlsx' in filename:
            # Assume that the user uploaded an excel file
            df = pd.read_excel(io.BytesIO(decoded))
            return df

    except:
        return html.Div([
            'There was an error processing this file.'
        ])

layout = html.Div(id="page_upload_auth_content")


logged_in_layout_upload = html.Div([
    dbc.Tabs([
        dbc.Tab([
            dbc.Row([

                dbc.Col([
                    dbc.Row([
                        dcc.Upload(
                            id='upload-data',
                            children=html.Div([
                                'Drag and Drop or ',
                                html.A('Select Files')
                            ]),
                            style={
                                'width': '100%',
                                'height': '60px',
                                'lineHeight': '60px',
                                'borderWidth': '1px',
                                'borderStyle': 'dashed',
                                'borderRadius': '5px',
                                'textAlign': 'center',
                                'margin': '10px'
                            },
                            style_active={
                                'borderStyle': 'solid', 'borderColor': '#blue', 'backgroundColor': '#eee',
                            },
                            # Allow multiple files to be uploaded
                            multiple=True
                        ),

                    ]),
                    dbc.Row([
                        html.Center(
                            html.P('Select appropriate columns', style={'color': 'black', 'margin-bottom': '1px'})),
                        dcc.Loading(
                            [html.Div(id='change-column-names', style={'margin-bottom': '20px'})]),
                        html.Center(
                            html.P('Click if you have changed the name of the columns', style={'color': 'black', 'margin-bottom': '1px'})),
                        dbc.Button('Change', id='change_button', n_clicks=0),
                    ])
                ], md=4),

                dbc.Col([
                    html.Center(html.H4('Loaded dataset', style={
                                'color': 'black', 'margin-bottom': '1px'})),
                    dcc.Loading([html.Div(id='output-data-upload'),
                                 dash_table.DataTable(
                                     id="download_df",
                                     # data=df[0].to_dict('records'),
                                     # columns=[{'id': c, 'name': c} for c in df[0].columns],
                                     #  columns=,
                                     style_cell={
                                         'textAlign': 'center', 'padding': '5px'},
                                     # filter_action="native",
                                     # fixed_rows={'headers': True},
                                     # style_table={'height': 400},  # defaults to 500,
                                     style_as_list_view=True,
                                     sort_action="native",
                                     sort_mode="multi",
                                     page_action="native",
                                     filter_action='native',
                                     style_header={
                                         'backgroundColor': '#3f454a',
                                         'fontWeight': 'bold',
                                         'border': '1px solid black',
                                         'font-size': '13px',
                                         'color': 'white'
                                     },
                                     style_data={
                                         'color': 'black',
                                     },
                                     style_table={
                                         'height': '500px', 'overflowY': 'auto'},
                                     page_size=14,
                                     page_current=0,
                    ),
                    ]),
                ], md=8)
            ]),
        ], label="Upload", tab_id='Upload'),

        dbc.Tab([
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dcc.Loading(dbc.CardBody([

                            html.Center(html.Strong('Good_Credit')),

                            html.Div(id='good_credit_upload')
                        ]))
                    ])
                ], md=6),

                dbc.Col([
                    dbc.Card([
                        dcc.Loading(dbc.CardBody([

                            html.Center(html.Strong('Bad_Credit_upload')),

                            html.Div(id='bad_credit_upload')
                        ]))
                    ])
                ], md=6)
            ]),

            

        ], label="Descriptive Statistics", tab_id="Descriptive_statistics", ),

        dbc.Tab([
            dcc.Loading(dbc.CardBody([
                html.Div(id='pivottable_upload')
            ]))
        ], label="Dynamic_Report", tab_id="Dynamic_Report", ),

    ], id="Main_tab", active_tab="Upload", className="mt-2"),
])



@callback(Output("page_upload_auth_content", "children"),
          Input("url", "href"),
          Input("partners", "data"))
def authenticate_update(_,partners_data):
    if current_user.is_authenticated and partners_data is not None:
        return logged_in_layout_upload
    return login

