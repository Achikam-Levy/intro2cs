#################################################################
# FILE : moogle.py
# WRITER : achikam levy , aaa997 , 208764944
# EXERCISE : intro2cs2 ex6 2021
# DESCRIPTION:
# STUDENTS I DISCUSSED THE EXERCISE WITH:
# WEB PAGES I USED:
# NOTES: ...
#################################################################
from part_B_page_rank import *
from part_d_last import *
from part_c_word_map import *

import pickle
import sys
import requests
import bs4
import urllib.parse


parameters = sys.argv




def get_links(name):
    global filter_lst
    dict_name = {}
    full_url = urllib.parse.urljoin(BASE_URL, name)
    response = requests.get(full_url)
    html = response.text
    soup = bs4.BeautifulSoup(html, 'html.parser')
    lst = []
    for p in soup.find_all("p"):
        for link in p.find_all("a"):
            target = link.get("href")
            lst.append(target)
            filter_lst = filter(None, lst)
            filter_lst = list(filter_lst)
    for index in open(DICT_FILE):
        index = index.rstrip()
        num = filter_lst.count(index)
        dict_name[index] = num
    return dict_name


def dictionary_of_dictionarys(list_of_urls):
    old_traffic_dict = {}
    for name in open(list_of_urls):
        name = name.rstrip()
        old_traffic_dict[name] = (get_links(name))
    traffic_dict = copy.deepcopy(old_traffic_dict)
    for key in old_traffic_dict:
        for dict1 in old_traffic_dict[key]:
            if old_traffic_dict[key][dict1] == 0:
                 traffic_dict[key].pop(dict1)
    with open(OUT_FILE, "wb") as f:
        pickle.dump(traffic_dict, f)


if __name__ == '__main__':
    if parameters[1] == 'crawl':
        BASE_URL = parameters[2]
        DICT_FILE = parameters[3]
        OUT_FILE = parameters[4]
        dictionary_of_dictionarys(DICT_FILE)
    elif parameters[1] == 'page_rank':
        ITERATIONS = parameters[2]
        DICT_FILE = parameters[3]
        OUT_FILE = parameters[4]
        dict_page_rank(DICT_FILE, ITERATIONS, OUT_FILE)
    elif parameters[1] == 'words_dict':
        BASE_URL = parameters[2]
        DICT_FILE = parameters[3]
        OUT_FILE = parameters[4]
        all_words_dict(DICT_FILE, BASE_URL, OUT_FILE)
    elif parameters[1] == 'search':
        QUERY = parameters[2]
        RANKING_DICT_FILE = parameters[3]
        WORDS_DICT_FILE = parameters[4]
        MAX_RESULTS = parameters[5]
        get_search_rank(QUERY, MAX_RESULTS, RANKING_DICT_FILE, WORDS_DICT_FILE)





