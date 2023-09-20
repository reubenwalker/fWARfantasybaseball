#PSEUDOCODE
import pandas as pd
import os
import glob
import pickle
#First step, run draft with opposing teams, default rankings
#Calculate value of total zscore? Distance from goal values?
#Randomize pre-draft rankings
#Repeat
#Monte Carlo to find optimal rankings
#hittersRaw = pd.read_csv('HittersRaw.csv')
#pitchersRaw = pd.read_csv('PitchersRaw.csv')

#players = pd.merge(players, hittersRaw[['PlayerId', 'PA']],how='left',on='PlayerId')
#players = pd.merge(players, pitchersRaw[['PlayerId', 'IP']],how='left',on='PlayerId')



def fillDepth(hitters,PAavailDict):
    #print('Fill Depth!')
    #if len(hitters) == 0:
    #    return hitters
    #In order:playerID,Name,Pos,PA,WAR,proratedProj,DHWAR, OWNER
    hittersTemp = hitters.copy().reset_index(drop=True)
    hittersTemp['Bench'] = hittersTemp['PA']
    for key in PAavailDict:
        hittersTemp[key] = 0
    #PAavailTemp = PAavailDict.copy()
    PAavailTemp = PAavailDict.copy()

    hittersTemp = hittersTemp.sort_values('PTS', ascending=False)

    sumPA = sum(list(PAavailTemp.values()))
    m = 0
    #print('\n')
    #print('Hitters: ')
    resortDH = 'no'
    #print(str(hittersTemp[0][9]['Bench']))
    while (sumPA > 0):
        if (PAavailTemp['DH'] == 0) & (resortDH == 'no'):
            resortDH = 'yes'
            hittersTemp = hittersTemp.sort_values('Dollars', ascending=False)
            m = 0
        #pickID = hittersTemp[m][0]
        #j = removePickID(hittersList,pickID)
        removePA = 0
        noMorePA = 0
        while (removePA < hittersTemp.loc[m, 'PA']) & (sumPA != 0) & (noMorePA == 0):# & (PAavailTemp['DH'] == 0):
            sumPA = sum(list(PAavailTemp.values()))
            noMorePA = 1
            for key in PAavailTemp:
                #if hittersTemp[m][1] == 'Yasmani Grandal':
                    #print(hittersTemp[m][1],', Pos: ',key,', ELIGIBLE? ', 1==hittersTemp[m][8][key])
                    #print(str(PAavailTemp['C']))
                #Put a PA in all non-filled positions
                if (hittersTemp.loc[m, 'Bench'] <= 0):
                    break
                if (PAavailTemp[key] > 0) & (key in hittersTemp.loc[m, 'POS']):
                    #hittersTemp[j[i][8][hittersTemp[j[i]][2]] += 1                        
                    PAavailTemp[key] -= 1
                    hittersTemp.loc[m, 'Bench'] -= 1
                    #hitterBank.append(hittersTemp[m][1] + ', Pos: ' + str(key) + ', +1, fillDepth')
                    hittersTemp.loc[m,key] += 1
                    noMorePA = 0
            if noMorePA == 1:
                break
            if m == len(hittersTemp):
                break
                #hittersTemp[m][8][hittersTemp[j[i]][2]] += 1
            #if PAavailTemp['DH'] > 0:
            #    removePA += 1
            #    for i in range(len(j)):
            #        hittersTemp[j[i]][8]['DH'] += 1
            #    PAavailTemp['DH'] -= 1
             
                
        
        #hittersTemp[m][9]['Bench'] -= removePA
        m += 1
        if m == len(hittersTemp):
            break
        #print(m)
        sumPA = sum(list(PAavailTemp.values()))
    return hittersTemp


