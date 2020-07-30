import requests
from bs4 import BeautifulSoup
import csv
import pandas as pd
from time import sleep
from random import randint
import time as t
from IPython.core.display import clear_output
from warnings import warn

Title = []
Company = []
Rating = []
Location = []
Date = []
Summary = []


pages = [str(i) for i in range(0,60,10)]
request = 0
count = 0
start_time = t.time()


for page in pages:
    response = requests.get('https://www.indeed.com/jobs?q=software+developer&start='+page)
    allJobs = BeautifulSoup(response.content,'lxml')

    #pause the loop
    sleep(randint(1,3))

    #monitor the request
    request += 1
    elapsed_time = t.time()-start_time
    print('requests:{}; Frequency:{} request/s'.format(request,request/elapsed_time))
    clear_output(wait = True)

    #throw warning for non 200 status code response
    if response.status_code != 200:
        warn('Request: {}; Status code: {}'.format(request, response.status_code))

    # Break the loop if the number of requests is greater than expected
    if request > 10:
        warn('Number of requests was greater than expected.')
        break

    for jobs in allJobs.find_all('div',class_='jobsearch-SerpJobCard'):

        

        jobTitle = jobs.find('a',class_='jobtitle')['title']
        Title.append(jobTitle)

        company = jobs.find('span',class_='company').text
        Company.append(company)

        try:
            jobRating = int(float(jobs.find('span',class_='ratingsContent').text))
            Rating.append(jobRating)
        except AttributeError:
            Rating.append('0')
        
        try:
            companyLocation = str(jobs.find('span', class_='location').text)
            Location.append(companyLocation)
        except AttributeError:
            Location.append('Not mention')
        

        jobSummary = jobs.find('div', class_='summary').text
        Summary.append(jobSummary)

        date = jobs.find('span', class_='date').text.replace('days ago','').replace('+','')
        Date.append(date)
        
        count +=1


d = {'Title':Title,'Company':Company,'Location':Location,'Rating':Rating,'Date':Date,'Summary':Summary}
df = pd.DataFrame(data=d)
print(df.head(3))

print('total number of jobs:',count)

df.to_csv('indeedScraper.csv')