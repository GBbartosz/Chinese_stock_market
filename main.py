import numpy as np
import matplotlib.pyplot as plt
import os
import time

import pandas as pd

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
    directory_path = 'C:\\Users\\Bartek\\Desktop\\ALK praca magisterska\\China_stock_data'
    #directory_path = 'C:\\Users\\Bartek\\Desktop\\ALK praca magisterska\\China_stock_data\\Nowy folder'
    all_files_list = os.listdir(directory_path)
    companys_dictionary = f.create_companys_dictionary(all_files_list)
    companys_sector_dic = f.create_companys_sector_dictionary()
    sector_companys_dic = f.create_sector_companys_dictionary()
    sectors_l = [sec for sec in sector_companys_dic.keys()]
    min_date = datetime.date(2017, 3, 1)
    number_of_periods = 20

    late_first_sector_all = {}
    late_first_sector_doc = {}
    late_first_sector_price = {}

    res = f.create_dictionaries_of_sectors_with_dicts(sectors_l, late_first_sector_all, late_first_sector_doc, late_first_sector_price)
    late_first_sector_all, late_first_sector_doc, late_first_sector_price = res
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
        verified_data_result = verify_data(company, companys_dictionary, companys_sector_dic, directory_path, first_date_by_company_dic, first_date_by_sector_collection_dic, min_date, number_of_periods, late_first_sector_all, late_first_sector_doc, late_first_sector_price)
        if verified_data_result is None:
            continue
        else:
            dfs, first_date_by_sector_collection_dic, first_date_by_company_dic, late_first_sector_all, late_first_sector_doc, late_first_sector_price = verified_data_result
            verified_companies[company] = dfs

    sector_capitalization_dict = {}
    sector_pe_ratio_dict = {}
    sector_ps_ratio_dict = {}
    sector_revenue_dict = {}
    sector_revenue_change_dict = {}
    sector_net_income_dict = {}
    sector_net_income_change_dict = {}
    res = f.create_dictionaries_of_sectors_with_lists(sectors_l, sector_capitalization_dict, sector_pe_ratio_dict, sector_ps_ratio_dict, sector_revenue_dict, sector_revenue_change_dict, sector_net_income_dict, sector_net_income_change_dict)
    sector_capitalization_dict, sector_pe_ratio_dict, sector_ps_ratio_dict, sector_revenue_dict, sector_revenue_change_dict, sector_net_income_dict, sector_net_income_change_dict = res

    number_of_companies_in_sector = {}
    number_of_companies_in_sector = number_of_companies_in_sector.fromkeys(sectors_l, 0)

    print('number of companies at beginning: ' + str(len(list(companys_dictionary.keys()))))
    print('number of verified companies: ' + str(len(list(verified_companies.keys()))))

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

        #company_capitalization_dict = calculations.get_company_capitalization_by_date_dict(min_date, incst, price)
        company_capitalization_dict = calculations.capitalization_calc(min_date, incst, price)
        sector_capitalization_dict = f.add_new_dict_to_sector_dict_list(sector_capitalization_dict, company_capitalization_dict, sector)

        company_pe_ratio_dict = calculations.pe_ratio_calc(min_date, incst, price)
        sector_pe_ratio_dict = f.add_new_dict_to_sector_dict_list(sector_pe_ratio_dict, company_pe_ratio_dict, sector)

        company_ps_ratio_dict = calculations.ps_ratio_calc(min_date, incst, price)
        sector_ps_ratio_dict = f.add_new_dict_to_sector_dict_list(sector_ps_ratio_dict, company_ps_ratio_dict, sector)

        company_revenue_dict = calculations.revenue_calc(min_date, incst)
        sector_revenue_dict = f.add_new_dict_to_sector_dict_list(sector_revenue_dict, company_revenue_dict, sector)

        company_revenue_change_dict = calculations.revenue_change_calc(min_date, incst)
        sector_revenue_change_dict = f.add_new_dict_to_sector_dict_list(sector_revenue_change_dict, company_revenue_change_dict, sector)
        
        company_net_income_dict = calculations.net_income_calc(min_date, incst)
        sector_net_income_dict = f.add_new_dict_to_sector_dict_list(sector_net_income_dict, company_net_income_dict, sector)

        company_net_income_change_dict = calculations.net_income_change_calc(min_date, incst)
        sector_net_income_change_dict = f.add_new_dict_to_sector_dict_list(sector_net_income_change_dict, company_net_income_change_dict, sector)
        
        number_of_companies_in_sector[sector] += 1



    #plotsandcharts.sector_bar_chart(sectors_l, sector_capitalization_dict, 'Capitalization', 'sum')
    #plotsandcharts.sector_bar_chart(sectors_l, sector_pe_ratio_dict, 'P/E ratio', 'average')
    #plotsandcharts.sector_bar_chart(sectors_l, sector_ps_ratio_dict, 'P/S ratio', 'average')
    #plotsandcharts.sector_bar_chart(sectors_l, sector_revenue_dict, 'Revenue', 'sum')
    #plotsandcharts.sector_bar_chart(sectors_l, sector_revenue_change_dict, 'Revenue change', 'average')
    #plotsandcharts.sector_bar_chart(sectors_l, sector_net_income_dict, 'Net income', 'sum')
    #plotsandcharts.sector_bar_chart(sectors_l, sector_net_income_change_dict, 'Net income change', 'average')
    #plotsandcharts.number_of_companies_in_sector_bar_chart(number_of_companies_in_sector)
    for k in number_of_companies_in_sector.keys():
        number_of_companies_in_sector[k] = [number_of_companies_in_sector[k]]
    df = pd.DataFrame(number_of_companies_in_sector)
    print(df)
    # lack of data excel reports
    # f.get_missed_companies_due_to_min_date(late_first_sector_all, 'late_first_sector_all.xlsx')
    # f.get_missed_companies_due_to_min_date(late_first_sector_doc, 'late_first_sector_doc.xlsx')
    # f.get_missed_companies_due_to_min_date(late_first_sector_price, 'late_first_sector_price.xlsx')

    et = time.time()
    print(et - st)
