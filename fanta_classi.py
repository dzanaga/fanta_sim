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
        
        Team.num_teams += 1
        Team.teams_names.append(self.name)
        
    def get_name(self):
        return self.name
        
    def get_players_list(self):
        return self.players
        
    def get_abs_points(self):
        return self.abs_points
        
    def get_goals_scored(self):
        return self.goals_scored
    
    def set_goals_scored(self, goals):
        self.goals_scored += goals

    def get_goals_taken(self):
        return self.goals_taken
    
    def set_goals_taken(self, goals):
        self.goals_taken += goals
    
    def get_num_of_teams():
        return Team.num_teams
        
    def get_all_teams():
        return Team.name_teams
    
    def get_league_points(self):
        return self.league_points
    
    def set_league_points(self,points):
        self.league_points += points
        
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
        self.set_league_points(3)
        #self.points_update(day)
        
    def loss(self,day):
        self.vic_draw_losses[day] = 'L'
        #self.points_update(day)
        
    def draw(self,day):
        self.vic_draw_losses[day] = 'D'
        self.set_league_points(1)
        #self.points_update(day)
        
        
class Match(object):
    
    def __init__(self, team1, team2, day):
        self.team1 = team1
        self.team2 = team2
        self.day = day
        
    def play_match(self, SE=0):
        
        points1 = self.team1.abs_points
        points2 = self.team2.abs_points

        sum1 = sum(points1[-5:])
        sum2 = sum(points2[-5:])
        
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
        
        self.team1.set_goals_scored(temp1)
        self.team1.set_goals_taken(temp2)
        
        self.team2.set_goals_scored(temp2)
        self.team2.set_goals_taken(temp1)
        
        self.team1.set_goals_per_day(temp1, self.day)
        self.team2.set_goals_per_day(temp2, self.day)
        
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
        
        self.rank_data = {i:[self.teams[i].get_league_points(),\
                             sum(self.teams[i].get_abs_points()),\
                             self.teams[i].get_goals_scored()] for i in\
                             teams_names}
        
        self.final_rank = self.order_ranking()
        
    def play(self):
        
        for i in self.days:
            i.play_day(self.SE)
            
    def get_teams(self):
        return self.teams_obj
    
    def get_teams_points(self):
        L = {}
        for i in self.teams:
            L[i] = self.teams[i].league_points
        return L
        
    def print_points(self):
        for i in self.teams_names:
            print(i + ':\t {} points'.format(self.teams[i].league_points))

    def order_ranking(self):

        ordered_ranking = sorted(sorted(sorted(self.rank_data.items(),\
                                key = lambda x : x[1][2], reverse = True),\
                                key = lambda x : x[1][1], reverse = True),\
                                key = lambda x : x[1][0], reverse = True)

        return ordered_ranking

    
    def print_ranking(self):
        self.ranking()
        for i in self.ranking:
            print(i[0] + ':\t {} points'.format(i[1]))
            #print(':\t {} points'.format(i.league_points))
            
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
    
    def get_frankings_team(self,t_name):
        return self.teams_frankings[t_name]

    def plot_frankings(self):
        for i in range(len(teams_names)):
            plt.plot(range(1, len(teams_names)),
                     self.get_frankings_team(teams_names[i]))
            plt.xlabel('Piazzamenti')
            plt.ylabel(teams_names[i])
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
    
teams_names, players, abs_points = scraping('fantascandalo')

n_days = len(abs_points[teams_names[0]])
random_leagues = create_league_random(teams_names,1000)

list_leagues = [League(random_leagues[i],teams_names, n_days) for i in
                range(len(random_leagues))]
                
#%%
stats1 = Stats(list_leagues)
#stats2 = Stats(list_leagues, 2)
                
#list_leagues[0].play(0)