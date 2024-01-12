from datetime import datetime
import speedtest
import plotly.express as px
import plotly.graph_objects as go
import dash
from dash.dependencies import Output, Input
import dash_core_components as dcc
import dash_html_components as html
import plotly
import random
import plotly.graph_objs as go
from collections import deque
import time

st = speedtest.Speedtest()
st.get_best_server()


def minutesToMilliseconds(minutes):
    return minutes * 60000


intervalTimeDelay = minutesToMilliseconds(30) #How long before we take a new bandwidth test
smaWindow = 1 #How "smoothed out" the graph will be (a higher number means more smoothed out).

downloads = []
uploads = []
DownloadsSMA = [] #The Simple Moving Average of the Download's

timeStamps = [] #This is where i put the Time stamps for all of the test's
  
#Initiating The Dash Server
app = dash.Dash(__name__)
  
app.layout = html.Div(
    [
        dcc.Graph(id = 'live-graph', animate = True),
        dcc.Interval(
            id = 'graph-update',
            interval = intervalTimeDelay,
            n_intervals = 0 #The means an infinant amount of intervals I.E the script will run forever.
        ),
    ]
)

#Setting up a Callback Function to update the website's graph live
@app.callback(
    Output('live-graph', 'figure'),
    [ Input('graph-update', 'n_intervals') ]
)

def update_graph_scatter(n):
    download = bytes_to_mb(st.download())
    downloads.append(download)
    timeStamps.append(datetime.now())
    DownloadsSMA = SMA(downloads, smaWindow)
    
    
  
    data = plotly.graph_objs.Scatter(
            x=list(timeStamps),
            y=list(DownloadsSMA),
            name='Scatter',
            mode= 'lines+markers'
    )
    if len(DownloadsSMA) == 0:
        return {'data': [data],
            'layout' : go.Layout(xaxis=dict(range=[0,100]),yaxis = dict(range = [0,100]),)}
    return {'data': [data],
            'layout' : go.Layout(xaxis=dict(range=[min(timeStamps),max(timeStamps)]),yaxis = dict(range = [min(DownloadsSMA)-10,max(DownloadsSMA)+50]),)}

def bytes_to_mb(bytes):
  KB = 1024
  MB = KB * 1024
  return int(bytes/MB)



def SMA(arr, window_size):
    #Simple Moving Average (SMA)
    i = 0
    moving_averages = []
  
    while i < len(arr) - window_size + 1:
        window = arr[i : i + window_size]
        window_average = round(sum(window) / window_size, 2)
        moving_averages.append(window_average)
        i += 1
    return moving_averages
  
if __name__ == '__main__':
    app.run_server()
    #This is setting up Plotly so it can update the data in the chart live. That's what the "FigureWidget" dose.
    fig = go.FigureWidget()
    fig.add_scatter()


    st = speedtest.Speedtest()
    st.get_best_server()

    DownloadsSMA = []
    while True:
        download = bytes_to_mb(st.download())
        upload = bytes_to_mb(st.upload())

        downloads.append(download)
        uploads.append(upload)

        timeStamps.append(datetime.now())
        timeStamps = timeStamps[0:len(DownloadsSMA)]
