import os
import numpy as np
import pandas as pd
import functions as f
import seaborn as sn
import matplotlib.pyplot as plt
import statistics
import matplotlib.ticker as mtick
import verifydata


def sector_color(sector):
    color_dict = {
    'Communication Services': 'magenta',
    'Industrials': 'grey',
    'Utilities': 'black',
    'Consumer Discretionary': 'darkgreen',
    'Information Technology': 'aqua',
    'Materials': 'indigo',
    'Real Estate': 'saddlebrown',
    'Healthcare': 'blue',
    'Financials': 'gold',
    'Energy': 'orange',
    'Consumer Staples': 'springgreen'
    }
    color = color_dict[sector]
    return color


def companies_by_sector(df, sectors_l):
    sec_comp_dict = {}
    sec_comp_df = df[['Sector', 'Company']]
    for sector in sectors_l:
        companies_in_sector = sec_comp_df[(sec_comp_df['Sector'] == sector)]['Company'].unique()
        sec_comp_dict[sector] = companies_in_sector
    return sec_comp_dict


def prepare_grouped_price_df(grouped_df):
    mean_df = grouped_df.mean()
    mean_df.reset_index(inplace=True)
    # sec_price_df = mean_df[mean_df['Indicator'] == 'Price']
    sec_price_df = mean_df
    sec_price_df.reset_index(inplace=True)
    sec_price_df = sec_price_df.set_index('Sector')
    sec_price_df.drop(['index'], axis=1, inplace=True)
    return sec_price_df

def correlation_for_sectors(grouped_df, sectors_l, indicators_l):
    mean_df = grouped_df.mean()
    mean_df.reset_index(inplace=True)
    sectors_correls = {}
    for sector in sectors_l:
        sec_df = mean_df[mean_df['Sector'] == sector]
        sec_avg_price = pd.Series(sec_df[(sec_df['Sector'] == sector) & (sec_df['Indicator'] == 'Price')].values.tolist()[0][2:])
        x = sec_avg_price
        correls_l = []
        for ind in indicators_l:
            y = pd.Series(sec_df[sec_df['Indicator'] == ind].values.tolist()[0][2:])
            corr = x.corr(y)
            correls_l.append(corr)
        sectors_correls[sector] = correls_l
    correls_df = pd.DataFrame(sectors_correls)
    correls_df.index = indicators_l
    sn.heatmap(correls_df, xticklabels=True, yticklabels=True, annot=True)
    plt.show()


def correlation_between_sectors(grouped_df, sectors_l):
    sec_price_df = prepare_grouped_price_df(grouped_df)
    sec_price_df = sec_price_df.transpose()
    corr_matrix = sec_price_df.corr()
    sn.heatmap(corr_matrix, annot=True)
    plt.show()


def indicators_distribution_chart_company_lvl(df, indicators_l, companies_l, sectors_l):
    x_axis = list(df.columns)[3:]
    x_parameters = list(range(1, 13))
    for indicator in indicators_l:
        x = []
        y = []
        if indicator == 'Revenue':
            indicator_df = df[df['Indicator'] == indicator]
            for company in companies_l:
                company_s = indicator_df[indicator_df['Company'] == company].squeeze()
                #company_s = company_s.replace(np.NaN, 0)
                company_s = company_s.to_list()[3:]
                print(len(company_s))
                print(company_s)

                x.append(x_parameters)
                y.append(company_s)

            plt.scatter(x, y)
            #plt.xticks(x_axis)
            plt.show()


def get_beta_of_stock_to_sector(df, sectors_l, companies_l, sec_comp_dict):

    # funkcja do sprawdzenia
    # wpływ większej ceny na średnią

    price_df = df[df['Indicator'] == 'Price']
    price_df.drop('Indicator', axis=1, inplace=True)
    sector_price_df = price_df.drop('Company', axis=1)
    sector_price_df = sector_price_df.groupby('Sector')
    sector_price_df = sector_price_df.mean()
    sector_price_df.reset_index(inplace=True)

    companies_price_df = price_df.drop('Sector', axis=1)
    beta_dict = {}
    for sector in sectors_l:
        sec_avg_price = sector_price_df[(sector_price_df['Sector'] == sector)].values.tolist()[0][1:]
        companies = sec_comp_dict[sector]
        for company in companies:
            print(company)
            company_price_l = companies_price_df[companies_price_df['Company'] == company].values.tolist()[0][1:]

            variance = statistics.pvariance(sec_avg_price)
            print(variance)
            covariance_data = [company_price_l, sec_avg_price]
            covariance = np.cov(covariance_data)[0][1]
            print(covariance)
            beta = covariance / variance
            beta_dict[company] = beta

    print(beta_dict)


