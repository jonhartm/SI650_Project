
import requests
from bs4 import BeautifulSoup
import sys
import json
import time
import csv
import codecs
sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer)


list_of_state_abbrv = ["ak", "al", "ar", "az", "ca", "co", "ct", "de", "fl",
                        "ga", "hi", "ia", "id", "il", "in", "ks", "ky", "la",
                        "ma", "md", "me", "mi", "mn", "mo", "ms", "mt", "nc",
                        "nd", "ne", "nh", "nj", "nm", "nv", "ny", "oh", "ok",
                        "or", "pa", "ri", "sc", "sd", "tn", "tx", "ut", "va",
                        "vt", "wa", "wi", "wv", "wy"]

with open('OnTheIssues.txt', 'r') as file:
     info = json.load(file)

chunks = {}
for each in info:
    page_soup = BeautifulSoup(info[each], 'html.parser')
    link_items = page_soup.find_all('a', href=True)
    house = []
    senate = []
    other = []
    for every in link_items:
        if 'House' in every['href']:
            #house.append(every['href'])
            pass
        if 'Senate' in every['href']:
            #senate.append(every['href'])
            pass
        else:
            other.append(every['href'])
    chunks[each] = [house, senate, other]

#print(chunks['ak'])

keep_topics = {}
for each_state in chunks:
    for each_item in chunks[each_state][0]:
        overall_key = each_state + "_" + "HOUSE_"
        try:
            search_url = "http://www.ontheissues.org{}".format(each_item[2:])
            if len(search_url.split("/")) > 4:
                cutup = search_url.split("/")
                overall_key += cutup[4]
                #request url
                time.sleep(5)
                page = requests.get(search_url)
                time.sleep(5)
                #grab text
                page_text = page.text
                #create soup object
                page_soup = BeautifulSoup(page_text, 'html.parser')

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
                keep_topics[overall_key] = test_bit
        except:
            print("http://www.ontheissues.org{}".format(each_item[2:]))
    for each_item in chunks[each_state][1]:
        overall_key = each_state + "_" + "SENATE_"
        try:
            search_url = "http://www.ontheissues.org{}".format(each_item[2:])
            if len(search_url.split("/")) > 4:
                cutup = search_url.split("/")
                overall_key += cutup[4]
                #request url
                time.sleep(5)
                page = requests.get(search_url)
                time.sleep(5)
                #grab text
                page_text = page.text
                #create soup object
                page_soup = BeautifulSoup(page_text, 'html.parser')

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
                keep_topics[overall_key] = test_bit
        except:
            print("http://www.ontheissues.org{}".format(each_item[2:]))
    for each_item in chunks[each_state][2]:
        overall_key = each_state + "_" + "UNSPEC_"
        try:
            search_url = "http://www.ontheissues.org{}".format(each_item[2:])
            #if len(search_url.split("/")) > 4:
            cutup = search_url.split("/")
            overall_key += cutup[-1]
            #request url
            time.sleep(5)
            page = requests.get(search_url)
            time.sleep(5)
            #grab text
            page_text = page.text
            #create soup object
            page_soup = BeautifulSoup(page_text, 'html.parser')

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
            keep_topics[overall_key] = test_bit
        except:
            print("http://www.ontheissues.org{}".format(each_item[2:]))


print(keep_topics.keys())
print(len(keep_topics))

with open('full_topic_bit_2.json', 'w', encoding='utf-8') as file:
     json.dump(keep_topics, file)
