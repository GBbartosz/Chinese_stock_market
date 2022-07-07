import matplotlib.pyplot as plt
from collections import OrderedDict, Counter
import numpy as np
import time

import pandas as pd

import functions as f
import os


def sort_inner_dictionary(my_dict):
    my_dict = OrderedDict(sorted(my_dict.items()))
    return my_dict


def add_zero_if_lack_of_date(my_dict_in, my_x_labels):
    # in case if sector doesnt have companies
    for x in my_x_labels:
        if x not in my_dict_in.keys():

            my_dict_in[x] = 0
    return my_dict_in


def create_x_labels(my_dict):
    my_x_labels = []
    for sector in my_dict.keys():
        dicts_in = my_dict[sector]
        for dict_in in dicts_in:
            for ki in dict_in.keys():
                my_x_labels.append(ki)
        my_x_labels = list(set(my_x_labels))
        my_x_labels.sort()
    return my_x_labels


def create_y(my_sector, my_dict, x_labels, my_calc_type):
    my_y = []
    dicts_in = my_dict[my_sector]
    number_of_companies = len(dicts_in)
    res_dict = {}
    for dict_in in dicts_in:
        for date in dict_in.keys():
            if date in res_dict.keys():
                res_dict[date] += dict_in[date]
            else:
                res_dict[date] = dict_in[date]
    res_dict = add_zero_if_lack_of_date(res_dict, x_labels)
    res_dict = sort_inner_dictionary(res_dict)
    for date in res_dict.keys():
        my_y.append(res_dict[date])

    if my_calc_type == 'average' and number_of_companies > 0:
        my_iter = list(range(len(my_y)))
        for i, y in zip(my_iter, my_y):
            y = y / number_of_companies
            my_y[i] = y
    return my_y


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


@f.dict_to_df_to_excel
def sector_bar_chart(sectors_l, sector_dict, title, my_calc_type, calculated_companies_l):
    sector_combined_dict = {}
    x_labels = create_x_labels(sector_dict)
    x_axis = np.arange(len(x_labels), dtype=float)
    x_axis0 = x_axis
    x_axis = x_axis - 0.45
    fig = plt.figure(figsize=(19, 12))
    width = 0.9 / len(sectors_l)
    for sector in sectors_l:
        ax = plt.subplot()
        color = sector_color(sector)
        y = create_y(sector, sector_dict, x_labels, my_calc_type)
        ax.bar(x_axis, y, width=width, label=sector, align='center', color=color)
        x_axis += width
        sector_combined_dict[sector] = y
    plt.xticks(x_axis0, x_labels, rotation=90)
    plt.legend(loc='upper center', bbox_to_anchor=(0.5, 1.1), ncol=4, fancybox=True, shadow=True)
    plt.title(title, loc='left', pad=40)
    #manager = plt.get_current_fig_manager().window.state('zoomed')
    fold_path = r'C:\Users\Bartek\Desktop\ALK praca magisterska\charts'
    f_name = title + '.png'
    path = os.path.join(fold_path, f_name)
    plt.savefig(path, dpi=300)
    plt.close(fig)
    #plt.show()
    return sector_combined_dict, title, x_labels


def number_of_companies_in_sector_bar_chart(number_of_companies_in_sector):
    x_labels = number_of_companies_in_sector.keys()
    x_axis = np.arange(len(x_labels), dtype=float)
    y = list(number_of_companies_in_sector.values())
    fig = plt.figure()
    plt.bar(x_axis, y)
    plt.xticks(x_axis, x_labels, rotation=45)
    plt.show()


@f.dict_to_df_to_excel
def companies_in_sector_bar_chart(sector, sector_dict, title, my_calc_type, calculated_companies_in_sector_dict):
    my_sector_l = sector_dict[sector]
    x_labels = create_x_labels(sector_dict)
    x_axis = np.arange(len(x_labels), dtype=float)
    x_axis0 = x_axis
    x_axis = x_axis - 0.45
    fig = plt.figure(figsize=(19, 12))
    width = 0.9 / len(my_sector_l)
    ind = list(range(len(my_sector_l)))
    calculated_companies_l = calculated_companies_in_sector_dict[sector]
    title = sector + '_' + title
    sector_combined_dict = {}
    for company, company_dict in zip(calculated_companies_l, my_sector_l):
        ax = plt.subplot()
        y = create_y_for_company(company_dict)
        ax.bar(x_axis, y, width=width, label=company, align='center')
        x_axis += width
        sector_combined_dict[company] = y
    plt.xticks(x_axis0, x_labels, rotation=90)
    plt.legend(loc='upper center', bbox_to_anchor=(0.5, 1.17), ncol=4, fancybox=True, shadow=True)
    plt.title(title, loc='left', pad=40)
    manager = plt.get_current_fig_manager().window.state('zoomed')
    fold_path = r'C:\Users\Bartek\Desktop\ALK praca magisterska\charts\sectors\{}'.format(sector)
    f_name = title + '.png'
    path = os.path.join(fold_path, f_name)
    plt.savefig(path, dpi=300)
    plt.close(fig)
    # plt.show()

    return sector_combined_dict, title, x_labels


