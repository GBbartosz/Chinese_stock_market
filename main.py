import os
import time
import preparedata
from preparedata import prepare_data, prepare_classes
import functions as f
from verifydata import verify_data
import calculations
import datetime
import plotsandcharts
import pandas as pd


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
    min_date = datetime.date(2019, 1, 1)
    max_date = datetime.date(2021, 12, 31)
    number_of_periods = 12

    late_first_sector_all = {}
    late_first_sector_doc = {}
    late_first_sector_price = {}
    res = f.create_dictionaries_of_sectors_with_dicts(sectors_l, late_first_sector_all, late_first_sector_doc, late_first_sector_price)
    late_first_sector_all, late_first_sector_doc, late_first_sector_price = res

    price_docs_date_not_compatible_sector_dict = f.create_companies_in_sector_dict(sectors_l)
    doc_dates_not_equal_dict = f.create_companies_in_sector_dict(sectors_l)
    late_first_sector_price_companies = f.create_companies_in_sector_dict(sectors_l)
    verified_companies = {}
    first_date_by_company_dic = {}
    first_date_by_sector_collection_dic = {}

    for company in companys_dictionary.keys():
        verified_data_result = verify_data(company, companys_dictionary, companys_sector_dic, directory_path, first_date_by_company_dic, first_date_by_sector_collection_dic, min_date, number_of_periods, late_first_sector_all, late_first_sector_doc, late_first_sector_price, price_docs_date_not_compatible_sector_dict, doc_dates_not_equal_dict, late_first_sector_price_companies)
        if verified_data_result is None:
            continue
        else:
            dfs, first_date_by_sector_collection_dic, first_date_by_company_dic, late_first_sector_all, late_first_sector_doc, late_first_sector_price, price_docs_date_not_compatible_sector_dict, doc_dates_not_equal_dict, late_first_sector_price_companies = verified_data_result
            verified_companies[company] = dfs

    sector_capitalization_dict = {}
    sector_capitalization_change_dict = {}
    sector_pe_ratio_dict = {}
    sector_ps_ratio_dict = {}
    sector_revenue_dict = {}
    sector_revenue_change_dict = {}

    sector_net_income_dict = {}
    sector_cf_operating = {}
    sector_cf_financing = {}
    sector_cf_investing = {}
    sector_operating_income = {}

    sector_net_income_change_dict = {}
    sector_pb_ratio = {}
    sector_price = {}
    sector_price_change = {}

    dicts_l = [sector_capitalization_dict, sector_capitalization_change_dict, sector_pe_ratio_dict, sector_ps_ratio_dict, sector_revenue_dict, sector_revenue_change_dict, sector_net_income_dict, sector_net_income_change_dict, sector_pb_ratio, sector_price, sector_price_change, sector_cf_operating, sector_cf_financing, sector_cf_investing, sector_operating_income]
    res_sectors_dicts = f.create_dictionaries_of_sectors_with_lists(sectors_l, dicts_l)
    sector_capitalization_dict, sector_capitalization_change_dict, sector_pe_ratio_dict, sector_ps_ratio_dict, sector_revenue_dict, sector_revenue_change_dict, sector_net_income_dict, sector_net_income_change_dict, sector_pb_ratio, sector_price, sector_price_change, sector_cf_operating, sector_cf_financing, sector_cf_investing, sector_operating_income = res_sectors_dicts

    companies_in_sector_dict = f.create_companies_in_sector_dict(sectors_l)
    number_of_companies_in_sector = {}
    number_of_companies_in_sector = number_of_companies_in_sector.fromkeys(sectors_l, 0)

    print('number of companies at beginning: ' + str(len(list(companys_dictionary.keys()))))
    print('number of verified companies: ' + str(len(list(verified_companies.keys()))))

    lack = 0
    calculated_companies_in_sector_dict = f.create_companies_in_sector_dict(sectors_l)
    close_price_in_sector_dict = f.create_dictionary_of_sectors_with_dicts(sectors_l)
    for company in verified_companies.keys():
        print(company)
        sector = companys_sector_dic[company][0]
        print(sector)
        calculated_companies_in_sector_dict[sector] = calculated_companies_in_sector_dict[sector] + [company]
        dfs = verified_companies[company]
        incst_df, b_df, cf_df, price_df = dfs
        full_price_df = preparedata.create_full_price_df_in_period(price_df, min_date, max_date)
        close_price_in_sector_dict[sector][company] = full_price_df[['Date', 'Close']]
        doc_first_date, price_first_date = first_date_by_company_dic[company]
        incst_df, b_df, cf_df, price_df = prepare_data(incst_df, b_df, cf_df, price_df, doc_first_date, min_date)
        incst, b, cf, price = prepare_classes(incst_df, b_df, cf_df, price_df)
        first_date = first_date_by_company_dic[company]

        company_capitalization_dict = calculations.capitalization_calc(min_date, incst, price)
        sector_capitalization_dict = f.add_new_dict_to_sector_dict_list(sector_capitalization_dict, company_capitalization_dict, sector)
        company_capitalization_change_dict = calculations.capitalization_change_calc(min_date, incst, price)
        sector_capitalization_change_dict = f.add_new_dict_to_sector_dict_list(sector_capitalization_change_dict, company_capitalization_change_dict, sector)
        company_pe_ratio_dict = calculations.pe_ratio_yearly_calc(min_date, incst, price)
        sector_pe_ratio_dict = f.add_new_dict_to_sector_dict_list(sector_pe_ratio_dict, company_pe_ratio_dict, sector)
        company_ps_ratio_dict = calculations.ps_ratio_yearly_calc(min_date, incst, price)
        sector_ps_ratio_dict = f.add_new_dict_to_sector_dict_list(sector_ps_ratio_dict, company_ps_ratio_dict, sector)
        company_revenue_dict = calculations.revenue_calc(min_date, incst)
        sector_revenue_dict = f.add_new_dict_to_sector_dict_list(sector_revenue_dict, company_revenue_dict, sector)
        company_revenue_change_dict = calculations.revenue_change_calc(min_date, incst)
        sector_revenue_change_dict = f.add_new_dict_to_sector_dict_list(sector_revenue_change_dict, company_revenue_change_dict, sector)

        company_net_income_dict = calculations.net_income_calc(min_date, incst)
        sector_net_income_dict = f.add_new_dict_to_sector_dict_list(sector_net_income_dict, company_net_income_dict, sector)

        company_cf_operating_dict = calculations.cash_flow_from_operating_activities_calc(min_date, cf)
        sector_cf_operating = f.add_new_dict_to_sector_dict_list(sector_cf_operating, company_cf_operating_dict, sector)

        company_cf_financing_dict = calculations.cash_flow_from_financing_activities_calc(min_date, cf)
        sector_cf_financing = f.add_new_dict_to_sector_dict_list(sector_cf_financing, company_cf_financing_dict, sector)

        company_cf_investing_dict = calculations.cash_flow_from_investing_calc(min_date, cf)
        sector_cf_investing = f.add_new_dict_to_sector_dict_list(sector_cf_investing, company_cf_investing_dict, sector)

        company_operating_income_dict = calculations.operating_income_calc(min_date, incst)
        sector_operating_income = f.add_new_dict_to_sector_dict_list(sector_operating_income, company_operating_income_dict, sector)

        company_net_income_change_dict = calculations.net_income_change_calc(min_date, incst)
        sector_net_income_change_dict = f.add_new_dict_to_sector_dict_list(sector_net_income_change_dict, company_net_income_change_dict, sector)
        company_pb_ratio = calculations.price_to_book_ratio_calc(min_date, incst, b, price)
        sector_pb_ratio = f.add_new_dict_to_sector_dict_list(sector_pb_ratio, company_pb_ratio, sector)
        company_price = calculations.price_calc(min_date, price)
        sector_price = f.add_new_dict_to_sector_dict_list(sector_price, company_price, sector)
        company_price_change = calculations.price_change_calc(min_date, price)
        sector_price_change = f.add_new_dict_to_sector_dict_list(sector_price_change, company_price_change, sector)
        companies_in_sector_dict[sector] = companies_in_sector_dict[sector] + [company]
        number_of_companies_in_sector[sector] += 1

    #plotsandcharts.sector_bar_chart(sectors_l, sector_capitalization_dict, 'Capitalization', 'sum', calculated_companies_in_sector_dict)
    #plotsandcharts.sector_bar_chart(sectors_l, sector_capitalization_change_dict, 'Capitalization change', 'average', calculated_companies_in_sector_dict)
    #plotsandcharts.sector_bar_chart(sectors_l, sector_pe_ratio_dict, 'PE ratio', 'average', calculated_companies_in_sector_dict)
    #plotsandcharts.sector_bar_chart(sectors_l, sector_ps_ratio_dict, 'PS ratio', 'average', calculated_companies_in_sector_dict)
    #plotsandcharts.sector_bar_chart(sectors_l, sector_revenue_dict, 'Revenue', 'sum', calculated_companies_in_sector_dict)
    #plotsandcharts.sector_bar_chart(sectors_l, sector_revenue_change_dict, 'Revenue change', 'average', calculated_companies_in_sector_dict)


    #plotsandcharts.sector_bar_chart(sectors_l, sector_net_income_dict, 'Net income', 'sum', calculated_companies_in_sector_dict)
    #plotsandcharts.sector_bar_chart(sectors_l, sector_cf_operating, 'Cash flow from operating activities', 'sum', calculated_companies_in_sector_dict)
    #plotsandcharts.sector_bar_chart(sectors_l, sector_cf_financing, 'Cash flow from financing activities', 'sum', calculated_companies_in_sector_dict)
    #plotsandcharts.sector_bar_chart(sectors_l, sector_cf_investing, 'Cash flow from investing activities', 'sum', calculated_companies_in_sector_dict)
    #plotsandcharts.sector_bar_chart(sectors_l, sector_operating_income, 'Operating income', 'sum', calculated_companies_in_sector_dict)


    plotsandcharts.sector_bar_chart(sectors_l, sector_net_income_change_dict, 'Net income change', 'average', calculated_companies_in_sector_dict)
    plotsandcharts.sector_bar_chart(sectors_l, sector_pb_ratio, 'Price to book ratio', 'average', calculated_companies_in_sector_dict)
    plotsandcharts.sector_bar_chart(sectors_l, sector_price, 'Price', 'average', calculated_companies_in_sector_dict)
    plotsandcharts.sector_bar_chart(sectors_l, sector_price_change, 'Price change', 'average', calculated_companies_in_sector_dict)
    plotsandcharts.number_of_companies_in_sector_bar_chart(number_of_companies_in_sector)

    for sector in sectors_l:
        #plotsandcharts.companies_in_sector_bar_chart(sector, sector_capitalization_dict, 'Capitalization', None, calculated_companies_in_sector_dict)
        #plotsandcharts.companies_in_sector_bar_chart(sector, sector_capitalization_change_dict, 'Capitalization change', None, calculated_companies_in_sector_dict)
        #plotsandcharts.companies_in_sector_bar_chart(sector, sector_pe_ratio_dict, 'PE ratio', None, calculated_companies_in_sector_dict)
        #plotsandcharts.companies_in_sector_bar_chart(sector, sector_ps_ratio_dict, 'PS ratio', None, calculated_companies_in_sector_dict)
        #plotsandcharts.companies_in_sector_bar_chart(sector, sector_revenue_dict, 'Revenue', None, calculated_companies_in_sector_dict)
        #plotsandcharts.companies_in_sector_bar_chart(sector, sector_revenue_change_dict, 'Revenue change', None, calculated_companies_in_sector_dict)

        #plotsandcharts.companies_in_sector_bar_chart(sector, sector_net_income_dict, 'Net income', None, calculated_companies_in_sector_dict)
        #plotsandcharts.companies_in_sector_bar_chart(sector, sector_cf_operating, 'Operating cf', None, calculated_companies_in_sector_dict)
        #plotsandcharts.companies_in_sector_bar_chart(sector, sector_cf_financing, 'Financing cf', None, calculated_companies_in_sector_dict)
        #plotsandcharts.companies_in_sector_bar_chart(sector, sector_cf_investing, 'Investing cf', None, calculated_companies_in_sector_dict)
        #plotsandcharts.companies_in_sector_bar_chart(sector, sector_operating_income, 'Operating income', None, calculated_companies_in_sector_dict)


        plotsandcharts.companies_in_sector_bar_chart(sector, sector_net_income_change_dict, 'Net income change', None, calculated_companies_in_sector_dict)
        plotsandcharts.companies_in_sector_bar_chart(sector, sector_pb_ratio, 'Price to book ratio', None, calculated_companies_in_sector_dict)
        plotsandcharts.companies_in_sector_bar_chart(sector, sector_price, 'Price', None, calculated_companies_in_sector_dict)
        plotsandcharts.companies_in_sector_bar_chart(sector, sector_price_change, 'Price change', None, calculated_companies_in_sector_dict)

    comp_standard_deviation_dict = calculations.create_close_price_volatility_for_comp_dict(close_price_in_sector_dict)
    sectors_standard_deviation_dict = calculations.create_close_price_volatility_for_sector_dict(comp_standard_deviation_dict)
    plotsandcharts.standard_deviation_bef_aft_bar_chart_for_comps_in_sec(comp_standard_deviation_dict)
    plotsandcharts.standard_deviation_bef_aft_bar_chart_for_sec(sectors_standard_deviation_dict)
    plotsandcharts.close_price_for_companies_in_sector_plot(close_price_in_sector_dict)
    plotsandcharts.close_price_for_sectors_plot(close_price_in_sector_dict)

    calculations.maximum_price_spread(close_price_in_sector_dict)

    plotsandcharts.close_price_change_for_each_sector(close_price_in_sector_dict)

    for k in number_of_companies_in_sector.keys():
        number_of_companies_in_sector[k] = [number_of_companies_in_sector[k]]
    df = pd.DataFrame(number_of_companies_in_sector)
    df.to_excel(r'C:\Users\Bartek\Desktop\ALK praca magisterska\number_of_companies_in_sector.xlsx')
    f.equalize_dict_lists_and_to_file(companies_in_sector_dict, 'companies_in_sector.xlsx')
    # lack of data excel reports
    f.equalize_dict_lists_and_to_file(price_docs_date_not_compatible_sector_dict, 'price_docs_date_not_compatible.xlsx')
    f.equalize_dict_lists_and_to_file(doc_dates_not_equal_dict, 'doc_dates_not_equal.xlsx')
    f.get_missed_companies_due_to_min_date(late_first_sector_all, 'late_first_sector_all.xlsx')
    f.get_missed_companies_due_to_min_date(late_first_sector_doc, 'late_first_sector_doc.xlsx')
    f.get_missed_companies_due_to_min_date(late_first_sector_price, 'late_first_sector_price.xlsx')
    et = time.time()
    print(et - st)
