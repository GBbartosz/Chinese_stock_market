import os
import numpy as np
import pandas as pd
import functions as f


def analyse():
    f.dataframe_display_options()
    file_path = r'C:\Users\Bartek\Desktop\ALK MGR 2022.10\wskazniki_opracowanie.xlsx'

    df = pd.read_excel(file_path)
    print(df)

    sectors_l = df['Sector'].unique()

    print(sectors_l)
    print(type(sectors_l))

if __name__ == '__main__':
    analyse()