def create_y_for_company(my_dict):
    y = []
    for val in my_dict.values():
        y.append(val)
    return y


def standard_deviation_bef_aft_bar_chart_for_sec(sectors_standard_deviation_dict):
    sectors_l = sectors_standard_deviation_dict.keys()
    x_labels = ['Before 01.01.2020', 'After 01.01.2020']
    x_axis = np.arange(len(x_labels), dtype=float)
    x_axis0 = x_axis
    x_axis = x_axis - 0.45
    fig = plt.figure(figsize=(19, 12))
    width = 0.9 / len(sectors_l)
    sector_combined_dict = {}
    for sector in sectors_l:
        ax = plt.subplot()
        color = sector_color(sector)
        y = sectors_standard_deviation_dict[sector]
        ax.bar(x_axis, y, width=width, label=sector, align='center', color=color)
        x_axis += width
        sector_combined_dict[sector] = y
    plt.xticks(x_axis0, x_labels)
    plt.legend(loc='upper center', bbox_to_anchor=(0.5, 1.1), ncol=4, fancybox=True, shadow=True)
    title = 'sectors standard deviation'
    plt.title(title, loc='left', pad=40)
    fold_path = r'C:\Users\Bartek\Desktop\ALK praca magisterska\charts'
    f_name = title + '.png'
    path = os.path.join(fold_path, f_name)
    plt.savefig(path, dpi=300)
    plt.close(fig)
    #plt.show()
    df = pd.DataFrame(sector_combined_dict, index=x_labels)
    fold_path = r'C:\Users\Bartek\Desktop\ALK praca magisterska\python_res_data'
    f_name = title + '.xlsx'
    path = os.path.join(fold_path, f_name)
    df.to_excel(path)


def standard_deviation_bef_aft_bar_chart_for_comps_in_sec(comp_standard_deviation_dict):
    sectors_l = comp_standard_deviation_dict.keys()
    for sector in sectors_l:
        comps_dict = comp_standard_deviation_dict[sector]
        x_labels = ['Before 01.01.2020', 'After 01.01.2020']
        x_axis = np.arange(len(x_labels), dtype=float)
        x_axis0 = x_axis
        x_axis = x_axis - 0.45
        fig = plt.figure(figsize=(19, 12))
        comps_l = comps_dict.keys()
        width = 0.9 / len(comps_l)
        title = sector + '_standard_deviation'
        sector_combined_dict = {}
        for comp in comps_dict.keys():
            ax = plt.subplot()
            y = comp_standard_deviation_dict[sector][comp]
            ax.bar(x_axis, y, width=width, label=comp, align='center')
            x_axis += width
            sector_combined_dict[comp] = y
        plt.xticks(x_axis0, x_labels)
        plt.legend(loc='upper center', bbox_to_anchor=(0.5, 1.13), ncol=4, fancybox=True, shadow=True)
        plt.title(title, loc='left', pad=40)
        fold_path = r'C:\Users\Bartek\Desktop\ALK praca magisterska\charts\sectors\{}'.format(sector)
        f_name = title + '.png'
        path = os.path.join(fold_path, f_name)
        plt.savefig(path, dpi=300)
        plt.close(fig)
        #plt.show()
        df = pd.DataFrame(sector_combined_dict, index=x_labels)
        fold_path = r'C:\Users\Bartek\Desktop\ALK praca magisterska\python_res_data'
        f_name = title + '.xlsx'
        path = os.path.join(fold_path, f_name)
        df.to_excel(path)


