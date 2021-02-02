import altair as alt
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from shared import app, data_raw

state_choice = data_raw.state.unique()
state_choice.sort()

company_size_choice = data_raw.no_employees.unique()
company_size_choice.sort()

tab_company_support_content = dbc.Card(
    dbc.CardBody([
        dbc.Row([
            dbc.Col(dbc.FormGroup([
                dbc.Label('State'),
                dcc.Dropdown(
                    id='company-support-state-dropdown',
                    value=[],
                    multi=True,
                    options=[{'label': col, 'value': col} for col in state_choice]),
                dbc.FormText('The state or territory where the respondents live in'),
                html.Br(),
                dbc.Label('Company Size'),
                dcc.Dropdown(
                    id='company-support-company-size-dropdown',
                    value=[],
                    multi=True,
                    options=[{'label': col, 'value': col} for col in company_size_choice]),
                dbc.FormText('Size of the companies the respondents working for'),
                html.Br(),
                dbc.Label('Tech Company'),
                dcc.RadioItems(
                    id='company-support-tech-company-radioitems',
                    options=[
                        {'label': 'All', 'value': 'All'},
                        {'label': 'Yes', 'value': 'Yes'},
                        {'label': 'No', 'value': 'No'}
                    ],
                    labelStyle={'display': 'inline-block', 'margin-right': '15px'},
                    inputStyle={'margin-right': '5px'},
                    value='All'
                ),
                dbc.FormText('Is the respondents\' company primarily a tech company or organization?'),
                html.Br(),
                dbc.Label('Remote Work'),
                dcc.RadioItems(
                    id='company-support-remote-work-radioitems',
                    options=[
                        {'label': 'All', 'value': 'All'},
                        {'label': 'Yes', 'value': 'Yes'},
                        {'label': 'No', 'value': 'No'}
                    ],
                    labelStyle={'display': 'inline-block', 'margin-right': '15px'},
                    inputStyle={'margin-right': '5px'},
                    value='All'
                ),
                dbc.FormText('Is the respondents\' work remotely (outside of an office) at least 50% of the time?')
            ]), md=2, align='baseline'),
            dbc.Col(dcc.Loading(
                id='company-support-loading',
                type='default',
                children=html.Iframe(
                    id='iframe-company-support',
                    style={'border-width': '0', 'width': '100%', 'height': '70vh'})
            ), align='center')
        ])
    ]),
    className='mt-3')


# Set up callbacks/backend
@app.callback(
    Output('iframe-company-support', 'srcDoc'),
    Input('company-support-state-dropdown', 'value'),
    Input('company-support-company-size-dropdown', 'value'),
    Input('company-support-tech-company-radioitems', 'value'),
    Input('company-support-remote-work-radioitems', 'value'))
def plot_general_overview(state, company_size, is_tech, is_remote_work):
    data = data_raw

    if len(state) != 0:
        data = data.query('state == @state')

    if len(company_size) != 0:
        data = data.query('no_employees == @company_size')

    if is_tech.lower() != 'all':
        data = data.query('tech_company == @is_tech')

    if is_remote_work.lower() != 'all':
        data = data.query('remote_work == @is_remote_work')

    wp = alt.Chart(data).mark_bar().encode(
        y=alt.Y('wellness_program', title='Wellness program'),
        x=alt.X('count()', title='Respondent count'),
        color='Gender'
    ).properties(
        title='Is Mental health part of the employee wellness program?',
        height=200
    )

    return wp.configure_legend(
        titleFontSize=15,
        labelFontSize=13
    ).configure_title(fontSize=18).configure_axis(
        labelFontSize=13,
        titleFontSize=13
    ).to_html()
