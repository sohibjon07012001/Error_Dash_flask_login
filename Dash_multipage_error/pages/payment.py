from pydoc import classname
import dash
from dash import dcc, html, State, Input, dash_table, Output, callback
from pkg_resources import load_entry_point
from stock import date_main
import dash_bootstrap_components as dbc
import dateutil.relativedelta
import calendar
import plotly.graph_objects as go
import pandas as pd
import pyodbc
from datetime import date, datetime, timedelta
import math
from dash import Dash
from plotly.subplots import make_subplots
from pages.login import layout as login
from flask_login import current_user

dash.register_page(__name__, title="Payment page")


start_date_picker_paymet = html.Div([
    dcc.DatePickerSingle(
        id='start_date_picker_payment',
        # min_date_allowed=date(1995, 8, 5),
        # max_date_allowed=date(2017, 9, 19),
        # initial_visible_month=date(2017, 8, 5),
        date=date.today().strftime('%Y-%m-%d'),
        display_format='DD-MM-YYYY'
    ),
])

end_date_picker_payment = html.Div([
    dcc.DatePickerSingle(
        id='end_date_picker_payment',
        # min_date_allowed=date(1995, 8, 5),
        # max_date_allowed=date(2017, 9, 19),
        # initial_visible_month=date(2017, 8, 5),
        date=date.today().strftime('%Y-%m-%d'),
        display_format='DD-MM-YYYY'
    ),
])

button_group_payment = html.Div(
    [
        dbc.RadioItems(
            id="radios_payment",
            className="btn-group",
            inputClassName="btn-check",
            labelClassName="btn btn-outline-primary",
            labelCheckedClassName="active",
            options=[
                # {"label": "Today", "value": 1},
                # {"label": "Yesterday", "value": 2},
                # {"label": "Weekly", "value": 3},
                # {"label": "Monthly", "value": 4},
                # {"label": "Annually", "value": 5},
                # {"label": "Last 6 Month", "value": 6},
            ],
            value=1,
        ),
        html.Div(id="output_paymetn"),
    ],
    className="radio-group",
)

layout = html.Div(id="page_payment_auth_content")

logged_in_layout_payment = html.Div(
    [
        dbc.Row([
            dbc.Col([button_group_payment]),
            dbc.Col([dcc.Dropdown(id='partner_id_dropdown_payment',
                                  clearable=False, style={"border-radius": "20px"})]),
            dbc.Col([start_date_picker_paymet]),
            dbc.Col([end_date_picker_payment]),

            dbc.Col([dbc.Button("Update", color="info",
                                className="me-1", id="button_update_payment")])
        ]),
        html.Hr(
            style={'margin-top': '10px', 'margin-bottom': '1px'}),
        dcc.Interval(
            id='interval_component_payment',
            interval=20*10*1000,
            n_intervals=0),

        dbc.Row([

            html.Center([
                        html.Strong(id="payment_logs")
                        ]),

            html.Center([
                dcc.Loading(dash_table.DataTable(
                        id='tbl_payment',
                        style_cell={'textAlign': 'center',
                                    'padding': '5px'},
                        filter_action="native",
                        # style_as_list_view=True,
                        sort_action="native",
                        sort_mode="multi",
                        page_action="native",
                        style_header={
                            'backgroundColor': '#e4ebf5',
                            'fontWeight': 'bold',
                            'border': '1px solid black',
                            'font-size': '13px'
                        },
                        style_table={'width': '600px', 'overflowY': 'auto', 'overflowX': 'auto',
                                     "margin-left": "400px"},
                        # page_size=15,
                        # page_current=0,

                        )),
            ]),




            dbc.Row([
                html.Center([
                    dbc.Button(id='btn_payment', children=[html.I(className="fa fa-download mr-1"), "Download"], color="info",
                               className="mt-1", style={"height": "50px", "width": "100px", "right": "0px"}),
                    dcc.Download(id="download-component_payment"),
                ])

            ])


        ]),
    ]
)



@callback(Output("page_payment_auth_content", "children"),
          Input("url", "href"),
          Input("partners", "data"))
def authenticate(_, partners_data):
    if current_user.is_authenticated and partners_data is not None:
        return logged_in_layout_payment
    return login



@callback(
    Output("partner_id_dropdown_payment", "options"),
    Output("partner_id_dropdown_payment", "value"),
    Input("partners", "data")
)
def update_count_of_partners(data):
    return data, list(data.keys())[0]


@callback(
    Output('radios_payment', 'options'),
    Input('interval_component_payment', 'n_intervals'),
)
def optionss(interval_payment):
    def datee(a, b):
        start_date = date.today().replace((date.today() + dateutil.relativedelta.relativedelta(months=-a)).year,
                                          (date.today() + dateutil.relativedelta.relativedelta(months=-a)).month, 1)

        lastday = date.today().replace((date.today() + dateutil.relativedelta.relativedelta(months=-b)).year,
                                       (date.today() + dateutil.relativedelta.relativedelta(months=-b)).month, 1)
        end_date = []
        for i in range(1, 2):
            end_date.append(str(lastday - timedelta(days=i)))
        return start_date.month, str(start_date), end_date[0]

    val = {1: 'January', 2: 'February', 3: 'March', 4: 'April', 5: 'May', 6: 'June', 7: 'July', 8: 'August',
           9: 'September', 10: 'October', 11: 'November', 12: 'Desember'}

    options = [{"label": "Today", "value": 1},
               {"label": "Yesterday", "value": 2},
               {"label": "Weekly", "value": 3},
               {"label": "Monthly", "value": 4},
               {"label": "Annually", "value": 5}, ]
    for i in range(6):
        options.append({'label': val.get(
            datee(i + 1, i)[0]), 'value': [datee(i + 1, i)[1], datee(i + 1, i)[2]]})
    return options


@callback(
    Output("start_date_picker_payment", "date"),
    Output("end_date_picker_payment", "date"),
    Input('interval_component_payment', 'n_intervals'),
    Input("radios_payment", "value"),
)
def update_date_logs(interval_payment, value_payment):
    if value_payment == 1:
        start_date = date_main("daily")[0]
        end_date = date_main("daily")[1]
    elif value_payment == 2:
        start_date = date_main("lastday")[0]
        end_date = date_main("lastday")[1]
    elif value_payment == 3:
        start_date = date_main("weekly")[0]
        end_date = date_main("weekly")[1]
    elif value_payment == 4:
        start_date = date_main("monthly")[0]
        end_date = date_main("monthly")[1]
    elif value_payment == 5:
        start_date = date_main("annually")[0]
        end_date = date_main("annually")[1]
    elif len(value_payment) == 2:
        start_date = value_payment[0]
        end_date = value_payment[1]
    return start_date, end_date