def calcVal(players, PAavailDict, IPavailDict):
    #sortedPitchers = players[players['pos'] == 'P']
    #Calculate pitchers innings. If IP < 1000, pitchVal = 0
    pVal = 0
    hVal = 0    
    totVal = 0
    pitchers = players[players['IP'] > 0].copy().reset_index(drop=True)
    hitters = players[players['PA'] > 0].copy().reset_index(drop=True)
    PAavailTemp = PAavailDict.copy()
    IPavailTemp = IPavailDict.copy()
    
    if len(pitchers) > 0:
        pitchers['prorDol'] = pitchers['Dollars']/pitchers['IP']
        sortedPitchers = pitchers.sort_values('prorDol', ascending=False)
        
        #IPavail = IPavailTemp['P']
        i = 0
        
        while ((IPavailTemp['P'] != 0) & (i < len(sortedPitchers))):
                if sortedPitchers.iloc[i]['IP'] > IPavailTemp['P']:
                    prorated = IPavailTemp['P']*sortedPitchers.iloc[i]['prorDol']#Prorated WAR 
                    pVal += prorated
                    #print(sortedPitchers.iloc[i]['Name'] + ', WAR: ' + str(round(prorated,1)) + ', IP: ' + str(round(IPavailTemp['P'],1)))
                    IPavailTemp['P'] = 0
                    break
                IPavailTemp['P'] -= sortedPitchers.iloc[i]['IP']
                pVal += sortedPitchers.iloc[i]['Dollars']
                #print(sortedPitchers.iloc[i]['Name'] + ', WAR: ' + str(round(sortedPitchers.iloc[i]['Dollars'],1)) + ', IP: ' + str(sortedPitchers.iloc[i]['IP']))
                i += 1    
        if IPavailTemp['P'] != 0:
            pVal = 0
    else:
        pval = 0
    if len(hitters) > 0:
        hitters2 = fillDepth(hitters, PAavailTemp)
        hVal = ((hitters2['PA']-hitters2['Bench'])/hitters2['PA']*hitters2['Dollars']).sum()
    else:
        hVal = 0
    totVal = pVal + hVal
    return totVal

def draftADP(players, numTeams, draftpos):
    for z_i in range(25):
        for m in range(numTeams):
                if z_i%2 == 0:
                    z = m
                if z_i%2 == 1:
                    z = numTeams-1-m
                if z != draftpos:
                    #print(z)
                    ADPmin = players.iloc[players[players['Owner'].isna()]['ADP'].argmin()].name
                    players.loc[ADPmin, 'Owner'] = z
                if z == draftpos:
                    #print(z)
                    rankMax = players.iloc[players[players['Owner'].isna()]['Dollars'].argmax()].name
                    players.loc[rankMax, 'Owner'] = z
    return players
    

#I want this to increment over the 
def shuffleRankings(players, partitions):
    shuffled = players.copy()
    for i in range(partitions):
        part = math.floor(1/partitions*len(players))
        start_index = i*part
        #print(start_index)
        end_index = start_index + part
        #print(end_index)
        shuffled.iloc[start_index:end_index] = shuffled.iloc[start_index:end_index].sample(frac=1)#.reset_index(drop=True)
    shuffled = shuffled.reset_index(drop=True)
    return shuffled

def shuffleOverlap(players, partitions):
    shuffled = players.copy()
    for i in range(2*partitions):
        halfPart = math.floor(1/partitions*len(players)/2)
        start_index = i*halfPart
        #print(start_index)
        end_index = start_index + halfPart*2
        #print(end_index)
        shuffled.iloc[start_index:end_index] = shuffled.iloc[start_index:end_index].sample(frac=1)
    return shuffled

def draftRankADP(players, numTeams, draftpos):
    draftSimPlayers = players.copy()
    for z_i in range(25):
        for m in range(numTeams):
                if z_i%2 == 0:
                    z = m
                if z_i%2 == 1:
                    z = numTeams-1-m
                if z != draftpos:
                    #print((z_i)*12+m)
                    undrafted = draftSimPlayers[draftSimPlayers['Owner'].isna()].copy()
                    ADPmin = undrafted.iloc[undrafted['ADP'].argmin()].name
                    draftSimPlayers.loc[ADPmin, 'Owner'] = z
                if z == draftpos:
                    print((z_i)*12+m)
                    undrafted = draftSimPlayers[draftSimPlayers['Owner'].isna()].copy()
                    rankMax = undrafted.iloc[undrafted['Rank'].argmin()].name
                    draftSimPlayers.loc[rankMax, 'Owner'] = z
    return draftSimPlayers

