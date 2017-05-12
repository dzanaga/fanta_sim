import time
import string
import copy
import sys
import numpy as np
import itertools
import os, random
import pandas as pd
import matplotlib.pylab as plt
from matplotlib import cm
import requests
from bs4 import BeautifulSoup as bs
from fanta_calendario import *

sys.setrecursionlimit(10000)

class Team(object):
    num_teams = 0
    teams_names = []
    def __init__(self, name):
        self.name = name
        self.players = players[self.name]
        self.abs_points = abs_points[self.name]
        self.league_points = 0
        self.goals_scored = 0
        self.goals_taken = 0
        self.vic_draw_losses = {}
        self.goals_per_day = {}
        self.vittorie = 0
        self.sconfitte = 0
        self.pareggi = 0
        self.diff_reti = self.goals_scored - self.goals_taken
        
        Team.num_teams += 1
        Team.teams_names.append(self.name)
        
    def get_goals_per_day(self, day):
        return self.goals_per_day[day]

    def set_goals_per_day(self, goals, day):
        self.goals_per_day[day] = goals
        
    def points_update(self,day):
        #Update points of team up to day
        self.league_points = 0
        for i in range(1,day+1):
            if self.vic_draw_losses[i] == 'V':
                self.league_points += 3
            elif self.vic_draw_losses[i] == 'L':
                self.league_points += 0
            elif self.vic_draw_losses[i] == 'D':
                self.league_points += 1
                
                
    def victory(self,day):
        self.vic_draw_losses[day] = 'V'
        self.league_points += 3
        self.vittorie += 1
        #self.points_update(day)
        
    def loss(self,day):
        self.vic_draw_losses[day] = 'L'
        self.sconfitte += 1
        #self.points_update(day)
        
    def draw(self,day):
        self.vic_draw_losses[day] = 'D'
        self.league_points += 1
        self.pareggi += 1
        #self.points_update(day)
        
        
