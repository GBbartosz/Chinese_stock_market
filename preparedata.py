import datetime
import pandas as pd
import functions as f
from incomestatement import IncomeStatement
from balance import Balance
from cashflow import CashFlow
from priceclass import Price


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


def reorganize_price_df(df, doc_dates):
    df = df.transpose()
    df.columns = df.iloc[0, :]
    df = df[1:]
    price_dates_list = list(df.columns)
    reorganized_price_dates = []
    price_doc_dates_dic = {}
    for doc_d in doc_dates:
        nearest_price_date = f.find_nearest_price_date(doc_d, price_dates_list)
        reorganized_price_dates.append(nearest_price_date)
        price_doc_dates_dic[nearest_price_date] = doc_d
    df = df[reorganized_price_dates]
    df.rename(columns=price_doc_dates_dic, inplace=True)
    return df


def prepare_data(incst_df, b_df, cf_df, price_df, doc_first_date, min_date):
    incst_df, b_df, cf_df, doc_dates_list = reorganize_doc_dfs(incst_df, b_df, cf_df, doc_first_date)
    price_df = reorganize_price_df(price_df, doc_dates_list)
    dfs = [incst_df, b_df, cf_df, price_df]
    incst_df, b_df, cf_df, price_df = prepare_dfs_to_common_timeline(dfs, min_date)
    return incst_df, b_df, cf_df, price_df


def prepare_classes(incst_df, b_df, cf_df, price_df):
    incst = IncomeStatement(incst_df)
    b = Balance(b_df)
    cf = CashFlow(cf_df)
    price = Price(price_df)
    return incst, b, cf, price


def prepare_dfs_to_common_timeline(dfs, min_date):
    rng = range(len(dfs))
    for i, df in zip(rng, dfs):
        for col in df.columns:
            if col != 'Positions':
                col_date = datetime.datetime.strptime(col, '%Y-%m-%d').date()
                if col_date < min_date:
                    df.drop(col, axis=1, inplace=True)
        dfs[i] = df
    incst_df, b_df, cf_df, price_df = dfs
    return incst_df, b_df, cf_df, price_df
