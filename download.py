import pandas as pd
import requests
import functions as f
import os
import yfinance as yf
import datetime as dt

pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)


yf_tickers = ['0386.HK', '9988.HK']


for yf_ticker in yf_tickers:
    url = f'https://query1.finance.yahoo.com/v7/finance/download/{yf_ticker}?period1=971913600&period2=1649548800&interval=1d&events=history&includeAdjustedClose=true'
    df = pd.read_csv(url)
    print(df)

baba = yf.Ticker('9988.HK')
print(baba.calendar)
print(baba.history(period='max'))
