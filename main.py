import numpy as np
import matplotlib.pyplot as plt
import os
import time
from preparedata import prepare_data, prepare_classes
import functions as f
from verifydata import verify_data
import calculations
import plotsandcharts
import datetime


def first_date_data_consolidate(first_date_by_sector_collection_dic):
    sector_keys = []
    sector_values = []
    sectors = []
    for k in first_date_by_sector_collection_dic.keys():
        sectors.append(k)
        for v in first_date_by_sector_collection_dic[k]:
            sector_keys.append(k)
            sector_values.append(v)
    return sector_keys, sector_values


if __name__ == '__main__':
    st = time.time()
    f.dataframe_display_options()
    directory_path = 'C:\\Users\\Bartek\\Desktop\\ALK praca magisterska\\China_stock_data_test'
    #directory_path = 'C:\\Users\\Bartek\\Desktop\\ALK praca magisterska\\China_stock_data'
    #directory_path = 'C:\\Users\\Bartek\\Desktop\\ALK praca magisterska\\China_stock_data\\Nowy folder'
    all_files_list = os.listdir(directory_path)
    companys_dictionary = f.create_companys_dictionary(all_files_list)
    companys_sector_dic = f.create_companys_sector_dictionary()
    sector_companys_dic = f.create_sector_companys_dictionary()
    sectors_l = [sec for sec in sector_companys_dic.keys()]
    min_date = datetime.date(2017, 3, 1)


    #for company in companys_dictionary.keys():
    #    prepared_data_result = prepare_data(company, companys_dictionary, companys_sector_dic, all_dates, directory_path, first_date_by_sector_dic)
    #    if prepared_data_result is None:
    #        continue
    #    else:
    #        incst, b, cf, price, all_dates, first_date_by_sector_dic = prepared_data_result
    ###########################################################################
    verified_companies = {}
    first_date_by_company_dic = {}
    first_date_by_sector_collection_dic = {}

    for company in companys_dictionary.keys():
        verified_data_result = verify_data(company, companys_dictionary, companys_sector_dic, directory_path, first_date_by_company_dic, first_date_by_sector_collection_dic, min_date)
        if verified_data_result is None:
            continue
        else:
            dfs, first_date_by_sector_collection_dic, first_date_by_company_dic = verified_data_result
            verified_companies[company] = dfs

    sector_capitalization_dict = {}
    res = f.create_dictionaries_of_sectors_with_lists(sectors_l, sector_capitalization_dict)
    sector_capitalization_dict = res[0]

    for company in verified_companies.keys():
        print(company)
        sector = companys_sector_dic[company][0]
        print(sector)
        dfs = verified_companies[company]
        incst_df, b_df, cf_df, price_df = dfs
        doc_first_date, price_first_date = first_date_by_company_dic[company]
        incst_df, b_df, cf_df, price_df = prepare_data(incst_df, b_df, cf_df, price_df, doc_first_date, min_date)
        incst, b, cf, price = prepare_classes(incst_df, b_df, cf_df, price_df)
    ############################################################################
        first_date = first_date_by_company_dic[company]

        company_capitalization_dict = calculations.get_company_capitalization_by_date_dict(min_date, incst, price)
        sector_capitalization_dict = f.add_new_dict_to_sector_dict_list(sector_capitalization_dict, company_capitalization_dict, sector)

    x_labels = plotsandcharts.create_x_labels(sector_capitalization_dict)
    x_axis = np.arange(len(x_labels), dtype=float)
    fig = plt.figure()
    for sector in sectors_l:
        y = plotsandcharts.create_y(sector, sector_capitalization_dict, x_labels)
        plt.bar(x_axis, y, 0.05, label=sector)
        x_axis += 0.05
        print(x_axis)

    plt.xticks(x_axis, x_labels, rotation=90)
    plt.legend(loc='upper center', bbox_to_anchor=(0.5, 1.17), ncol=4, fancybox=True, shadow=True)

    plt.show()

    #fig, axs = plt.subplots(1, 1)
    #sector_keys, sector_values = first_date_data_consolidate(first_date_by_sector_collection_dic)
    #xticks_loc = range(len(sector_keys))
    #axs.scatter(sector_keys, sector_values)
    #plt.xlabel('Sektory', labelpad=15)
    #plt.ylabel('Początek danych')
    #plt.xticks(rotation=90)
    #plt.tight_layout()
    #plt.show()

    et = time.time()
    print(et - st)
