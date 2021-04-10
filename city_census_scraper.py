import requests
import pandas as pd
import threading
from bs4 import BeautifulSoup
import time

list_cities = []
list_status = []
list_counties = []
list_nonwhite_pct = []
list_nonwhite_or_asian_pct = []

def scrape_census_info(city, status, og):
    if status == "city":
        page = requests.get("https://www.towncharts.com/Massachusetts/Demographics/{}-city-MA-Demographics-data.html".format(city))
    elif status == "town":
        page = requests.get("https://www.towncharts.com/Massachusetts/Demographics/{}-town-MA-Demographics-data.html".format(city))
    else:
        page = requests.get("https://www.towncharts.com/Massachusetts/Demographics/{}-CDP-MA-Demographics-data.html".format(city))
    time.sleep(.1)
    soup = BeautifulSoup(page.content, "html.parser")
    tags = soup.find_all("script", {"type": "text/javascript"})
    script = ""
    for tag in tags:
        if "createDashboard1()" in str(tag):
            script = str(tag)
    try:
        if not status == "CDP" and og + " CDP" in script:
            relevant_info = script.split("[\'" + og + " town")[1].split(",\'<")[0]
        else:
            relevant_info = script.split("[\'" + og)[1].split(",\'<")[0]
        values = relevant_info.split(",")
        list_cities.append(city)
        list_nonwhite_pct.append(1-float(values[15]))
        list_nonwhite_or_asian_pct.append(1-float(values[15])-float(values[19]))
    except IndexError as e:
        print("ERROR:", og)

df = pd.read_csv(r"C:\Users\novac\Documents\cvt\covid-and-climate\city_info.csv")

for i in range(len(df["Cities"].index)):
    city_name = df["Cities"][i]
    city = city_name.replace("_", " ")
    passed_city = city_name.replace("_", "-")
    passed_status = df["Status"][i]
    if passed_status == "town" or passed_status == "city":
        if city == "Palmer":
            passed_city = "Palmer-Town"
            passed_status = "city"
        if city == "Amesbury":
            passed_city = "Amesbury-Town"
            passed_status = "city"
        if city == "Lanesboro":
            passed_city = "Lanesborough"
            passed_status = "town"
        if city == "Franklin":
            passed_city = "Franklin-Town"
        if city == "Weymouth":
            passed_city = "Weymouth-Town"
            passed_status = "city"
        if city == "Braintree":
            passed_city = "Braintree-Town"
            passed_status = "city"
        if city == "East Longmeadow":
            passed_status = "town"
        if city == "Barnstable":
            passed_city = "Barnstable-Town"
            passed_status = "city"
        if city == "Bridgewater":
            passed_status = "town"
        if city == "West Springfield":
            passed_city = "West-Springfield-Town"
        if city == "Agawam":
            passed_city = "Agawam-Town"
        if city == "Southbridge":
            passed_city = "Southbridge-Town"
            passed_status = "city"
        if city == "Randolph":
            passed_status = "town"
        if city == "Watertown":
            passed_city = "Watertown-Town"
            passed_status = "city"
        if city == "Winthrop":
            passed_city = "Winthrop-Town"
        if city == "Easthampton":
            passed_city = "Easthampton-Town"
        if city == "Framingham":
            passed_status = "CDP"
        if city == "Manchester":
            passed_city = "Manchester-by-the-Sea"
        if city == "Methuen":
            passed_city = "Methuen-Town"
        if city == "Greenfield":
            passed_city = "Greenfield-Town"
        #print(passed_city, passed_status)
        scrape_census_info(passed_city, passed_status, city)

print(len(list_cities))
print(len(list_nonwhite_pct))
print(len(list_nonwhite_or_asian_pct))

df2 = pd.DataFrame({"City/Town": list_cities, "Proportion Non-White Population": list_nonwhite_pct, "Proportion Non-White or Asian Population": list_nonwhite_or_asian_pct})

#for i in range(len(df["TOWN"].index)):
#    city_name = df["TOWN"][i]
#    if " " in city_name:
    #    words = city_name.split()
    #    final_word = ""
    #    for word in words:
    #        final_word = final_word + word[0] + word[1:len(word)].lower()
        #    if not words.index(word) == len(words) - 1:
            #    final_word = final_word + "_"

    #    list_cities.append(final_word)
    #else:
    #    list_cities.append(city_name[0] + city_name[1:len(city_name)].lower())

#for city in list_cities:
#    if not city == "Byfield":
    #    soup = BeautifulSoup(requests.get("https://en.wikipedia.org/wiki/{}".format(city + ",_Massachusetts")).content, "html.parser")
    #    time.sleep(.1)
    #    tag = soup.find("div", {"class": "shortdescription nomobile noexcerpt noprint searchaux"})
    #    if tag is not None:
        #    list_status.append(str(tag.text).split()[0].lower())
        #    a_tags = soup.find_all("a", title = True)
        #    for tag in a_tags:
        #        if "County, Massachusetts" in tag["title"]:
            #        list_counties.append(tag.text)
            #        break

#df2 = pd.DataFrame({"Cities": list_cities, "County": list_counties, "Status": list_status})
#list_count = list(dic_count.values())
#df2 = df2.drop_duplicates()
#df2["Number of Sites"] = list_count
df2.to_csv("mass_city_demographic_data.csv", index = False)
