import altair as alt
import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
from dash.dependencies import Input, Output

from us_map import plot_map

data_raw = pd.read_csv('data/processed.csv')

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

tab_general_overview_content = dbc.Card(
    dbc.CardBody([
        dbc.Row([
            dbc.Col([
                html.H5('State:'),
                dcc.Dropdown(
                    id='overview-state-dropdown',
                    value=[],
                    multi=True,
                    options=[{'label': col, 'value': col} for col in data_raw.state.values]),
                html.H5('Company Size:'),
                dcc.Dropdown(
                    id='overview-company-size-dropdown',
                    value=[],
                    multi=True,
                    options=[{'label': col, 'value': col} for col in data_raw.no_employees.unique()]),
                html.H5('Gender:'),
                dcc.Dropdown(
                    id='overview-gender-dropdown',
                    value=[],
                    multi=True,
                    options=[{'label': col, 'value': col} for col in data_raw.Gender.unique()]),
                html.H5('Age:'),
                dcc.RangeSlider(
                    id='overview-age-slider',
                    min=data_raw.Age.min(),
                    max=data_raw.Age.max(),
                    step=1,
                    tooltip={
                        'placement': 'bottomLeft'
                    },
                    value=[data_raw.Age.min(), data_raw.Age.max()]
                ),
                html.Div(id='overview-age-range-text')
            ], md=2),
            dbc.Col([
                dcc.Loading(
                    id="overview-loading",
                    type="default",
                    children=html.Iframe(
                        id='iframe-general-overview',
                        style={'border-width': '0', 'width': '100%', 'height': '60vh'})
                )
            ])
        ])
    ]),
    className="mt-3",
)

app.layout = dbc.Container([
    dbc.Row(html.H2('Mental Health in Tech Dashboard'), justify="center"),
    dbc.Row([
        dbc.Col([
            dbc.Tabs(
                [
                    dbc.Tab(tab_general_overview_content,
                            label="General Overview",
                            tab_id="tab-general-overview"),
                    dbc.Tab(label="Company Support", 
                            tab_id="tab-company-support"),
                ],
                id="card-tabs",
                active_tab="tab-general-overview" 
            )
        ])
    ])
], fluid=True, style={'border-width': '10'})


# Set up callbacks/backend
@app.callback(
    Output('iframe-general-overview', 'srcDoc'),
    Input('overview-state-dropdown', 'value'),
    Input('overview-company-size-dropdown', 'value'),
    Input('overview-gender-dropdown', 'value'),
    Input('overview-age-slider', 'value'))
def plot_general_overview(state, company_size, gender, age_range):
    data = data_raw

    if len(state) != 0:
        data = data.query('state == @state')

    if len(company_size) != 0:
        data = data.query('no_employees == @company_size')

    if len(gender) != 0:
        data = data.query('Gender == @gender')

    if len(age_range) != 0:
        min_age = age_range[0]
        max_age = age_range[1]
        data = data.query('Age >= @min_age and Age <= @max_age')

    wi = alt.Chart(data).mark_bar().encode(
        y='work_interfere',
        x='count()'
    )

    age = alt.Chart(data).mark_bar().encode(
        y='Age',
        x='count()'
    )

    wp = alt.Chart(data).mark_bar().encode(
        y='wellness_program',
        x='count()'
    )

    return (wi & age | plot_map(data) & wp).to_html()

@app.callback(
    Output('overview-age-range-text', 'children'),
    Input('overview-age-slider', 'value'))
def update_output(age_range):
    return f'Selected age range: {age_range[0]} - {age_range[1]}'




if __name__ == '__main__':
    app.run_server(debug=True)
