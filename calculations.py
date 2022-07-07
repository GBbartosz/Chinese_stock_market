import datetime

import functions as f
import math
import numpy as np
import pandas as pd

def fulfill_dict(equation):
    def inner(min_date, *args):
        tmp_dict = {}
        dates_l = f.get_following_dates_list(min_date)
        attempt = 0
        for date in dates_l:
            year = date[0]
            quarter = date[1]
            date = str(year) + '-' + str(quarter)
            dates_obj = [year, quarter, date, min_date, attempt]
            res = equation(dates_obj, *args)
            if res is None:
                if equation.__name__ == 'pe_ratio_yearly_calc' and attempt >= 3 or \
                        equation.__name__ == 'ps_ratio_yearly_calc' and attempt >= 3 or \
                        equation.__name__ == 'revenue_change_calc' and attempt >= 1 or \
                        equation.__name__ == 'net_income_change_calc' and attempt >= 1:
                    print(equation.__name__)
                    print('is none')
            elif math.isnan(res):
                print(equation.__name__)
                print('isnan')
            if res is not None:
                tmp_dict[date] = res
            attempt += 1
        return tmp_dict
    return inner


def handling_empty_shares_out(incst, year, quarter):
    shares_out = incst.WeightedAverageDilutedSharesOut.period(year, quarter)
    if np.isnan(shares_out):
        shares_out = incst.NetIncometoStockholders.period(year, quarter) / incst.DilutedEPSContOps.period(year, quarter)
        if np.isnan(shares_out):
            try:
                prev_year1, prev_quarter1 = f.get_prev_year_quarter(year, quarter, 1)
                shares_out = incst.WeightedAverageDilutedSharesOut.period(prev_year1, prev_quarter1)
                if np.isnan(shares_out):
                    next_year1, next_quarter1 = f.get_prev_year_quarter(year, quarter, -1)
                    shares_out = incst.WeightedAverageDilutedSharesOut.period(next_year1, next_quarter1)
            except KeyError:
                next_year1, next_quarter1 = f.get_prev_year_quarter(year, quarter, -1)
                shares_out = incst.WeightedAverageDilutedSharesOut.period(next_year1, next_quarter1)

    return shares_out


def if_nan_find_prev_or_next(obj, year, quarter):
    try:
        prev_year1, prev_quarter1 = f.get_prev_year_quarter(year, quarter, 1)
        res = obj(prev_year1, prev_quarter1)
    except KeyError:
        next_year1, next_quarter1 = f.get_prev_year_quarter(year, quarter, -1)
        res = obj(next_year1, next_quarter1)
    return res


@fulfill_dict
def capitalization_calc(dates_obj, incst, price):
    year, quarter, date, min_date, attempt = dates_obj
    shares_out = handling_empty_shares_out(incst, year, quarter)
    capitalization = shares_out * price.close.period(year, quarter)
    return capitalization


@fulfill_dict
def capitalization_change_calc(dates_obj, incst, price):
    year, quarter, date, min_date, attempt = dates_obj
    if attempt >= 1:
        prev_year, prev_quarter = f.get_prev_year_quarter(year, quarter, 1)
        current_shares_out = handling_empty_shares_out(incst, year, quarter)
        current_capitalization = current_shares_out * price.close.period(year, quarter)
        prev_shares_out = handling_empty_shares_out(incst, prev_year, prev_quarter)
        prev_capitalization = prev_shares_out * price.close.period(prev_year, prev_quarter)
        capitalization_change = current_capitalization / prev_capitalization - 1
        return capitalization_change


@fulfill_dict
def pe_ratio_yearly_calc(dates_obj, incst, price):
    year, quarter, date, min_date, attempt = dates_obj
    if attempt >= 3:
        prev_year1, prev_quarter1 = f.get_prev_year_quarter(year, quarter, 1)
        prev_year2, prev_quarter2 = f.get_prev_year_quarter(year, quarter, 2)
        prev_year3, prev_quarter3 = f.get_prev_year_quarter(year, quarter, 3)
        current_year_net_income_company = incst.NetIncometoCompany.period(year, quarter) + incst.NetIncometoCompany.period(prev_year1, prev_quarter1) + incst.NetIncometoCompany.period(prev_year2, prev_quarter2) + incst.NetIncometoCompany.period(prev_year3, prev_quarter3)
        shares_out = handling_empty_shares_out(incst, year, quarter)
        pe_ratio = shares_out * price.close.period(year, quarter) / current_year_net_income_company
        return pe_ratio


