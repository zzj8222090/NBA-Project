import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
import numpy as np



# ['Year', 'Player', 'Pos', 'Age', 'Tm', 'G', 'GS', 'MP', 'PER', 'TS%', '3PAr', 'FTr', 'ORB%', 'DRB%', 'TRB%', 'AST%', 'STL%', 'BLK%', 'TOV%', 'USG%', 'blanl', 'OWS', 'DWS', 'WS', 'WS/48', 'blank2', 'OBPM', 'DBPM', 'BPM', 'VORP', 'FG', 'FGA', 'FG%', '3P', '3PA', '3P%', '2P', '2PA', '2P%', 'eFG%', 'FT', 'FTA', 'FT%', 'ORB', 'DRB', 'TRB', 'AST', 'STL', 'BLK', 'TOV', 'PF', 'PTS']

seasons = pd.read_csv('Seasons_stats.csv', header=0)
players = pd.read_csv('Players.csv', header=0)
# print(seasons)
newPlayers = seasons.dropna(thresh=50)  # remove old players who have not some stats
newPlayers = newPlayers.reset_index().drop(['index'], axis=1)


# print(newPlayers.sort_values('Player'))
# CHH-CHA KCK-SAC NOH/NOK-NOP SDC-LAC SEA-OKC VAN-MEM WSB-WAS
# print(newPlayers[['Player','Tm']].groupby('Tm',as_index=False).count())
# print(newPlayers.loc[newPlayers['Tm']=='TOT'])|
# print(players.sort_values('Player'))
# print(seasons)
# print(seasons.groupby('Player').count())
# print(seasons.sort_values('Player'))

def convertteamname():
    for ind in newPlayers.index:
        if newPlayers['Tm'][ind] == 'CHH': newPlayers['Tm'][ind] = 'CHA'
        if newPlayers['Tm'][ind] == 'KCK': newPlayers['Tm'][ind] = 'SAC'
        if newPlayers['Tm'][ind] == 'NOH': newPlayers['Tm'][ind] = 'NOP'
        if newPlayers['Tm'][ind] == 'NOK': newPlayers['Tm'][ind] = 'NOP'
        if newPlayers['Tm'][ind] == 'SDC': newPlayers['Tm'][ind] = 'LAC'
        if newPlayers['Tm'][ind] == 'SEA': newPlayers['Tm'][ind] = 'OKC'
        if newPlayers['Tm'][ind] == 'VAN': newPlayers['Tm'][ind] = 'MEM'
        if newPlayers['Tm'][ind] == 'CHO': newPlayers['Tm'][ind] = 'CHA'
        if newPlayers['Tm'][ind] == 'WSB': newPlayers['Tm'][ind] = 'WAS'
        if newPlayers['Tm'][ind] == 'NJN': newPlayers['Tm'][ind] = 'BRK'
        f = newPlayers.drop(newPlayers[newPlayers['Tm'] == 'TOT'].index)
    numteams = f[['Player', 'Tm']].groupby('Tm', as_index=False).count()
    numteams.to_csv('teams.txt', sep='|')
    # print(type(numteams))
    return f


# convertteamname()
teams = pd.read_csv('teams.txt', sep='|')


# print(teams)
# print(newPlayers.sort_values('Player'))


def ve():
    n = convertteamname()
    n['VE'] = None
    for ind in n.index:
        n['VE'][ind] = 0.4 * n['PER'][ind] + 0.2 * n['WS'][ind] + 0.2 * (n['PTS'][
            ind]/n['G'][ind]) + 0.1 * (n['AST'][ind]/n['G'][ind]) + 0.1 * (n['TRB'][ind]/n['G'][ind]) - (n['TOV'][ind]/n['G'][ind])
    print(n)
    n.to_csv(r'newPlayers1.csv', sep='|')


ve()

p = pd.read_csv('newPlayers1.csv',sep='|')
p = p.drop_duplicates(['Player', 'Tm']).sort_values(['Tm', 'Player'])
pi = p[['Year', 'Player', 'Tm', 'Pos', 'VE']].sort_values(['Tm', 'Pos', 'VE'], ascending=False)
best = pi.drop_duplicates(['Tm', 'Pos'])
# best.to_csv('best.csv',index=False)
# print(best)
# print(p[['Tm','Player','VE']].sort_values(['Tm','VE']))
# p.to_csv('newPlayers1.csv',index=False)
# print(p)
# print(players)

def addhw():
    best['height'] = None
    best['weight'] = None
    for i in best.index:
        for j in players.index:
            if best['Player'][i] == players['Player'][j]:
                best['height'][i] = players['height'][j]
                best['weight'][i] = players['weight'][j]
    print(best)
    best.to_csv('best.csv', index=False)
# addhw()

# new = p.merge(players, on=['Player'])
new = seasons.merge(players, on=['Player'])
newless = p.merge(players,on=['Player'])
# print(new.sort_values(['Year','Pos']).groupby('Year').count())
h = []

# for ind in new.index-1:
#     temp = []
#     temp.append(new['height'][ind])
#     if new['Year'][ind] == new['Year'][ind+1]:
#         temp.append(new['height'][ind+1])
#     h.append(sum(temp)/len(temp))
def formlist(para):
    l = ['C','PF','SF','SG','PG']
    for j in l:
        temp = []
        for i in range(1950, 2018):
            se = new.loc[(new['Year']==i) & (new['Pos']==j)][para]
            temp.append(sum(se)/len(se))
        h.append(temp)
    # print(h)
    # print(len(set(new['Year'].dropna())),len(h))
# formlist('weight')

def plot1():
    fig,ax = plt.subplots()
    l = ['C', 'PF', 'SF', 'SG', 'PG']
    for i in range(0,5):
        ax.plot(list(set(new['Year'].dropna())),h[i])
    ax.legend(l,loc='upper left',fontsize=8)
    ax.set(xlabel='Time(years)',ylabel='Weight(Kg)',title='NBA Player Body Weight Trend for Each Position')
    ax.grid()
    fig.savefig("Weightvstime.png")
    plt.show()

# plot1()

def plotAllPlayers():
    x = list(set(new['Year'].dropna()))
    x = [int(x) for x in x]
    y = list(seasons.groupby('Year').count()['Player'])
    y_pos = np.arange(len(x))

    plt.bar(y_pos,y,alpha=0.5)
    plt.xticks(y_pos,x)
    plt.xticks(fontsize=6.5,rotation=90)
    plt.ylabel('# of Players')
    plt.title('# of Players Each Year in NBA')
    plt.show()
    plt.savefig("AllPlayers.png")
# plotAllPlayers()

def plotVEallPlayers(para):
    x = range(1980,2018)
    l = []
    for i in x:
        se = newless.loc[newless['Year'] == i][para]
        l.append(sum(se)/len(se))
    fig,ax = plt.subplots()
    ax.set(xlabel='Time(years)', ylabel='VE', title='NBA Player Average VE Trend')
    ax.plot(x,l)
    ax.grid()
    plt.show()
# plotVEallPlayers('VE')