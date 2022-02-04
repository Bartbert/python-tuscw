import dash
import dash_bootstrap_components as dbc
from dash import html
from dash import dcc
from dash.dependencies import Input, Output, State
import plotly.graph_objs as go
import combat_results as cr
import combatant

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

crt = cr.CombatResultsTable()
attacker = combatant.Attacker()
defender = combatant.Defender()

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
        dbc.Input(type="number", min=0, max=16, step=1, value=1, id="attacker-sp-count"),
    ],
    id="attacker-sp-count-div",

)

attacker_leader_mod = html.Div(
    [
        html.P("Attacking Leader Modifier:", className="m-0"),
        dbc.Input(type="number", min=0, max=6, step=1, value=0, id="attacker-leader-mod"),
    ],
    id="attacker-leader-mod-div",
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

defender_sp_count = html.Div(
    [
        html.P("Defending SP's:", className="m-0"),
        dbc.Input(type="number", min=0, max=16, step=1, value=1, id="defender-sp-count"),
    ],
    id="defender-sp-count-div",
)

defender_leader_mod = html.Div(
    [
        html.P("Defending Leader Modifier:", className="m-0"),
        dbc.Input(type="number", min=0, max=6, step=1, value=0, id="defending-leader-mod"),
    ],
    id="defending-leader-mod-div",
)

defender_fortifications = html.Div(
    [
        html.P("Defending Fortifications Modifier:", className="m-0"),
        dbc.Input(type="number", min=0, max=6, step=1, value=0, id="defender-fortifications"),
    ],
    id="defender-fortifications-div",
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
                dbc.Col(html.Div([
                    dbc.Row(html.Div([
                        dcc.Graph(id='expected-winner', animate=True,
                                  style={'backgroundColor': '#1a2d46', 'color': '#ffffff'})
                    ])),
                    dbc.Row(html.Div("Expected Losses")),
                ]), width=8),
                dbc.Col(html.Div(""), width=1),
            ]
        ),
    ]
)

"""Final Layout Render"""
app.layout = html.Div([
    navbar, body
])

"""App Callback"""


def plot_expected_winner(df_results):
    df_stats = df_results.groupby(['battle_result'], as_index=False)['combined_probability'].sum()

    x = list(df_stats['battle_result'])
    y = list(df_stats['combined_probability'])

    graph = go.Bar(
        x=x,
        y=y,
        name='Expected Battle Outcome',
        marker=dict(color='lightgreen')
    )

    layout = go.Layout(
        paper_bgcolor='#27293d',
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(type='category'),
        yaxis=dict(range=[0, 1]),
        font=dict(color='white')
    )

    return {'data': [graph], 'layout': layout}


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


# Expected Battle Outcome Graph
@app.callback(
    Output('expected-winner', 'figure'),
    [Input('attacker-sp-count', 'value'),
     Input('attacker-leader-mod', 'value'),
     Input('attacker-demoralized', 'value'),
     Input('attacker-special-card', 'value'),
     Input('attacker-naval-support', 'value'),
     Input('defender-sp-count', 'value'),
     Input('defending-leader-mod', 'value'),
     Input('defender-fortifications', 'value'),
     Input('defending-behind-mountains', 'value'),
     Input('defending-behind-river', 'value'),
     Input('defending-naval-support', 'value'),
     Input('defender-foraging', 'value')])
def update_output(attacker_sp_count_value, attacker_leader_mod_val, attacker_demoralized_val,
                  attacker_special_card_val, attacker_naval_support_val, defender_sp_count_val, defender_leader_mod_val,
                  defender_fortifications_val, defender_behind_mountains_val, defender_behind_river_val,
                  defender_naval_support_val, defender_foraging_val):
    attacker.sp_count = attacker_sp_count_value
    attacker.leader_modifier = attacker_leader_mod_val
    attacker.is_demoralized = attacker_demoralized_val
    attacker.special_action = attacker_special_card_val
    attacker.naval_support = attacker_naval_support_val

    defender.sp_count = defender_sp_count_val
    defender.leader_modifier = defender_leader_mod_val
    defender.fortification_modifier = defender_fortifications_val
    defender.defending_behind_mountain = defender_behind_mountains_val
    defender.defending_behind_river = defender_behind_river_val
    defender.naval_support = defender_naval_support_val
    defender.is_foraging = defender_foraging_val

    df = crt.analyze_combat(attacker, defender)

    return plot_expected_winner(df_results=df)


if __name__ == '__main__':
    app.run_server(debug=True, port=8888)
