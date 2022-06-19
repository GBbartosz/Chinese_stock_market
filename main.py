
import matplotlib.pyplot as plt
import os
import time
from preparedata import prepare_data, prepare_classes
import functions as f
from verifydata import verify_data
import calculations


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
    directory_path = 'C:\\Users\\Bartek\\Desktop\\ALK praca magisterska\\China_stock_data'
    #directory_path = 'C:\\Users\\Bartek\\Desktop\\ALK praca magisterska\\China_stock_data\\Nowy folder'
    all_files_list = os.listdir(directory_path)
    companys_dictionary = f.create_companys_dictionary(all_files_list)
    companys_sector_dic = f.create_companys_sector_dictionary()
    sector_companys_dic = f.create_sector_companys_dictionary()
    comp_dic = {}


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
        verified_data_result = verify_data(company, companys_dictionary, companys_sector_dic, directory_path, first_date_by_company_dic, first_date_by_sector_collection_dic)
        if verified_data_result is None:
            continue
        else:
            dfs, first_date_by_sector_collection_dic, first_date_by_company_dic = verified_data_result
            verified_companies[company] = dfs

    capitalization_dict = {}
    for company in verified_companies.keys():
        print(company)
        dfs = verified_companies[company]
        incst_df, b_df, cf_df, price_df = dfs
        doc_first_date, price_first_date = first_date_by_company_dic[company]
        incst_df, b_df, cf_df, price_df = prepare_data(incst_df, b_df, cf_df, price_df, doc_first_date)
        incst, b, cf, price = prepare_classes(incst_df, b_df, cf_df, price_df)
    ############################################################################
        # print(incst.Revenue.period(2021, 4))
        # print(incst.WeightedAverageDilutedSharesOut.period(2021, 4))
        first_date = first_date_by_company_dic[company]

        #company_capitalization_dict = calculations.get_company_capitalization_by_date_dict(first_date, incst, price)
        #print('Price {} - year({}), quarter({}): {}'.format(company, year, quarter, str(price.close.period(year, quarter))))
        #capitalization_dict[company] = company_capitalization_dict





    #print(capitalization_dict)

    fig, axs = plt.subplots(1, 1)




    sector_keys, sector_values = first_date_data_consolidate(first_date_by_sector_collection_dic)
    xticks_loc = range(len(sector_keys))
    axs.scatter(sector_keys, sector_values)
    plt.xlabel('Sektory', labelpad=15)
    plt.ylabel('Początek danych')
    plt.xticks(rotation=90)
    plt.tight_layout()
    plt.show()

    et = time.time()
    print(et - st)
