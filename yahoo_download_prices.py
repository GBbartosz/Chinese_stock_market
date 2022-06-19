import os
import pandas as pd
import requests
import numpy as np
import functions as f
import matplotlib.pyplot as plt

def prepare_data_for_loop():
    directory_path = 'C:\\Users\\Bartek\\Desktop\\ALK praca magisterska\\China_stock_data'




def download_longer_hkd_prices():
    companys_dictionary = f.create_companys_yahoo_ticker_dictionary()
    base_link = 'https://query1.finance.yahoo.com/v7/finance/download/{}?period1=1356998400&period2=1655510400&interval=1d&events=history&includeAdjustedClose=true'
    headers = {'User-agent': 'Mozilla/5.0'}
    for company in companys_dictionary.keys():
        print(company)
        ticker = companys_dictionary[company]
        link = base_link.format(ticker)
        r = requests.get(link, headers=headers, allow_redirects=True)
        f_name = '{}_price.csv'.format(ticker)
        open(f_name, 'wb').write(r.content)


def count_instances(last_price_dict, last_price):
    if last_price in last_price_dict.keys():
        last_price_dict[last_price] += 1
    else:
        last_price_dict[last_price] = np.array(1)
    return last_price_dict


if __name__ == '__main__':
    f.dataframe_display_options()
    dir_path = r'C:\Users\Bartek\Desktop\ALK praca magisterska\China_stock_data\price longer hkd'
    all_files_list = os.listdir(dir_path)
    last_price_dict = {}
    for fil in all_files_list:
        name = fil[:-4]
        fil_path = os.path.join(dir_path, fil)
        df = pd.read_csv(fil_path)
        current_price = df['Date'].iloc[-1]
        last_price = str(df['Date'].iloc[0])[:4]
        count_instances(last_price_dict, last_price)
        print(name)
        print('current_price: {}'.format(str(current_price)))
        print('last_price: {}'.format(last_price))

    print(last_price_dict)

    names = list(last_price_dict.keys())
    names.sort()
    values = []
    for k in names:
        values.append(last_price_dict[k])
    plt.bar(range(len(last_price_dict)), values, tick_label=names)
    plt.show()