def sectors_price_compared_to_start_date(grouped_df, sectors_l):
    sec_price_df = prepare_grouped_price_df(grouped_df)
    print(sec_price_df)
    dates_l = sec_price_df.columns
    res_l = []
    for sector in sectors_l:
        sec_price_l = pd.Series(sec_price_df.loc[sector]).values.tolist()
        start_v = sec_price_l[0]
        next_values_l = sec_price_l[1:]
        tmp_l = [1]
        for v in next_values_l:
            n = v / start_v
            tmp_l.append(n)
        res_l.append(tmp_l)
    df = pd.DataFrame(data=res_l, index=sectors_l, columns=dates_l)
    print(df)
    df = df.transpose()
    sec_color_dict = {}
    for sector in sectors_l:
        color = sector_color(sector)
        sec_color_dict[sector] = color

    lines = df.plot.line(color=sec_color_dict)
    plt.grid(visible=True)
    lines.yaxis.set_major_formatter(mtick.PercentFormatter(1))
    plt.show()


def market_cap_influence_on_price_volatility():
    pass


def market_cap_of_companies_in_sectors():
    pass


def company_loop_indicator_level_to_mean(df, companies_l, indicators_l):
    df = df.drop('Sector', axis=1)
    headers_l = df.columns
    companies_res_l = []
    for company in companies_l:
        company_df = df[df['Company'] == company]
        company_l = []
        for ind in indicators_l:
            indicator_l = company_df[company_df['Indicator'] == ind].values.tolist()[0][2:]
            n = 0
            nans_pos = []
            for i in indicator_l:
                if np.isnan(i):
                    nans_pos.append(n)
                n += 1
            indicator_l = np.array(indicator_l)
            clear_indicator_l = indicator_l[np.logical_not(np.isnan(indicator_l))]
            indicator_l = indicator_l.tolist()
            clear_indicator_l = clear_indicator_l.tolist()
            if len(clear_indicator_l) > 0:
                res_l = indicator_level_to_mean(clear_indicator_l)
                n2 = 0
                c = 0
                for i in indicator_l:
                    if n2 not in nans_pos:
                        indicator_l[n2] = res_l[c]
                        c += 1
                    else:
                        indicator_l[n2] = np.NaN
                    n2 += 1
            else:
                indicator_l = 12 * [np.nan]
            new_ind_l = [company, ind] + indicator_l
            companies_res_l.append(new_ind_l)
    df = pd.DataFrame(companies_res_l)
    df.columns = headers_l
    path_indicator_to_mean = r'C:\Users\Bartek\Desktop\ALK MGR 2022.10\wskaznik_do_sredniej.xlsx'
    df.to_excel(path_indicator_to_mean)


def indicator_level_to_mean(indicator_l):
    ind_mean = statistics.mean(indicator_l)
    res_l = []
    for ind in indicator_l:
        res = ind / ind_mean
        res_l.append(res)
    return res_l


def create_full_price_df(companies_l):
    companys_sector_dic = f.create_companys_sector_dictionary()
    all_price_df = None
    for company in companies_l:
        sector, yf_ticker = companys_sector_dic[company]
        company_price_df = verifydata.create_price_df(yf_ticker)
        company_price_df = company_price_df.transpose()
        company_price_df.columns = company_price_df.iloc[0, :]
        company_price_df = company_price_df[1:]
        company_price_df = company_price_df.loc[:, '2019-01-02':]
        if all_price_df is None:
            company_price_df['Company'] = company
            all_price_df = company_price_df
        else:
            company_price_df['Company'] = company
            all_price_df = pd.concat([all_price_df, company_price_df])
    file_path = r'C:\Users\Bartek\Desktop\ALK MGR 2022.10\all_type_prices.xlsx'
    all_price_df.to_excel(file_path)


