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
            
def organize_round(line):
    days = []
    girone = []
    list_line = [i for i in line[:-1]]
    while len(girone) < len(teams) - 1:
        while len(days) < len(teams) // 2:
            a = list_line[0]
            b = list_line[1]
            days.append((a, b))
            del list_line[:2]
        girone.append(days)
        days = []
    return girone
        
        
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


teams = ['Ciolle United', 'FC Pastaboy', 'Bucalina FC', 'LA CORRAZZATA POTEMKIN',\
         'Fc Stress', 'FC Roxy', 'FC BOMBAGALLO', 'AC PICCHIA']
         
assignments = assign_teams(teams)

league = get_random_line('leagues_{}_teams_lines.txt'.format(len(teams)))

rounds = organize_round(league)

cal = gen_cal(8, rounds)
















