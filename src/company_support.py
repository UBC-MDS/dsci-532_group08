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

    #melt dataframe for questions plot
    df_melted = data[['benefits', 'wellness_program', 'seek_help', 'anonymity', 'mental_vs_physical']] \
        .melt(var_name="Question",
            value_name="Answer")
            
    #replace question names       
    df_melted = df_melted.replace({'benefits': 'Benefits', 'anonymity': 'Anonymity', 
                                'seek_help': 'Resources', 'wellness_program': 'Wellness program', 
                                'mental_vs_physical': 'Mental vs physical'})

    #question plot
    plot_question = alt.Chart(df_melted, title = "Survey Questions").mark_bar().encode(
                    x=alt.X('count()', stack="normalize", axis=alt.Axis(format='%')),
                    y=alt.Y('Question'),
                    color=alt.Color('Answer', scale=alt.Scale(scheme='blues')),
                    tooltip=[alt.Tooltip('count()', title='Respondent count')]
                ).properties(height=200, width = 425)

    #boxplot
    plot_box = alt.Chart(data).mark_boxplot(size = 50).encode(
                     alt.X("mental_health_consequence", title= " "),
                     alt.Y("Age"),
                     alt.Color("Gender", scale=alt.Scale(scheme='tableau10'), legend=None)
                ).properties(
                     height=300,
                     width =275
                 ).facet(facet= "Gender", title = "Do employees feel that there might be consequences discussing mental health conditions?")

    #heatmap plot
    plot_heat = alt.Chart(data, title=['Discussing with','Coworkers & Supervisors']).mark_rect().encode(
                    x='supervisor',
                    y=alt.Y('coworkers', sort='-y'),
                    color=alt.Color('count()', legend=alt.Legend(title="Count"), scale=alt.Scale(scheme='greenblue')),
                    tooltip=[alt.Tooltip('count()', title='Respondent count')]
                ).properties(height=200, width= 220)


            
    return (plot_box & (plot_question|plot_heat)
        ).resolve_scale(color ='independent'
        ).configure_axisX(labelAngle=360
        ).configure_legend(titleFontSize=15,labelFontSize=13, gradientLength=100, gradientThickness=20
        ).configure_title(fontSize=18, anchor='middle'
        ).configure_axis(labelFontSize=13,titleFontSize=13
        ).to_html()
