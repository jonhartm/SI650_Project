# webscrape

import requests
from bs4 import BeautifulSoup
import sys
import json
import time


#search_url = "http://www.ontheissues.org/default.htm"

#request url
#page = requests.get(search_url)
#grab text
#page_text = page.text
#create soup object
#page_soup = BeautifulSoup(page_text, 'html.parser')

#state_links = page_soup.find_all(href=True)

#for a in state_links:
#    print(a['href'])

list_of_state_abbrv = ["ak", "al", "ar", "az", "ca", "co", "ct", "de", "fl",
                        "ga", "hi", "ia", "id", "il", "in", "ks", "ky", "la",
                        "ma", "md", "me", "mi", "mn", "mo", "ms", "mt", "nc",
                        "nd", "ne", "nh", "nj", "nm", "nv", "ny", "oh", "ok",
                        "or", "pa", "ri", "sc", "sd", "tn", "tx", "ut", "va",
                        "vt", "wa", "wi", "wv", "wy"]
#save_data = {}

#for each in list_of_state_abbrv:
#    search_url = "http://www.ontheissues.org/states/{}.htm".format(each)
#    #request url
#    time.sleep(5)
#    page = requests.get(search_url)
#    time.sleep(5)
#    #grab text
#    page_text = page.text
#    #create soup object
#    page_soup = BeautifulSoup(page_text, 'html.parser')
#    save_data[each] = page_text


#with open('OnTheIssues.txt', 'w') as file:
#     file.write(json.dumps(save_data))

# grab all politician lists from sidebar

# read in dataset

with open('OnTheIssues.txt', 'r') as file:
     info = json.load(file)

chunks = {}
for each in info:
    page_soup = BeautifulSoup(info[each], 'html.parser')
    link_items = page_soup.find_all('a', href=True)
    house = []
    senate = []
    for every in link_items:
        if 'House' in every['href']:
            house.append(every['href'])
        if 'Senate' in every['href']:
            senate.append(every['href'])
    chunks[each] = [house, senate]

print(chunks['ak'])

#person_data = {}

#for each in list_of_state_abbrv:
#    search_url = "http://www.ontheissues.org{}".format(chunks[each][0][0][2:])
    #print(search_url)
    #request url
#    time.sleep(5)
#    page = requests.get(search_url)
#    time.sleep(5)
    #grab text
#    page_text = page.text
    #create soup object
    #page_soup = BeautifulSoup(page_text, 'html.parser')
#    if each not in person_data:
#        person_data[each] = {}
#        if 'House' not in person_data[each]:
#            person_data[each]['House'] = {}

#    person_data[each]['House'] = page_text

    #print(person_data['mi']['House'])

for each_state in chunks:
    for each_item in chunks[each_state][0]:
        try:
            search_url = "http://www.ontheissues.org{}".format(each_item[2:])
            #request url
            time.sleep(5)
            page = requests.get(search_url)
            time.sleep(5)
            #grab text
            page_text = page.text
            #create soup object
            #page_soup = BeautifulSoup(page_text, 'html.parser')
            if each_state not in person_data:
                person_data[each_state] = {}
            if 'House' not in person_data[each_state]:
                person_data[each_state]['House'] = {}
            person_data[each_state]['House'] = page_text
        except:
            print("http://www.ontheissues.org{}".format(each_item[2:]))
    for each_item in chunks[each_state][1]:
        try:
            search_url = "http://www.ontheissues.org{}".format(each_item[2:])
            #request url
            time.sleep(5)
            page = requests.get(search_url)
            time.sleep(5)
            #grab text
            page_text = page.text
            #create soup object
            #page_soup = BeautifulSoup(page_text, 'html.parser')
            if 'Senate' not in person_data[each_state]:
                person_data[each_state]['Senate'] = {}
            person_data[each_state]['Senate'] = page_text
        except:
            print("http://www.ontheissues.org{}".format(each_item[2:]))

print(person_data)

with open('StatePeople.txt', 'w') as file:
     file.write(json.dumps(person_data))