def covid_influence_on_volatility(all_price_df, covid_df):
    print(all_price_df.head())
    print(covid_df.head())
    print(all_price_df.columns[0])
    print(covid_df.columns[0])


    # incr = (all_price_df.loc['Close', t] - all_price_df.loc['Close', t-1]) / all_price_df.loc['Close', t-1]
    # inedv = (all_price_df.loc['Close', t] - all_price_df.loc['Open', t]) / all_price_df.loc['Open', t]
    # intdv = (all_price_df.loc['Open', t] - all_price_df.loc['Close', t-1]) / all_price_df.loc['Close', t-1]
    
    # Open
    # High
    # Low
    # Close
    # Adj
    # Close
    # Volume


def abnormal_returns_of_sectors(price_df, sectors_l):
    columns_names = price_df.columns
    columns = list(range(len(columns_names)))
    change_avg_l = []
    change_df = price_df.iloc[:, 1:3]

    for t in columns[4:]:
        curr_price = price_df.iloc[:, t]
        prev_price = price_df.iloc[:, t-1]
        change = curr_price / prev_price - 1
        change_df[t] = change
        change_avg = statistics.mean(change)
        change_avg_l.append(change_avg)
    grouped_price_df = change_df.groupby('Sector').mean()
    abnormal_dict = {}
    for sector in sectors_l:
        sector_avg_l = grouped_price_df.loc[sector, :].values.tolist()
        abnormal = np.array(sector_avg_l) - np.array(change_avg_l)
        abnormal_dict[sector] = abnormal
    abnormal_df = pd.DataFrame(abnormal_dict, index=columns_names[4:])
    #file_path = r'C:\Users\Bartek\Desktop\ALK MGR 2022.10\abnormal_returns.xlsx'
    #abnormal_df.to_excel(file_path)
    sec_color_dict = {}
    for sector in sectors_l:
        color = sector_color(sector)
        sec_color_dict[sector] = color
    lines = abnormal_df.plot.line(color=sec_color_dict)
    plt.grid(visible=True)
    lines.yaxis.set_major_formatter(mtick.PercentFormatter(1))
    plt.show()


def analyse():
    f.dataframe_display_options()

    file_path = r'C:\Users\Bartek\Desktop\ALK MGR 2022.10\wskazniki_opracowanie.xlsx'
    df = pd.read_excel(file_path)

    file_path = r'C:\Users\Bartek\Desktop\ALK MGR 2022.10\price_1.xlsx'
    price_df = pd.read_excel(file_path)

    file_path = r'C:\Users\Bartek\Desktop\ALK MGR 2022.10\WHO-COVID-19-global-data.csv'
    covid_df = pd.read_csv(file_path)
    covid_df = covid_df[covid_df['Country'] == 'China']

    # create_full_price_df(companies_l)
    file_path = r'C:\Users\Bartek\Desktop\ALK MGR 2022.10\all_type_prices.xlsx'
    all_price_df = pd.read_excel(file_path)
    all_price_df.index = all_price_df.iloc[:, 0]
    all_price_df = all_price_df.iloc[:, 1:]

    sectors_l = list(df['Sector'].unique())
    companies_l = list(df['Company'].unique())
    indicators_l = list(df['Indicator'].unique())
    sec_comp_dict = companies_by_sector(df, sectors_l)

    # grouped_df = df.groupby(['Sector', 'Indicator'])
    # price_df_grouped = price_df.groupby('Sector')
    # correlation_for_sectors(grouped_df, sectors_l, indicators_l)
    # correlation_between_sectors(price_df_grouped, sectors_l)
    # indicators_distribution_chart_company_lvl(df, indicators_l, companies_l, sectors_l)
    # get_beta_of_stock_to_sector(df, sectors_l, companies_l, sec_comp_dict)
    # sectors_price_compared_to_start_date(price_df_grouped, sectors_l)
    # company_loop_indicator_level_to_mean(df, companies_l, indicators_l)
    # covid_influence_on_volatility(all_price_df, covid_df)                                     # to do
    abnormal_returns_of_sectors(price_df, sectors_l)                                            # summarize to months

if __name__ == '__main__':
    analyse()
