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
df["trip_duration"] = df.dropoff_datetime -  df.pickup_datetime
df["trip_duration"] = df["trip_duration"].dt.total_seconds()
df_agg_cmt = df[df["vendor_id"] == "CMT"].groupby('pickup_weekday_name')['trip_duration'].aggregate(np.sum).reset_index()
df_agg_vts = df[df["vendor_id"] == "VTS"].groupby('pickup_weekday_name')['trip_duration'].aggregate(np.sum).reset_index()
app.layout = html.Div(children=[
    html.H1(children='Hello Dash'),

    html.Div(children='''
        Dash: A web application framework for Python.
    '''),

    dcc.Graph(
        id='example-graph',
        figure={
            'data': [
                {'x': df_agg_cmt['pickup_weekday_name'].tolist(), 'y': df_agg_cmt['trip_duration'].tolist(), 'type': 'bar', 'name': 'CMT'},
                {'x': df_agg_vts['pickup_weekday_name'].tolist(), 'y': df_agg_vts['trip_duration'].tolist(),'type': 'bar', 'name': 'VTS'},
            ],
            'layout': {
                'title': 'Distrubution of trip duration group by day in week for 2 verdor'
            }
        }
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)