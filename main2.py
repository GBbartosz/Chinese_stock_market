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


def make_calculations(min_date, incst, b, cf, price):
    capitalization_df = calculations.capitalization_calc(min_date, incst, price)
    capitalization_change_df = calculations.capitalization_change_calc(min_date, incst, price)
    pe_ratio_df = calculations.pe_ratio_yearly_calc(min_date, incst, price)
    ps_ratio_df = calculations.ps_ratio_yearly_calc(min_date, incst, price)
    revenue_df = calculations.revenue_calc(min_date, incst)
    revenue_change_df = calculations.revenue_change_calc(min_date, incst)
    operating_income_df = calculations.operating_income_calc(min_date, incst)
    net_income_df = calculations.net_income_calc(min_date, incst)
    net_income_change_df = calculations.net_income_change_calc(min_date, incst)
    cf_operating_df = calculations.cash_flow_from_operating_activities_calc(min_date, cf)
    cf_financing_df = calculations.cash_flow_from_financing_activities_calc(min_date, cf)
    cf_investing_df = calculations.cash_flow_from_investing_calc(min_date, cf)
    pb_ratio_df = calculations.price_to_book_ratio_calc(min_date, incst, b, price)
    price_df = calculations.price_calc(min_date, price)
    prices_change_df = calculations.price_change_calc(min_date, price)
    total_debt = calculations.total_debt_calc(min_date, b)
    roe_df = calculations.roe_calc(min_date, incst, b)
    roa_df = calculations.roa_calc(min_date, incst, b)
    roc_df = calculations.roc_calc(min_date, incst, b)
    roce_df = calculations.roce_calc(min_date, incst, b)
    gross_margin = calculations.gross_margin_calc(min_date, incst)
    ebitda_margin = calculations.ebitda_margin_calc(min_date, incst)
    ebit_margin = calculations.ebit_margin_calc(min_date, incst)
    net_margin = calculations.net_margin_calc(min_date, incst)
    debt_to_equity = calculations.debt_to_equity_ratio_calc(min_date, b)
    total_debt_to_total_assets = calculations.total_debt_to_total_assets_ratio_calc(min_date, b)

    dfs = [capitalization_df, capitalization_change_df, pe_ratio_df, ps_ratio_df, revenue_df,
           revenue_change_df, operating_income_df, net_income_df, net_income_change_df, cf_operating_df,
           cf_financing_df, cf_investing_df, pb_ratio_df, price_df, prices_change_df,
           total_debt, roe_df, roa_df, roc_df, roce_df,
           gross_margin, ebitda_margin, ebit_margin, net_margin, debt_to_equity,
           total_debt_to_total_assets]
    return dfs


def get_company_df(dfs, sector, company, indicators_l):
    company_df = pd.concat(dfs)
    date_columns = list(company_df.columns)
    company_df['Company'] = company
    company_df['Sector'] = sector
    company_df['Indicator'] = indicators_l
    ordered_columns = ['Sector', 'Company', 'Indicator'] + date_columns
    company_df = company_df[ordered_columns]
    return company_df


