import os.path
import pandas as pd
import datetime



def dataframe_display_options():
    pd.set_option('display.max_rows', 500)
    pd.set_option('display.max_columns', 500)
    pd.set_option('display.width', 1000)


def create_companys_dictionary(all_files_list):
    companys_dictionary = {}
    document_types_dic = {'Income Statement': -23, 'Balance Sheet': -20, 'Cash Flow Statement': -26}
    document_types = ['Income Statement', 'Balance Sheet', 'Cash Flow Statement']
    for file_name in all_files_list:
        if 'Income Statement' in file_name:
            file_name = file_name[:document_types_dic['Income Statement']]
            companys_dictionary[file_name] = document_types
        elif 'Balance Sheet' in file_name:
            file_name = file_name[:document_types_dic['Balance Sheet']]
            companys_dictionary[file_name] = document_types
        elif 'Cash Flow Statement' in file_name:
            file_name = file_name[:document_types_dic['Cash Flow Statement']]
            companys_dictionary[file_name] = document_types
    return companys_dictionary


def create_companys_sector_dictionary():
    df = pd.read_excel('C:\\Users\\Bartek\\Desktop\\ALK praca magisterska\\Companies list.xlsx',
                       sheet_name='CompanysSector')
    companys_sector_dic = {}
    for i in df.index:
        companys_sector_dic[df['Name'][i]] = [df['Sector'][i], df['Yahoo ticker'][i]]
    return companys_sector_dic


def create_sector_companys_dictionary():
    df = pd.read_excel('C:\\Users\\Bartek\\Desktop\\ALK praca magisterska\\Companies list.xlsx',
                       sheet_name='CompanysSector')
    sector_companys_dic = {}
    sectors_l = set(df['Sector'].values)
    for sector in sectors_l:
        temp_df = df.loc[df['Sector'] == sector, 'Name']
        sector_companys_dic[sector] = list(temp_df)
    return sector_companys_dic


def create_companys_yahoo_ticker_dictionary():
    df = pd.read_excel('C:\\Users\\Bartek\\Desktop\\ALK praca magisterska\\Companies list.xlsx',
                       sheet_name='CompanysSector')
    companys_yticker_dic = {}
    for i in df.index:
        companys_yticker_dic[df['Name'][i]] = df['Yahoo ticker'][i]
    return companys_yticker_dic


def prepare_df(df):
    df.columns = df.iloc[0]
    df.drop(df.index[0], inplace=True)
    df.reset_index(drop=True, inplace=True)
    df.rename(columns={'Period End Date': 'Positions'}, inplace=True)
    return df


def find_nearest_price_date(f_d_d, price_dates_list):
    if f_d_d in price_dates_list:
        f_p_d = f_d_d
    else:
        d = 0
        while f_d_d > price_dates_list[d]:
            d += 1
        f_p_d = price_dates_list[d-1]
    return f_p_d


def get_following_dates_list(first_date):
    year = first_date.year
    month = first_date.month
    quarter = None
    if month == 3:
        quarter = 1
    elif month == 6:
        quarter = 2
    elif month == 9:
        quarter = 3
    elif month == 12:
        quarter = 4
    else:
        ValueError('Month out of [3, 6, 9, 12]')
    dates_l = []
    while year != 2022:
        while quarter != 5:
            yq = [year, quarter]
            dates_l.append(yq)
            quarter += 1
        year += 1
        quarter = 1
    return dates_l


def create_dictionaries_of_sectors_with_lists(sectors_l, my_l):
    for arg in my_l:
        for sector in sectors_l:
            arg[sector] = []
    return my_l


def create_dictionaries_of_sectors_with_dicts(sectors_l, *args):
    for arg in args:
        for sector in sectors_l:
            arg[sector] = {}
    return args


