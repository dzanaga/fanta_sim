import bs4
import urllib
import pandas as pd
import re
import requests
import numpy as np

def string_from_tab(a):
    L = []
    for i in a.descendants:
        if type(i) is bs4.NavigableString:
            L.append(i)
    return L

def scrape_names_points(league_name = 'fantascandalo'):
    
    domain = 'http://leghe.fantagazzetta.com/'
    
    url = domain + league_name + '/tutte-le-rose'

    source = requests.get(url)
    soup = bs4.BeautifulSoup(source.content, "lxml")

    tr = soup.find_all('tr')
    team_names = []
    for i in tr:
        trows = [k.string for k in i.children]
        for j in range(len(trows)):
            if trows[j] == "squadra":
                team_names.append(trows[j-1])  
                print(trows[j-1])   

    a = np.empty((36,len(team_names)))
    a[:] = np.nan
    df_teams = pd.DataFrame(data = a, index = np.arange(36)+1, columns=team_names)
    df_teams.head()

    url = domain + league_name + '/calendario'
    source = requests.get(url)
    soup = bs4.BeautifulSoup(source.content, "lxml")
    tr = soup.find_all('tr')    

    L = []
    trows = []
    for i in range(len(tr)):
        L.append(string_from_tab(tr[i]))


    index_list = []

    c = 0
    for i in L:
        if 'GIORNATA' in i[0]:
            c += 1
        elif 'Dettagli' in i[0]:
            pass
        else:

            try:
                df_teams.loc[c,i[0]]= i[2]
                df_teams.loc[c,i[6]]= i[4]
            except IndexError:
                break

    return team_names, df_teams
    
team_names, df_teams =  scrape_names_points('anal')

df_teams.head(28)