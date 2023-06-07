#################################################################
# FILE : part_d_last.py
# WRITER : achikam levy , aaa997 , 208764944
# EXERCISE : intro2cs2 ex6 2021
# DESCRIPTION:
# STUDENTS I DISCUSSED THE EXERCISE WITH:
# WEB PAGES I USED:
# NOTES: ...
#################################################################

from moogle import *

import copy
import pickle


def get_search_rank(query, MAX_RESULTS, RANKING_DICT_FILE , WORDS_DICT_FILE):
    with open(WORDS_DICT_FILE, 'rb') as f:
        dict_map = pickle.load(f)
    with open(RANKING_DICT_FILE, 'rb') as file:
        traffic_dict_rank = pickle.load(file)
    query = query.split()
    new_query = [i for i in query if i in dict_map]
    init_dict = {}
    for search_word in new_query:
        for page, grade in dict_map[search_word].items():
            if page not in init_dict:
                init_dict[page] = {}
                init_dict[page][search_word] = grade
            if page in init_dict:
                init_dict[page][search_word] = grade
    init_dict1 = copy.deepcopy(init_dict)
    for page, word_num in init_dict.items():
        if len(word_num) != len(new_query):
            init_dict1.pop(page)
    sort_traffic_dict_rank = dict(
        sorted(traffic_dict_rank.items(), key=lambda item: item[1],
               reverse=True))
    finel_dict = {}
    for page, words in init_dict1.items():
        rank = []
        for word, val in words.items():
            rank.append(val)
        finel_dict[page] = min(rank)
    dicto = {}
    for name, num in sort_traffic_dict_rank.items():
        if len(dicto) < int(MAX_RESULTS):
            if name in finel_dict:
                dicto.update({name: num})
    dict_for_print = {}
    for name in dicto:
        grade = finel_dict[name] * traffic_dict_rank[name]
        dict_for_print.update({name: grade})
    dict_for_print = dict(sorted(dict_for_print.items(), key=lambda item: item[1], reverse=True))
    for grade in dict_for_print:
        print(grade, dict_for_print[grade])




