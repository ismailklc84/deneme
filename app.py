from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from flask import Flask, session
from datetime import timedelta
import dash
import dash_mantine_components as dmc
from dash.dependencies import Input, Output, State
from dash_iconify import DashIconify
from dash import Output, Input, clientside_callback, dcc, page_container, State, Dash, html
import dash_bootstrap_components as dbc
dash._dash_renderer._set_react_version("18.2.0")
import pandas as pd
from dash.exceptions import PreventUpdate

stylesheets = [
    dmc.styles.DATES,
    dmc.styles.CODE_HIGHLIGHT,
    dmc.styles.CHARTS,
    dmc.styles.CAROUSEL,
    dmc.styles.NOTIFICATIONS,
    dmc.styles.NPROGRESS,
]

scripts = [
    "https://cdnjs.cloudflare.com/ajax/libs/dayjs/1.10.8/dayjs.min.js",
    "https://cdnjs.cloudflare.com/ajax/libs/dayjs/1.10.8/locale/ru.min.js",
    "https://cdnjs.cloudflare.com/ajax/libs/dayjs/1.10.8/locale/fr.min.js",
    "https://www.googletagmanager.com/gtag/js?id=G-4PJELX1C4W",
    "https://media.ethicalads.io/media/client/ethicalads.min.js",
    "https://unpkg.com/hotkeys-js/dist/hotkeys.min.js",
]

stock_list = pd.read_excel('data/stock_list.xlsx')
# stock_list['stock_full_name'] = stock_list['code'] + ' - ' + stock_list['title']
stock_names = stock_list['code'].tolist()

server = Flask(__name__)
server.secret_key = 'edwDash'
server.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=10)


app = Dash(
    __name__,
    suppress_callback_exceptions=True,
    use_pages=True,  
    server=server,  
    external_scripts=scripts,
    external_stylesheets=stylesheets,
    update_title=None,
)


# Initialize LoginManager
login_manager = LoginManager()
login_manager.init_app(server)

# User model


class User(UserMixin):
    def __init__(self, id):
        self.id = id

# User loader callback


@login_manager.user_loader
def load_user(user_id):
    return User(user_id)

header = dmc.AppShellHeader(
    px=0,
    children=[
    dmc.Stack(
        justify="center",
                h=70,
        children=[
            dmc.Grid(
            children=[
                dmc.GridCol(
                    dmc.Group(
                        [
                            dmc.Burger(id="burger-button",  size="sm"),
                            dmc.Anchor(
                                "edwDash", size="xl", href="/", underline=False
                            ),
                            dmc.Select(
                                id='stock_dropdown',
                                # value='ISMEN',
                                searchable=True,
                                data=[{'label': x, 'value': x}
                                      for x in stock_names],
                                style={"flexGrow": 1, "maxWidth": "400px",
                                       "marginLeft": "auto", "marginRight": "auto"},
                                placeholder="Search"),
                        ],
                        h="100%",
                        px="md",
                    ),
                    span="content",
                ),
                dmc.GridCol(
                    span="auto",
                    children=dmc.Group(
                        justify="flex-end",
                        h=31,
                        gap="xl",
                        children=[
                            dmc.ActionIcon(
                                [
                                    DashIconify(
                                        icon="radix-icons:moon",
                                        width=25,
                                        id="dark-theme-icon",
                                    ),
                                ],
                                variant="transparent",
                                color="yellow",
                                id="color-scheme-toggle",
                                size="lg",
                            )
                        ],
                    ),
                )
            ])
        ]
    )
    ]
)



def create_main_link(icon, label, href):
    return dmc.Anchor(
        dmc.Group(
            [
                DashIconify(
                    icon=icon,
                    width=23,
                    #color=dmc.DEFAULT_THEME["colors"][PRIMARY_COLOR][5],
                ),
                dmc.Text(label, size="sm"),
            ]
        ),
        href=href,
        variant="text",
        mb=5,
        underline=False,
    )
    

def get_icon(icon):
    return DashIconify(icon=icon, height=16)


main_links = dmc.Stack(
    gap=0,    
    children=[
        dmc.NavLink(
            label="Home",
            leftSection=get_icon(icon="bi:house-door-fill"),
            variant="filled",
            href="/",
        ),
        dmc.NavLink(
            label="Job Connections",
            leftSection=get_icon(icon="icon-park-outline:connection-box"),
            href="/page1",
        ),
        dmc.NavLink(
            label="Report Analysis",
            leftSection=get_icon(icon="lsicon:report-filled"),
            href="/page2",
        ),
    ],
)

navbar = dmc.AppShellNavbar(
    [
        #dmc.AppShellSection("Navbar header"),
        dmc.AppShellSection(
            [
                dmc.ScrollArea(
                    offsetScrollbars=False,
                    scrollbarSize=5,
                    type="scroll",
                    style={"height": "100%", "overflow": "auto"},
                    children=dmc.Stack(
                        gap=0, children=[main_links, dmc.Space(h=3)]),
                )

            ],
            grow=True,
            #my="md",
            style={"display": "flex", "flexDirection": "column"},
        ),
        #dmc.AppShellSection("Navbar footer – always at the bottom"),
    ],
    #p="md",
    id="navbar",
    style={"display": "flex", "flexDirection": "column",},
)