def close_price_for_sectors_plot(close_price_in_sector_dict):
    sectors_l = close_price_in_sector_dict.keys()
    fig = plt.figure(figsize=(19, 12))
    sector_combined_dict = {}
    for sector in sectors_l:
        if sector != 'Communication Services':
            comps_dict = close_price_in_sector_dict[sector]
            comps_l = list(comps_dict.keys())
            number_of_companies = len(comps_l)
            color = sector_color(sector)
            y = None
            for comp in comps_l:
                df = comps_dict[comp]
                x_labels = list(df['Date'])
                x_axis = np.arange(len(x_labels), dtype=float)
                tmp_y = np.array(df['Close'])
                if y is None:
                    y = tmp_y
                else:
                    y += tmp_y
            y = y / number_of_companies
            plt.plot(x_axis, y, color=color, label=sector)
            sector_combined_dict[sector] = y
    xlab = []
    xax = []
    for x, d in zip(x_axis, x_labels):
        if d.year not in xlab:
            xax.append(x)
            xlab.append(d.year)
    plt.xticks(xax, xlab)
    plt.legend(loc='upper center', bbox_to_anchor=(0.5, 1.1), ncol=4, fancybox=True, shadow=True)
    plt.grid()
    title = 'Average close price for sectors'
    plt.title(title, loc='left', pad=40)
    fold_path = r'C:\Users\Bartek\Desktop\ALK praca magisterska\charts'
    f_name = title + '.png'
    path = os.path.join(fold_path, f_name)
    plt.savefig(path, dpi=300)
    plt.close(fig)
    df = pd.DataFrame(sector_combined_dict, index=x_labels)
    fold_path = r'C:\Users\Bartek\Desktop\ALK praca magisterska\python_res_data'
    f_name = title + '.xlsx'
    path = os.path.join(fold_path, f_name)
    df.to_excel(path)


def close_price_for_companies_in_sector_plot(close_price_in_sector_dict):
    sectors_l = close_price_in_sector_dict.keys()
    for sector in sectors_l:
        print(sector)
        fig = plt.figure(figsize=(19, 12))
        comps_dict = close_price_in_sector_dict[sector]
        comps_l = list(comps_dict.keys())
        sector_combined_dict = {}

        for comp in comps_l:
            df = comps_dict[comp]
            x_labels = list(df['Date'])
            x_axis = np.arange(len(x_labels), dtype=float)
            y = np.array(df['Close'])
            plt.plot(x_axis, y, label=comp)
            sector_combined_dict[comp] = y
        xlab = []
        xax = []
        for x, d in zip(x_axis, x_labels):
            if d.year not in xlab:
                xax.append(x)
                xlab.append(d.year)
        plt.xticks(xax, xlab)
        plt.grid()
        plt.legend(loc='upper center', bbox_to_anchor=(0.5, 1.1), ncol=4, fancybox=True, shadow=True)
        title = 'Close price for companies in {}'.format(sector)
        plt.title(title, loc='left', pad=40)
        fold_path = r'C:\Users\Bartek\Desktop\ALK praca magisterska\charts\sectors\{}'.format(sector)
        f_name = title + '.png'
        path = os.path.join(fold_path, f_name)
        plt.savefig(path, dpi=300)
        plt.close(fig)
        df = pd.DataFrame(sector_combined_dict, index=x_labels)
        fold_path = r'C:\Users\Bartek\Desktop\ALK praca magisterska\python_res_data'
        f_name = title + '.xlsx'
        path = os.path.join(fold_path, f_name)
        df.to_excel(path)


def close_price_change_for_each_sector(close_price_in_sector_dict):
    sectors_l = close_price_in_sector_dict.keys()
    for sector in sectors_l:
        sector_combined_dict = {}
        fig = plt.figure(figsize=(19, 12))
        comps_dict = close_price_in_sector_dict[sector]
        comps_l = list(comps_dict.keys())
        color = sector_color(sector)
        y = None
        for comp in comps_l:
            df = comps_dict[comp]
            x_labels = list(df['Date'])
            x_axis = np.arange(len(x_labels), dtype=float)
            tmp_y = np.array(df['Close'])
            if y is None:
                y = tmp_y
            else:
                y += tmp_y
        attempt = 0
        y_change = []
        for i in y:
            if attempt > 0:
                tmp_y = y[attempt] / y[attempt-1] -1
                y_change.append(tmp_y)
            attempt += 1
        x_axis = x_axis[1:]
        x_labels = x_labels[1:]
        plt.plot(x_axis, y_change, color=color, label=sector)
        sector_combined_dict[sector] = y_change
        xlab = []
        xax = []
        for x, d in zip(x_axis, x_labels):
            if d.year not in xlab:
                xax.append(x)
                xlab.append(d.year)
        plt.xticks(xax, xlab)
        plt.legend(loc='upper center', bbox_to_anchor=(0.5, 1.1), ncol=4, fancybox=True, shadow=True)
        plt.grid()
        title = 'close price change for {}'.format(sector)
        plt.title(title, loc='left', pad=40)
        fold_path = r'C:\Users\Bartek\Desktop\ALK praca magisterska\charts'
        f_name = title + '.png'
        path = os.path.join(fold_path, f_name)
        plt.savefig(path, dpi=300)
        plt.close(fig)
        df = pd.DataFrame(sector_combined_dict, index=x_labels)
        fold_path = r'C:\Users\Bartek\Desktop\ALK praca magisterska\python_res_data'
        f_name = title + '.xlsx'
        path = os.path.join(fold_path, f_name)
        df.to_excel(path)



