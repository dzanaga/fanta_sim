import bs4
import urllib
import pandas as pd
import re
import requests
import numpy as np
from IPython.core.display import display, HTML

url = 'http://leghe.fantagazzetta.com/fantascandalo/tutte-le-rose'
# url = 'http://leghe.fantagazzetta.com/fantascandalo/calendario'
source = requests.get(url)
soup = bs4.BeautifulSoup(source.content, "lxml")

# print(soup.prettify())

tr = soup.find_all('tr')
team_names = []
for i in tr:
    trows = [k.string for k in i.children]
    for j in range(len(trows)):
        if trows[j] == "squadra":
            team_names.append(trows[j-1])  
            print(trows[j-1])
            
a = np.random.rand(36,8)
a[:] = (a[:]*30+60)*2
a = a.round()/2

df_teams = pd.DataFrame(data = a, index = np.arange(36)+1, columns=team_names)
df_teams.head()