
#################################################################
# FILE : part_c_word_map.py
# WRITER : achikam levy , aaa997 , 208764944
# EXERCISE : intro2cs2 ex6 2021
# DESCRIPTION:
# STUDENTS I DISCUSSED THE EXERCISE WITH:
# WEB PAGES I USED:
# NOTES: ...
#################################################################
from moogle import *
import pickle
import requests
import bs4
import urllib.parse


def all_words_dict(url_lst, BASE_URL, OUT_FILE):
    dict_map = {}
    for name in open(url_lst):
        name = name.rstrip()
        full_url = urllib.parse.urljoin(BASE_URL, name)
        response = requests.get(full_url)
        html = response.text
        soup = bs4.BeautifulSoup(html, 'html.parser')
        for p in soup.find_all("p"):
            content = p.text
            content = content.split()
            for word in content:
                if word not in dict_map:
                    dict_map[word] = {name: 1}
                else:
                    if name not in dict_map[word]:
                        dict_map[word].update({name: 1})
                    else:
                        dict_map[word][name] += 1
    with open(OUT_FILE, "wb") as f:
        pickle.dump(dict_map, f)


