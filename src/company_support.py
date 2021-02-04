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
                dbc.RadioItems(
                    id='company-support-tech-company-radioitems',
                    options=[
                        {'label': 'All', 'value': 'All'},
                        {'label': 'Yes', 'value': 'Yes'},
                        {'label': 'No', 'value': 'No'}
                    ],
                    inline=True,
                    value='All'
                ),
                dbc.FormText('Is the respondents\' company primarily a tech company or organization?'),
                html.Br(),
                dbc.Label('Remote Work'),
                dbc.RadioItems(
                    id='company-support-remote-work-radioitems',
                    options=[
                        {'label': 'All', 'value': 'All'},
                        {'label': 'Yes', 'value': 'Yes'},
                        {'label': 'No', 'value': 'No'}
                    ],
                    inline=True,
                    value='All'
                ),
                dbc.FormText('Is the respondents\' work remotely (outside of an office) at least 50% of the time?')
            ]), md=2, align='baseline'),
            dbc.Col(dcc.Loading(
                id='company-support-loading',
                type='default',
                children=dbc.Col([
                    html.Iframe(id='iframe-company-support-1',
                                style={'border-width': '0', 'width': '100%', 'height': '48vh'}),
                    dbc.Col([
                        html.Hr(),
                        html.P('Plots below are related to specific questions in the survey. Full description of the '
                               'question labels is listed in the following table:'),
                        dbc.Table([
                            html.Thead(html.Tr([html.Th('Label'), html.Th('Full Description')])),
                            html.Tr([html.Td('Anonymity'), html.Td('Is your anonymity protected if you choose to take '
                                                                   'advantage of mental health or substance abuse '
                                                                   'treatment resources?')]),
                            html.Tr(
                                [html.Td('Benefits'), html.Td('Does your employer provide mental health benefits?')]),
                            html.Tr([html.Td('Mental vs physical'), html.Td('Do you feel that your employer takes '
                                                                            'mental health as seriously as physical '
                                                                            'health?')]),
                            html.Tr([html.Td('Resources'), html.Td(
                                'Does your employer provide resources to learn more about mental health issues and how '
                                'to seek help?')]),
                            html.Tr([html.Td('Wellness program'), html.Td(
                                'Has your employer ever discussed mental health as part of an employee wellness '
                                'program?')]),
                            html.Tr([html.Td('Coworkers'), html.Td('Would you be willing to discuss a mental health '
                                                                   'issue with your coworkers?')]),
                            html.Tr([html.Td('Supervisors'), html.Td('Would you be willing to discuss a mental health '
                                                                     'issue with your direct supervisor(s)?')])
                        ], bordered=False, dark=False, responsive=True, striped=True, size='sm')
                    ],
                        md=12, align='center'),
                    html.Br(),
                    html.Iframe(id='iframe-company-support-2',
                                style={'border-width': '0', 'width': '100%', 'height': '40vh'})
                ], md=12, align='center')
            ), align='center')
        ])
    ]),
    className='mt-3')


def style_plot(plot):
    """
    Apply consistent styling for plots in the company support dashboard

    :param plot: The Altair plot object which should have styling applied
    :return: The Altair plot object with the styling applied
    """
    return plot.resolve_scale(color='independent') \
        .configure_axisX(labelAngle=360) \
        .configure_legend(titleFontSize=15, labelFontSize=13, gradientLength=100, gradientThickness=20) \
        .configure_title(fontSize=18, anchor='middle').configure_axis(labelFontSize=13, titleFontSize=13)


# Set up callbacks/backend
@app.callback(
    [
        Output('iframe-company-support-1', 'srcDoc'),
        Output('iframe-company-support-2', 'srcDoc')
    ],
    Input('company-support-state-dropdown', 'value'),
    Input('company-support-company-size-dropdown', 'value'),
    Input('company-support-tech-company-radioitems', 'value'),
    Input('company-support-remote-work-radioitems', 'value'))
def plot_general_overview(state, company_size, is_tech, is_remote_work):
    """
    Callback function to be responsible for refreshing the dashboard. This function will read in the latest parameters,
    apply appropriate filters and generate plots

    :param state: States in the US that should be included in the result
    :param company_size: Company size that should be included in the result
    :param is_tech: Are the companies traditional tech companies?
    :param is_remote_work: Are the companies allow remote work?
    :return: The rendered html of the dashboard
    """
    data = data_raw

    if len(state) != 0:
        data = data.query('state == @state')

    if len(company_size) != 0:
        data = data.query('no_employees == @company_size')

    if is_tech.lower() != 'all':
        data = data.query('tech_company == @is_tech')

    if is_remote_work.lower() != 'all':
        data = data.query('remote_work == @is_remote_work')

    # melt dataframe for questions plot
    df_melted = data[['benefits', 'wellness_program', 'seek_help', 'anonymity', 'mental_vs_physical']] \
        .melt(var_name='Question',
              value_name='Answer')

    # replace question names
    df_melted = df_melted.replace({'benefits': 'Benefits', 'anonymity': 'Anonymity',
                                   'seek_help': 'Resources', 'wellness_program': 'Wellness program',
                                   'mental_vs_physical': 'Mental vs physical'})

    # question plot
    plot_question = alt.Chart(df_melted, title='Survey Questions').mark_bar().encode(
        x=alt.X('count()', stack='normalize', axis=alt.Axis(format='%')),
        y=alt.Y('Question'),
        color=alt.Color('Answer', scale=alt.Scale(scheme='blues')),
        tooltip=[alt.Tooltip('count()', title='Respondent count')]
    ).properties(height=250, width=425)

    # boxplot
    plot_box = alt.Chart(data).mark_boxplot(size=50).encode(
        alt.X('mental_health_consequence', title=' '),
        alt.Y('Age'),
        alt.Color('Gender', scale=alt.Scale(scheme='tableau10'), legend=None)
    ).properties(
        height=300,
        width=275
    ).facet(facet='Gender',
            title='Do employees feel that there might be consequences discussing mental health conditions?')

    # heatmap plot
    plot_heat = alt.Chart(data, title=['Discussing with', 'Coworkers & Supervisors']).mark_rect().encode(
        x=alt.X('supervisor', title='Supervisors'),
        y=alt.Y('coworkers', sort='-y', title='Coworkers'),
        color=alt.Color('count()', legend=alt.Legend(title='Count'), scale=alt.Scale(scheme='greenblue')),
        tooltip=[alt.Tooltip('count()', title='Respondent count')]
    ).properties(height=250, width=220)

    return [style_plot(plot_box).to_html(), style_plot(plot_question | plot_heat).to_html()]
