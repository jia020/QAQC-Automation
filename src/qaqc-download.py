import subprocess
import requests
import urllib.request
import zipfile
from io import BytesIO
import shutil
import os
from pathlib import Path
import glob
def clean_directory(mydir):
    if (os.path.exists(mydir)):
        shutil.rmtree(mydir)

def move_files(src_dir,dest_dir):
    if not os.path.exists(dest_dir):
        os.mkdir(dest_dir)
    pathlist = Path(src_dir).glob('**/*.*')
    for path in pathlist:
        path_in_str = str(path)
        txt = ''.join(path_in_str.split())
        fn = txt.split("\\")
        fn.pop(0)
        fn = '-'.join(map(str, fn))
        fpath = dest_dir + fn
        print(">>move file:" + fpath)
        shutil.move(path_in_str, fpath)

def clean_directory2(mydir):
    filelist = [ f for f in os.listdir(mydir) ]
    for f in filelist:
        os.remove(os.path.join(mydir, f))

def unzipFile(url,save_path):
    if not os.path.exists(save_path):
        os.mkdir(save_path)
    z = zipfile.ZipFile(BytesIO(urllib.request.urlopen(url).read()))
    z.extractall(save_path)

def download_url(url, save_path, chunk_size=1024*64):
    r = requests.get(url, stream=True)
    with open(save_path, 'wb') as fd:
        for chunk in r.iter_content(chunk_size=chunk_size):
            fd.write(chunk)

mydir = '.\\working'
clean_directory(mydir)
print('>>nvcl-qaqc:clean_directory:'+ mydir)
mydir = '.\\working2'
clean_directory(mydir)
print('>>nvcl-qaqc:clean_directory:'+ mydir)

data_url_file = open('data_url_file.txt', 'r')
urlLines = data_url_file.readlines() 
mydir = '.\working2'
count = 0
for url in urlLines:
    if url[0] == '#':
        continue
    count += 1
    print(">>get data from URL:{}: {}".format(count, url.strip()))
    unzipFile(url,mydir)
    print('>>nvcl-qaqc:download&unzipTo:'+ mydir)
mydir = '.\\working2'

move_files(mydir, '.\\working\\')
print('>>nvcl-qaqc:moved data to :'+ mydir)
print('>>nvcl-qaqc:finished!')