@fulfill_dict
def ps_ratio_yearly_calc(dates_obj, incst, price):
    year, quarter, date, min_date, attempt = dates_obj
    if attempt >= 3:
        prev_year1, prev_quarter1 = f.get_prev_year_quarter(year, quarter, 1)
        prev_year2, prev_quarter2 = f.get_prev_year_quarter(year, quarter, 2)
        prev_year3, prev_quarter3 = f.get_prev_year_quarter(year, quarter, 3)
        current_year_revenue = incst.Revenue.period(year, quarter) + incst.Revenue.period(prev_year1, prev_quarter1) + incst.Revenue.period(prev_year2, prev_quarter2) + incst.Revenue.period(prev_year3, prev_quarter3)
        shares_out = handling_empty_shares_out(incst, year, quarter)
        ps_ratio = shares_out * price.close.period(year, quarter) / current_year_revenue
        return ps_ratio


@fulfill_dict
def revenue_calc(dates_obj, incst):
    year, quarter, date, min_date, attempt = dates_obj
    revenue = incst.Revenue.period(year, quarter)
    return revenue


@fulfill_dict
def revenue_change_calc(dates_obj, incst):
    year, quarter, date, min_date, attempt = dates_obj
    if attempt >= 1:
        try:
            prev_year, prev_quarter = f.get_prev_year_quarter(year, quarter, 1)
            revenue_change = incst.Revenue.period(year, quarter) / incst.Revenue.period(prev_year, prev_quarter) - 1
        except ZeroDivisionError:
            revenue_change = 1
        return revenue_change


@fulfill_dict
def net_income_calc(dates_obj, incst):
    year, quarter, date, min_date, attempt = dates_obj
    net_income = incst.NetIncometoCompany.period(year, quarter)
    return net_income


@fulfill_dict
def net_income_change_calc(dates_obj, incst):
    year, quarter, date, min_date, attempt = dates_obj
    if attempt >= 1:
        prev_year, prev_quarter = f.get_prev_year_quarter(year, quarter, 1)
        net_income_change = incst.NetIncometoCompany.period(year, quarter) / incst.NetIncometoCompany.period(prev_year, prev_quarter) - 1
        return net_income_change


@fulfill_dict
def price_to_book_ratio_calc(dates_obj, incst, b, price):
    year, quarter, date, min_date, attempt = dates_obj
    shares_out = handling_empty_shares_out(incst, year, quarter)
    total_equity = b.TotalEquity.period(year, quarter)
    if math.isnan(total_equity):
        total_equity = if_nan_find_prev_or_next(b.TotalEquity.period, year, quarter)
    pb_ratio = price.close.period(year, quarter) * shares_out / total_equity
    return pb_ratio


@fulfill_dict
def price_calc(dates_obj, price):
    year, quarter, date, min_date, attempt = dates_obj
    price = price.close.period(year, quarter)
    return price


@fulfill_dict
def price_change_calc(dates_obj, price):
    year, quarter, date, min_date, attempt = dates_obj
    prev_year, prev_quarter = f.get_prev_year_quarter(year, quarter, 1)
    if attempt >= 1:
        price_change = price.close.period(year, quarter) / price.close.period(prev_year, prev_quarter) - 1
        return price_change


def create_close_price_volatility_for_comp_dict(close_price_in_sector_dict):
    def average(my_l):
        my_average = sum(my_l) / len(my_l)
        return my_average

    outer_standard_deviation_dict = {}
    for sec in close_price_in_sector_dict.keys():
        outer_standard_deviation_dict[sec] = {}
        close_price_sec_dict = close_price_in_sector_dict[sec]
        for comp in close_price_sec_dict.keys():
            df = close_price_sec_dict[comp]
            border_date = datetime.date(year=2020, month=1, day=1)
            df.loc[:, 'Date'] = df.loc[:, 'Date'].apply(f.convert_to_date)
            df_bef = df[df['Date'] < border_date]
            df_aft = df[df['Date'] >= border_date]
            dfs = df_bef, df_aft
            standard_deviations = []
            for df in dfs:
                vls = list(df['Close'])
                comp_avg = average(vls)
                comp_deviations_l = []
                for cl_price in vls:
                    this_deviation = cl_price - comp_avg
                    comp_deviations_l.append(this_deviation)
                comp_deviations = np.array(comp_deviations_l)
                comp_squared_deviations = comp_deviations ** 2
                comp_squared_deviations_sum = np.sum(comp_squared_deviations)
                variance = comp_squared_deviations_sum / len(vls)
                standard_deviation = np.sqrt(variance)
                standard_deviations.append(standard_deviation)
            outer_standard_deviation_dict[sec][comp] = standard_deviations
    return outer_standard_deviation_dict


