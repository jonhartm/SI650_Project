import requests
from bs4 import BeautifulSoup
import sys
import json
import time
import csv

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

with open("Individual_People2.txt", 'r', encoding = 'utf-8') as file:
    info = json.load(file)

#print(info.keys())
page_soup = BeautifulSoup(info['Bernie Sanders_vt_Senate'], 'html.parser')
link_items = page_soup.find_all('li')
for every in link_items:
    print(every.encode('utf-8').encode('cp850', 'replace').decode('cp850'))
    #name_join = 'Bernie Sanders' + ' ' + "on"
    #if name_join in every:
    #    print(every)
    #for each in every.findChildren('font'):
    #    print(each.text)
