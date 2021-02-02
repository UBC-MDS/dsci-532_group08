import altair as alt
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from shared import app, data_raw
from viz.us_map import plot_map

state_choice = data_raw.state.unique()
state_choice.sort()

company_size_choice = data_raw.no_employees.unique()
company_size_choice.sort()

tab_general_overview_content = dbc.Card(
    dbc.CardBody([
        dbc.Row([
            dbc.Col(dbc.FormGroup([
                dbc.Label('State'),
                dcc.Dropdown(
                    id='overview-state-dropdown',
                    value=[],
                    multi=True,
                    options=[{'label': col, 'value': col} for col in state_choice]),
                dbc.FormText('The state or territory where the respondents live in'),
                html.Br(),
                dbc.Label('Company Size'),
                dcc.Dropdown(
                    id='overview-company-size-dropdown',
                    value=[],
                    multi=True,
                    options=[{'label': col, 'value': col} for col in company_size_choice]),
                dbc.FormText('Size of the companies the respondents working for'),
                html.Br(),
                dbc.Label('Gender'),
                dcc.RadioItems(
                    id='overview-gender-radioitems',
                    options=[
                        {'label': 'All', 'value': 'All'},
                        {'label': 'Female', 'value': 'female'},
                        {'label': 'Male', 'value': 'male'},
                        {'label': 'Other', 'value': 'Other'}
                    ],
                    labelStyle={'display': 'inline-block', 'margin-right': '10px'},
                    inputStyle={'margin-right': '5px'},
                    value='All'
                ),
                dbc.FormText('Gender of the respondents'),
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
                dbc.FormText('Age range of the respondents'),
                dbc.FormText(id='overview-age-range-text')
            ]), md=2, align='baseline'),
            dbc.Col(dcc.Loading(
                id='overview-loading',
                type='default',
                children=html.Iframe(
                    id='iframe-general-overview',
                    style={'border-width': '0', 'width': '100%', 'height': '90vh'})),
                align='center')
        ])
    ]),
    className='mt-3')


# Set up callbacks/backend
@app.callback(
    Output('iframe-general-overview', 'srcDoc'),
    Input('overview-state-dropdown', 'value'),
    Input('overview-company-size-dropdown', 'value'),
    Input('overview-gender-radioitems', 'value'),
    Input('overview-age-slider', 'value'))
def plot_general_overview(state, company_size, gender, age_range):
    data = data_raw

    if len(state) != 0:
        data = data.query('state == @state')

    if len(company_size) != 0:
        data = data.query('no_employees == @company_size')

    if gender.lower() != 'all':
        data = data.query('Gender == @gender')

    if len(age_range) != 0:
        min_age = age_range[0]
        max_age = age_range[1]
        data = data.query('Age >= @min_age and Age <= @max_age')

    wi = alt.Chart(data).mark_bar().encode(
        y=alt.Y('work_interfere', title='Work interference frequency'),
        x=alt.X('count()', title='Respondent count'),
        color='Gender'
    ).properties(
        title='Does mental health condition interferes work?',
        height=200
    )

    age = alt.Chart(data).mark_bar().encode(
        y=alt.Y('Age', title='Age', bin=alt.Bin(maxbins=20)),
        x=alt.X('count()', title='Respondent count'),
        color='Gender'
    ).properties(
        title='Age distribution',
        height=200
    )

    return (plot_map(data) & (wi | age)).configure_legend(
        titleFontSize=15,
        labelFontSize=13
    ).configure_title(fontSize=18).configure_axis(
        labelFontSize=13,
        titleFontSize=13
    ).to_html()


@app.callback(
    Output('overview-age-range-text', 'children'),
    Input('overview-age-slider', 'value'))
def update_output(age_range):
    return f'Selected age range: {age_range[0]} - {age_range[1]}'