app_shell = dmc.AppShell(
    [
        header,
        navbar,
        dmc.AppShellMain(children=page_container),
    ],
    header={"height": 60},
    navbar={
        "width": 200,
        "breakpoint": "sm",
        "collapsed": {"desktop": True},
    },
    padding="sm",
    id="app-shell",
)


""" def login_layout():
    return dmc.MantineProvider([
        dbc.Container([
        html.H2("Login", className="text-center"),
        dbc.Input(id="username", placeholder="Enter username",
                  type="text", className="mb-2"),
        dbc.Input(id="password", placeholder="Enter password",
                  type="password", className="mb-2"),
        dbc.Button("Login", id="login-button",
                   color="primary", className="mt-2"),
        html.Div(id="login-output", className="text-danger mt-2")
    ], className="mt-5")
    ],
    forceColorScheme="dark") """
    

def login_layout():
    return dmc.MantineProvider([
        dcc.Store(id="theme-store", storage_type="local"),
           dmc.Box(
           dmc.Center(
               dmc.Paper([
                   # Add logo here
                   html.Img(src="/assets/edwDash_Logo.png",
                            style={"width": "400px", "marginBottom": "20px"}),
                   dmc.TextInput(
                       id="username", placeholder="Enter username",value="",leftSection= DashIconify(icon="radix-icons:person"), style={"width": "400px"}, mt=10),
                   dmc.PasswordInput(
                       id="password", placeholder="Enter password",value="", leftSection=DashIconify(icon="radix-icons:lock-closed"),style={"width": "400px"}, mt=10),
            #       dmc.Checkbox(
            #           label="Remember me",
            #           checked=True,
            #           mt=10
                   #       ),
                   dmc.Button("Login", id="login-button", color="blue", style={"width": "400px"}, mt=10),
                   dmc.Space(h=2),
                   html.Div(id="login-alert-container",
                            style={"display": "flex", "justifyContent": "center"}),
               ],
                withBorder=True,p=20)
           ),
               style={
               "display": "flex",
               "alignItems": "center",
               "justifyContent": "center",
               "height": "100vh"
           }
           )
    ],
        forceColorScheme="dark")



def app_layout():
    return dmc.MantineProvider([dcc.Store(id="color-scheme-storage", storage_type="local"),  app_shell],
                               forceColorScheme="dark",
                               id="m2d-mantine-provider",
                               )


app.title = "Multi-Page Dash Application"
app.layout = html.Div([
    dcc.Store(id="login-state", data=False),  # Stores login state
    # Layout Wrapper for Login and Main Content
    html.Div(id="page-content", children=[]),
    html.Div(id="login-error-message",
              style={"color": "red", "marginTop": "10px"}),
    # Placeholder for error message
])


@app.callback(
    Output("page-content", "children"),
    Input("login-state", "data")
)
def display_layout(is_logged_in):
    if is_logged_in or current_user.is_authenticated:
        return app_layout()  # Show main app if logged in
    return login_layout()  # Show login page if not logged in

@app.callback(
    Output("login-state", "data", allow_duplicate=True),
    Output("login-error-message", "children"),    
    State("username", "value"),
    State("password", "value"),
    Input("login-button", "n_clicks"),
    prevent_initial_call=True
)
def verify_login(username, password, n_clicks):
    if n_clicks is None:
        return dash.no_update, dash.no_update
    
    if username == "admin" and password == "password":
        user = User(id=username)
        login_user(user)
        session.permanent = True
        return True, ""
    return False, dmc.MantineProvider([
        dmc.Alert(
        "Invalid username or password",
        title="Info",
        color="red",
        variant="light",
        duration=1500,
        withCloseButton=True,
            style={
                "position": "fixed",
                "top": "20px",
                "left": "50%",
                "transform": "translateX(-50%)",
                "zIndex": 9999,
                "width": "400px"
            }
    )
    ], forceColorScheme="dark")



@app.callback(
    Output("app-shell", "navbar"),
    Input("burger-button", "opened"),
    State("app-shell", "navbar"),
)
def toggle_navbar(opened, navbar):
    navbar["collapsed"]["desktop"] = not opened
    return navbar


clientside_callback(
    "function(colorScheme) {return colorScheme}",
    Output("m2d-mantine-provider", "forceColorScheme"),
    Input("color-scheme-storage", "data")
)

clientside_callback(
    'function(n_clicks, theme) {return theme === "dark" ? "light" : "dark"}',
    Output("color-scheme-storage", "data"),
    Input("color-scheme-toggle", "n_clicks"),
    State("color-scheme-storage", "data"),
    prevent_initial_call=True,
)


if __name__ == "__main__":
    app.run_server(debug=True)


