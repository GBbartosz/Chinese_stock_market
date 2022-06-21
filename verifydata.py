import datetime
import io
import os
import pandas as pd
import functions as f


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
        f_price_date = f.find_nearest_price_date(f_doc_date, price_dates_list)
    else:
        i = 2
        while f_doc_date < f_price_date:
            f_doc_date = get_doc_first_date(i)
            i += 1
        f_price_date = f.find_nearest_price_date(f_doc_date, price_dates_list)
    return f_doc_date, f_price_date


def first_date_data_collect(first_date, sector, first_date_by_sector_dic):
    if sector in first_date_by_sector_dic.keys():
        first_date_by_sector_dic[sector].append(first_date)
    else:
        first_date_by_sector_dic[sector] = [first_date]
    return first_date_by_sector_dic


def compare_doc_dates(df1, df2, df3):
    df1_cols = df1.columns
    df2_cols = df2.columns
    df3_cols = df3.columns
    comparison = False
    if len(df1_cols.difference(df2_cols)) == 0 and len(df1_cols.difference(df3_cols)) == 0 and len(
            df2_cols.difference(df3_cols)) == 0:
        comparison = True
    return comparison


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


def create_doc_dfs(company, companys_dictionary, directory_path):
    for doc in companys_dictionary[company]:
        file_name = '{0} - {1}.csv'.format(company, doc)
        file_path = os.path.join(directory_path, file_name)
        doc_df = pd.read_csv(file_path)
        doc_df = f.prepare_df(doc_df)
        if doc == 'Income Statement':
            incst_df = doc_df
        elif doc == 'Balance Sheet':
            b_df = doc_df
        elif doc == 'Cash Flow Statement':
            cf_df = doc_df
    return incst_df, b_df, cf_df


def create_price_df(yfticker):
    price_file_name = r'C:\Users\Bartek\Desktop\ALK praca magisterska\China_stock_data\price longer hkd\{}_price.csv'.format(yfticker)
    price_df = pd.read_csv(price_file_name)
    return price_df


def verify_data(company, companys_dictionary, companys_sector_dic, directory_path, first_date_by_company_dic, first_date_by_sector_dic, min_date):
    incst_df, b_df, cf_df = create_doc_dfs(company, companys_dictionary, directory_path)

    sector, yf_ticker = companys_sector_dic[company]
    price_df = create_price_df(yf_ticker)
    incst_dates, b_dates, cf_dates, price_dates = create_docs_and_price_date_lists(incst_df, b_df, cf_df, price_df)

    if compability_price_and_docs_dates([incst_dates, b_dates, cf_dates, price_dates]) is False:
        print('{}: dates are not compatible'.format(company))
        return None

    doc_first_date, price_first_date = find_first_date(incst_df, b_df, cf_df, price_df)

    if compare_doc_dates(incst_df, b_df, cf_df) is False:
        print('Dates in docs are not equal for {}'.format(company))
        return None

    if doc_first_date > min_date or price_first_date > min_date:
        print('Date greater than min_date for {}'.format(company))
        return None

    first_date_by_company_dic[company] = [doc_first_date, price_first_date]
    first_date_by_sector_collection_dic = first_date_data_collect(doc_first_date, sector, first_date_by_sector_dic)
    dfs = incst_df, b_df, cf_df, price_df
    return dfs, first_date_by_sector_collection_dic, first_date_by_company_dic

