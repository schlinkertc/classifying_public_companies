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
import sqlalchemy

_sql_alchemy_connection = (
                                f'mysql+mysqlconnector://'
                                f'{config.admin}:{config.password}'
                                f'@{config.host}:{config.port}'
                                f'/{config.schema}'
                           )
db = sqlalchemy.create_engine(_sql_alchemy_connection,
                              echo = False,
                              connect_args = {'ssl_disabled' : True})

directories = [x[0] for x in os.walk('/Users/schlinkertc/Flatiron/projects/classification/txt_files')][1:]
file_names = [x[2] for x in os.walk(directories[0])][0]

tag_paths = sorted([x+'/'+file_names[0] for x in directories],reverse=True)
pre_paths = sorted([x+'/'+file_names[1] for x in directories],reverse=True)
sub_paths = sorted([x+'/'+file_names[2] for x in directories],reverse=True)
num_paths = sorted([x+'/'+file_names[4] for x in directories],reverse=True)

tag_paths[:7]==su

#Dataframes for results from 2018-2019

tags = pd.concat([pd.read_csv(x,sep='\t',
             lineterminator='\n',
             header=0,encoding='unicode_escape') for x in tag_paths[:7]
          ],axis=0
         )

presentations = pd.concat([pd.read_csv(x,sep='\t',
             lineterminator='\n',
             header=0,encoding='utf-8') for x in pre_paths[:7]
          ],axis=0
         )

numbers = pd.concat([pd.read_csv(x,sep='\t',
             lineterminator='\n',
             header=0,encoding='unicode_escape') for x in num_paths[:7]
          ],axis=0
         )

submissions = pd.concat([pd.read_csv(x,sep='\t',
             lineterminator='\n',
             header=0,encoding='utf-8') for x in sub_paths[:7]
          ],axis=0
         )

submissions.to_sql('submissions',db,if_exists='replace',chunksize=20000,index=False)

presentations.to_sql('presentations',db,if_exists='replace',chunksize=20000,index=False)

tags.to_sql('tags',db,if_exists='replace',chunksize=20000,index=False)

numbers.to_sql('numbers',db,if_exists='replace',chunksize=20000,index=False)
