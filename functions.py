import pandas as pd


def extract_sectors():
    df = pd.read_excel('C:\\Users\\Bartek\\Desktop\\ALK praca magisterska\\Companies list.xlsx',
                       sheet_name='CompanysSector')
    sectors = pd.unique(df['Sector'])
    return sectors


def create_companys_sector_dictionary():
    df = pd.read_excel('C:\\Users\\Bartek\\Desktop\\ALK praca magisterska\\Companies list.xlsx',
                       sheet_name='CompanysSector')
    companys_sector_dic = {}
    for i in df.index:
        companys_sector_dic[df.iloc[i, 0]] = [df.iloc[i, 1], df['Yahoo ticker'][i]]
    return companys_sector_dic


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


