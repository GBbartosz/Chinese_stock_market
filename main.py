import datetime
import matplotlib.pyplot as plt
import os
import pandas as pd
import time
from incomestatement import IncomeStatement
from balance import Balance
from cashflow import CashFlow
import yfinance as yf

import functions as f


def dataframe_display_options():
    pd.set_option('display.max_rows', 500)
    pd.set_option('display.max_columns', 500)
    pd.set_option('display.width', 1000)


def find_nearest_price_date(f_d_d, price_dates_list):
    if f_d_d in price_dates_list:
        f_p_d = f_d_d
    else:
        d = 0
        while f_d_d > price_dates_list[d]:
            d += 1
        f_p_d = price_dates_list[d]
    return f_p_d


def find_first_date():

    def get_doc_first_date(n):
        incst_first_date = datetime.datetime.strptime(incst_df.columns[n], '%Y-%m-%d').date()
        b_first_date = datetime.datetime.strptime(b_df.columns[n], '%Y-%m-%d').date()
        cf_first_date = datetime.datetime.strptime(cf_df.columns[n], '%Y-%m-%d').date()
        f_d_d = max(incst_first_date, b_first_date, cf_first_date)
        return f_d_d

    f_doc_date = get_doc_first_date(1)
    price_dates_list = list(datetime.datetime.strptime(p, '%Y-%m-%d').date() for p in price_df['Date'].values)
    f_price_date = min(price_dates_list)
    if f_doc_date > f_price_date:
        f_price_date = find_nearest_price_date(f_doc_date, price_dates_list)
    else:
        i = 2
        while f_doc_date < f_price_date:
            f_doc_date = get_doc_first_date(i)
            i += 1
        f_price_date = find_nearest_price_date(f_doc_date, price_dates_list)
    return f_doc_date, f_price_date


def first_date_data_collect(first_date):
    global first_date_by_sector_dic
    if sector in first_date_by_sector_dic.keys():
        first_date_by_sector_dic[sector].append(first_date)
    else:
        first_date_by_sector_dic[sector] = [first_date]


def first_date_data_consolidate():
    global all_dates
    all_dates = list(all_dates)
    all_dates.sort()
    sector_keys = []
    sector_values = []
    sectors = []
    for k in first_date_by_sector_dic.keys():
        sectors.append(k)
        for v in first_date_by_sector_dic[k]:
            sector_keys.append(k)
            sector_values.append(v)
    return sector_keys, sector_values


def reorganize_doc_dfs(df1, df2, df3, f_date):
    dfs = [df1, df2, df3]
    for df, n in zip(dfs, list(range(3))):
        f_date = str(f_date)
        f_date_ind = df.columns.get_loc(f_date)
        frames = [df.iloc[:, 0], df.iloc[:, f_date_ind:]]
        #uwaga na utrate informacji
        df = pd.concat(frames, axis=1, join='inner')
        dfs[n] = df
    df1, df2, df3 = dfs
    doc_dates_list = list(df1.columns)[1:]
    return df1, df2, df3, doc_dates_list


def compare_doc_dates(df1, df2, df3):
    df1_cols = df1.columns
    df2_cols = df2.columns
    df3_cols = df3.columns
    comparison = False
    if len(df1_cols.difference(df2_cols)) == 0 and len(df1_cols.difference(df3_cols)) == 0 and len(df2_cols.difference(df3_cols)) == 0:
        comparison = True
    return comparison


def reorganize_price_df(df, doc_dates):
    df = df.transpose()
    df.columns = df.iloc[0, :]
    df = df[1:]
    price_dates_list = list(df.columns)
    reorganized_price_dates = []
    doc_price_dates_dic = {}
    for doc_d in doc_dates:
        nearest_price_date = find_nearest_price_date(doc_d, price_dates_list)
        reorganized_price_dates.append(nearest_price_date)
        doc_price_dates_dic[doc_d] = nearest_price_date
    df = df[reorganized_price_dates]
    return df


def download_price_df(yf_tic):
    print(yf_tic)
    url = f'https://query1.finance.yahoo.com/v7/finance/download/{yf_tic}?period1=971913600&period2=1649548800&interval=1d&events=history&includeAdjustedClose=true'
    p_df = pd.read_csv(url)
    return p_df


st = time.time()
dataframe_display_options()

companys_sector_dic = f.create_companys_sector_dictionary()
# sectors = f.extract_sectors
first_date_by_sector_dic = {}
all_dates = set()

directory_path = 'C:\\Users\\Bartek\\Desktop\\ALK praca magisterska\\China_stock_data'
all_files_list = os.listdir(directory_path)
companys_dictionary = f.create_companys_dictionary(all_files_list)

for company in companys_dictionary.keys():
    print(company)
    #print(companys_sector_dic[company])
    for doc in companys_dictionary[company]:

        file_name = '{0} - {1}.csv'.format(company, doc)
        file_path = os.path.join(directory_path, file_name)
        doc_df = pd.read_csv(file_path)
        doc_df = f.prepare_df(doc_df)
        all_dates.update(doc_df.columns)

        if doc == 'Income Statement':
            incst_df = doc_df
        elif doc == 'Balance Sheet':
            b_df = doc_df
        elif doc == 'Cash Flow Statement':
            cf_df = doc_df

    sector, yf_ticker = companys_sector_dic[company]
    price_df = download_price_df(yf_ticker)
    doc_first_date, price_first_date = find_first_date()
    incst_df, b_df, cf_df, doc_dates_list = reorganize_doc_dfs(incst_df, b_df, cf_df, doc_first_date)

    if compare_doc_dates(incst_df, b_df, cf_df) is False:
        print('Dates in docs are not equal for {}'.format(company))
        continue

    price_reorganized_df = reorganize_price_df(price_df, doc_dates_list)
    first_date_data_collect(doc_first_date)

    incst = IncomeStatement(incst_df)
    b = Balance(b_df)
    cf = CashFlow(cf_df)

    print(incst.Revenue.period(2021, 4))
    #print(incst.WeightedAverageDilutedSharesOut.period(2021, 4))


sector_keys, sector_values = first_date_data_consolidate()


xticks_loc = range(len(sector_keys))
fig, ax = plt.subplots()
ax.scatter(sector_keys, sector_values)
#fig, ax = plt.subplots(1,2)
#ax[0][0].scatter(sector_keys, sector_values)
#ax[0][1].scatter()
plt.xlabel('Sektory', labelpad=15)
plt.ylabel('Początek danych')
plt.xticks(rotation=90)
plt.tight_layout()
plt.show()

et = time.time()
print(et - st)
print()
