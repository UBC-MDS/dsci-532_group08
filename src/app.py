import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
from dash.dependencies import Input, Output
import altair as alt

from src.us_map import plot_map

data_raw = pd.read_csv('data/processed.csv')

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server
app.layout = dbc.Container([
    dbc.Row(html.H1('Mental Health in Tech Dashboard')),
    dbc.Row([
        dbc.Col([
            html.H4('State:'),
            dcc.Dropdown(
                id='state-dropdown',
                value=[],  # REQUIRED to show the plot on the first page load
                multi=True,
                options=[{'label': col, 'value': col} for col in data_raw.state.values]),
            html.H4('Company Size:'),
            dcc.Dropdown(
                id='company-size-dropdown',
                value=[],  # REQUIRED to show the plot on the first page load
                multi=True,
                options=[{'label': col, 'value': col} for col in data_raw.no_employees.unique()])
        ], md=2),
        dbc.Col([
            html.Iframe(
                id='scatter',
                style={'border-width': '0', 'width': '100%', 'height': '60vh'})
        ])
    ])
], fluid=True)


# Set up callbacks/backend
@app.callback(
    Output('scatter', 'srcDoc'),
    Input('state-dropdown', 'value'),
    Input('company-size-dropdown', 'value'))
def plot_altair(state, company_size):
    data = data_raw

    if len(state) != 0:
        data = data.query('state == @state')

    if len(company_size) != 0:
        data = data.query('no_employees == @company_size')

    wi = alt.Chart(data).mark_bar().encode(
        y='work_interfere',
        x='count()'
    )

    ge = alt.Chart(data).mark_bar().encode(
        y='Gender',
        x='count()'
    )

    return (wi & ge | plot_map(data)).to_html()


if __name__ == '__main__':
    app.run_server(debug=True)
