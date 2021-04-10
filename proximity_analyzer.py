import pandas as pd
from threading import Thread
import time
from os import path
import os

average_mass_demo = 0.279
list_cities = []
all_proximity_cities = {}
proximity_data = {}
proximity_cities = {}
proximity_means = {}

pm_data = pd.read_csv(r"C:\Users\novac\Documents\cvt\covid-and-climate\MA_PM2.5_1998-2016.csv")
city_data = pd.read_csv(r"C:\Users\novac\Documents\cvt\covid-and-climate\mass_city_demographic_data.csv")
for i in range(len(city_data["City/Town"].index)):
    list_cities.append(city_data["City/Town"][i])

def compile_dic(index):
    key = list(proximity_data.keys())
    for file in proximity_data[key[index]]:
        df = pd.read_csv(str(os.getcwd() + "/" + file), header = None)
        proximity_city = file.split("kilometers_")[1].split(".")[0]
        all_proximity_cities[key[index]][proximity_city] = []
        proximity_cities[key[index]][proximity_city] = []
        for i in range(len(df.index)):
            city = df[0][i]
            if city in list_cities:
                all_proximity_cities[key[index]][proximity_city].append(city)

for filename in os.listdir(os.getcwd()):
    category = filename.split("_")[0]
    if category.isdigit() and category not in proximity_data.keys():
        proximity_data[int(category)] = []
        all_proximity_cities[int(category)] = []
        proximity_cities[int(category)] = []
        proximity_means[int(category)] = []

proximity_data = dict.fromkeys(sorted(list(proximity_data.keys())))
all_proximity_cities = dict.fromkeys(sorted(list(all_proximity_cities.keys())))
proximity_cities = dict.fromkeys(sorted(list(proximity_cities.keys())))
proximity_means = dict.fromkeys(sorted(list(proximity_cities.keys())))

for key in proximity_data.keys():
    proximity_data[key] = []
    all_proximity_cities[key] = {}
    proximity_cities[key] = {}
    proximity_means[key] = []

for filename in os.listdir(os.getcwd()):
    try:
        category = int(filename.split("_")[0])
        proximity_data[category].append(filename)
    except ValueError as e:
        continue

threads = []
for i in range(len(proximity_data.keys())):
    thread = Thread(target = compile_dic, args = [i])
    thread.start()
    time.sleep(.1)
    threads.append(thread)

for thread in threads:
    thread.join()

dic_already_done = {}

for key in all_proximity_cities:
    for city in all_proximity_cities[key]:
        dic_already_done[city] = []

for key in all_proximity_cities:
    for city in all_proximity_cities[key]:
        for proximity in all_proximity_cities[key][city]:
            if proximity not in dic_already_done[city]:
                proximity_cities[key][city].append(proximity)
                dic_already_done[city].append(proximity)

for key in proximity_cities:
    list_pms = []
    #list_non_white = []
    #list_non_white_or_asian = []
    for city in proximity_cities[key]:
        for proximity in proximity_cities[key][city]:
            col = pm_data.loc[pm_data["TOWN"] == proximity.upper()]
            list_pms.append(float(col["PM"]))
            #list_non_white.append(float(col["Proportion Non-White Population"].values[0]))
        #    list_non_white_or_asian.append(float(col["Proportion Non-White or Asian Population"].values[0]))
    mean_pm = sum(list_pms)/len(list_pms)
    proximity_means[key].append(mean_pm)
    #mean_non_white = sum(list_non_white)/len(list_non_white)
    #mean_non_white_or_asian = sum(list_non_white_or_asian)/len(list_non_white_or_asian)
    #proximity_means[key].append(mean_non_white)
    #proximity_means[key].append(mean_non_white_or_asian)

df2 = pd.DataFrame(proximity_means)
df2.to_csv("proximity_to_NPL_sites_pm.csv", index = False)
