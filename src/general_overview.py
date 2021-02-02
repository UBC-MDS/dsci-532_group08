import altair as alt
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from shared import app, data_raw
from viz.us_map import plot_map

tab_general_overview_content = dbc.Card(
    dbc.CardBody([
        dbc.Row([
            dbc.Col(dbc.FormGroup([
                dbc.Label('State'),
                dcc.Dropdown(
                    id='overview-state-dropdown',
                    value=[],
                    multi=True,
                    options=[{'label': col, 'value': col} for col in data_raw.state.sort_values().unique()]),
                html.Br(),
                dbc.Label('Company Size'),
                dcc.Dropdown(
                    id='overview-company-size-dropdown',
                    value=[],
                    multi=True,
                    options=[{'label': col, 'value': col} for col in data_raw.no_employees.unique()]),
                html.Br(),
                dbc.Label('Gender'),
                dcc.Dropdown(
                    id='overview-gender-dropdown',
                    value=[],
                    multi=True,
                    options=[{'label': col, 'value': col} for col in data_raw.Gender.unique()]),
                html.Br(),
                dbc.Label('Age'),
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
                dbc.FormText(id='overview-age-range-text')
            ]), md=2, align='baseline'),
            dbc.Col(dcc.Loading(
                id='overview-loading',
                type='default',
                children=html.Iframe(
                    id='iframe-general-overview',
                    style={'border-width': '0', 'width': '100%', 'height': '70vh'})
            ), align='center')
        ])
    ]),
    className='mt-3',
)


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