def add_lack_of_data_instance(out_dict, sector, my_date):
    inner_dict = out_dict[sector]
    if my_date in inner_dict.keys():
        inner_dict[my_date] += 1
    else:
        for d in out_dict.keys():
            tmp_dict = out_dict[d]
            tmp_dict[my_date] = 0
        inner_dict[my_date] = 1
    return out_dict


def add_new_dict_to_sector_dict_list(main_dict, new_dict, k):
    tmp_sector_dict_list = main_dict[k]
    tmp_sector_dict_list.append(new_dict)
    main_dict[k] = tmp_sector_dict_list
    return main_dict


def get_prev_year_quarter(year, quarter, back):
    quarters = 4
    prev_quarter = quarter - back
    prev_year = year
    while prev_quarter < 1:
        prev_quarter += quarters
        prev_year -= 1
    return prev_year, prev_quarter


def key_error_handler(self, year, month, day):
    try:
        col_name = '{year}-{month}-{day}'.format(year=year, month=month, day=day)
        res = float(self.df[col_name])
    except KeyError:
        try:
            col_name = '{year}-{month}-{day}'.format(year=year, month=month, day=day)
            col_name = datetime.datetime.strptime(col_name, '%Y-%m-%d').date()
            col_name = col_name + datetime.timedelta(days=1)
            col_name = str(col_name)
            res = float(self.df[col_name])
        except KeyError:
            col_name = '{year}-{month}-{day}'.format(year=year, month=month, day=day)
            col_name = datetime.datetime.strptime(col_name, '%Y-%m-%d').date()
            col_name = col_name - datetime.timedelta(days=1)
            col_name = str(col_name)
            res = float(self.df[col_name])
    return res


def get_missed_companies_due_to_min_date(late_first, f_name):
    #for k in late_first.keys():
    #    late_first[k] = [late_first[k]]
    late_first_df = pd.DataFrame(late_first)
    #late_first_df = late_first_df.reindex(sorted(late_first_df.columns), axis=1)
    fold = 'C:\\Users\\Bartek\\Desktop\\ALK praca magisterska\\lack_of_data_cause\\'
    path = fold + f_name
    late_first_df.to_excel(path)


#def dict_to_df_to_excel(my_dicts, f_names):
#    fold_path = r'C:\Users\Bartek\Desktop\ALK praca magisterska\python_res_data'
#    for my_dict, f_name in zip(my_dicts, f_names):
#        df = pd.DataFrame(my_dict)
#        path = os.path.join(fold_path, f_name)
#        df.to_excel(path)


def dict_to_df_to_excel(f):
    def inner(sectors_l, sector_dict, title, my_calc_type):
        sector_combined_dict, title, x_labels = f(sectors_l, sector_dict, title, my_calc_type)
        fold_path = r'C:\Users\Bartek\Desktop\ALK praca magisterska\python_res_data'
        df = pd.DataFrame(sector_combined_dict, index=x_labels)
        f_name = title + '.xlsx'
        path = os.path.join(fold_path, f_name)
        df.to_excel(path)
        return None
    return inner


def remove_item_if_empty(my_dict):
    for k in my_dict:
        it = my_dict[k]
        if len(it.keys()) == 0:
            del my_dict[k]
    return my_dict


def create_companies_in_sector_dict(sectors_l):
    companies_in_sector_dict = {}
    for sector in sectors_l:
        companies_in_sector_dict[sector] = []
    return companies_in_sector_dict


def equalize_dict_lists_and_to_file(my_dict, f_name):
    k = max(my_dict, key=lambda k: len(my_dict[k]))
    max_length = len(my_dict[k])
    for k in my_dict.keys():
        length = len(my_dict[k])
        difference = max_length - length
        equalizer_data = difference * [0]
        my_dict[k] = my_dict[k] + equalizer_data
    df = pd.DataFrame(my_dict)
    fold_path = r'C:\Users\Bartek\Desktop\ALK praca magisterska\python_res_data'
    path = os.path.join(fold_path, f_name)
    df.to_excel(path)
