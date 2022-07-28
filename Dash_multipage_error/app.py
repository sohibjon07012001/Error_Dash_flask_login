import os
from flask import Flask
from flask_login import login_user, LoginManager, UserMixin, logout_user, current_user
import dash_bootstrap_components as dbc
import dash
from dash import dcc, html, Input, Output, State
import hashlib
from stock import partner_names1

# Exposing the Flask Server to enable configuring it for logging in
server = Flask(__name__)
app = dash.Dash(
    __name__, server=server, use_pages=True, suppress_callback_exceptions=True, external_stylesheets=[dbc.themes.MORPH],
)

# Keep this out of source code repository - save in a file or a database
#  passwords should be encrypted
VALID_USERNAME_PASSWORD = {"test": "test", "hello": "world"}


# Updating the Flask Server configuration with Secret Key to encrypt the user session cookie
server.config.update(SECRET_KEY=os.urandom(24))

# Login manager object will be used to login / logout users
login_manager = LoginManager()
login_manager.init_app(server)
login_manager.login_view = "/login"


class User(UserMixin):
    # User data model. It has to have at least self.id as a minimum
    def __init__(self, username):
        self.id = username


@login_manager.user_loader
def load_user(username):
    """This function loads the user by user id. Typically this looks up the user from a user database.
    We won't be registering or looking up users in this example, since we'll just login using LDAP server.
    So we'll simply return a User object with the passed in username.
    """
    return User(username)



navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("Payment", href=dash.page_registry['pages.payment']['path'], 
        style={
                    "padding-right": "4rem"})),
        dbc.NavItem(dbc.NavLink("Upload",
                    href=dash.page_registry['pages.upload']['path'],
                    style={"padding-right": "4rem"})),
       
        dbc.DropdownMenu(
            nav=True,
            in_navbar=True,
            label="Menu",
            menu_variant="dark",
            align_end=True,
        ),
        html.Div(id="user-status-header", style={"margin-left":"10px", "margin-top":'3px'}),
    ],
    brand="zypl.score post-analysis",
    brand_href="#",
    dark=True,
    fluid=True,
    style={
        # 'margin-right':'20px',
        # 'fontSize': '1px ',
        # "position": "fixed",
        # "top": 10,
        # "left": 1,
        # "bottom": 1,
        # "width": "10rem",
        # "height": "100%",
        # "z-index": 1,
        # "overflow-x": "hidden",
        # "transition": "all 0.4s",
        # "padding": "0.5rem 1rem",
    },
    class_name='color-navbar'
)



app.layout = html.Div(
    [
        navbar,
        dcc.Location(id="url"),
        dcc.Store(id="login-status", storage_type="session"),
        dcc.Store(id="partners", storage_type="session"),
        html.Hr(),
        dash.page_container,
    ]
)

@app.callback(
    Output("user-status-header", "children"),
    Input("url", "pathname"),
)
def update_authentication_status(path):
    logged_in = current_user.is_authenticated
    if path == "/logout" and logged_in:
        logout_user()
    if logged_in:
        return html.Span(dbc.Badge("logout",href="/logout",color="danger",className="me-1 text-decoration-none")), #dcc.Link("logout", href="/logout")
    return html.Span(dbc.Badge("Login",href="/login",color="info",className="me-1 text-decoration-none")), #dcc.Link("login", href="/login")


@app.callback(
    Output("partners", "data"),
    Output("output-state", "children"),
    Input("login-button", "n_clicks"),
    State("uname-box", "value"),
    State("pwd-box", "value"),
    prevent_initial_call=True,
)
def login_button_click(n_clicks, username, password):
    df = partner_names1()
    if n_clicks is not None:
        hash_password = hashlib.md5(password.encode("utf-8")).hexdigest()
        if username in str(df['login']) and  hash_password in str(df[df['login'] == username]['password']):
            login_user(User(username))
            if username == "zyplscore":
                zyp_all_partners = df[~df['login'].isin(['zyplscore'])]
                option = {i: z for i,z in zip(zyp_all_partners['id'], zyp_all_partners['partner'])}
            else:
                s = df[df['login']==username]
                option = {i:z for i,z in zip(s['id'], s['partner'])}
            return option, "Successful login"
        else:
            return None, "incorrect username or password"
    else:
        return None, "Enter your username and password"

 
if __name__ == "__main__":
    app.run_server(debug=True)



