#################################################################
# FILE : part_B_page_rank.py
# WRITER : achikam levy , aaa997 , 208764944
# EXERCISE : intro2cs2 ex6 2021
# DESCRIPTION:
# STUDENTS I DISCUSSED THE EXERCISE WITH:
# WEB PAGES I USED:
# NOTES: ...
#################################################################

import pickle

from moogle import *


def create_dictionary(DICT_FILE, n):
    dict = {}
    for index in DICT_FILE:
        index = index.rstrip()
        dict[index] = n
    return dict


def total_num_links(dictionary):
    value = 0
    for key in dictionary:
        value += dictionary[key]
    return value


def sum_dict_values(dict):
    n = 0
    for key in dict:
        n += dict[key]
    return n


def first_rank(DICT_FILE):
    rank_dict = create_dictionary(DICT_FILE, 1)
    new_rank_dict = create_dictionary(DICT_FILE, 0)
    for name in rank_dict:
        key_num_links = total_num_links(DICT_FILE[name])
        for key in DICT_FILE[name].keys():
            new_rank_dict[key] += (rank_dict[name] * (DICT_FILE[name][key] / key_num_links))
    return new_rank_dict


def dict_page_rank(DICT_FILE, ITERATIONS, OUT_FILE):
    with open(DICT_FILE, 'rb') as f:
        DICT_FILE = pickle.load(f)
    rank_dict = first_rank(DICT_FILE)
    if int(ITERATIONS) == 0:
        new_rank_dict = create_dictionary(DICT_FILE, 1)
    elif int(ITERATIONS) == 1:
        new_rank_dict = rank_dict
    else:
        for iterate in range(int(ITERATIONS)-1):
            new_rank_dict = create_dictionary(DICT_FILE, 0)
            for name in rank_dict:
                key_num_links = total_num_links(DICT_FILE[name])
                for key in DICT_FILE[name].keys():
                    new_rank_dict[key] += (rank_dict[name] * (
                                DICT_FILE[name][key] / key_num_links))
            rank_dict = new_rank_dict
    with open(OUT_FILE, "wb") as f:
        pickle.dump(new_rank_dict, f)


