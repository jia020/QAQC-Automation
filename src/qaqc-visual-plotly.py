import chart_studio
import chart_studio.plotly as py
import chart_studio.tools as tls

import chart_studio.plotly as py
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import plotly.express as px 
from plotly.subplots import make_subplots

username = 'cg-admin'
api_key = 'UST1BFDdnBOekJjZ9v4e'
chart_studio.tools.set_credentials_file(username=username, api_key=api_key)#
df=pd.read_csv('./out/20210819_MRTalltest_aux9.csv')
#Quartz_8625_mean
df2=pd.read_csv('./out/20210818_2Bstd_testrocks_wvl_q86256.csv')
df_q86256=df2[df2.Quartz_8625_mean>0]
#PUKWCAL 
df3=pd.read_csv('./out/20210908_2Bstd_tircalrep_GSWA.csv')
#TALC 
df4=pd.read_csv('./out/20210908_2Bstd_testrocks_wvl_GSWA.csv')
df_testrocks_wvl_gswa_950=df4[["Scan_Date","Talc_ 950.0"]][df4["Talc_ 950.0"]>0]
df_testrocks_wvl_gswa_2467=df4[["Scan_Date","Talc_2467.0"]][df4["Talc_2467.0"]>0]
df_testrocks_wvl_gswa_2230=df4[["Scan_Date","Talc_2230.0"]][df4["Talc_2230.0"]>0]


fig = make_subplots(rows=5, cols=1)

fig.add_trace(go.Scatter(x=df.DATE, y=df.SWIRALBEDOCAL,name ="SWIRALBEDOCAL", mode="lines", legendgroup = '1'), row=1, col=1)
fig.add_trace(go.Scatter(x=df.DATE, y=df.TIRALBEDOCAL,name ="TIRALBEDOCAL", mode="lines", legendgroup = '1'), row=1, col=1)
fig.add_trace(go.Scatter(x=df.DATE, y=df.VISALBEDOCAL/1000000,name ="VISALBEDOCAL", mode="lines", legendgroup = '1'), row=1, col=1)

fig.add_trace(go.Scatter(x=df.DATE, y=df.SWIRTEMPERATURE,name ="SWIRTEMPERATURE", mode="lines", legendgroup = '2'), row=2, col=1)
fig.add_trace(go.Scatter(x=df.DATE, y=df.CAMTEMPERATURE,name ="CAMTEMPERATURE", mode="lines", legendgroup = '2'), row=2, col=1)
fig.add_trace(go.Scatter(x=df.DATE, y=df.AMBTEMPERATURE,name ="AMBTEMPERATURE", mode="lines", legendgroup = '2'), row=2, col=1)

fig.add_trace(go.Scatter(x=df_q86256.Scan_Date, y=df_q86256.Quartz_8625_mean,name ="Quartz_8625_mean", mode="markers",legendgroup = '3'), row=3, col=1)

fig.add_trace(go.Scatter(x=df3.Scan_Date, y=df3["6245_mean"],name ="6245_mean", mode="markers",legendgroup = '3'), row=4, col=1)

fig.add_trace(go.Scatter(x=df_testrocks_wvl_gswa_950.Scan_Date, y=df_testrocks_wvl_gswa_950["Talc_ 950.0"],name ="Talc_950.0", mode="markers",legendgroup = '3'), row=5, col=1)
fig.add_trace(go.Scatter(x=df_testrocks_wvl_gswa_2230.Scan_Date, y=df_testrocks_wvl_gswa_2230["Talc_2230.0"],name ="Talc_2230.0", mode="markers",legendgroup = '3'), row=5, col=1)
fig.add_trace(go.Scatter(x=df_testrocks_wvl_gswa_2467.Scan_Date, y=df_testrocks_wvl_gswa_2467["Talc_2467.0"],name ="Talc_2467.0", mode="markers",legendgroup = '3'), row=5, col=1)

fig.update_layout(
    height=3600, 
    width=1800, 
    title_text="QAQC Measurements", 
    #xaxis_title = 'Date',
    yaxis1_title = 'ALBEDOCAL',
    yaxis2_title = 'TEMPERATURE',
    yaxis3_title = 'Quartz_8625_mean',
    yaxis4_title = 'PUKWCAL',
    yaxis5_title = 'Talc_',
    legend_tracegroupgap = 50,
    #yaxis1_range=[0, 0.2],
    #yaxis2_range=[0, 30]
    #yaxis3_range=[8600, 8800]    
)
pyUrl = py.plot(fig,filename='QAQC')
print(pyUrl)