def create_close_price_volatility_for_sector_dict(outer_standard_deviation_dict):
    sectors_standard_deviation_dict = {}
    for sec in outer_standard_deviation_dict.keys():
        sec_volatility_dict = outer_standard_deviation_dict[sec]
        total_sec_std_dev_aft = 0
        total_sec_std_dev_bef = 0
        number_of_companies_in_sector = len(sec_volatility_dict.keys())
        for comp in sec_volatility_dict.keys():
            bef_std_dev, aft_std_dev = sec_volatility_dict[comp]
            total_sec_std_dev_bef += bef_std_dev
            total_sec_std_dev_aft += aft_std_dev
        total_sec_std_dev_bef = total_sec_std_dev_bef / number_of_companies_in_sector
        total_sec_std_dev_aft = total_sec_std_dev_aft / number_of_companies_in_sector
        sectors_standard_deviation_dict[sec] = [total_sec_std_dev_bef, total_sec_std_dev_aft]
    return sectors_standard_deviation_dict


def maximum_price_spread(close_price_in_sector_dict):
    sectors_avg_price_dict = avg_price_of_sector(close_price_in_sector_dict)
    sectors_l = (sectors_avg_price_dict.keys())
    spread_dict = {}
    for sector in sectors_l:
        y = sectors_avg_price_dict[sector][1]
        y = list(y)
        x_dates = sectors_avg_price_dict[sector][0]
        min_y = min(y)
        min_index = y.index(min_y)
        min_date = x_dates[min_index]
        max_y = max(y)
        max_index = y.index(max_y)
        max_date = x_dates[max_index]
        spread = max_y - min_y
        spread_adjst = spread / max_y
        spread_dict[sector] = [min_date, min_y, max_date, max_y, spread, spread_adjst]
    index_l = ['min_date', 'min_y', 'max_date', 'max_y', 'spread', 'spread_adjst']
    df = pd.DataFrame(spread_dict)
    df.index = index_l
    path = r'C:\Users\Bartek\Desktop\ALK praca magisterska\python_res_data\sectors_spread.xlsx'
    df.to_excel(path)


def avg_price_of_sector(close_price_in_sector_dict):
    sectors_avg_price_dict = {}
    sectors_l = list(close_price_in_sector_dict.keys())
    for sector in sectors_l:
        comps_dict = close_price_in_sector_dict[sector]
        comps_l = list(comps_dict.keys())
        number_of_companies = len(comps_l)
        y = None
        for comp in comps_l:
            df = comps_dict[comp]
            tmp_y = np.array(df['Close'])
            if y is None:
                y = tmp_y
            else:
                y += tmp_y
        y = y / number_of_companies
        x_dates = np.array(df['Date'])
        sectors_avg_price_dict[sector] = [x_dates, y]
    return sectors_avg_price_dict


@fulfill_dict
def cash_flow_from_operating_activities_calc(dates_obj, cf):
    year, quarter, date, min_date, attempt = dates_obj
    cf_from_operating_activities = cf.CashfromOperations.period(year, quarter)
    return cf_from_operating_activities


@fulfill_dict
def cash_flow_from_financing_activities_calc(dates_obj, cf):
    year, quarter, date, min_date, attempt = dates_obj
    cf_from_financing_activities = cf.CashfromInvesting.period(year, quarter)
    return cf_from_financing_activities


@fulfill_dict
def cash_flow_from_investing_calc(dates_obj, cf):
    year, quarter, date, min_date, attempt = dates_obj
    cf_from_investing = cf.CashfromInvesting.period(year, quarter)
    return cf_from_investing


@fulfill_dict
def operating_income_calc(dates_obj, incst):
    year, quarter, date, min_date, attempt = dates_obj
    operating_income = incst.OperatingIncome.period(year, quarter)
    return operating_income
