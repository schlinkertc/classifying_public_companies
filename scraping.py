import requests
import json
import pandas as pd
from bs4 import BeautifulSoup
import edgar_datafied
import sec
from Humble_Chuck import mysql_helper1 as sql
from urllib.request import urlopen
from urllib.request import urlretrieve
from zipfile import ZipFile
import config
import os

#scrape financial data zip files
def scrape_zips():
    url = 'https://www.sec.gov/dera/data/financial-statement-data-sets.html'
    page = requests.get(url).content
    bs = BeautifulSoup(page)
    return ['https://www.sec.gov/{}'.format(x['href'])
            for x in bs.find('table').find_all('a')]

zip_urls = scrape_zips()

def download_zips(urls):
    zip_directory = '/Users/schlinkertc/Flatiron/projects/classification/zips'
    files_directory = '/Users/schlinkertc/Flatiron/projects/classification/txt_files/'
    for url in urls:
        period = url[-10:-4]
        zip_filename = zip_directory+'/'+period+'.zip'
        urlretrieve(url,filename=zip_filename)

        zip_file = ZipFile(
            '/Users/schlinkertc/Flatiron/projects/classification/zips/{}.zip'.format(period),
            mode='r',
            compression=0,
            allowZip64=True)

        zip_file.extractall('/Users/schlinkertc/Flatiron/projects/classification/txt_files/{}'.format(period))

download_zips(zip_urls)
