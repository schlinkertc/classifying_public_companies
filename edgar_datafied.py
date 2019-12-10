import config
APPKEY = config.edgar_apiKey
import requests
import json

# datafied.api.edgar-online.com/{Version}/{Endpoints}{Format}?{Parameters}appkey={API Key}

def corefinancials(primary_symbol):
    request = requests.get(f"""https://datafied.api.edgar-online.com/v2/corefinancials/ann?primarysymbols={primary_symbol}&numperiods=1&appkey={APPKEY}""")
    return request.json()
