
import datetime
import os
import pandas as pd
import functions as f
from incomestatement import IncomeStatement
from balance import Balance
from cashflow import CashFlow
from priceclass import Price

# uporządkować kod
# stworzyć słownik z df spółek z podziałem na sektory
# może jakaś klasa




def find_nearest_price_date(f_d_d, price_dates_list):
    if f_d_d in price_dates_list:
        f_p_d = f_d_d
    else:
        d = 0
        while f_d_d > price_dates_list[d]:
            d += 1
        f_p_d = price_dates_list[d]
    return f_p_d


def find_first_date(incst_df, b_df, cf_df, price_df):
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


def first_date_data_collect(first_date, sector, first_date_by_sector_dic):
    if sector in first_date_by_sector_dic.keys():
        first_date_by_sector_dic[sector].append(first_date)
    else:
        first_date_by_sector_dic[sector] = [first_date]
    return first_date_by_sector_dic


def reorganize_doc_dfs(df1, df2, df3, f_date):
    dfs = [df1, df2, df3]
    for df, n in zip(dfs, list(range(3))):
        f_date = str(f_date)
        f_date_ind = df.columns.get_loc(f_date)
        frames = [df.iloc[:, 0], df.iloc[:, f_date_ind:]]
        # uwaga na utrate informacji
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
    if len(df1_cols.difference(df2_cols)) == 0 and len(df1_cols.difference(df3_cols)) == 0 and len(
            df2_cols.difference(df3_cols)) == 0:
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


def create_docs_and_price_date_lists(d_df1, d_df2, d_df3, p_df):
    d1 = list(d_df1.columns)[1:]
    d2 = list(d_df2.columns)[1:]
    d3 = list(d_df3.columns)[1:]
    p_d = list(p_df['Date'])
    return d1, d2, d3, p_d


def compability_price_and_docs_dates(dates_lists):
    min_dates_list = []
    max_dates_list = []
    successes = []
    for dates_list in dates_lists:
        min_dates_list.append(min(dates_list))
        max_dates_list.append(max(dates_list))
    for min_date in min_dates_list:
        for max_date in max_dates_list:
            if min_date < max_date:
                successes.append(True)
            else:
                successes.append(False)
    if False in successes:
        success = False
    else:
        success = True
    return success


def prepare_data(company, companys_dictionary, companys_sector_dic, all_dates, directory_path, first_date_by_sector_dic):
    print(company)
    # print(companys_sector_dic[company])
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
    price_file_name = 'C:\\Users\\Bartek\\Desktop\\ALK praca magisterska\\China_stock_data\\price\\{} price.csv'\
        .format(company)
    price_df = pd.read_csv(price_file_name).iloc[:, 1:]

    incst_dates, b_dates, cf_dates, price_dates = create_docs_and_price_date_lists(incst_df, b_df, cf_df, price_df)

    if compability_price_and_docs_dates([incst_dates, b_dates, cf_dates, price_dates]) is False:
        print('dates are not compatible')
        return None

    doc_first_date, price_first_date = find_first_date(incst_df, b_df, cf_df, price_df)
    incst_df, b_df, cf_df, doc_dates_list = reorganize_doc_dfs(incst_df, b_df, cf_df, doc_first_date)

    if compare_doc_dates(incst_df, b_df, cf_df) is False:
        print('Dates in docs are not equal for {}'.format(company))
        return None

    price_reorganized_df = reorganize_price_df(price_df, doc_dates_list)
    first_date_data_collect(doc_first_date, sector, first_date_by_sector_dic)

    incst = IncomeStatement(incst_df)
    b = Balance(b_df)
    cf = CashFlow(cf_df)
    price = Price(price_reorganized_df)
    return incst, b, cf, price, all_dates, first_date_by_sector_dic
