import dash
import dash_bootstrap_components as dbc
from dash import html
from dash.dependencies import Input, Output, State

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

"""Navbar"""
APP_LOGO = "static/images/tuscw.jpg"

nav = dbc.Nav(
    [
        dbc.DropdownMenu(
            [
                dbc.DropdownMenuItem('GMT Game Page',
                                     href='https://www.gmtgames.com/p-729-the-us-civil-war-2nd-printing.aspx',
                                     target='blank'),
                dbc.DropdownMenuItem(divider=True),
                dbc.DropdownMenuItem('Rules',
                                     href='https://s3-us-west-2.amazonaws.com/gmtwebsiteassets/USCW/TUSCWRULESAug2017-LR.pdf',
                                     target='blank'),
                dbc.DropdownMenuItem('Player Aid Card',
                                     href='https://s3-us-west-2.amazonaws.com/gmtwebsiteassets/USCW/TUSCW-PAC-May2017-FINAL.pdf',
                                     target='blank')],
            label="Useful Resources",
            nav=True
        )
    ],
    navbar=True)

navbar = dbc.Navbar(
    dbc.Container(
        [
            html.A(
                # Use row and col to control vertical alignment of logo / brand
                dbc.Row(
                    [
                        dbc.Col(html.Img(src=APP_LOGO, height="50px")),
                        dbc.Col(dbc.NavbarBrand("The U.S. Civil War Battle Analyzer", className="ms-2")),
                    ],
                    align="center",
                    className="g-0",
                ),
                style={"textDecoration": "none"},
            ),
            dbc.NavbarToggler(id="navbar-toggler", n_clicks=0),
            dbc.Collapse(
                [nav],
                className='ml-auto',
                id="navbar-collapse",
                is_open=False,
                navbar=True,
            ),
        ]
    ),
    color="dark",
    dark=True,
    className='mb-5'
)

"""Navbar END"""

"""Body Content"""

attacker_sp_count = html.Div(
    [
        html.P("Attacking SP's:", className="m-0"),
        dbc.Input(type="number", min=0, max=16, step=1, value=1),
    ],
    id="attacker-sp-count",

)

attacker_leader_mod = html.Div(
    [
        html.P("Attacking Leader Modifier:", className="m-0"),
        dbc.Input(type="number", min=0, max=6, step=1, value=1),
    ],
    id="attacker-leader-mod",
)

attacker_options = html.Div(
    [
        html.Div(
            [
                dbc.Checkbox(
                    id="attacker-demoralized",
                    label="Attacker is Demoralized",
                    value=False,
                ),
                dbc.Checkbox(
                    id="attacker-special-card",
                    label="Attacker played Special Card",
                    value=False,
                ),
                dbc.Checkbox(
                    id="attacker-naval-support",
                    label="Attacker has Naval Support",
                    value=False,
                ),
            ]
        ),
        html.P(id="attacker-options"),
    ]
)

defender_leader_mod = html.Div(
    [
        html.P("Defending Leader Modifier:", className="m-0"),
        dbc.Input(type="number", min=0, max=6, step=1, value=1),
    ],
    id="defending-leader-mod",
)

defender_sp_count = html.Div(
    [
        html.P("Defending SP's:", className="m-0"),
        dbc.Input(type="number", min=0, max=16, step=1, value=1),
    ],
    id="defender-sp-count",
)

defender_fortifications = html.Div(
    [
        html.P("Defending Fortifications Modifier:", className="m-0"),
        dbc.Input(type="number", min=0, max=6, step=1, value=1),
    ],
    id="defender-fortifications",
)

defender_options = html.Div(
    [
        html.Div(
            [
                dbc.Checkbox(
                    id="defending-behind-mountains",
                    label="Defending behind mountains",
                    value=False,
                ),
                dbc.Checkbox(
                    id="defending-behind-river",
                    label="Defending behind river",
                    value=False,
                ),
                dbc.Checkbox(
                    id="defending-naval-support",
                    label="Defender has Naval Support",
                    value=False,
                ),
                dbc.Checkbox(
                    id="defender-foraging",
                    label="Defender is Foraging",
                    value=False,
                ),
            ]
        ),
        html.P(id="defender-options"),
    ]
)
body = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(html.Div(), width=1),
                dbc.Col(html.Div([
                    dbc.Row(html.Div([
                        attacker_sp_count,
                        html.P(),
                        attacker_leader_mod,
                        html.P(),
                        attacker_options,
                    ]),
                        className="p-2 bg-light border rounded-3 border-primary"),
                    dbc.Row(html.Div([html.P(), html.Hr()])),
                    dbc.Row(html.Div([
                        defender_sp_count,
                        html.P(),
                        defender_leader_mod,
                        html.P(),
                        defender_fortifications,
                        html.P(),
                        defender_options,
                    ],
                        className="p-2 bg-light border rounded-3 border-success")),
                ]), width=2),
                dbc.Col(html.Div("Spacer"), width=1),
                dbc.Col(html.Div([
                    dbc.Row(html.Div("Expected Winner")),
                    dbc.Row(html.Div("Expected Losses")),
                ]), width=8),

            ]
        ),
    ]
)

"""Final Layout Render"""
app.layout = html.Div([
    navbar, body
])

"""App Callback"""


# Navbar
@app.callback(
    Output("navbar-collapse", "is_open"),
    [Input("navbar-toggler", "n_clicks")],
    [State("navbar-collapse", "is_open")],
)
def toggle_navbar_collapse(n, is_open):
    if n:
        return not is_open
    return is_open


if __name__ == '__main__':
    app.run_server(debug=True, port=8888)
