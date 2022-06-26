import datetime
import os
import pandas as pd
import functions as f


def date_convert(x):
    year = int(x[-4:])
    month_name = x[:3]
    datetime_object = datetime.datetime.strptime(month_name, "%b")
    month = datetime_object.month
    day = int(x[-8:-6])
    new_date = str(datetime.date(year=year, month=month, day=day))
    return new_date


def exchange(my_hkd, my_date, my_convert_df):
    price = my_convert_df.loc[my_convert_df['Date'] == my_date, 'Price'].iloc[0]
    cny = my_hkd * price
    return cny


if __name__ == '__main__':
    f.dataframe_display_options()
    currency_convert_path = r'C:\Users\Bartek\Desktop\ALK praca magisterska\HKD_CNY Historical Data.csv'
    convert_df = pd.read_csv(currency_convert_path)
    convert_df['Date'] = convert_df['Date'].apply(lambda x: date_convert(x))

    origin_fold = r'C:\Users\Bartek\Desktop\ALK praca magisterska\China_stock_data\price longer hkd'
    destination_fold = r'C:\Users\Bartek\Desktop\ALK praca magisterska\China_stock_data\price longer after calc cny'

    all_files_list = os.listdir(origin_fold)

    for f_name in all_files_list:
        print(f_name)
        origin_path = os.path.join(origin_fold, f_name)
        df = pd.read_csv(origin_path)
        for col in df.columns:
            if col != 'Date':
                for i in df.index:
                    i_date = df['Date'][i]
                    hkd = df[col][i]
                    df.loc[i, col] = exchange(hkd, i_date, convert_df)
        destination_path = os.path.join(destination_fold, f_name)
        df.to_csv(destination_path, index=False)
