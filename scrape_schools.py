import requests
from bs4 import BeautifulSoup
import json

address = "https://en.wikipedia.org/wiki/List_of_high_schools_in_California?oldformat=true"
page = requests.get(address)
soup = BeautifulSoup(page.text)
items = soup.select("#mw-content-text li")
school_names = []
start = False
for item in items:
    school_name = item.text
    if school_name == "Alameda Community Learning Center": # replace with
        # first school
        start = True
    if not start:
        continue
    if school_name == "Wheatland High School, Wheatland": # replace with last
        #  school
        name = school_name.split(",")[0]
        school_names.append(name)
        break
    bad = False
    for child in item.children:
        if "li" in child or "ul" in child:
            bad = True
    if not bad:
        name = school_name.split(",")[0]
        school_names.append(name)

school_names = [school_names.pop(school_names.index("Menlo School"))]\
               + school_names
print(school_names)
json.dump(school_names, open("school_names.json", "w"))