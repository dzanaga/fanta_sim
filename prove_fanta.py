import sys
sys.path.append('C:/Users/Andrea/Desktop/fanta_sim_dz')
import time
import string
import numpy as np
import itertools
import os, random
import pandas as pd
import matplotlib.pylab as plt
import requests
from bs4 import BeautifulSoup as bs
from fanta_calendario import *

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
        
    def empty():
        Team.num_teams = 0
        Team.name_teams = []
        
class Match(object):
    def __init__(self, team1, team2, day):
        self.team1 = team1.name
        self.team2 = team2.name
        self.day = day
        
    def get_result(team1, team2, day, weight, SE = 'No'):
        
        points1 = abs_points[team1]
        points2 = abs_points[team2]
        sum1 = sum(abs_points[team1][0:day])
        sum2 = sum(abs_points[team2][0:day])

        if SE == 'No' or day < len(teams) or sum1 == sum2:
            temp1 = int(((points1[day - 1] - 66) // 6) + 1)
            temp2 = int(((points2[day - 1] - 66) // 6) + 1)
            if temp1 < 0:
                temp1 = 0
            if temp2 < 0:
                temp2 = 0
#==============================================================================
#             team1.goals += temp1
#             team2.goals += temp2
#==============================================================================
        
        elif SE == 'Sì' and sum1 > sum2:
            factor = ((sum1 - sum2) // day) * weight
            temp1 = int(((points1[day - 1] - 66) // 6) + 1)
            temp2 = int(((points2[day - 1] - (66 + factor)) // 6) + 1)
            if temp1 < 0:
                temp1 = 0
            if temp2 < 0:
                temp2 = 0
#==============================================================================
#             team1.goals += temp1
#             team2.goals += temp2
#==============================================================================
                
        elif SE == 'Sì' and sum1 < sum2:
            factor = ((sum2 - sum1) // day) * weight
            temp1 = int(((points1[day - 1] - (66 + factor)) // 6) + 1)
            temp2 = int(((points2[day - 1] - 66) // 6) + 1)
            if temp1 < 0:
                temp1 = 0
            if temp2 < 0:
                temp2 = 0
#==============================================================================
#             team1.goals += temp1
#             team2.goals += temp2
#==============================================================================
        
        return (team1, team2, temp1, temp2)
        
def get_abs_points(_list_):
    temp = list(_list_.children)
    temp2 = list(temp[0].children)
    
    res = (temp2[0].string, temp2[6].string,\
           float(temp2[2].string.replace(',', '.')),\
           float(temp2[4].string.replace(',', '.')))
    
    return res

#Scraping teams' names, players and absolute points

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
    
def play_match(team1, team2, day, points, weight, SE):
    
    temp = Match.get_result(team1, team2, day, weight, SE)
    
    if temp[2] > temp[3]:
        points[temp[0]] += 3
    elif temp[2] < temp[3]:
        points[temp[1]] += 3
    else:
        points[temp[0]] += 1
        points[temp[1]] += 1
    
    return points
    
def play_league(cal, days, weight, SE):
    
    dati = {}
    points = {i:0 for i in teams}

    for i in cal:
        for j in i:
            play_match(j[0], j[1], (cal.index(i) + 1), points, weight, SE)
            
    for i in points:
        dati[i] = (points[i], (dict_teams[i].get_abs_points())[0:days])

    return classifica(dati)
    
#==============================================================================
# def play_all_leagues(n_leagues, days, weight, SE):
#     
#     wins = {i: 0 for i in teams}
#     rounds = create_league_random(teams,n_leagues)
#     
#     for i in rounds:
#         cal = gen_cal(days, i)
#         league = play_league(cal, weight, SE)
#         wins[]
# 
#==============================================================================
#%%

teams, players, abs_points = scraping('fantascandalo')

#%%

dict_teams = {i: Team(i) for i in teams}

#%%


rounds = create_league_random(teams,1)

#%%

cal = gen_cal(26, rounds[0])

print(play_league(cal, 26, 1, SE = 'No'))







