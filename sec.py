import requests
import json
import pandas as pd
from bs4 import BeautifulSoup

#DCN is the numerical id for financial statements
#function takes in company cik, returns list of DCNs
def get_dcn_list(cik):
    url = 'https://www.sec.gov/Archives/edgar/data/{}/'.format(cik)
    page = BeautifulSoup(requests.get(url).content)
    a = page.find_all('a')
    text = [x.get_text() for x in a]
    dcn_list = [x for x in text[1:] if x[0]=='0']

    return dcn_list


# takes in cik and dcn, returns income statement
# requires that the dcn number represents a 10Q or 10K
# also requires that the income statement link is formated as 'R4'
def get_incomeStatement(cik,dcn):
    url = 'https://www.sec.gov/Archives/edgar/data/{}/{}/R4.htm'.format(cik,dcn)
    page = BeautifulSoup(requests.get(url).content)
    rows = page.find_all(attrs={'class':['ro','re','reu','rou']})

    return [x.get_text(strip=True,separator=';').split(';') for x in rows]

# trying a different approach:
# get the headers for all filings related to a company cik
# then we can parse the files based on type
# this works but it takes forever, and it gets mostly files we don't care about
def get_fileHeaders(cik):
    dcn_list = get_dcn_list(cik)
    filings = []
    print(len(dcn_list))
    for dcn in dcn_list:
        try:
            url = 'https://www.sec.gov/Archives/edgar/data/{}/{}'.format(cik,dcn)

            page = BeautifulSoup(requests.get(url).content)

            page_text = [x.get_text() for x in page.find_all('a')]

            headers_file = [x for x in page_text if 'index-headers' in x][0]

            headers_url = 'https://www.sec.gov/Archives/edgar/data/{}/{}/{}'.format(cik,dcn_list[0],headers_file)

            headers_html =  BeautifulSoup(requests.get(headers_url).content)

            headers_text = headers_html.get_text(strip=True,separator=';').split(';')[1].split('\t')
            headers_text = [x for x in headers_text if x!='']
            headers_text = [x for x in headers_text if x!='\n']

            index = {x.strip(':'):headers_text[i+1].strip('\n') for i, x in enumerate(headers_text) if 'FORM TYPE' in x}
            index['CIK']=cik
            index['DCN']=dcn
            filings.append(index)
        except:
            continue
        finally:
            pass
    return filings

# the above functions use the sec archives. this the url for the 'viewer'
# 'https://www.sec.gov/cgi-bin/viewer?action=view&cik=789019&accession_number=0001564590-19-027952&xbrl_type=v#'

#scrape financial data zip files
def scrape_zips():
    url = 'https://www.sec.gov/dera/data/financial-statement-data-sets.html'
    page = requests.get(url).content
    bs = BeautifulSoup(page)
    return ['https://www.sec.gov/{}'.format(x['href'])
            for x in bs.find('table').find_all('a')]
