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

keep_topics = {}
for each_key in info:
    page_soup = BeautifulSoup(info[each_key], 'html.parser')
    headers = page_soup.find_all('td')
    test_bit = {}
    for each in headers:
        if 'Click here for' in each.text:
            info_tabs = []
            text_chunk = each.text
            splitup = text_chunk.split('\r\n')
            keytouse = splitup[1].split(' on ')
            #print(keytouse)
            if len(keytouse) > 1:
                if keytouse[1] not in test_bit:
                    test_bit[keytouse[1]] = []
                for each_text in splitup[4:-1]:
                    new_text = str(each_text)
                    stripped = new_text.strip()
                    remove_tabs = stripped.replace('\t', '')
                    remove_n = remove_tabs.replace('\n', '')
                    text_bit = remove_n[:-11]
                    date_bit = remove_n[-11:]
                    info_tabs.append([text_bit.strip(), date_bit.strip()])
                test_bit[keytouse[1]].append(info_tabs)
    keep_topics[each_key] = test_bit

#print(keep_topics.keys())
#print(info.keys())
#keep_topics = {}

#for each_key in info:
#    page_soup = BeautifulSoup(info[each_key], 'html.parser')
#    link_items = page_soup.find_all('li')
#    info_tabs = []
#    for every in link_items:
#        new_text = str(every.text)
#        bumped_split = new_text.split("\r\n")
        #new_text2 = new_text.strip()[:-11]
        # extract ( DATE )
        #print(new_text2)
        #new_date = every.text.strip()[-11:]
        #print(new_date)
#        for each in bumped_split:
#            text_stripped = each.strip()
            # split date off end
#            text_bit = text_stripped[:-11]
#            date_bit = text_stripped[-11:]
#            info_tabs.append([text_bit.strip(), date_bit.strip()])

#    keep_topics[each_key] = info_tabs

#print(keep_topics['Debbie Stabenow_mi_Senate'][0:5])

with open("by_topic.json", "w", encoding = 'utf-8') as tsw:
    json.dump(keep_topics, tsw)
