import time
import string
import numpy as np
import itertools
import os, random
import pandas as pd
import matplotlib.pylab as plt
import requests
import random

from bs4 import BeautifulSoup as bs

def check_unique_team(L):
    #flatten L and convert to string
    L_string = [item for sublist in L for item in sublist]
    if len(L_string) == len(set(L_string)):
        return True
    else:
        return False
        
def combinations_noteams(iterable, r):
    for matches in itertools.combinations(iterable, int(r)):
        #print(matches)
        if check_unique_team(matches):
            yield matches

def get_compatible_lists(giornata,giornate_list):
    gi = []
    for j in giornate_list:
        gg = []
        gg.append(giornata)
        gg.append(j)
        if len(set(flatten_list(gg))) == len(teams):
            gi.append(j)
    return gi

def get_compatible_lists2(giornata,giornate_list,n_teams):
    gi = []
    for j in giornate_list:
        gg = []
        gg.append(giornata)
        gg.append(j)
        if len(set(flatten_list(gg))) == n_teams:
            gi.append(j)
    return gi

def flatten_list(L): return [item for sublist in L for item in sublist]

def create_matches_days(teams):

    matches_iter = itertools.combinations(teams,2)
    matches = [i for i in matches_iter]
    
    days_iter = combinations_noteams(matches, len(teams)/2)

    days = [i for i in days_iter]

    return matches,days

def create_league(teams):
    
    L = []
    L_all = []
    matches, days = create_matches_days(teams)
    
    def create_league_subf(L, days):
        while len(L_all) == 0:
            for i in days:
                L1 = L.copy()
                L1.append(i)
                
                if len(L1) == len(teams) - 1:
                    L_all.append(L1)
                    
                else:
                    s1 = get_compatible_lists(i, days)
                    create_league_subf(L1, s1)
            
    create_league_subf(L, days)
    
    return L_all[0]

def create_league_random(teams,n_leagues):
    
    n_teams = len(teams)
    L_all = []
    matches, days = create_matches_days(teams)

    while len(L_all) < n_leagues:

        days0 = days.copy()
        L0 = []

        for i in range(n_teams-1):

            if len(days0):
                random_day = days0[random.randint(1,len(days0))-1]
                L0.append(random_day)
                days0 = get_compatible_lists2(random_day, days0, n_teams)

        if len(L0) == n_teams - 1:
            L_all.append(L0)
            
    return L_all

def gen_cal(days, girone):
    ''' Dal girone creo il calendario con tutte le partite del campionato. La variable
        days rappresenta il numero di giornate. La variabile girone è una lista ed è 
        l'output di all_tourn. L'output è una lista di tuples ed ogni tuples rappresenta
        una partita del torneo, già in ordine secondo il calendario.'''
    

    if days % len(girone) == 0:
#        return list(itertools.chain(*(girone * (days // len(girone)))))
        return girone * (days // len(girone))
    
    else:
        if days == 1:
            return [girone[0]]
            
        elif days > len(girone):
            temp = girone * (days // len(girone))
            resto = days % len(girone)
            for i in range(resto):
                temp.append(girone[i])
#            temp = list(itertools.chain(*temp))
            return temp
            
        else:
            temp = [i for i in girone[0:days]]
#            temp = list(itertools.chain(*temp))
            return temp

def get_abs_points(_list_):
    temp = list(_list_.children)
    temp2 = list(temp[0].children)
    
    res = (temp2[0].string, temp2[6].string,\
           float(temp2[2].string.replace(',', '.')),\
           float(temp2[4].string.replace(',', '.')))
    
    return res
    
def classifica(dati):
    '''dati è un dict (disordinato) nel quale ad ogni squadra è associato un tuple di 3 elementi.
       Questi 3 elementi rappresentano nell'ordine: punti, punti totali, gol segnati.
       L'output è unua lista di tuples (ordinata) che rappresenta la classifica finale.'''
       
    classifica_ordinata = sorted(sorted(sorted(dati.items(), key = lambda x : \
                            x[1][2], reverse = True), key = lambda x : x[1][1], \
                            reverse = True), key = lambda x : x[1][0], reverse = True)


    return classifica_ordinata
#%% Scraping teams' names, players and absolute points

def scraping(league_name):
    
    domain = 'http://leghe.fantagazzetta.com/'
    url = domain + league_name + '/tutte-le-rose'
    link = requests.get(url)
    soup = bs(link.content, 'lxml')
    tr = soup.find_all('tr')
    
    teams = []
    players_list = []
    
    for i in tr:
        if len(i) == 3:
            teams.append(list(i.children)[0].string)
        else:
            temp = list(i.children)
            players_list.append((temp[0].string, temp[1].string,\
                                 temp[2].string, int(temp[3].string)))
            
    ppt = len(players_list) // len(teams)                                      # Players Per Team
            
    players = {i:players_list[(teams.index(i) * ppt):(teams.index(i) + 1)\
                                 * ppt] for i in teams}
                  
    
    url = domain + league_name + '/calendario'
    link = requests.get(url)
    soup = bs(link.content, 'lxml')
    tr = soup.find_all('tr')
    
    abs_points = {i:[] for i in teams}
    
    for i in tr:
        if len(i) == 2:
            res = get_abs_points(i)
            abs_points[res[0]].append(res[2])
            abs_points[res[1]].append(res[3])
            
    return teams, players, abs_points
    
def play_league(team1, team2, day, SE):
    
    temp = Match(team1, team2, day)
    temp2 = Match.get_result(team1, team2, day, SE)
    
    if temp2[2] > temp2[3]:
        points[temp2[0]] += 3
    elif temp2[2] < temp2[3]:
        points[temp2[1]] += 3
    else:
        points[temp2[0]] += 1
        points[temp2[1]] += 1
    
    return points

#%%

'''
teams, players, abs_points = scraping('fantascandalo')
points = {i:0 for i in teams}

galli = Team('FC BOMBAGALLO')
pasta = Team('FC Pastaboy')

for i in range(26):
    play_league(pasta, galli, i, SE = 'Sì')
print(points)
'''