class Match(object):
    
    def __init__(self, team1, team2, day):
        self.team1 = team1
        self.team2 = team2
        self.day = day
        
    def play_match(self, SE=0):
        
        points1 = self.team1.abs_points
        points2 = self.team2.abs_points

        sum1 = sum(points1[-7:])
        sum2 = sum(points2[-7:])
        
        if self.day < len(teams_names) or sum1 == sum2:
            temp1 = int(((points1[self.day - 1] - 66) // 6) + 1)
            temp2 = int(((points2[self.day - 1] - 66) // 6) + 1)
        elif sum1 > sum2:
            factor = ((sum1 - sum2) // self.day) * SE
            temp1 = int(((points1[self.day - 1] - 66) // 6) + 1)
            temp2 = int(((points2[self.day - 1] - (66 + factor)) // 6) + 1)
        else:
            factor = ((sum2 - sum1) // self.day) * SE
            temp1 = int(((points1[self.day - 1] - (66 + factor)) // 6) + 1)
            temp2 = int(((points2[self.day - 1] - 66) // 6) + 1)
            
        if temp1 < 0:
            temp1 = 0
        if temp2 < 0:
            temp2 = 0
        
        self.team1.goals_scored += temp1
        self.team1.goals_taken += temp2
        
        self.team2.goals_scored += temp2
        self.team2.goals_taken += temp1
        
        self.team1.set_goals_per_day(temp1, self.day)
        self.team2.set_goals_per_day(temp2, self.day)
        
        self.team1.diff_reti = self.team1.goals_scored - self.team1.goals_taken
        self.team2.diff_reti = self.team2.goals_scored - self.team2.goals_taken
        
        
        if temp1 > temp2:
            self.team1.victory(self.day)
            self.team2.loss(self.day)
        elif temp1 < temp2:
            self.team2.victory(self.day)
            self.team1.loss(self.day) 
        else:
            self.team2.draw(self.day)
            self.team1.draw(self.day)
            
class Day(object):
    # class defines a Day, consisting of several Matches objects
    
    def __init__(self, list_matches, day):
        self.list_matches = list_matches
        self.day = day
        
    def play_day(self, SE):
        for i in self.list_matches:
            i.play_match(SE)

class League(object):
    
    def __init__(self, calendar, teams_names, n_days, SE=0):
        
        #la variabile calendar rappresenta il girone da ripetere sulle n_days giornate
        self.calendar = calendar
        self.days = []
        self.teams = {i:Team(i) for i in teams_names}
        self.teams_names = teams_names
        self.SE = SE
        self.classifica_provv = {i:[] for i in teams_names}
        
        n_teams = len(self.teams_names)
        day = 0
        
        for i in range(n_days):
            m = []
            day += 1
            day_schedule = self.calendar[i%(n_teams-1)]

            for match in day_schedule: #crea una giornata
                m.append(Match(self.teams[match[0]],self.teams[match[1]],day))
                
            d = Day(m,day)
            
            self.days.append(d)
            
        self.play()
        
#==============================================================================
#         self.rank_data = {i:[self.teams[i].league_points,\
#                              len(self.days),\
#                              self.teams[i].vittorie,\
#                              self.teams[i].pareggi,\
#                              self.teams[i].sconfitte,\
#                              self.teams[i].goals_scored,\
#                              self.teams[i].goals_taken,\
#                              self.teams[i].diff_reti,\
#                              sum(self.teams[i].abs_points[0:n_days])] for i in\
#                              teams_names}
#==============================================================================
        
#        self.final_rank = self.order_ranking()
        
    def play(self):
        
        for i in self.days:
            i.play_day(self.SE)
            self.rank_data = {i:[self.teams[i].league_points,\
                             len(self.days),\
                             self.teams[i].vittorie,\
                             self.teams[i].pareggi,\
                             self.teams[i].sconfitte,\
                             self.teams[i].goals_scored,\
                             self.teams[i].goals_taken,\
                             self.teams[i].diff_reti,\
                             sum(self.teams[i].abs_points[0:n_days])] for i in\
                             teams_names}
            self.final_rank = self.order_ranking()
            for j in self.final_rank:
                self.classifica_provv[j[0]].append(j[1][0])
    
    def get_teams_points(self):
        L = {}
        for i in self.teams:
            L[i] = self.teams[i].league_points
        return L
        
    def print_points(self):
        for i in self.teams_names:
            print(i + ':\t {} points'.format(self.teams[i].league_points))

    def order_ranking(self):

        ordered_ranking = sorted(sorted(sorted(sorted(self.rank_data.items(),\
                                key = lambda x : x[1][6], reverse = True),\
                                key = lambda x : x[1][5], reverse = True),\
                                key = lambda x : x[1][8], reverse = True),\
                                key = lambda x : x[1][0], reverse = True)

        return ordered_ranking
            
    def print_order_ranking(self):
        data = []
        names = []
        first_row = ['Points', 'Matches', 'V', 'D', 'L', 'GS', 'GT', 'D', 'Abs Points']
        for i in self.final_rank:
            names.append(i[0])
            data.append(i[1])
        
        table = pd.DataFrame(data, names, first_row)
        return table
            
    def print_league(self):
        c = 0
        for day in self.days:
            c += 1
            print('\n\n***************Giornata {}***************\n'.format(c))
            for match in day.list_matches:
                print(match.team1.name,'\t {} - {} \t'
                      .format(match.team1.get_goals_per_day(c),
                              match.team2.get_goals_per_day(c)),
                              match.team2.name)
        
class Stats(object):
    
    def __init__(self, list_leagues):
        self.list_leagues = list_leagues
        self.average_points = []
        self.positions = {}
        self.teams_names = list_leagues[0].teams_names
        self.teams_frankings = {i: [0 for _ in range(len(self.teams_names))]\
                                    for i in teams_names}
        self.gen_frankings()
        
        
    def gen_frankings(self):
        
        for i in self.list_leagues:
            for pos in range(len(self.teams_names)):
                           
                t_name = i.final_rank[pos][0]          
                self.teams_frankings[t_name][pos] += 1

    def plot_frankings(self):
        for i in range(len(teams_names)):
            plt.plot(range(1, len(teams_names) + 1),
                     self.teams_frankings[teams_names[i]], label=teams_names[i]
                     , linewidth=4)
            plt.xlabel('Piazzamenti')
            plt.ylabel(teams_names[i])
        plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
        plt.show()
            
    def avrg_points(self):
        
        from collections import Counter
    
        L = Counter({i:0 for i in teams_names})
        
        for i in self.list_leagues:
            d = i.get_teams_points()
            d = Counter(d)
            L += d
        
        L2 = {k: round(L[k]/len(self.list_leagues),2) for k in L.keys()}
        
        L3 = sorted([(i,L2[i]) for i in L2],key = lambda j: j[1], reverse = True)

            
        return L3
        
    def print_stats(L):
        people = list(zip(*L))[0]
        score = list(zip(*L))[1]
        x_pos = np.arange(len(people))
        
        slope, intercept = np.polyfit(x_pos, score, 1)
        trendline = intercept + (slope * x_pos)
        
        plt.plot(x_pos, trendline, color='red', linestyle='--')    
        plt.bar(x_pos, score, align = 'center')
        plt.xticks(x_pos, people, fontsize = 8)
        plt.ylabel('Media punti')
        plt.gcf().autofmt_xdate()
        plt.show()
    
#%%
    
teams_names, players, abs_points, real_round = scraping('fantascandalo')

n_days = len(abs_points[teams_names[0]])
#random_leagues = create_league_random(teams_names,1000)

#list_leagues1 = [League(i, teams_names, n_days, 2) for i in random_leagues]

#list_leagues2 = [League(i, teams_names, n_days, 2) for i in random_leagues]

our_league = League(real_round, teams_names, n_days, 0)

#stats = Stats(list_leagues1)

#stats2 = Stats(list_leagues2)

#%%
                
#==============================================================================
# lista_punti = {i: [] for i in teams_names}
# stats = [Stats(i) for i in L]
# for i in stats:    
#     punti_medi = i.avrg_points()
#     for z in punti_medi:
#         lista_punti[z[0]].append(z[1])
#==============================================================================

#%%

#==============================================================================
# plt.plot(SE_vals, lista_punti['FC Pastaboy'], label = 'FC Pastaboy')
# plt.plot(SE_vals, lista_punti['FC BOMBAGALLO'], label = 'FC BOMBAGALLO')
# plt.plot(SE_vals, lista_punti['Ciolle United'], label = 'Ciolle United')
# plt.plot(SE_vals, lista_punti['Fc Stress'], label = 'Fc Stress')
# plt.plot(SE_vals, lista_punti['FC ROXY'], label = 'FC ROXY')
# plt.plot(SE_vals, lista_punti['Bucalina FC'], label = 'Bucalina FC')
# plt.plot(SE_vals, lista_punti['LA CORRAZZATA POTEMKIN'], label = 'LA CORRAZZATA POTEMKIN')
# plt.plot(SE_vals, lista_punti['AC PICCHIA'], label = 'AC PICCHIA')
# #plt.axis([-2.5, 22.5, 22, 31])
# plt.xlabel('Peso soglie elastiche')
# plt.ylabel('Media punti su 1000 campionati')
# plt.title('Media Punti vs Soglie Elastiche')
# plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
# plt.show()
#==============================================================================

#%%
#==============================================================================
# counts = 0
# for i in list_leagues:
#     if i.final_rank[0][0] == 'FC Pastaboy' and i.final_rank[1][0] == 'Bucalina FC'\
#     and i.final_rank[2][0] == 'Fc Stress' and i.final_rank[3][0] == 'LA CORRAZZATA POTEMKIN'\
#     and i.final_rank[4][0] == 'Ciolle United' and i.final_rank[5][0] == 'FC BOMBAGALLO'\
#     and i.final_rank[6][0] == 'FC ROXY' and i.final_rank[7][0] == 'AC PICCHIA':
#         counts += 1
# #print(str((counts*100)/len(list_leagues)) + ' %')
# 
# print(counts)
#==============================================================================
        
        
#%%
        
def plot_league(our_league, team):
    team_points = []
    for i in range(len(our_league.classifica_provv[team])):
        val = 100
        for j in our_league.classifica_provv:
            if our_league.classifica_provv[j][i] < val:
                val = our_league.classifica_provv[j][i]
        team_points.append(our_league.classifica_provv[team][i] - val)
        
#==============================================================================
#     plt.plot(team_points)
#     plt.show()
#==============================================================================
    return team_points
    
#%%
#==============================================================================
# aaa = {}
# for i in teams_names:
#     temp = plot_league(our_league, i)
#     aaa[i] = temp
#     plt.plot(aaa[i], label = i)
#     plt.xlabel('Giornate')
#     plt.ylabel('Diff punti con ultimo posto')
# plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
# plt.show()
#==============================================================================

#%% Gol Mertens

mertens = [[9, 1], [15, 3], [16, 4], [17, 1], [19, 1], [21, 1],\
            [22, 3], [26, 2], [27, 1], [28, 1], [31, 1]]

goals_m = 19

def no_mertens(hyp_goals, mertens):
    counts = 0
    mertens2 = copy.deepcopy(mertens)
    abs_points = {z:0 for z in teams_names}
    for x in abs_points:
        temp = abs_points2[x]
        abs_points[x] = temp
    while counts < (goals_m - hyp_goals):
        temp = random.choice(mertens2)
        if temp[1] != 0:
            abs_points['FC Pastaboy'][temp[0] - 1] -= 3.0
            counts += 1
            temp[1] -= 1
    
    new_league = League(real_round, teams_names, n_days, 0)
    
    return new_league.order_ranking()



def sim_no_mert(hyp_goals, trials):
    new_dict = {i:0 for i in teams_names}
    for i in range(trials):
        abs_points = {z:0 for z in teams_names}
        for x in abs_points:
            temp = abs_points2[x]
            abs_points[x] = temp
        res = no_mertens(hyp_goals, mertens)
        for y in res:
            new_dict[y[0]] += y[1][0]
            
    for i in new_dict:
        new_dict[i] /= trials
        
    return sorted(new_dict.items(), key = lambda x: x[1], reverse = True)
    


abs_points2 = {z:0 for z in teams_names}
for x in abs_points:
    temp = abs_points[x]
    abs_points2[x] = temp






