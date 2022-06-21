import matplotlib.pyplot as plt
from collections import OrderedDict, Counter
import numpy as np


def sort_inner_dictionary(my_dict):
    my_dict = OrderedDict(sorted(my_dict.items()))
    return my_dict


def add_zero_if_lack_of_date(my_dict_in, my_x_labels):
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


def create_y(my_sector, my_dict, x_labels):
    my_y = []
    dicts_in = my_dict[my_sector]
    res_dict = {}
    res_dict = Counter(res_dict)
    for dict_in in dicts_in:
        res_dict += dict_in
    res_dict = add_zero_if_lack_of_date(res_dict, x_labels)
    res_dict = sort_inner_dictionary(res_dict)
    for date in res_dict.keys():
        my_y.append(res_dict[date])
    return my_y

