import matplotlib.pyplot as plt
import pandas as pd

import yfinance as yf
import functions as f


companys_sector_dic = f.create_companys_sector_dictionary()
companys_yticker_dic = f.create_companys_yahoo_ticker_dictionary()
fin_data_dic = {}
for company in companys_sector_dic.keys():
    ticker = companys_yticker_dic[company]
    ticker = yf.Ticker(ticker)
    print(ticker)
    df = ticker.history(period='max')
    first_date = df.index[0]
    sector = companys_sector_dic[company]
    if sector in fin_data_dic:
        fin_data_dic[sector].append(first_date)
    else:
        fin_data_dic[sector] = [first_date]

sector_with_largest_number_of_cases = max(fin_data_dic, key=lambda x: len(fin_data_dic[x]))
max_number_of_cases = len(fin_data_dic[sector_with_largest_number_of_cases])
for sector in fin_data_dic:
    while len(fin_data_dic[sector]) != max_number_of_cases:
        fin_data_dic[sector].append(None)

x_arr = fin_data_dic.keys()

df = pd.DataFrame(fin_data_dic)
df.to_excel('C:\\Users\\Bartek\\Desktop\\ALK praca magisterska\\report.xlsx')