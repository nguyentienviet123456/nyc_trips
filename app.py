import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import numpy as np
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

filename = 'nyc_taxi_data_2014.csv'
df = pd.read_csv(filename, dtype={"store_and_fwd_flag": object})
#String to Datetime conversion
df["pickup_datetime"]= pd.to_datetime(df["pickup_datetime"])
df["dropoff_datetime"]= pd.to_datetime(df["dropoff_datetime"])
df["pickup_dayofweek"] = df.pickup_datetime.dt.dayofweek
df["pickup_weekday_name"] = df.pickup_datetime.dt.weekday_name
df["pickup_hour"] = df.pickup_datetime.dt.hour
df["pickup_month"] = df.pickup_datetime.dt.month
df["trip_duration"] = df.dropoff_datetime -  df.pickup_datetime
df["trip_duration"] = df["trip_duration"].dt.total_seconds()
df_agg = df.groupby('pickup_weekday_name')['trip_duration'].aggregate(np.sum).reset_index()
list_day = df_agg['pickup_weekday_name'].tolist()
trip_duration = df_agg['trip_duration'].tolist()
app.layout = html.Div(children=[
    html.H1(children='Hello Dash'),

    html.Div(children='''
        Dash: A web application framework for Python.
    '''),

    dcc.Graph(
        id='example-graph',
        figure={
            'data': [
                {'x': list_day, 'y': trip_duration, 'type': 'bar', 'name': 'DEMO'},
            ],
            'layout': {
                'title': 'Dash Data Visualization'
            }
        }
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)