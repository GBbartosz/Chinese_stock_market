import os, sys
import yfinance as yf
import functions as f
import pandas as pd
import requests
import io
from incomestatement import IncomeStatement
import datetime


def download_price_df(yf_tic):
    print(yf_tic)
    #https://query1.finance.yahoo.com/v7/finance/download/{yf_tic}?period1=971913600&period2=1649548800&interval=1d&events=history&includeAdjustedClose=true
    success = False
    while success is False:
        try:
            url = 'https://query1.finance.yahoo.com/v7/finance/download/{0}?period1=971913600&period2=1649548800&interval=1d&events=history&includeAdjustedClose=true'.format(yf_tic)
            headers = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
            p_df = pd.DataFrame()
            resp = requests.get(url, headers=headers)
            p_df = pd.read_csv(io.StringIO(resp.text))
        except:
            print('download price')
        else:
            success = True
    return p_df


def download_and_save_prices():
    companys_sector_dic = f.create_companys_sector_dictionary()
    directory_path = 'C:\\Users\\Bartek\\Desktop\\ALK praca magisterska\\China_stock_data'
    all_files_list = os.listdir(directory_path)
    companys_dictionary = f.create_companys_dictionary(all_files_list)
    print(list(companys_dictionary.keys()))

    for company in companys_dictionary.keys():
        print(company)
        sector, yf_ticker = companys_sector_dic[company]
        price_df = download_price_df(yf_ticker)
        dest_path = 'C:\\Users\\Bartek\\Desktop\\ALK praca magisterska\\China_stock_data\\price\\{} price.csv'.format(company)
        price_df.to_csv(dest_path)


companys_sector_dic = f.create_companys_sector_dictionary()
directory_path = 'C:\\Users\\Bartek\\Desktop\\ALK praca magisterska\\China_stock_data'
all_files_list = os.listdir(directory_path)
companys_dictionary = f.create_companys_dictionary(all_files_list)
comp_dic = {}

for company in companys_dictionary.keys():
    print(company)
    sector, yf_ticker = companys_sector_dic[company]

    for doc in companys_dictionary[company]:
        file_name = '{0} - {1}.csv'.format(company, doc)
        file_path = os.path.join(directory_path, file_name)
        doc_df = pd.read_csv(file_path)
        doc_df = f.prepare_df(doc_df)

        if doc == 'Income Statement':
            incst_df = doc_df

    ticker = yf.Ticker(yf_ticker)
    tic = ticker.ticker
    try:
        yf_currency = ticker.info['financialCurrency']
    except:
        print('no ticker')
        continue
    df_f = ticker.quarterly_financials
    test_col = list(df_f.columns)[0]
    if not isinstance(test_col, datetime.datetime):
        print('no dates')
        continue
    df_f_dates = [str(x.date()) for x in list(df_f.columns)]
    if '2021-09-30' not in df_f_dates:
        print('lack of date')
        continue
    yf_net_income = float(df_f.loc['Net Income', '2021-09-30'])

    incst = IncomeStatement(incst_df)

    if yf_net_income == float(incst.NetIncometoStockholders.period(2021, 3)) * 1000000:
        l = [company, True, yf_currency, 1]
        comp_dic[tic] = l
    else:
        res = float(incst.NetIncometoStockholders.period(2021, 3)) * 1000000 / yf_net_income
        l = [company, False, yf_currency, res]
        comp_dic[tic] = l

comp_df = pd.DataFrame(comp_dic)

comp_df.to_csv('C:\\Users\\Bartek\\Desktop\\ALK praca magisterska\\res.csv')

