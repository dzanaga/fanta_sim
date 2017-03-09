class Team(object):
    num_teams = 0
    def __init__(self, name, players_list, abs_points, position):
        self.name = name
        self.players_list = players_list
        self.abs_points = abs_points
        self.position = position
        Team.num_teams += 1
        
    def total_teams():
        print('Total number of teams is: %s' % Team.num_teams)
        
class Match(object):
    def __init__(self, team1, team2, day):
        self.team1 = team1.name
        self.team2 = team2.name
        self.day = day
        
    def result(team1, team2, day):
        temp1 = int(((df_teams[team1.name][day] - 66) // 6) + 1)
        temp2 = int(((df_teams[team2.name][day] - 66) // 6) + 1)
        if temp1 < 0:
            temp1 = 0
        if temp2 < 0:
            temp2 = 0
        
        print('%s - %s     %s - %s' % (team1.name, team2.name, temp1, temp2))
        
        
#%%        

roxy = Team('FC Roxy', ['lista squadra'], 66.5, 5)
ciolle = Team('Ciolle United', ['lista squadra'], 78.5, 2)

#%%

temp = Match(roxy, ciolle, 3)

#%%

df_teams = {'FC Roxy': [72], 'Ciolle United': [78]}