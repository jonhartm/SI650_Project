import requests
from bs4 import BeautifulSoup
import sys
import json
import time
import csv
import codecs
sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer)

#people_list = []
# read in csv file
#with open('People_Lists.csv', 'r') as csvfile:
#    spamreader = csv.reader(csvfile)
#    for row in spamreader:
#        people_list.append(row)

# store in dictionary
#people_storage = {}
# scrape each person's page
#for each_person in people_list:
#    each_item = each_person[0]
#    search_url = "http://www.ontheissues.org{}".format(each_item[2:])
    #request url
#    time.sleep(5)
#    page = requests.get(search_url)
#    time.sleep(5)
    #grab text
#    page_text = page.text

#    identifier = each_person[1] + '_' + each_person[2] + '_' + each_person[3]
#    people_storage[identifier] = page_text

# output to text file
#with open('Individual_People2.txt', 'w', encoding = 'utf-8') as file:
#     file.write(json.dumps(people_storage))

with open("C:/Users/julie/Documents/SI650/Individual_People2.txt", 'r') as file:
    info = json.load(file)

#print(info.keys())
keep_topics = {}

for each_key in info:
    page_soup = BeautifulSoup(info[each_key], 'html.parser')
    link_items = page_soup.find_all('li')
    info_tabs = ""
    for every in link_items:
        new_text = every.text.replace(",", " ")
        new_text2 = new_text.replace("\r", " ")
        new_text3 = new_text2.replace("\n", " ")
        info_tabs = info_tabs + " " + new_text3

    keep_topics[each_key] = info_tabs

#print(keep_topics)

with open("totalsheet.csv", "w", encoding = 'utf-8') as tsw:
    for each_person in keep_topics:
        begin = each_person.split("_")
        tsw.write("{}, {}, {}, {}\n".format(begin[0], begin[1], begin[2], keep_topics[each_person]))
