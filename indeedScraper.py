import requests
from bs4 import BeautifulSoup
import csv
import pandas as pd
from time import sleep
from random import randint
import time as t
from IPython.core.display import clear_output
from warnings import warn

start_time = t.time()
request = 0
pages = [str(i) for i in range(0,60,10)]

for page in pages:
    
    #make a request
    response = requests.get('https://www.imdb.com/search/title/?groups=top_1000&sort=user_rating,desc&count=100&start='+page)

    sleep(randint(1,3))

    request += 1
    elapsed_time = t.time()-start_time
    print('request:{}; Frequency:{} requests/s'.format(request,request/elapsed_time))    
    clear_output(wait = True)

    if response.status_code != 200:
        warn('Request: {}; Status code: {}'.format(request, response.status_code))

    # Break the loop if the number of requests is greater than expected
    if request > 7:
        warn('Number of requests was greater than expected.')
        break

    soup = BeautifulSoup(response.content,'lxml')

    
    for job in soup.find_all('div',class_='jobsearch-SerpJobCard'):
        job_title = job.find('a',class_='jobtitle')['title']
        print(job_title)