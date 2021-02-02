import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Input, Output, State

from shared import app

collapse_button = dbc.Row(
    dbc.Button('Help', id='collapse-button', color='primary'),
    no_gutters=True,
    className='ml-auto flex-nowrap mt-5 mt-md-0',
    align='center'
)

collapse = dbc.Collapse(
    [
        dbc.Card(dbc.CardBody('This content is hidden in the collapse')),
        html.Br()
    ],
    id='collapse'
)


@app.callback(
    Output('collapse', 'is_open'),
    [Input('collapse-button', 'n_clicks')],
    [State('collapse', 'is_open')],
)
def toggle_collapse(n, is_open):
    if n:
        return not is_open
    return is_open
