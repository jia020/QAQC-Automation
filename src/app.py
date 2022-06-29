import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc 
import dash_html_components as html

from pandas_datareader import data as web 
from datetime import datetime as dt
import pandas as pd

app = dash.Dash('Hello World')
df = pd.read_csv('.\\out\\20210819_MRTalltest_aux9.csv')

app.layout = html.Div([
    dcc.Dropdown(
        id='my-dropdown',
        options=[
            {'label': 'SWIRALBEDOCAL', 'value': 'SWIRALBEDOCAL'},
            {'label': 'TIRALBEDOCAL', 'value': 'TIRALBEDOCAL'},
            {'label': 'EXTTEMPERATURE', 'value': 'EXTTEMPERATURE'}
        ],  
        value='SWIRALBEDOCAL'
    ),  
    dcc.Graph(id='my-graph')
], style={'width': '1000'})

@app.callback(Output('my-graph', 'figure'), [Input('my-dropdown', 'value')])
def update_graph(selected_dropdown_value):
  
    return {
        'data': [{
            'x': df.DATE,
            'y': df[selected_dropdown_value]
        }], 
        'layout': {'margin': {'l': 40, 'r': 0, 't': 20, 'b': 30}}
    }   

if __name__ == '__main__':
    app.run_server()