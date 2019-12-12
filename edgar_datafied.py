import config
APPKEY = config.edgar_apiKey
import requests
import json

# datafied.api.edgar-online.com/{Version}/{Endpoints}{Format}?{Parameters}appkey={API Key}

def get_symbol(companyname):
    request = requests.get(f'https://datafied.api.edgar-online.com/v2/companies?companynames={companyname}&appkey={config.edgar_apiKey}')
    response = request.json()
    symbol = ({x['field']:x['value']
               for x in response
               ['result']['rows'][0]['values']}
              ['primarysymbol'])
    return symbol

def corefinancials(primary_symbol):
    request = requests.get(f"""https://datafied.api.edgar-online.com/v2/corefinancials/ann?primarysymbols={primary_symbol}&numperiods=1&appkey={config.edgar_apiKey}""")
    return request.json()

def get_coreFinancials(company_names):
    dfs = []
    for name in company_names:
        try:
            contents = corefinancials(get_symbol(name))
            financials = {x['field']:x['value'] for x in contents['result']['rows'][0]['values']}
            temp_df = pd.DataFrame(financials,index=[financials['cik']])
            dfs.append(temp_df)
        except:
            continue
    return pd.concat(dfs,sort=True)
