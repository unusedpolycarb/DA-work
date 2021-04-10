from selenium import webdriver
from selenium.common.exceptions import StaleElementReferenceException
import pandas as pd
import time
import os

driver = webdriver.Chrome(executable_path = r"C:\Users\novac\Documents\program_files\chromedriver.exe")
df = pd.read_csv(r"C:\Users\novac\Documents\cvt\covid-and-climate\list_of_NPL_sites.csv")
df = df.drop_duplicates(subset = "City", keep = "first")
max_proximity = int(input("How many kilometers away do you want to search (please enter a multiple of 5): "))
while not max_proximity%5 == 0:
    max_proximity = int(input("How many kilometers away do you want to search (please enter a multiple of 5): "))

driver.get("https://www.freemaptools.com/find-cities-and-towns-inside-radius.htm")

for i in range(len(df["City"].index)):
    try:
        city = df["City"][i] + ", MA"
        for i in [5 * x for x in range(1, int((max_proximity+5)/5))]:
            attempts = 0
            time.sleep(.1)
            km_to_search = str(i)
            while attempts < 5:
                try:
                    element = driver.find_element_by_xpath("//*[@id='tb_radius']")
                    element.clear()
                    element.send_keys(km_to_search)
                    element = driver.find_element_by_xpath("//*[@id='tb_place']")
                    element.clear()
                    element.send_keys(city)
                    driver.find_element_by_xpath("//*[@id='go_button']").click()
                    while len(driver.find_elements_by_id("btnDownloadCSV")) == 0:
                        continue
                    time.sleep(3)
                    driver.find_element_by_xpath("//*[@id='btnDownloadCSV']").click()
                    os.chdir(r"C:\Users\novac\Downloads")
                    while not os.path.exists("20200726.csv"):
                        continue
                    os.rename("20200726.csv",'{}_kilometers_{}.csv'.format(km_to_search, city.split(",")[0]))
                    break
                except(StaleElementReferenceException) as e:
                    attempts = attempts + 1
    except (KeyError) as e:
        continue

driver.close()