def draftHalf(players, numTeams, draftpos):
    draftSimPlayers = players.copy()
    for z_i in range(25):
        for m in range(numTeams):
                if z_i%2 == 0:
                    z = m
                if z_i%2 == 1:
                    z = numTeams-1-m
                if z != draftpos:
                    #print(z)
                    ADPmin = draftSimPlayers.iloc[draftSimPlayers[draftSimPlayers['Owner'].isna()]['RankADP'].argmin()].name
                    draftSimPlayers.loc[ADPmin, 'Owner'] = z
                if z == draftpos:
                    #print(z)
                    rankMax = draftSimPlayers.iloc[draftSimPlayers[draftSimPlayers['Owner'].isna()]['RankADP'].argmin()].name
                    draftSimPlayers.loc[rankMax, 'Owner'] = z
    return draftSimPlayers
    




user_PA = 700
user_IP = 25*40 #1000
PAavailDict = {'C':user_PA,'1B':user_PA,'2B':user_PA,'3B':user_PA,'SS':user_PA,'OF':user_PA*3,'DH':user_PA}
IPavailDict = {'P':user_IP} #Th

#In order to run this code, we need:
#In order:playerID,Name,Pos,PA,WAR,proratedProj,DHWAR, OWNER
hitters = pd.read_csv('Hitters_ATC2023.csv')
pitchers = pd.read_csv('Pitchers_ATC2023.csv')
players = pd.concat([hitters, pitchers]).sort_values('Dollars', ascending=False).reset_index(drop=True)
players['Owner'] = np.nan
players['Rank'] = players['Dollars'].rank(ascending=False)
#players['Rank'] = players['Dollars'].rank(ascending=False)
players['RankADP'] = ((players['ADP'] + players['Rank'])/2).rank()
draftablePlayers = players[((players['Rank'] <= 300) | (players['ADP'] <= 300))]
draftablePlayers.sort_values('RankADP').to_csv('AvgRankADP.csv')
#PSEUDOCODE
#Draft based on rankings
#Calculate value
#Save highest rankings
#Shuffle rankings
#Calculate value
#If value higher than old max, save rankings
#Repeat
draftpos = 8
numTeams = 12
import time
start_time = time.time()
hours = float(input('How many hours to sim? '))
seconds = round(hours*3600)
elapsed_time = 0#current_time - start_time
saveValDol = 0
saveValADP = 0
saveValHalf = 0
playersDol = draftablePlayers.copy()
playersHalf = draftablePlayers.copy()
savePlayersDol = draftablePlayers.copy()
savePlayersADP = draftablePlayers.copy()
savePlayersHalf = draftablePlayers.copy()

while elapsed_time < seconds:
    current_time = time.time()
    elapsed_time = current_time - start_time
    pickedPlayersDol = draftRankADP(playersDol, numTeams, draftpos)
    pickedPlayersHalf = draftHalf(playersHalf, numTeams, draftpos)
    # valDol = calcVal(pickedPlayersDol[pickedPlayersDol['Owner'] == draftpos],PAavailDict, IPavailDict)
    valHalf = calcVal(pickedPlayersHalf[pickedPlayersHalf['Owner'] == draftpos],PAavailDict, IPavailDict)
    
    # if valDol > saveValDol:
        # savePlayersDol = pickedPlayersDol
        # print('Better!')
        # saveValDol = valDol
    if valHalf > saveValHalf:
       savePlayersHalf = pickedPlayersHalf
       print('Better!')
       saveValHalf = valHalf
       savePlayersHalf.to_csv('savePlayersHalf.csv')
    # playersDol = shuffleRankings(savePlayersDol, random.randint(20,30))
    playersHalf = shuffleRankings(savePlayersHalf, random.randint(20,30))
    # playersDol['Rank'] = playersDol.index
    playersHalf['RankADP'] = playersHalf.index
savePlayersDol


###ADP Seed for player rankings

