from datetime import datetime
import requests
import urllib.request
import zipfile
from io import BytesIO
import os
from pathlib import Path
import pandas as pd
import io
import requests
   
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

fo = open(f'prisma-proc-cellout.txt', 'a')
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
dfDone = pd.read_csv(f'.\\PRISMA-Data-Done.csv')
doneUrls = dfDone['url'].tolist()
dual_print(fo,f'>>nvcl-prisma: open prisma-data-done:{len(dfDone)}')

mydir = 'Z:\\source\\PRISMA\\L2D'
count = 0
dual_print(fo,f'>>nvcl-prisma: mydir:{mydir}')

for index , row in df.iterrows():
    url = row.url
    filename = Path(url).stem + '.he5'
    if  os.path.exists(f'{mydir}\\{filename}'):
        dual_print(fo,f'skip an existing file  {url}')
        continue
    dual_print(fo, f'>get data from URL:{index} {url} {datetime.now().strftime(timeFormat)}')
    if (url not in doneUrls):
        unzipFile(url,mydir)
        count +=1    
        dual_print(fo,f'download&unzip 1 file {count} {url} to {mydir}\\{filename} at {datetime.now().strftime(timeFormat)}')
    else:
        dual_print(fo,f'skip a file  {url}')
        continue
    dfDone.loc[len(dfDone)] = [row.date,row.url,datetime.now().strftime(timeFormat)]
    dfDone.to_csv(f'.\\PRISMA-Data-Done.csv',index=False)
dfDone.to_csv(f'.\\PRISMA-Data-Done.csv',index=False)
dual_print(fo,f'>>nvcl-prisma:finished and total count { count } {datetime.now().strftime(timeFormat)}!')
