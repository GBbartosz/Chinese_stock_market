import os
import numpy as np
import pandas as pd
import functions as f
import seaborn as sn
import matplotlib.pyplot as plt
import statistics


def companies_by_sector(df, sectors_l):
    sec_comp_dict = {}
    sec_comp_df = df[['Sector', 'Company']]
    for sector in sectors_l:
        companies_in_sector = sec_comp_df[(sec_comp_df['Sector'] == sector)]['Company'].unique()
        sec_comp_dict[sector] = companies_in_sector
    return sec_comp_dict


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
    mean_df = grouped_df.mean()
    mean_df.reset_index(inplace=True)
    sec_price_df = mean_df[mean_df['Indicator'] == 'Price']
    sec_price_df.reset_index(inplace=True)
    sec_price_df = sec_price_df.set_index('Sector')
    sec_price_df.drop(['Indicator', 'index'], axis=1, inplace=True)
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






def analyse():
    f.dataframe_display_options()
    file_path = r'C:\Users\Bartek\Desktop\ALK MGR 2022.10\wskazniki_opracowanie.xlsx'
    df = pd.read_excel(file_path)

    sectors_l = list(df['Sector'].unique())
    companies_l = list(df['Company'].unique())
    indicators_l = list(df['Indicator'].unique())
    sec_comp_dict = companies_by_sector(df, sectors_l)

    grouped_df = df.groupby(['Sector', 'Indicator'])
    # correlation_for_sectors(grouped_df, sectors_l, indicators_l)
    # correlation_between_sectors(grouped_df, sectors_l)
    # indicators_distribution_chart_company_lvl(df, indicators_l, companies_l, sectors_l)
    get_beta_of_stock_to_sector(df, sectors_l, companies_l, sec_comp_dict)



if __name__ == '__main__':
    analyse()