user_PA = 700
user_IP = 25*40 #1000
PAavailDict = {'C':user_PA,'1B':user_PA,'2B':user_PA,'3B':user_PA,'SS':user_PA,'OF':user_PA*3,'DH':user_PA}
IPavailDict = {'P':user_IP} #Th

#In order to run this code, we need:
#In order:playerID,Name,Pos,PA,WAR,proratedProj,DHWAR, OWNER
hitters = pd.read_csv('Hitters_ATC2023.csv')
pitchers = pd.read_csv('Pitchers_ATC2023.csv')
players = pd.concat([hitters, pitchers]).sort_values('Dollars', ascending=False).reset_index(drop=True)
players['Owner'] = np.nan
#players['Rank'] = players['Dollars'].rank(ascending=False)
players['Rank'] = players['ADP']
players['RankADP'] = ((players['ADP'] + players['Rank'])/2).rank()
draftablePlayers = players[((players['Rank'] <= 300) | (players['ADP'] <= 300))]

draftablePlayers = players[((players['Rank'] <= 350) | (players['ADP'] <= 350))]

draftpos = 8
numTeams = 12
import time
start_time = time.time()
hours = float(input('How many hours to sim? '))
seconds = round(hours*3600)
elapsed_time = 0#current_time - start_time
saveValDol = 0
saveValADP = 0
saveValHalf = 0
playersDol = draftablePlayers.copy()
playersHalf = draftablePlayers.copy()
playersADP = draftablePlayers.copy()
savePlayersDol = draftablePlayers.copy()
savePlayersADP = draftablePlayers.copy()
savePlayersHalf = draftablePlayers.copy()

while elapsed_time < seconds:
    current_time = time.time()
    elapsed_time = current_time - start_time
    pickedPlayersADP = draftRankADP(playersADP, numTeams, draftpos)
    #pickedPlayersHalf = draftHalf(playersHalf, numTeams, draftpos)
    valADP = calcVal(pickedPlayersADP[pickedPlayersADP['Owner'] == draftpos],PAavailDict, IPavailDict)
    # valHalf = calcVal(pickedPlayersHalf[pickedPlayersHalf['Owner'] == draftpos],PAavailDict, IPavailDict)
    
    if valADP > saveValADP:
        savePlayersADP = pickedPlayersADP
        print('Better!')
        saveValADP = valADP
    # if valHalf > saveValHalf:
       # savePlayersHalf = pickedPlayersHalf
       # print('Better!')
       # saveValHalf = valHalf
       # savePlayersHalf.to_csv('savePlayersHalf.csv')
    playersADP = shuffleRankings(savePlayersADP, random.randint(20,30))
    # playersHalf = shuffleRankings(savePlayersHalf, random.randint(20,30))
    playersADP['Rank'] = playersADP.index
    playersADP['Owner'] = np.nan
    # playersHalf['RankADP'] = playersHalf.index
savePlayersADP


###Dollar/ADP Seed for player rankings

user_PA = 700
user_IP = 25*40 #1000
PAavailDict = {'C':user_PA,'1B':user_PA,'2B':user_PA,'3B':user_PA,'SS':user_PA,'OF':user_PA*3,'DH':user_PA}
IPavailDict = {'P':user_IP} #Th

#In order to run this code, we need:
#In order:playerID,Name,Pos,PA,WAR,proratedProj,DHWAR, OWNER
hitters = pd.read_csv('Hitters_ATC2023.csv')
pitchers = pd.read_csv('Pitchers_ATC2023.csv')
players = pd.concat([hitters, pitchers]).sort_values('Dollars', ascending=False).reset_index(drop=True)
players['Owner'] = np.nan
#players['Rank'] = players['Dollars'].rank(ascending=False)
players['Rank'] = ((players['ADP'] + players['Dollars'].rank(ascending=False))/2).rank()
draftablePlayers = players[((players['Rank'] <= 300) | (players['ADP'] <= 300))]

draftablePlayers = players[((players['Rank'] <= 350) | (players['ADP'] <= 350))]

