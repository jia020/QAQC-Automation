from datetime import datetime
import subprocess
import requests
import urllib.request
import zipfile
from io import BytesIO
import shutil
import os
from pathlib import Path
import glob

import pandas as pd
import io
import requests

from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from datetime import datetime

def sendemail(toaddress,key,emailContent):
    # datetime object containing current date and time
    now = datetime.now()
    # dd/mm/YY H:M:S
    datetimeOfReport = now.strftime("%d-%m-%Y %H:%M:%S")    
    message = Mail(
        from_email='help@tsg.csiro.au',
        to_emails=toaddress,
        subject=f'Prisma-auto-result-{datetimeOfReport}',
        html_content=emailContent
    )
    sg = SendGridAPIClient(key)
    try:
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers) 
    except Exception as e:
        print(e)

def unzipFile(url,save_path):
    if not os.path.exists(save_path):
        os.mkdir(save_path)
    z = zipfile.ZipFile(BytesIO(urllib.request.urlopen(url).read()), allowZip64=True)
    z.extractall(save_path)

def download_url(url, save_path, chunk_size=1024*64):
    r = requests.get(url, stream=True)
    with open(save_path, 'wb') as fd:
        for chunk in r.iter_content(chunk_size=chunk_size):
            fd.write(chunk)



#prismaDir=r'Z:/source/PRISMA/L2D/'
#workDir=r'Z:/source/PRISMA/'
prismaDir=r'\\fs1-per.nexus.csiro.au\{mr-p1-hypersat}/source/PRISMA/L2D/'
workDir=r'c:/Users/jia020/Desktop/'
fo = open(f'{workDir}prisma-proc-cellout.txt', 'a')
def dual_print(f, *args, **kwargs):
  print(*args, **kwargs)
  print(*args, **kwargs, file=f)
  fo.flush()

timeFormat = "%Y-%m-%d %H:%M:%S"
dual_print(fo,f'>>nvcl-prisma: start at:{datetime.now().strftime(timeFormat)}')
prismaUrl = "https://tsgfuncstorage.z8.web.core.windows.net/PRISMAResults/PRISMA-Data.csv"
s = requests.get(prismaUrl).content
df = pd.read_csv(io.StringIO(s.decode('utf-8')))
dual_print(fo,f'>>nvcl-prisma: open prismaUrl:{len(df)}')
dfDone = pd.read_csv(f'{workDir}PRISMA-Data-Done.csv')
dfDone.drop_duplicates(subset="url",keep=False,inplace=True)
dfDone.to_csv(f'{workDir}PRISMA-Data-Done.csv',index=False)
doneUrls = dfDone['url'].tolist()
dual_print(fo,f'>>nvcl-prisma: open prisma-data-done:{len(dfDone)}')


count = 0
dual_print(fo,f'>>nvcl-prisma: workDir :{workDir}')

for index , row in df.iterrows():
    url = row.url
    filename = Path(url).stem + '.he5'

    if (url in doneUrls):
        #dual_print(fo,f'skip a done file  {url}')
        continue
    if  os.path.exists(f'{prismaDir}{filename}'):
        dual_print(fo,f'skip an existing file  {url}')
        dfDone.loc[len(dfDone)] = [row.date,row.url,datetime.now().strftime(timeFormat)]
        continue
    dual_print(fo, f'>get data from URL:{index} {url} {datetime.now().strftime(timeFormat)}')
    unzipFile(url,prismaDir)
    count +=1    
    dfDone.loc[len(dfDone)] = [row.date,row.url,datetime.now().strftime(timeFormat)]
    dual_print(fo,f'download&unzip file {count} to {prismaDir}{filename} at {datetime.now().strftime(timeFormat)}') 
    dfDone.to_csv(f'{workDir}PRISMA-Data-Done.csv',index=False)
dfDone.to_csv(f'{workDir}PRISMA-Data-Done.csv',index=False)
dual_print(fo,f'>>nvcl-prisma:finished and total count { count } {datetime.now().strftime(timeFormat)}!')
csvHtml = '<a href=\"https://tsgfuncstorage.z8.web.core.windows.net/PRISMAResults/index.html\">https://tsgfuncstorage.z8.web.core.windows.net/PRISMAResults/PRISMA-Data.csv</a>'
emailContent = f'>>nvcl-prisma:finished and total count { count } {datetime.now().strftime(timeFormat)}! \\n {csvHtml}'
sendemail('Lingbo.Jiang@csiro.au','sendgridkeyinstead',emailContent)

