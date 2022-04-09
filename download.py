import pandas as pd
import requests
import functions as f
import os


companys_sector_dic = f.create_companys_sector_dictionary()

directory_path = 'C:\\Users\\Bartek\\Desktop\\ALK praca magisterska\\China_stock_data'
all_files_list = os.listdir(directory_path)
companys_dictionary = f.create_companys_dictionary(all_files_list)

sec_dic = {}
for company in companys_dictionary.keys():

    file_name = '{0} - {1}.csv'.format(company, companys_dictionary[company][0])
    #print(file_name)
    file_path = os.path.join(directory_path, file_name)
    df = pd.read_csv(file_path)
    df = f.prepare_df(df)

    df = df['Positions']
    if companys_sector_dic[company] in sec_dic.keys():
        df_diff = pd.concat([sec_dic[companys_sector_dic[company]], df]).drop_duplicates(keep=False)
        print(company)
        print(companys_sector_dic[company])
        print(df_diff)
    else:
        sec_dic[companys_sector_dic[company]] = df

print(sec_dic[companys_sector_dic['Bank of China Limited']])