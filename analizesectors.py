import calculations
import functions as f

def analize_sectors(min_date, sector, company, incst, b, cf, price, *args):
    sector_capitalization_dict, sector_pe_ratio_dict, sector_ps_ratio_dict, sector_revenue_dict, sector_revenue_change_dict, sector_net_income_dict, sector_net_income_change_dict, sector_pb_ratio, sector_price_change, companies_in_sector_dict, number_of_companies_in_sector = args

    # company_capitalization_dict = calculations.get_company_capitalization_by_date_dict(min_date, incst, price)
    company_capitalization_dict = calculations.capitalization_calc(min_date, incst, price)
    sector_capitalization_dict = f.add_new_dict_to_sector_dict_list(sector_capitalization_dict, company_capitalization_dict, sector)

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

    company_net_income_change_dict = calculations.net_income_change_calc(min_date, incst)
    sector_net_income_change_dict = f.add_new_dict_to_sector_dict_list(sector_net_income_change_dict, company_net_income_change_dict, sector)

    company_pb_ratio = calculations.price_to_book_ratio_calc(min_date, incst, b, price)
    sector_pb_ratio = f.add_new_dict_to_sector_dict_list(sector_pb_ratio, company_pb_ratio, sector)

    company_price_change = calculations.price_change_calc(min_date, price)
    sector_price_change = f.add_new_dict_to_sector_dict_list(sector_price_change, company_price_change, sector)

    companies_in_sector_dict[sector] = companies_in_sector_dict[sector] + [company]
    number_of_companies_in_sector[sector] += 1

    res_sector_dicts = [sector_capitalization_dict, sector_pe_ratio_dict, sector_ps_ratio_dict, sector_revenue_dict, sector_revenue_change_dict, sector_net_income_dict, sector_net_income_change_dict, sector_pb_ratio, sector_price_change, companies_in_sector_dict, number_of_companies_in_sector]
    return res_sector_dicts


