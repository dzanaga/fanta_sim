import time
import string
import numpy as np
import itertools
import os, random
import pandas as pd
import matplotlib.pylab as plt


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
    
    def create_league_subf(L,glist, txt):

        for i in glist:
            L1 = L.copy()
            L1.append(i)
            
            if len(L1) == n_teams - 1:
                txt.write('%s\n' % ''.join(flatten_list(flatten_list(flatten_list(L1)))))
                
            else:
                s1 = get_compatible_lists(i,glist)
                create_league_subf(L1,s1, txt)
            
    create_league_subf(L,glist, txt)
#    return txt2

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
            
def classifica(dati):
    '''dati è un dict (disordinato) nel quale ad ogni squadra è associato un tuple di 3 elementi.
       Questi 3 elementi rappresentano nell'ordine: punti, punti totali, gol segnati.
       L'output è unua lista di tuples (ordinata) che rappresenta la classifica finale.'''
       
    classifica_ordinata = sorted(sorted(sorted(dati.items(), key = lambda x : \
                            x[1][2], reverse = True), key = lambda x : x[1][1], \
                            reverse = True), key = lambda x : x[1][0], reverse = True)


    return classifica_ordinata
            
def play_league(teams, goals, days, cal):
    letters = [i for i in string.ascii_lowercase[0:len(teams)]]
    alias = {}
    for i in letters:
        alias['{}'.format(i)] = teams[letters.index(i)]
    
    points = {i:0 for i in teams}
              
    dati = {}
              
    value = len(teams) // 2
    
    for i in range(len(cal)):
        match = []
        team1 = alias[cal[i][0]]
        team2 = alias[cal[i][1]]
        match.append(goals[team1][i // value])
        match.append(goals[team2][i // value])
        
        if match[0] > match[1]:
            points[team1] += 3
        elif match[0] < match[1]:
            points[team2] += 3
        else:
            points[team1] += 1
            points[team2] += 1

    for i in points:
        dati[i] = (points[i], punti_totali[i], sum(goals[i]))
    
    return classifica(dati)
    
def play_league_SE(teams, goals, absolute_points, days, cal):
    letters = [i for i in string.ascii_lowercase[0:len(teams)]]
    alias = {}
    for i in letters:
        alias['{}'.format(i)] = teams[letters.index(i)]
    
    points = {i:0 for i in teams}
              
    dati = {}
              
    value = len(teams) // 2
    
    for i in range(len(cal)):
        match = []
        team1 = alias[cal[i][0]]
        team2 = alias[cal[i][1]]
        points1 = absolute_points[team1][i // value]
        points2 = absolute_points[team2][i // value]
        difference = abs(points1 - points2)
        
        if points1 > points2:
            calcola_goals(punti)
        
            
        match.append(goals[team1][i // value])
        match.append(goals[team2][i // value])
        
        if match[0] > match[1]:
            points[team1] += 3
        elif match[0] < match[1]:
            points[team2] += 3
        else:
            points[team1] += 1
            points[team2] += 1

    for i in points:
        dati[i] = (points[i], punti_totali[i], sum(goals[i]))
    
    return classifica(dati)

def play_all_leagues(teams, goals, days, trials, SE = 'No'):
    
    vittorie = {i:[0 for j in range(len(teams))] for i in teams}
    
    if SE == 'No':    
        counts = 0
        for i in range(trials):
            league = get_random_line('leagues_%s_teams_lines - Copy.txt' % len(teams))
            if league != '':
                girone = organize_round(league)
                cal = gen_cal(days, girone)
                temp = play_league(teams, goals, days, cal)
                counts += 1
                for i in range(len(temp)):
                    squadra = temp[i][0]
                    vittorie[squadra][i] += 1
        else:
            break
    
    else:
        counts = 0
        for i in range(trials):
            league = get_random_line('leagues_%s_teams_lines - Copy.txt' % len(teams))
            if league != '':
                girone = organize_round(league)
                cal = gen_cal(days, girone)
        
        
        
    L = []
    for i in vittorie:
       L.append((round(vittorie[i][0] * 100 / counts, 2)))
       
    plt.plot(L,'rs')
    plt.axis([-1,8,-3,100])    
    plt.show()
    
    return vittorie, counts
    
def get_random_line(file_name):
    total_bytes = os.stat(file_name).st_size 
    random_point = random.randint(0, total_bytes)
    file = open(file_name)
    file.seek(random_point)
    file.readline() # skip this line to clear the partial line
    temp = file.readline()
    file.close()
    return temp
   
   
#%% Create text file
    
n_teams = 4

teams,matches,days = create_teams_matches_days(n_teams)

start_time = time.time()
txt = open('leagues_4_teams_lines.txt', 'a+')
leagues = create_league(days)
txt.close()


print("--- %s seconds ---" % (time.time() - start_time))

#%% Run simulation

teams = ['Ciolle United', 'FC Pastaboy', 'Bucalina FC', 'LA CORRAZZATA POTEMKIN',\
         'Fc Stress', 'FC Roxy', 'FC BOMBAGALLO', 'AC PICCHIA']
         

goals = {'Ciolle United':          [3,1,1,2,1,1,2,0,2,2,4,3,0,1,3,1,3,1,0,2,1,2,2,1,1,2,], \
         'FC Pastaboy':            [1,3,2,2,2,0,0,1,2,1,0,2,1,2,6,5,1,1,3,2,2,6,4,2,0,3,], \
         'Bucalina FC':            [2,3,0,3,1,2,2,1,1,2,3,1,1,1,0,1,1,1,0,2,3,2,2,2,1,2,], \
         'LA CORRAZZATA POTEMKIN': [0,3,3,2,1,0,0,2,2,0,3,2,3,0,0,0,2,1,2,1,3,2,2,1,2,3,], \
         'Fc Stress':              [0,0,2,1,0,0,0,3,0,2,1,1,1,1,2,0,0,3,3,3,2,1,3,2,2,3,], \
         'FC Roxy':                [3,1,1,1,1,1,1,3,3,2,0,2,0,1,2,2,1,2,1,1,0,4,2,2,4,1,], \
         'FC BOMBAGALLO':          [0,2,1,2,0,2,1,1,0,0,0,0,3,0,2,0,2,1,3,3,1,2,1,3,0,1,], \
         'AC PICCHIA':             [2,1,0,2,0,0,2,2,3,1,3,3,4,0,1,1,2,0,1,1,1,1,2,1,0,1,]}
         

punti_totali = {'Ciolle United': 1888, 'FC Pastaboy': 1953.5, 'Bucalina FC': 1871.5, \
               'LA CORRAZZATA POTEMKIN': 1873.5, 'Fc Stress': 1851.5, 'FC Roxy': 1886,\
               'FC BOMBAGALLO': 1812, 'AC PICCHIA': 1838.5}


start = time.time()
results, counts = play_all_leagues(teams, goals, 26, 1000)
tabella = pd.DataFrame(results)
tabella.loc[:] = round(tabella.loc[:]/counts*100,2)
tabella.index = np.arange(1,len(tabella)+1)
print(tabella.head(8))
print('\n')
print(time.time() - start)


