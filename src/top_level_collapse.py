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
                html.P('There are 2 tabs for the dashboard. The General Overview tab contains summaries across all '
                       'companies and all respondents, the Company Overview tab contains summaries mainly focus on '
                       'statistics across companies only.'),
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
