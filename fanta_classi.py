import time
import string
import numpy as np
import itertools
import os, random
import pandas as pd
import matplotlib.pylab as plt
import requests
from bs4 import BeautifulSoup as bs

#%%

class Team(object):
    num_teams = 0
    name_teams = []
    def __init__(self, name):
        self.name = name
        self.players = players[self.name]
        self.abs_points = abs_points[self.name]
        self.position = 0
        self.goals = 0
        Team.num_teams += 1
        Team.name_teams.append(self.name)
        
    def get_name(self):
        return self.name
        
    def get_players_list(self):
        return self.players
        
    def get_abs_points(self):
        return self.abs_points
        
    def get_position(self):
        return self.position
        
    def get_goals(self):
        return self.goals
        
    def get_num_of_teams():
        return Team.num_teams
        
    def get_all_teams():
        return Team.name_teams
        
class Match(object):
    def __init__(self, team1, team2, day):
        self.team1 = team1.name
        self.team2 = team2.name
        self.day = day
        
    def get_result(team1, team2, day, SE = 'No'):
        
        points1 = abs_points[team1.name]
        points2 = abs_points[team2.name]
        sum1 = sum(abs_points[team1.name][0:day])
        sum2 = sum(abs_points[team2.name][0:day])

        if SE == 'No' or day < len(teams) or sum1 == sum2:
            temp1 = int(((points1[day - 1] - 66) // 6) + 1)
            temp2 = int(((points2[day - 1] - 66) // 6) + 1)
            team1.goals += temp1
            team2.goals += temp2
            if temp1 < 0:
                temp1 = 0
            if temp2 < 0:
                temp2 = 0
        
        if SE == 'Sì' and sum1 > sum2:
            factor = (sum1 - sum2) // day
            temp1 = int(((points1[day - 1] - 66) // 6) + 1)
            temp2 = int(((points2[day - 1] - (66 + factor)) // 6) + 1)
            team1.goals += temp1
            team2.goals += temp2
            if temp1 < 0:
                temp1 = 0
            if temp2 < 0:
                temp2 = 0
                
        if SE == 'Sì' and sum1 < sum2:
            factor = (sum2 - sum1) // day
            temp1 = int(((points1[day - 1] - (66 + factor)) // 6) + 1)
            temp2 = int(((points2[day - 1] - 66) // 6) + 1)
            team1.goals += temp1
            team2.goals += temp2
            if temp1 < 0:
                temp1 = 0
            if temp2 < 0:
                temp2 = 0
        
        return (team1.name, team2.name, temp1, temp2)
        
#==============================================================================
# def assign_teams(teams):
#     letters = [i for i in string.ascii_lowercase[0:len(teams)]]
#     alias = {}
#     for i in letters:
#         alias['{}'.format(i)] = teams[letters.index(i)]
#         
#     for i in alias:
#         i = Team(alias[i], ['list_of_players'])
#         
# def get_random_line(file_name):
#     total_bytes = os.stat(file_name).st_size 
#     random_point = random.randint(0, total_bytes)
#     file = open(file_name)
#     file.seek(random_point)
#     file.readline() # skip this line to clear the partial line
#     temp = file.readline()
#     file.close()
#     return temp
#==============================================================================
    
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

def gen_cal(days, girone):
    ''' Dal girone creo il calendario con tutte le partite del campionato. La variable
        days rappresenta il numero di giornate. La variabile girone è una lista ed è 
        l'output di all_tourn. L'output è una lista di tuples ed ogni tuples rappresenta
        una partita del torneo, già in ordine secondo il calendario.'''
    

    if days % len(girone) == 0:
        return list(itertools.chain(*(girone * (days // len(girone)))))
    
    else:
        if days == 1:
            return girone[0]
            
        elif days > len(girone):
            temp = list(girone * (days // len(girone)))
            resto = days % len(girone)
            temp.append(list(itertools.chain(*(girone[0 : resto]))))
            temp = list(itertools.chain(*temp))
            return temp
            
        else:
            temp = [i for i in girone[0:days]]
            temp = list(itertools.chain(*temp))
            return temp
            
#==============================================================================
# def organize_round(line):
#     days = []
#     girone = []
#     list_line = [i for i in line[:-1]]
#     while len(girone) < len(teams) - 1:
#         while len(days) < len(teams) // 2:
#             a = list_line[0]
#             b = list_line[1]
#             days.append((a, b))
#             del list_line[:2]
#         girone.append(days)
#         days = []
#     return girone
#==============================================================================
        
def get_abs_points(_list_):
    temp = list(_list_.children)
    temp2 = list(temp[0].children)
    
    res = (temp2[0].string, temp2[6].string,\
           float(temp2[2].string.replace(',', '.')),\
           float(temp2[4].string.replace(',', '.')))
    
    return res
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


teams, players, abs_points = scraping('fantascandalo')
points = {i:0 for i in teams}

galli = Team('FC BOMBAGALLO')
pasta = Team('FC Pastaboy')

for i in range(26):
    play_league(pasta, galli, i, SE = 'Sì')
print(points)









