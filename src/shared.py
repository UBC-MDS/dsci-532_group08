import dash
import dash_bootstrap_components as dbc
import pandas as pd

app = dash.Dash('dashboard_app',
                title='Mental Health in Tech Dashboard',
                external_stylesheets=[dbc.themes.BOOTSTRAP])

data_raw = pd.read_csv('data/processed.csv')
