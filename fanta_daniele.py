import time
import string
import numpy as np
import itertools

def print_league(L,n=0):
    if n == 0:
        n = len(L)
    c = 0
    for i in L:
        if c == n:
            break
        c += 1
        print('\nCampionato {}:'.format(c))
        for j in i:
            print(j)
            
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
        if len(set(flatten_list(gg))) == n_teams:
            gi.append(j)
    return gi

def flatten_list(L): return [item for sublist in L for item in sublist]

def create_teams_matches_days(n_teams):

    teams = [i for i in string.ascii_lowercase[0:n_teams]]

    matches_iter = itertools.combinations(teams,2)
    matches = [i for i in matches_iter]
    
    days_iter = combinations_noteams(matches, n_teams/2)

    days = [i for i in days_iter]

    return teams,matches,days

def create_league(glist):
    
    L = []
    L_all = []
    
    def create_league_subf(L,glist):

        for i in glist:
            L1 = L.copy()
            L1.append(i)
            
            if len(L1) == n_teams - 1:
                L_all.append(L1)
            else:
                s1 = get_compatible_lists(i,glist)
                create_league_subf(L1,s1)
            
    create_league_subf(L,glist)
    return L_all


n_teams = 8

teams,matches,days = create_teams_matches_days(n_teams)

start_time = time.time()

#leagues = create_league(days)


print("--- %s seconds ---" % (time.time() - start_time))
print(len(matches))
print(len(days))
#print(len(leagues))
#print_league(leagues,1) # print first 3 leagues
