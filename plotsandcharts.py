import matplotlib.pyplot as plt
from collections import OrderedDict, Counter
import numpy as np
import time


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
    print(my_sector)
    my_y = []
    dicts_in = my_dict[my_sector]
    number_of_companies = len(dicts_in)
    res_dict = {}
    res_dict = Counter(res_dict)
    for dict_in in dicts_in:
        res_dict += dict_in
    res_dict = add_zero_if_lack_of_date(res_dict, x_labels)
    res_dict = sort_inner_dictionary(res_dict)
    for date in res_dict.keys():
        my_y.append(res_dict[date])

    if my_calc_type == 'average' and number_of_companies > 0:
        print('average')
        print(number_of_companies)
        print(my_y)
        my_iter = list(range(len(my_y)))
        for i, y in zip(my_iter, my_y):
            y = y / number_of_companies
            my_y[i] = y
        print(my_y)
    return my_y


def sector_bar_chart(sectors_l, sector_capitalization_dict, title, my_calc_type):
    x_labels = create_x_labels(sector_capitalization_dict)
    x_axis = np.arange(len(x_labels), dtype=float)
    x_axis0 = x_axis
    x_axis = x_axis - 0.45
    fig = plt.figure()
    width = 0.9 / len(sectors_l)
    for sector in sectors_l:
        y = create_y(sector, sector_capitalization_dict, x_labels, my_calc_type)
        plt.bar(x_axis, y, width=width, label=sector, align='center')
        x_axis += width
    plt.xticks(x_axis0, x_labels, rotation=90)
    plt.legend(loc='upper center', bbox_to_anchor=(0.5, 1.17), ncol=4, fancybox=True, shadow=True)
    plt.title(title, loc='left', pad=40)
    manager = plt.get_current_fig_manager().window.state('zoomed')
    plt.show()


def number_of_companies_in_sector_bar_chart(number_of_companies_in_sector):
    x_labels = number_of_companies_in_sector.keys()
    x_axis = np.arange(len(x_labels), dtype=float)
    y = list(number_of_companies_in_sector.values())
    fig = plt.figure()
    plt.bar(x_axis, y)
    plt.xticks(x_axis, x_labels, rotation=45)
    plt.show()
