import functions as f


def get_number_of_companies_in_sector_by_date():
    companies_in_sector_dict = {}
    for sector in sector_companys_dic.keys():
        companies_in_sector = len(sector_companys_dic[sector])
        companies_in_sector_dict[sector] = companies_in_sector
    return


def get_company_capitalization_by_date_dict(min_date, incst, price):
    company_capitalization_dict = {}
    dates_l = f.get_following_dates_list(min_date)
    for date in dates_l:
        year = date[0]
        quarter = date[1]
        date = str(year) + '-' + str(quarter)
        capitalization = incst.WeightedAverageDilutedSharesOut.period(year, quarter) * price.close.period(year, quarter)
        company_capitalization_dict[date] = capitalization
    return company_capitalization_dict
