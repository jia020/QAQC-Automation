import chart_studio
import chart_studio.plotly as py
import chart_studio.tools as tls

import chart_studio.plotly as py
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import plotly.express as px 

username = 'Lingbo.Jiang'
api_key = 'lZ3BiOl21dpSn4tJcl62'
chart_studio.tools.set_credentials_file(username=username, api_key=api_key)
df=pd.read_csv('.\\out\\20210819_MRTalltest_aux9.csv')
#fig = go.Figure(go.line(x=df.DATE, y=df.SWIRALBEDOCAL, text=yd, mode='markers', name='2007'))
fig = px.line(df,x=df.DATE, y=[df.SWIRALBEDOCAL,df.TIRALBEDOCAL,df.EXTTEMPERATURE,df.CAMTEMPERATURE,df.SWIRTEMPERATURE,df.AMBTEMPERATURE])
fig.update_xaxes(title_text='QAQC Date')
fig.update_yaxes(title_text='QAQC Measurement')
plotly = py.plot(fig, filename='QAQC')
print(plotly)
