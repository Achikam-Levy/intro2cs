# # import sys
# # import requests
# # import bs4
# # import urllib.parse
# import pickle
# #
# # from moogle import *
# #
# #
# # def create_dictionary(file, n):
# #     dict = {}
# #     for index in open(file):
# #         index = index.rstrip()
# #         dict[index] = n
# #     return dict
# #
# #
# # def total_num_links(dictionary: dict) -> int:
# #     value = 0
# #     for key in dictionary:
# #         value += dictionary[key]
# #     return value
# #
# #
# # def sum_dict_values(dict):
# #     n = 0
# #     for key in dict:
# #         n += dict[key]
# #     return n
# #
# #
# # def first_rank(DICT_FILE):
# #     rank_dict = create_dictionary(DICT_FILE, 1)
# #     new_rank_dict = create_dictionary(DICT_FILE, 0)
# #     for name in rank_dict:
# #         key_num_links = total_num_links(DICT_FILE[name])
# #         for key in DICT_FILE:
# #             new_rank_dict[key] += (rank_dict[key] * (DICT_FILE[name][key] / key_num_links))
# #     return new_rank_dict
# #
# #
# def dict_page_rank(DICT_FILE, ITERATIONS, OUT_FILE):
#     global new_rank_dict
#     rank_dict = first_rank(DICT_FILE)
#     if ITERATIONS == 0:
#         return create_dictionary(DICT_FILE, 1)
#     if ITERATIONS == 1:
#         return rank_dict
#     for iterate in range(ITERATIONS-1):
#         new_rank_dict = create_dictionary(DICT_FILE, 0)
#         for name in rank_dict:
#             key_num_links = total_num_links(DICT_FILE[name])
#             for key in DICT_FILE:
#                 new_rank_dict[key] += (rank_dict[name] * (DICT_FILE[name][key] / key_num_links))
#         rank_dict = new_rank_dict
#     with open(OUT_FILE, "wb") as f:
#         pickle.dump(new_rank_dict, f)
# #
# #
# #
# #
# #
# #
# #
# # import copy
# # import pickle
# # import sys
# # import requests
# # import bs4
# # import urllib.parse
# #
# # from moogle import *
# # # with open('traffic_dict_rank', 'rb') as f:
# # #     traffic_dict_rank = pickle.load(f)
# # # with open('dict_map', 'rb') as f:
# # #     dict_map = pickle.load(f)
# # # print(dict_map)
# # # print(traffic_dict_rank)
# #
# # def short_dict(dict1, dict2):
# #     x = dict1
# #     if len(dict2) < len(dict1):
# #         x = dict2
# #     return x
# #
# #
# # def dict_compare(dict1, dict2):
# #     dict = copy.deepcopy(dict1)
# #     for key in dict1:
# #         if key not in dict2:
# #             dict.pop(key)
# #     return dict
# #
# #
# # def choose_common_dicts(lst):
# #     dict = lst[0]
# #     for i in range(len(lst)):
# #         for dict1 in lst:
# #             for key in dict1:
# #                 if dict[key] > dict1[key]:
# #                     dict[key] = dict1[key]
# #     return dict
# # # lst = [{'one':1, "two": 4}, {'one':2, "two": 3}, {"one" : 0,"two" : 1}]
# # #
# # # print(choose_common_dicts(lst))
# # #
# #
# #
# #
# # def get_search_rank(query, MAX_RESULTS,RANKING_DICT_FILE ,WORDS_DICT_FILE):
# #     with open(WORDS_DICT_FILE, 'rb') as f:
# #         dict_map = pickle.load(f)
# #     with open(RANKING_DICT_FILE, 'rb') as f:
# #         traffic_dict_rank = pickle.load(f)
# #     sort_traffic_dict_rank = sorted(traffic_dict_rank,
# #                                     key=traffic_dict_rank.get, reverse=True)
# #     global shortest_dict, filter_short_dict
# #     query = query.split()
# #     lst = []
# #     finel_dict = {}
# #     dict_for_print = {}
# #     for search_word in query:
# #         if search_word in dict_map:
# #             search_word_places = dict_map[search_word]
# #             lst.append(search_word_places)
# #         else:
# #             continue
# #     lst = choose_common_dicts(lst)
# #     for i in lst:
# #         shortest_dict = short_dict(lst[0], i)
# #     for r in lst:
# #         filter_short_dict = dict_compare(shortest_dict, r)
# #     for page in sort_traffic_dict_rank:
# #         if page in filter_short_dict:
# #             if len(finel_dict) == int(MAX_RESULTS):
# #                 break
# #             finel_dict.update({page: traffic_dict_rank[page]})
# #         else:
# #             continue
# #     for q in finel_dict:
# #         grade = finel_dict[q]*filter_short_dict[q]
# #         dict_for_print.update({q: grade})
# #     dict_for_print = dict(sorted(dict_for_print.items(), key=lambda item: item[1], reverse=True))
# #     for grade in dict_for_print:
# #         print(grade, dict_for_print[grade])
# #
# # # python3 moogle.py search "Pensieve McGonagall" /Users/hyqmlwy/Desktop/intro/exercises/week6/ex6/traffic_dict_rank /Users/hyqmlwy/Desktop/intro/exercises/week6/ex6/dict_map 4
# #
# #
#
#
# rd = {'a': {'A.html': 4, 'B.html': 4, 'C.html': 2}, 'b': {'A.html': 2, 'B.html': 1, 'C.html': 1}, 'c': {'A.html': 1, 'B.html': 1, 'C.html': 6}, 'd': {'A.html': 2, 'B.html': 2, 'C.html': 1}, 'e': {'A.html': 1, 'B.html': 1, 'C.html': 1}, 'f': {'A.html': 2}, 'g': {'A.html': 2, 'B.html': 1}, 'h': {'A.html': 2, 'B.html': 3, 'C.html': 2}}
# with open("new_rank_test", "wb") as f:
#     pickle.dump(rd, f)