def main():
    st = time.time()
    f.dataframe_display_options()
    directory_path = 'C:\\Users\\Bartek\\Desktop\\ALK praca magisterska\\China_stock_data_test'
    directory_path = r'C:\Users\Bartek\Desktop\ALK MGR 2022.10\China_stock_data'
    # directory_path = 'C:\\Users\\Bartek\\Desktop\\ALK praca magisterska\\China_stock_data\\Nowy folder'
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
    res = f.create_dictionaries_of_sectors_with_dicts(sectors_l, late_first_sector_all, late_first_sector_doc,
                                                      late_first_sector_price)
    late_first_sector_all, late_first_sector_doc, late_first_sector_price = res

    price_docs_date_not_compatible_sector_dict = f.create_companies_in_sector_dict(sectors_l)
    doc_dates_not_equal_dict = f.create_companies_in_sector_dict(sectors_l)
    late_first_sector_price_companies = f.create_companies_in_sector_dict(sectors_l)
    verified_companies = {}
    first_date_by_company_dic = {}
    first_date_by_sector_collection_dic = {}

    for company in companys_dictionary.keys():
        verified_data_result = verify_data(company, companys_dictionary, companys_sector_dic, directory_path,
                                           first_date_by_company_dic, first_date_by_sector_collection_dic, min_date,
                                           number_of_periods, late_first_sector_all, late_first_sector_doc,
                                           late_first_sector_price, price_docs_date_not_compatible_sector_dict,
                                           doc_dates_not_equal_dict, late_first_sector_price_companies)
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

    dicts_l = [sector_capitalization_dict, sector_capitalization_change_dict, sector_pe_ratio_dict,
               sector_ps_ratio_dict, sector_revenue_dict, sector_revenue_change_dict, sector_net_income_dict,
               sector_net_income_change_dict, sector_pb_ratio, sector_price, sector_price_change, sector_cf_operating,
               sector_cf_financing, sector_cf_investing, sector_operating_income]
    res_sectors_dicts = f.create_dictionaries_of_sectors_with_lists(sectors_l, dicts_l)
    sector_capitalization_dict, sector_capitalization_change_dict, sector_pe_ratio_dict, sector_ps_ratio_dict, sector_revenue_dict, sector_revenue_change_dict, sector_net_income_dict, sector_net_income_change_dict, sector_pb_ratio, sector_price, sector_price_change, sector_cf_operating, sector_cf_financing, sector_cf_investing, sector_operating_income = res_sectors_dicts

    companies_in_sector_dict = f.create_companies_in_sector_dict(sectors_l)
    number_of_companies_in_sector = {}
    number_of_companies_in_sector = number_of_companies_in_sector.fromkeys(sectors_l, 0)

    print('number of companies at beginning: ' + str(len(list(companys_dictionary.keys()))))
    print('number of verified companies: ' + str(len(list(verified_companies.keys()))))

    main_df = None
    indicators_l = ['Capitalization', 'Capitalization change', 'P/E', 'P/S', 'Revenue',
                    'Revenue change', 'Operating income', 'Net income', 'Net income change', 'Operating CF',
                    'Financing CF', 'Investing CF', 'Price/book', 'Price', 'Price change',
                    'Total debt', 'ROE', 'ROA', 'ROC', 'ROCE',
                    'Gross margin', 'EBITDA margin', 'EBIT margin', 'Net income margin', 'Debt to equity ratio',
                    'Total debt to total assets ratio']
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

        dfs = make_calculations(min_date, incst, b, cf, price)
        company_df = get_company_df(dfs, sector, company, indicators_l)

        if main_df is None:
            main_df = company_df
            continue

        main_df = pd.concat([main_df, company_df])

    main_df_f_path = r'C:\Users\Bartek\Desktop\ALK MGR 2022.10\wskazniki.xlsx'
    main_df.to_excel(main_df_f_path)

    # full price
    final_full_price_df = None
    for s in close_price_in_sector_dict.keys():
        for c in close_price_in_sector_dict[s].keys():
            if final_full_price_df is None:
                final_full_price_df_columns = list(close_price_in_sector_dict[s][c].iloc[:, 0])
                final_full_price_df = close_price_in_sector_dict[s][c].iloc[:, 1].to_frame()
                final_full_price_df = final_full_price_df.transpose()
                final_full_price_df.columns = final_full_price_df_columns
                final_full_price_df['Sector'] = s
                final_full_price_df['Company'] = c
            else:
                tmp_df_columns = list(close_price_in_sector_dict[s][c].iloc[:, 0])
                tmp_df = close_price_in_sector_dict[s][c].iloc[:, 1].to_frame()
                tmp_df = tmp_df.transpose()
                tmp_df.columns = tmp_df_columns
                tmp_df['Sector'] = s
                tmp_df['Company'] = c
                tmp_frames = [final_full_price_df, tmp_df]
                final_full_price_df = pd.concat(tmp_frames)
                if tmp_df_columns != final_full_price_df_columns:
                    print('Different columns for: {}'.format(c))
    final_full_price_df = pd.concat([final_full_price_df.iloc[:, -2:],final_full_price_df.iloc[:, :-2]], axis=1)
    final_full_price_df_path = r'C:\Users\Bartek\Desktop\ALK MGR 2022.10\price.xlsx'
    final_full_price_df.to_excel(final_full_price_df_path)

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


if __name__ == '__main__':
    main()
