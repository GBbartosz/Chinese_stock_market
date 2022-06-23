import functions as f





#def get_company_capitalization_by_date_dict(min_date, incst, price):
#    company_capitalization_dict = {}
#    dates_l = f.get_following_dates_list(min_date)
#    for date in dates_l:
#        year = date[0]
#        quarter = date[1]
#        date = str(year) + '-' + str(quarter)
#        capitalization = incst.WeightedAverageDilutedSharesOut.period(year, quarter) * price.close.period(year, quarter)
#        company_capitalization_dict[date] = capitalization
#    return company_capitalization_dict






@f.fulfill_dict
def capitalization_calc(dates_obj, incst, price):
    year, quarter, date, min_date, attempt = dates_obj
    capitalization = incst.WeightedAverageDilutedSharesOut.period(year, quarter) * price.close.period(year, quarter)
    return capitalization


@f.fulfill_dict
def pe_ratio_calc(dates_obj, incst, price):
    year, quarter, date, min_date, attempt = dates_obj
    if attempt >= 3:
        prev_year1, prev_quarter1 = f.get_prev_year_quarter(year, quarter, 1)
        prev_year2, prev_quarter2 = f.get_prev_year_quarter(year, quarter, 2)
        prev_year3, prev_quarter3 = f.get_prev_year_quarter(year, quarter, 3)
        last_year_net_income_company = incst.NetIncometoCompany.period(year, quarter) + incst.NetIncometoCompany.period(prev_year1, prev_quarter1) + incst.NetIncometoCompany.period(prev_year2, prev_quarter2) + incst.NetIncometoCompany.period(prev_year3, prev_quarter3)
        pe_ratio = incst.WeightedAverageDilutedSharesOut.period(year, quarter) * price.close.period(year, quarter) / last_year_net_income_company
        return pe_ratio


@f.fulfill_dict
def ps_ratio_calc(dates_obj, incst, price):
    year, quarter, date, min_date, attempt = dates_obj
    if attempt >= 3:
        prev_year1, prev_quarter1 = f.get_prev_year_quarter(year, quarter, 1)
        prev_year2, prev_quarter2 = f.get_prev_year_quarter(year, quarter, 2)
        prev_year3, prev_quarter3 = f.get_prev_year_quarter(year, quarter, 3)
        last_year_revenue = incst.Revenue.period(year, quarter) + incst.Revenue.period(prev_year1, prev_quarter1) + incst.Revenue.period(prev_year2, prev_quarter2) + incst.Revenue.period(prev_year3, prev_quarter3)
        ps_ratio = incst.WeightedAverageDilutedSharesOut.period(year, quarter) * price.close.period(year, quarter) / last_year_revenue
        return ps_ratio


@f.fulfill_dict
def revenue_calc(dates_obj, incst):
    year, quarter, date, min_date, attempt = dates_obj
    revenue = incst.Revenue.period(year, quarter)
    return revenue


@f.fulfill_dict
def revenue_change_calc(dates_obj, incst):
    year, quarter, date, min_date, attempt = dates_obj
    if attempt >= 1:
        prev_year, prev_quarter = f.get_prev_year_quarter(year, quarter, 1)
        revenue_change = incst.Revenue.period(year, quarter) / incst.Revenue.period(prev_year, prev_quarter) - 1
        return revenue_change


@f.fulfill_dict
def net_income_calc(dates_obj, incst):
    year, quarter, date, min_date, attempt = dates_obj
    net_income = incst.NetIncometoCompany.period(year, quarter)
    return net_income


@f.fulfill_dict
def net_income_change_calc(dates_obj, incst):
    year, quarter, date, min_date, attempt = dates_obj
    if attempt >= 1:
        prev_year, prev_quarter = f.get_prev_year_quarter(year, quarter, 1)
        net_income_change = incst.NetIncometoCompany.period(year, quarter) / incst.NetIncometoCompany.period(prev_year, prev_quarter) - 1
        return net_income_change
    
    