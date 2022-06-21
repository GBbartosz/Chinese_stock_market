import pandas as pd


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


def create_dictionaries_of_sectors_with_lists(sectors_l, *args):
    for arg in args:
        for sector in sectors_l:
            arg[sector] = []
    return args


def add_new_dict_to_sector_dict_list(main_dict, new_dict, k):
    tmp_sector_dict_list = main_dict[k]
    tmp_sector_dict_list.append(new_dict)
    main_dict[k] = tmp_sector_dict_list
    return main_dict


