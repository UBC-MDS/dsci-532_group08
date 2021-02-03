import altair as alt
import pandas as pd
from vega_datasets import data

us_state_abbrev = {
    'Alabama': 'AL',
    'Alaska': 'AK',
    'American Samoa': 'AS',
    'Arizona': 'AZ',
    'Arkansas': 'AR',
    'California': 'CA',
    'Colorado': 'CO',
    'Connecticut': 'CT',
    'Delaware': 'DE',
    'District of Columbia': 'DC',
    'Florida': 'FL',
    'Georgia': 'GA',
    'Guam': 'GU',
    'Hawaii': 'HI',
    'Idaho': 'ID',
    'Illinois': 'IL',
    'Indiana': 'IN',
    'Iowa': 'IA',
    'Kansas': 'KS',
    'Kentucky': 'KY',
    'Louisiana': 'LA',
    'Maine': 'ME',
    'Maryland': 'MD',
    'Massachusetts': 'MA',
    'Michigan': 'MI',
    'Minnesota': 'MN',
    'Mississippi': 'MS',
    'Missouri': 'MO',
    'Montana': 'MT',
    'Nebraska': 'NE',
    'Nevada': 'NV',
    'New Hampshire': 'NH',
    'New Jersey': 'NJ',
    'New Mexico': 'NM',
    'New York': 'NY',
    'North Carolina': 'NC',
    'North Dakota': 'ND',
    'Northern Mariana Islands': 'MP',
    'Ohio': 'OH',
    'Oklahoma': 'OK',
    'Oregon': 'OR',
    'Pennsylvania': 'PA',
    'Puerto Rico': 'PR',
    'Rhode Island': 'RI',
    'South Carolina': 'SC',
    'South Dakota': 'SD',
    'Tennessee': 'TN',
    'Texas': 'TX',
    'Utah': 'UT',
    'Vermont': 'VT',
    'Virgin Islands': 'VI',
    'Virginia': 'VA',
    'Washington': 'WA',
    'West Virginia': 'WV',
    'Wisconsin': 'WI',
    'Wyoming': 'WY'
}

capitals = pd.read_json(data.us_state_capitals.url)
capitals['state'] = capitals['state'].map(us_state_abbrev)
capitals = capitals[['state', 'lon', 'lat']]

states = alt.topo_feature(data.us_10m.url, 'states')


def plot_map(df):
    background = alt.Chart(states).mark_geoshape(
        fill='lightgray',
        stroke='white'
    ).properties(
        title='Respondent distribution',
        width=850,
        height=400
    ).project('albersUsa')

    df_geo = df.merge(capitals, on='state')
    base = alt.Chart(df_geo).encode(
        longitude='lon:Q',
        latitude='lat:Q',
    )

    points = base.mark_circle(fill='#E45756').encode(
        size=alt.Size('count()', scale=alt.Scale(domain=[0, 150], range=[50, 800]), title='Respondent count'),
        tooltip=[
            alt.Tooltip('state', title='State'),
            alt.Tooltip('count()', title='Respondent count')
        ]
    )

    return background + points
