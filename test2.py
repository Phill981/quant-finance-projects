from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium import webdriver
import tkinter as tk
import time
import requests
import pandas as pd
import re
import yfinance as yf

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'
}


def get_id(symbol: str):
    query = re.sub(r'[^a-zA-Z0-9 ]', '', yf.Ticker(symbol).info['longName'])
    resp = requests.get(
        f'https://www.ls-tc.de/_rpc/json/.lstc/instrument/search/main?q={query}&localeId=2', headers=headers)
    assert resp.status_code == 200, resp.status_code
    return resp.json()[0]['id']


def get_history(symbol: str, type: str):
    id = get_id(symbol)
    url = f'https://www.ls-tc.de/_rpc/json/instrument/chart/dataForInstrument?instrumentId={id}&marketId=1&quotetype={type}&series=history&localeId=2'
    resp = requests.get(url, headers=headers)
    assert resp.status_code == 200, resp.status_code

    return resp.json()["series"]["history"]["data"][-1]


# df = pd.DataFrame(resp.json()['series']['history']
#                  ['data'], columns=['Date', 'Price'])
# df.Date *= 1000000
# df.Date = pd.to_datetime(df.Date)
# df.set_index('Date', inplace=True)
# return df


while True:
    print(f"ASK: {get_history('TSLA', 'ask')}")
    print(f"BID: {get_history('TSLA', 'bid')}")
    print(f"MID: {get_history('TSLA', 'mid')}")
    time.sleep(0.1)
