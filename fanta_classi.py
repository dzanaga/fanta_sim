import time
import string
import numpy as np
import itertools
import os, random
import pandas as pd
import matplotlib.pylab as plt



class Team(object):
    num_teams = 0
    name_teams = []
    def __init__(self, name, players_list):
        self.name = name
        self.players_list = players_list
        self.abs_points = 0
        self.position = 0
        self.goals = 0
        Team.num_teams += 1
        Team.name_teams.append(self.name)
        
    def get_name():
        return self.name
        
    def get_players_list():
        return self.players_list
        
    def get_abs_points():
        return self.abs_points
        
    def get_position():
        return self.position
        
    def get_goals():
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
        
    def get_result(team1, team2, day):
        temp1 = int(((df_teams[team1.name][day] - 66) // 6) + 1)
        temp2 = int(((df_teams[team2.name][day] - 66) // 6) + 1)
        team1.goals += temp1
        team2.goals += temp2
        if temp1 < 0:
            temp1 = 0
        if temp2 < 0:
            temp2 = 0
        
#        print('%s - %s     %s - %s' % (team1.name, team2.name, temp1, temp2))
        return (team1.name, team2.name, temp1, temp2)
        
def assign_teams(teams):
    letters = [i for i in string.ascii_lowercase[0:len(teams)]]
    alias = {}
    for i in letters:
        alias['{}'.format(i)] = teams[letters.index(i)]
        
    for i in alias:
        i = Team(alias[i], ['list_of_players'])
        
def get_random_line(file_name):
    total_bytes = os.stat(file_name).st_size 
    random_point = random.randint(0, total_bytes)
    file = open(file_name)
    file.seek(random_point)
    file.readline() # skip this line to clear the partial line
    temp = file.readline()
    file.close()
    return temp
        
        
#==============================================================================
# #%%        
# 
# roxy = Team('FC Roxy', ['lista squadra'], 66.5, 5)
# ciolle = Team('Ciolle United', ['lista squadra'], 78.5, 2)
# 
# #%%
# 
# temp = Match(roxy, ciolle, 3)
# 
# #%%
# 
# df_teams = {'FC Roxy': [72, 66], 'Ciolle United': [78, 66.5]}
#==============================================================================


names = ['Ciolle United', 'FC Pastaboy', 'Bucalina FC', 'LA CORRAZZATA POTEMKIN',\
         'Fc Stress', 'FC Roxy', 'FC BOMBAGALLO', 'AC PICCHIA']
         
teams = assign_teams(names)

league = get_random_line('leagues_%s_teams_lines.txt' % len(names))

print(league)















