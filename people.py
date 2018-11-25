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
    info_tabs = []
    for every in link_items:
        new_text = str(every.text)
        bumped_split = new_text.split("\r\n")
        #new_text2 = new_text.strip()[:-11]
        # extract ( DATE )
        #print(new_text2)
        #new_date = every.text.strip()[-11:]
        #print(new_date)
        for each in bumped_split:
            info_tabs.append(each.strip())

    keep_topics[each_key] = info_tabs

#print(keep_topics['Debbie Stabenow_mi_Senate'][0:5])

with open("totalsheet.json", "w", encoding = 'utf-8') as tsw:
    json.dump(keep_topics, tsw)
