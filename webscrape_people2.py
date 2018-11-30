import requests
from bs4 import BeautifulSoup
import sys
import json
import time


with open('StatePeople.txt', 'r') as file:
     info = json.load(file)

print(type(info))
print(len(info))
print(type(info['mi']['House']))

people_lists = []
for each_state in info:
    for every_gov in info[each_state]:
        page_soup = BeautifulSoup(info[each_state][every_gov], 'html.parser')
        link_items = page_soup.find_all('li')
        for every in link_items:
            for each in every.findChildren('a', href=True):
                fit_string = ""
                name_check = "../" + every_gov + "/"
                if 'javascript' not in each['href'] and name_check in each['href']:
                    fit_string += each['href'] + ","
                    fit_string += each.text + ","
                    fit_string += each_state + ","
                    fit_string += every_gov + "\n"
                #print(each['href'])
                    people_lists.append(fit_string)
#inside_links = link_items.findChildren('a', href=True)
#print(inside_links)

print(people_lists[0])

with open('People_Lists.csv', 'w', encoding = "utf-8") as pl:
    for each_line in people_lists:
        pl.write(each_line)
