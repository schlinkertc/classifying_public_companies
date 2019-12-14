import config
APPKEY = config.edgar_apiKey
import requests
import json

# datafied.api.edgar-online.com/{Version}/{Endpoints}{Format}?{Parameters}appkey={API Key}

def corefinancials(primary_symbol):
    request = requests.get(f"""https://datafied.api.edgar-online.com/v2/corefinancials/ann?primarysymbols={primary_symbol}&numperiods=1&appkey={APPKEY}""")
    return request.json()

def get_coreFinancials(symbols):
    dfs = []
    for symbol in symbols:
        try:
            contents = edgar_datafied.corefinancials(symbol)
            financials = {x['field']:x['value'] for x in contents['result']['rows'][0]['values']}
            temp_df = pd.DataFrame(financials,index=[symbol])
            dfs.append(temp_df)
        except:
            continue
    return pd.concat(dfs,sort=True)

    
