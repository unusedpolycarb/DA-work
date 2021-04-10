import requests
import pandas as pd
import threading
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, WebDriverException
from bs4 import BeautifulSoup
from requests import HTTPError, ConnectionError, Timeout

try:
    df = pd.read_csv(path);
except (FileNotFoundError) as e:
    print(e)

print()
list_id = []
list_reviews_in_dic = []

for i in range(len(df.index)):
    if not df.iloc[i, 0] == "":
        list_id.append({df.iloc[i, 0]: df.iloc[i, 1]})

print(len(list_id))
def generate_reviews(df, index, start, end):
    dic_to_add = {}
    redo_counter = 0
    for i in range(start, end):
        reviews = []
        page_num = 0
        has_next_page = True
        while has_next_page == True:
            if redo_counter < 10:
                try:
                    if page_num == 0:
                        url = "https://www.yelp.com/biz/{}".format(df.iloc[i, 1])
                    else:
                        url = "https://www.yelp.com/biz/{}?start={}".format(df.iloc[i, 1], page_num*20)
                    page = requests.get(url)
                    if not page.ok:
                        break
                    soup = BeautifulSoup(page.content, "html.parser")
                    next_page_button = soup.findAll('a', {"class": "page-option prev-next next"})
                    review_content = soup.findAll('p', {"itemprop": "description"})
                    for review in review_content:
                        reviews.append(review.text)
                    has_next_page = False
                    if not len(next_page_button) == 0:
                        has_next_page = True
                        page_num+=1
                except(HTTPError) as e:
                    break
                except(TimeoutError, MemoryError, OSError, SystemError, RuntimeError, ConnectionError, Timeout) as e:
                    redoCounter+=1

        dic_to_add[df.iloc[i, 0]] = reviews
    list_reviews_in_dic[index] = dic_to_add

threads = []
num_partitions = int(input("How many threads should be created?: "))
num_cols = int(len(list_id)/num_partitions)
list_starting = []
list_ending = []
for i in range(num_partitions):
    dic_to_add = {}
    list_reviews_in_dic.append(dic_to_add)
    list_starting.append(int(i * num_cols))
    if(not i == (num_partitions - 1)):
        list_ending.append((i + 1) * num_cols) #splits up csv
    else:
        list_ending.append(len(df.index)) #final split takes till eof

for i in range(len(list_starting)):
    threads.append(threading.Thread(target = generate_reviews, args = (df, i, list_starting[i], list_ending[i])))
    threads[i].start() #starts each thread

for thread in threads:
    thread.join()

list_formatted_id = []
list_reviews = []
for dic_of_review in list_reviews_in_dic:
    for review_key in dic_of_review:
        for review in dic_of_review[review_key]:
            list_formatted_id.append(review_key)
            list_reviews.append(review)

final_format = {"Business ID": list_formatted_id, "Reviews": list_reviews}
new_df = pd.DataFrame(final_format)
new_df.to_csv(outfile, index = False)
