import requests
from bs4 import BeautifulSoup
import csv
import pandas as pd
from time import sleep
from random import randint
import time as t
from IPython.core.display import clear_output
from warnings import warn




# Lists to store the scraped data in
names =[]
release_date =[]
time =[]
genre =[]
imdb_rating =[]
metascore =[]


pages = [str(i) for i in range(201,601,100)]
start_time = t.time()
request = 0




for page in pages:

    #make a request
    response = requests.get('https://www.imdb.com/search/title/?groups=top_1000&sort=user_rating,desc&count=100&start='+page)

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
    if request > 50:
        warn('Number of requests was greater than expected.')
        break

    
    soup = BeautifulSoup(response.content,'lxml')

    for movies in soup.find_all('div', class_='lister-item mode-advanced'):
        if movies.find('div', class_ = 'ratings-metascore') is not None:
            #list movies title
            movies_title = movies.h3.a.text
            names.append(movies_title)

            # list movies released date
            movies_rel_date = (movies.find('span',class_='lister-item-year').text.strip("()"))
            release_date.append(movies_rel_date)

            movies_time = int(float(movies.find('span',class_='runtime').text.replace('min','')))
            time.append(movies_time)

            movies_genre = movies.find('span',class_='genre').text
            genre.append(movies_genre)

            movies_imdb_rating = float(movies.find('div',class_='ratings-imdb-rating')['data-value'])
            imdb_rating.append(movies_imdb_rating)


            movies_metascore = int(float(movies.find('span',class_='metascore').text))
            metascore.append(movies_metascore)


d = {'name':names,'date':release_date,'time':time,'genre':genre,'imdb':imdb_rating,'metascore':metascore}


df = pd.DataFrame(data=d)


print(df.info())

print(df.head(3))

df_max_min=df.describe().loc[['min', 'max'], ['imdb', 'metascore']]
print(df_max_min)

df.to_csv('movie_ratings.csv')