draftpos = 8
numTeams = 12
import time
start_time = time.time()
hours = float(input('How many hours to sim? '))
seconds = round(hours*3600)
elapsed_time = 0#current_time - start_time
saveValDol = 0
saveValADP = 0
saveValHalf = 0
playersDol = draftablePlayers.copy()
playersHalf = draftablePlayers.copy()
playersADP = draftablePlayers.copy()
savePlayersDol = draftablePlayers.copy()
savePlayersADP = draftablePlayers.copy()
savePlayersHalf = draftablePlayers.copy()
valList = []
timeList = []

while elapsed_time < seconds:
    current_time = time.time()
    elapsed_time = current_time - start_time
    pickedPlayersADP = draftRankADP(playersADP, numTeams, draftpos)
    #pickedPlayersHalf = draftHalf(playersHalf, numTeams, draftpos)
    valADP = calcVal(pickedPlayersADP[pickedPlayersADP['Owner'] == draftpos],PAavailDict, IPavailDict)
    # valHalf = calcVal(pickedPlayersHalf[pickedPlayersHalf['Owner'] == draftpos],PAavailDict, IPavailDict)
    
    if valADP > saveValADP:
        savePlayersADP = pickedPlayersADP
        #print('Better!')
        saveValADP = valADP
        valList.append(valADP)
        timeList.append(time.time())
    # if valHalf > saveValHalf:
       # savePlayersHalf = pickedPlayersHalf
       # print('Better!')
       # saveValHalf = valHalf
       # savePlayersHalf.to_csv('savePlayersHalf.csv')
    playersADP = shuffleRankings(savePlayersADP, random.randint(20,30))
    # playersHalf = shuffleRankings(savePlayersHalf, random.randint(20,30))
    playersADP['Rank'] = playersADP.index
    playersADP['Owner'] = np.nan
    # playersHalf['RankADP'] = playersHalf.index
savePlayersADP


# draftSimPlayers = playersADP.copy()
# for z_i in range(25):
    # print(z_i)
    # for m in range(numTeams):
            # if z_i%2 == 0:
                # z = m
            # if z_i%2 == 1:
                # z = numTeams-1-m
            # if z != draftpos:
                # print(z)
                # undrafted = draftSimPlayers[draftSimPlayers['Owner'].isna()].copy()
                # ADPmin = undrafted.iloc[undrafted['ADP'].argmin()].name
                # draftSimPlayers.loc[ADPmin, 'Owner'] = z
            # if z == draftpos:
                # print(z)
                # undrafted = draftSimPlayers[draftSimPlayers['Owner'].isna()].copy()
                # rankMax = undrafted.iloc[undrafted['Rank'].argmin()].name
                # draftSimPlayers.loc[rankMax, 'Owner'] = z
                
                
    #print('Fill Depth!')
    #if len(hitters) == 0:
    #    return hitters
    #In order:playerID,Name,Pos,PA,WAR,proratedProj,DHWAR, OWNER


# hittersTemp = myP[myP['PA'] > 0].copy().
# hittersTemp['Bench'] = hittersTemp['PA']
# for key in PAavailDict:
    # hittersTemp[key] = 0
# # PAavailTemp = PAavailDict.copy()
# PAavailTemp = PAavailDict.copy()

# hittersTemp = hittersTemp.sort_values('PTS', ascending=False)

