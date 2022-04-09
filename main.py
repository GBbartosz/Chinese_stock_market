import os
import pandas as pd
import time
from incomestatement import IncomeStatement
from balance import Balance
from cashflow import CashFlow

import functions as f

st = time.time()
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

companys_sector_dic = f.create_companys_sector_dictionary()

directory_path = 'C:\\Users\\Bartek\\Desktop\\ALK praca magisterska\\China_stock_data'
all_files_list = os.listdir(directory_path)
companys_dictionary = f.create_companys_dictionary(all_files_list)

for company in companys_dictionary.keys():
    print(company)
    print(companys_sector_dic[company])
    for doc in companys_dictionary[company]:
        file_name = '{0} - {1}.csv'.format(company, doc)
        #print(file_name)
        file_path = os.path.join(directory_path, file_name)
        df = pd.read_csv(file_path)
        df = f.prepare_df(df)

        #if companys_sector_dic[company] != 'Financials':
        if doc == 'Income Statement':
            incst = IncomeStatement(df)
        elif doc == 'Balance Sheet':
            b = Balance(df)
        elif doc == 'Cash Flow Statement':
            cf = CashFlow(df)

et = time.time()
print(et - st)
