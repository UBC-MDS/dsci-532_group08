import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Input, Output, State

from shared import app

collapse_button = dbc.Row(
    dbc.Button('Help', id='top-level-collapse-button', color='primary'),
    no_gutters=True,
    className='ml-auto flex-nowrap mt-5 mt-md-0',
    align='center'
)

collapse = dbc.Collapse(
    [
        dbc.Card(dbc.CardBody(
            [
                html.P('Welcome to the mental health in tech dashboard. This dashboard is created to help identify '
                       'main factors that associate with mental health conditions, and help the government and '
                       'organizations understand why supporting mental health is essential.'),
                html.H5('Tabs and dashboards'),
                html.P('There are 2 clickable tabs in the app. The dashboard in General Overview tab contains overall '
                       'summaries across all companies and all respondents, the dashboard in Company Overview tab '
                       'contains summaries on statistics across companies only.'),
                html.H5('Interactive components'),
                html.P('Many plots contains interactive components like tooltips that can reveal more information when '
                       'you hover your mouse on the figures. '),
                html.Hr(),
                html.P('This message can be collapsed/hidden by clicking the Help button.')
            ]
        )),
        html.Br()
    ],
    id='dashboard_description')


@app.callback(
    Output('dashboard_description', 'is_open'),
    [Input('top-level-collapse-button', 'n_clicks')],
    [State('dashboard_description', 'is_open')],
)
def toggle_collapse(n, is_open):
    if n:
        return not is_open
    return is_open