# sumPA = sum(list(PAavailTemp.values()))
# m = 0
# # print('\n')
# # print('Hitters: ')
# resortDH = 'no'
# # print(str(hittersTemp[0][9]['Bench']))
# while (sumPA > 0):
    # if (PAavailTemp['DH'] == 0) & (resortDH == 'no'):
        # resortDH = 'yes'
        # hittersTemp = hittersTemp.sort_values('Dollars', ascending=False)
        # m = 0
    # # pickID = hittersTemp[m][0]
    # # j = removePickID(hittersList,pickID)
    # removePA = 0
    # noMorePA = 0
    # while (removePA < hittersTemp.loc[m, 'PA']) & (sumPA != 0) & (noMorePA == 0):# & (PAavailTemp['DH'] == 0):
        # sumPA = sum(list(PAavailTemp.values()))
        # noMorePA = 1
        # for key in PAavailTemp:
            # # if hittersTemp[m][1] == 'Yasmani Grandal':
                # # print(hittersTemp[m][1],', Pos: ',key,', ELIGIBLE? ', 1==hittersTemp[m][8][key])
                # # print(str(PAavailTemp['C']))
            # # Put a PA in all non-filled positions
            # if (hittersTemp.loc[m, 'Bench'] <= 0):
                # break
            # if (PAavailTemp[key] > 0) & (key in hittersTemp.loc[m, 'POS']):
                # # hittersTemp[j[i][8][hittersTemp[j[i]][2]] += 1                        
                # PAavailTemp[key] -= 1
                # hittersTemp.loc[m, 'Bench'] -= 1
                # # hitterBank.append(hittersTemp[m][1] + ', Pos: ' + str(key) + ', +1, fillDepth')
                # hittersTemp.loc[m,key] += 1
                # noMorePA = 0
        # if noMorePA == 1:
            # break
        # if m == len(hittersTemp):
            # break
            # # hittersTemp[m][8][hittersTemp[j[i]][2]] += 1
        # # if PAavailTemp['DH'] > 0:
           # # removePA += 1
           # # for i in range(len(j)):
               # # hittersTemp[j[i]][8]['DH'] += 1
           # # PAavailTemp['DH'] -= 1
         
            
    
# # hittersTemp[m][9]['Bench'] -= removePA
# m += 1
# if m == len(hittersTemp):
    # break
# # print(m)
# sumPA = sum(list(PAavailTemp.values()))

# players = myP

# # sortedPitchers = players[players['pos'] == 'P']
# # Calculate pitchers innings. If IP < 1000, pitchVal = 0
# pVal = 0
# hVal = 0    
# totVal = 0
# pitchers = players[players['IP'] > 0].copy().reset_index(drop=True)
# hitters = players[players['PA'] > 0].copy().reset_index(drop=True)
# PAavailTemp = PAavailDict.copy()
# IPavailTemp = IPavailDict.copy()

# if len(pitchers) > 0:
    # pitchers['prorDol'] = pitchers['Dollars']/pitchers['IP']
    # sortedPitchers = pitchers.sort_values('prorDol', ascending=False)
    
    # # IPavail = IPavailTemp['P']
    # i = 0
    
    # while ((IPavailTemp['P'] != 0) & (i < len(sortedPitchers))):
            # if sortedPitchers.iloc[i]['IP'] > IPavailTemp['P']:
                # prorated = IPavailTemp['P']*sortedPitchers.iloc[i]['prorDol']#Prorated WAR 
                # pVal += prorated
                # # print(sortedPitchers.iloc[i]['Name'] + ', WAR: ' + str(round(prorated,1)) + ', IP: ' + str(round(IPavailTemp['P'],1)))
                # IPavailTemp['P'] = 0
                # break
            # IPavailTemp['P'] -= sortedPitchers.iloc[i]['IP']
            # pVal += sortedPitchers.iloc[i]['Dollars']
            # print(sortedPitchers.iloc[i]['Name'] + ', WAR: ' + str(round(sortedPitchers.iloc[i]['Dollars'],1)) + ', IP: ' + str(sortedPitchers.iloc[i]['IP']))
            # i += 1    
    # if IPavailTemp['P'] > 0:
        # pVal = 0
# else:
    # pval = 0
# if len(hitters) > 0:
    # hitters2 = fillDepth(hitters, PAavailTemp)
    # hVal = ((hitters2['PA']-hitters2['Bench'])/hitters2['PA']*hitters2['Dollars']).sum()
# else:
    # hVal = 0
# totVal = pVal + hVal
# totVal
partitions = 25
shuffled = players.copy()
for i in range(partitions):
    part = math.floor(1/partitions*len(players))
    start_index = i*part
    #print(start_index)
    end_index = start_index + part
    #print(end_index)
    shuffled.iloc[start_index:end_index] = shuffled.iloc[start_index:end_index].sample(frac=1)#.reset_index(drop=True)
shuffled = shuffled.reset_index(drop=True)
#return shuffled