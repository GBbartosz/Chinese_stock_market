import functions as f
import math
import numpy as np


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
        prev_year, prev_quarter = f.get_prev_year_quarter(year, quarter, 1)
        revenue_change = incst.Revenue.period(year, quarter) / incst.Revenue.period(prev_year, prev_quarter) - 1
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
def price_change_calc(dates_obj, price):
    year, quarter, date, min_date, attempt = dates_obj
    prev_year, prev_quarter = f.get_prev_year_quarter(year, quarter, 1)
    if attempt >= 1:
        price_change = price.close.period(year, quarter) / price.close.period(prev_year, prev_quarter) - 1
        return price_change


