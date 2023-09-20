import copy
import copy
import time
import random
from operator import itemgetter
from csv import reader

#This iteration of code split the pitchers and hitters
    #That means we could get rid of the DHWAR for pitchers
#Jesse had too many PAs at catcher??
#Temporarily solved by declaring PAavailDict as a global variable in function. Less than ideal.
#Need to print out underperforming players as well
#Whole number innings from FG for some reason.

#To do:
    #Take team names automatically from spreadsheet rather than hard-coding them.

#How many total games have been played?
user_games = int(input("How many games have been played so far? "))
user_time = float(input("How much time do you have to iterate in hours? "))
user_IP = round(1400*user_games/162)
user_PA = round(700*user_games/162)

def removePick(players,pick):
    j = []
    #for n in range(10):
    for n in range(len(players)):
        if players[n][1] == pick:
            j.append(n)
    #if j == []:
    #    print(pick)
    return j

def removePickID(players,pickID):
    j = []
    #for n in range(10):
    for n in range(len(players)):
        if players[n][0] == pickID:
            j.append(n)
    #if j == []:
    #    print(pick)
    return j

def fillDepth(hitters,PAavailDict):
    #print('Fill Depth!')
    #Jesse had too many C PAs...
    #If we 
    
    hittersTemp = []
    for i in range(len(hitters)):
        hittersTemp.append(copy.deepcopy(hitters[i]))
    #PAavailTemp = PAavailDict.copy()
    PAavailTemp = copy.deepcopy(PAavailDict)

    hittersTemp = sorted(hittersTemp, key=itemgetter(5), reverse=True)

    sumPA = sum(list(PAavailTemp.values()))
    m = 0
    #print('\n')
    #print('Hitters: ')
    resortDH = 'no'
    #print(str(hittersTemp[0][9]['Bench']))
    while sumPA > 0:
        if (PAavailTemp['DH'] == 0) & (resortDH == 'no'):
            resortDH = 'yes'
            hittersTemp = sorted(hittersTemp, key=itemgetter(5), reverse=True)
            m = 0
        #pickID = hittersTemp[m][0]
        #j = removePickID(hittersList,pickID)
        removePA = 0
        noMorePA = 0
        while (removePA < hittersTemp[m][3]) & (sumPA != 0) & (noMorePA == 0):# & (PAavailTemp['DH'] == 0):
            sumPA = sum(list(PAavailTemp.values()))
            noMorePA = 1
            for key in PAavailTemp:
                #if hittersTemp[m][1] == 'Yasmani Grandal':
                    #print(hittersTemp[m][1],', Pos: ',key,', ELIGIBLE? ', 1==hittersTemp[m][8][key])
                    #print(str(PAavailTemp['C']))
                #Put a PA in all non-filled positions
                if (hittersTemp[m][9]['Bench'] == 0):
                    break
                if (PAavailTemp[key] > 0) & (hittersTemp[m][8][key] == 1):
                    #hittersTemp[j[i][8][hittersTemp[j[i]][2]] += 1                        
                    PAavailTemp[key] -= 1
                    hittersTemp[m][9]['Bench'] -= 1
                    hitterBank.append(hittersTemp[m][1] + ', Pos: ' + str(key) + ', +1, fillDepth')
                    hittersTemp[m][9][key] += 1
                    noMorePA = 0
            if noMorePA == 1:
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

def optimizeDH(hitters,PAavailDict):
    hittersTemp = []
    for i in range(len(hitters)):
        hittersTemp.append(copy.deepcopy(hitters[i]))
    PAavailTemp = PAavailDict.copy()
    #Sort ASCENDING!
    hittersTemp = sorted(hittersTemp, key=itemgetter(6), reverse=False)

    for i in range(len(hittersTemp)-1):
        for ii in range(i+1,len(hittersTemp)-1):
            while (hittersTemp[i][9]['DH'] > 0) & (hittersTemp[ii][9]['Bench'] > 0):
                hittersTemp[i][9]['DH'] -= 1
                hittersTemp[i][9]['Bench'] += 1
                hitterBank.append(hittersTemp[i][1] + ', Pos: ' + str('DH') + ', -1, DHFILL')
                hitterBank.append(hittersTemp[i][1] + ', Pos: ' + str('Bench') + ', -1, DHFILL')
                hittersTemp[ii][9]['DH'] += 1
                hittersTemp[ii][9]['Bench'] -= 1
                hitterBank.append(hittersTemp[ii][1] + ', Pos: ' + str('DH') + ', +1, DHFILL')

    hittersTemp = sorted(hittersTemp, key=itemgetter(6), reverse=True)
    for iii in range(len(hittersTemp)):
        while (PAavailTemp['DH'] > 0) & (hittersTemp[iii][9]['Bench'] >0):
            hittersTemp[iii][9]['DH'] += 1
            hitterBank.append(hittersTemp[iii][1] + ', Pos: ' + str('DH') + ', +1, DHFILL')
            hittersTemp[iii][9]['Bench'] -= 1
            PAavailTemp['DH'] -= 1
        if PAavailTemp['DH'] == 0:
            break
        

    return hittersTemp

def monteCarlo(hitters,PAavailDict,weightedProb):
    #DECLARE VARIABLES
    #INITIALIZE ARRAYS AND VALUES
    
    hittersTemp = []
    hittersTest = []
    #hittersTemp = copy.deepcopy(hitters)
    for i in range(len(hitters)):
        hittersTemp.append(copy.deepcopy(hitters[i]))
        hittersTemp[i][8]['Bench'] = 1
        #hittersTemp[i][9].append(('Bench',hittersTemp[i][3]))
    PAavailTemp = PAavailDict.copy()
    for i in range(len(hittersTemp)):
        #hittersTest.append(hittersTemp[i].copy())
        hittersTest.append(copy.deepcopy(hittersTemp[i]))
        

    global hitterBank
    hitterBank = []
    #print('initVal')
    initVal = calcVal(hittersTest)
    #print("initVal")
    #print(hittersTest[0])
    bench = False
    firstRun = True
    key1 = 'Bench'
    
    while bench == False:
        nonBenchPA = 0
        #randomPlayer = random.randrange(0,len(hittersTemp))
        samePos = False
        while (nonBenchPA == 0) & (firstRun == True):
            #randomPlayer = random.randrange(0,len(hittersTemp))
            randomList = random.choices(hittersTemp,weights=weightedProb)
            randomPlayer = randomList[0]
            nonBenchPA = randomPlayer[3] - randomPlayer[9]['Bench']
        val0 = 0
        key0 = 'Bench'
        while (firstRun == False) & (samePos == False):
            #randomPlayer = random.randrange(0,len(hittersTemp))
            randomList = random.choices(hittersTemp,weights=weightedProb)
            randomPlayer = randomList[0]
            if randomPlayer[9][key1] > 0:
                samePos = True
                val0 = randomPlayer[9][key1]
                key0 = key1
                
        #print(hittersTemp[randomPlayer][1] + ', PA: ' + str(hittersTemp[randomPlayer][3]) + ', Bench: ' + str(hittersTemp[randomPlayer][9]['Bench']))
        #Find a random OCCUPIED position where we can subtract a PA
        #print('val0')
        while (firstRun == True) & ((val0 == 0) or (key0 == 'Bench')):
            res0 = key0, val0 = random.choice(list(randomPlayer[9].items()))
        #while (firstRun == False) & ((val0 == 0) or (key0 == 'Bench')):
        #    res0 = key0, val0 = random.choice(list(hittersTemp[randomPlayer][9].items()))
        randomPlayer[9][key0] -= 1
        PAavailTemp[key0] +=1
        hitterBank.append(randomPlayer[1] + ', Pos: ' + str(key0) + ', -1')
        val1 = 0
        key1 = key0
        #Find a random OTHER position ELIGIBILITY where we can put that subtracted PA
        #print(key0)
        #print('val1')
        while (val1 == 0) or (key1 == key0) or (key1 == 'DH'):
            res1 = key1, val1 = random.choice(list(randomPlayer[8].items()))
            #print(key1)
        randomPlayer[9][key1] += 1
        hitterBank.append(randomPlayer[1] + ', Pos: ' + str(key1) + ', +1')
        #print('randomSwitch')
        #print(hittersTest[0])
        if key1 == 'Bench':
            #hittersTemp = optimizeDH(hittersTemp,PAavailTemp)
            #print('OptimizeDH')
            #print(hittersTest[0])
            #PAavailTemp['DH'] = 0
            #for iii in range(len(hitterBank)):
            #    print(hitterBank[iii])
            hittersTemp = fillDepth(hittersTemp,PAavailTemp)
            #print('fillDepth')
            #print(hittersTest[0])
            #PAavailTemp['DH'] = 0
            break
            #Resort for DHWAR
            #if PAavailTemp['DH'] != 0:
            #    hittersTemp = sorted(hittersTemp, key=itemgetter(6), reverse=True)
            #for ii in range(len(hittersTemp)):
            #    if (hittersTemp[ii][9]['Bench'] > 0) & (hittersTemp[ii][8][key0]==1):
            #        hittersTemp[ii][9]['Bench'] -= 1
            #        print(hittersTemp[ii][0] + ', Pos: ' + 'Bench' + ', +1')
            #        hittersTemp[ii][9][key0] += 1
            #        print(hittersTemp[ii][0] + ', Pos: ' + str(key0) + ', +1')
            #bench = True
        else:
            PAavailTemp[key1] -=1
        firstRun = False
    #print('finVal')
    finVal = calcVal(hittersTemp)
    if finVal > initVal:
        #global PAavailDict
        #PAavailDict = PAavailTemp
        #print(str(finVal-initVal) + ", IMPROVED!!!")
        #for iii in range(len(hitterBank)):
        #    print(hitterBank[iii])
        return hittersTemp
    else:
        #print("DIDN'T HELP!")
        hitterBank = []
        return hitters

    #RUN THE CALCULATION
    #STORE THE RESULTS
    #DISPLAY THE RESULTS GRAPHICALLY
    
    
def calcPA(hitters):
    PAavailDict = {'C':user_PA,'1B':user_PA,'2B':user_PA,'3B':user_PA,'SS':user_PA,'OF':user_PA*3,'DH':user_PA}
    for i in range(len(hitters)):
        for key in PAavailDict:
            PAavailDict[key] -= hitters[i][9][key]
    return PAavailDict

def calcVal(hitters):
    hVal = 0
    for i in range(len(hitters)):
        if hitters[i][9]['C'] > 0:
            #print(hitters[i][1],', C, PA: ',str(hitters[i][8]['C']),', WAR: ',str(hitters[i][5]*hitters[i][8]['C']))
            hVal += hitters[i][5]*hitters[i][9]['C']
    for i in range(len(hitters)):
        if hitters[i][9]['1B'] > 0:
            #print(hitters[i][1],', 1B, PA: ',str(hitters[i][8]['1B']),', WAR: ',str(hitters[i][5]*hitters[i][8]['1B']))
            hVal += hitters[i][5]*hitters[i][9]['1B']
    for i in range(len(hitters)):
        if hitters[i][9]['2B'] > 0:
            #print(hitters[i][1],', 2B, PA: ',str(hitters[i][9]['2B']),', WAR: ',str(hitters[i][5]*hitters[i][8]['2B']))
            hVal += hitters[i][5]*hitters[i][9]['2B']
    for i in range(len(hitters)):
        if hitters[i][9]['SS'] > 0:
            #print(hitters[i][1],', SS, PA: ',str(hitters[i][9]['SS']),', WAR: ',str(hitters[i][5]*hitters[i][9]['SS']))
            hVal += hitters[i][5]*hitters[i][9]['SS']
    for i in range(len(hitters)):
        if hitters[i][9]['3B'] > 0:
            #print(hitters[i][1],', 3B, PA: ',str(hitters[i][9]['3B']),', WAR: ',str(hitters[i][5]*hitters[i][9]['3B']))
            hVal += hitters[i][5]*hitters[i][9]['3B']
    for i in range(len(hitters)):
        if hitters[i][9]['OF'] > 0:
            #print(hitters[i][1],', OF, PA: ',str(hitters[i][9]['OF']),', WAR: ',str(hitters[i][5]*hitters[i][9]['OF']))
            hVal += hitters[i][5]*hitters[i][9]['OF']
    for i in range(len(hitters)):
        if hitters[i][9]['DH'] > 0:
            #print(hitters[i][1],', DH, PA: ',str(hitters[i][9]['DH']),', WAR: ',str(hitters[i][5]*hitters[i][9]['DH']))
            hVal += hitters[i][6]*hitters[i][9]['DH']
    #print('hVal: ' + str(hVal))
    return hVal

def replacementVal(hitters):
    hittersAR = sortedHitters.copy()
    mask = sortedHitters['Pos'].str.contains('C')
    hittersAR.loc[mask,'C_R'] = (sortedHitters['hWAR700PA'] - sortedHitters[(sortedHitters['PA'] == sortedHitters['Bench']) & sortedHitters['Pos'].str.contains('C')]['hWAR700PA'].max())/700*sortedHitters['PA']
    mask = sortedHitters['Pos'].str.contains('1B')
    hittersAR.loc[mask,'1B_R'] = (sortedHitters['hWAR700PA'] - sortedHitters[(sortedHitters['PA'] == sortedHitters['Bench']) & sortedHitters['Pos'].str.contains('1B')]['hWAR700PA'].max())/700*sortedHitters['PA']
    mask = sortedHitters['Pos'].str.contains('2B')
    hittersAR.loc[mask,'2B_R'] = (sortedHitters['hWAR700PA'] - sortedHitters[(sortedHitters['PA'] == sortedHitters['Bench']) & sortedHitters['Pos'].str.contains('2B')]['hWAR700PA'].max())/700*sortedHitters['PA']
    mask = sortedHitters['Pos'].str.contains('SS')
    hittersAR.loc[mask,'SS_R'] = (sortedHitters['hWAR700PA'] - sortedHitters[(sortedHitters['PA'] == sortedHitters['Bench']) & sortedHitters['Pos'].str.contains('SS')]['hWAR700PA'].max())/700*sortedHitters['PA']
    mask = sortedHitters['Pos'].str.contains('3B')
    hittersAR.loc[mask,'3B_R'] = (sortedHitters['hWAR700PA'] - sortedHitters[(sortedHitters['PA'] == sortedHitters['Bench']) & sortedHitters['Pos'].str.contains('3B')]['hWAR700PA'].max())/700*sortedHitters['PA']
    mask = sortedHitters['Pos'].str.contains('OF')
    hittersAR.loc[mask,'OF_R'] = (sortedHitters['hWAR700PA'] - sortedHitters[(sortedHitters['PA'] == sortedHitters['Bench']) & sortedHitters['Pos'].str.contains('OF')]['hWAR700PA'].max())/700*sortedHitters['PA']
    mask = sortedHitters['Pos'].str.contains('DH')
    hittersAR.loc[mask,'DH_R'] = (sortedHitters['DHWAR700PA'] - sortedHitters[(sortedHitters['PA'] == sortedHitters['Bench']) & sortedHitters['Pos'].str.contains('DH')]['DHWAR700PA'].max())/700*sortedHitters['PA']
    hittersAR['WAR_AR'] = hittersAR.iloc[:,-7:].max(axis=1)
    #Let's send that above replacement to a csv
    hittersAR = hittersAR.sort_values('WAR_AR', ascending=False)
    leaderboardAR = pd.concat([hittersAR[['Name', 'Pos', 'WAR_AR']], pitchersAR])
    leaderboardAR = leaderboardAR.sort_values('WAR_AR', ascending=False)
    leaderboardAR = leaderboardAR.groupby('Name').aggregate({'Pos': 'first', 'WAR_AR': 'sum'})
    leaderboardAR = leaderboardAR.sort_values('WAR_AR', ascending=False)
    leaderboardAR
    leaderboardAR.to_csv('LeaderboardAR2022.csv', sep=',')

#Outline
#DECLARE VARIABLES
#INITIALIZE ARRAYS AND VALUES
#RUN THE CALCULATION
#STORE THE RESULTS
#DISPLAY THE RESULTS GRAPHICALLY
def main():
#DECLARE VARIABLES

#You need a list that stores all drafted players

#Here the team names are hard-coded in. 
#Should be taken automatically from the spreadsheet.
    teamNames = ['Graham','Alden','Jesse','Nick','Sid','Benji','Reuben']#,'', Ruel]
    hitterVal = []
    pitcherVal = []
    teamVal = []

      
    playersList = []
    #Then you need a list where you will store all drafted players
    #You will run your firstGuess on only one of the teams in this list.
    playerBank = []
    #Were not sure yet how we're going to do the positions,
    #But let's try a position bank first:
    posBank = []
    #You are operating in a world in which you aren't able to perform linear algebra operations
    #Is that going to come back to bite you?
    #You could certainly store the string information in a list
    #and then store the float information in an array with the playerid
    #For now, let's keep going.
    #You need an array or dictionary for the PA and inning goals
    PAavailDict = {}
    #Anything else?
    #Since the calculation for pitchers is so easy, you might as well split pitchers and hitters
    pitchersList = []
    masterPitchers = []
    hittersList = []
    masterHitters = []

    #INITIALIZE ARRAYS AND VALUES
    # read csv file as a list of lists
    #the only reason to split string and float data would be for speed.
    #In that case, you would use tuple.
    with open('FinalRankingsHitters.csv', 'r', encoding="utf8") as read_obj:
        # pass the file object to reader() to get the reader object
        #This is not generalized for any CSV, obviously.
        #Right now the column headers are:
        #In order:playerID,Name,Pos,PA,WAR,proratedProj,DHWAR, OWNER
        #Strings: playerID,Name,Pos
        #Float: PAorIP,projWAR,proratedProj,DHWAR
        csv_reader = reader(read_obj)
        # Pass reader object to list() to get a list of lists
        masterHitters = list(csv_reader)
        #print(list_of_rows)
    #Pop headers
    #masterHittersHeaders = masterHitters.pop(0)
    #Convert numerical data to float
    #Remove players from all but chosen team
    #for i in range(len(masterHitters)):
    #    if (masterHitters[i][7] != "Reuben"):
    #        #print(masterHitters[i][7])
    #        masterHitters.pop(i)

    for i in range(len(masterHitters)):
        for j in range(3,7):
            masterHitters[i][j] = float(masterHitters[i][j])

    with open('FinalRankingsPitchers.csv', 'r', encoding="utf8") as read_obj:
        # pass the file object to reader() to get the reader object
        #This is not generalized for any CSV, obviously.
        #Right now the column headers are:
        #In order:playerID,Name,Pos,PA,WAR,proratedProj,DHWAR (NULL), OWNER
        #Strings: playerID,Name,Pos
        #Float: PAorIP,projWAR,proratedProj,DHWAR
        csv_reader = reader(read_obj)
        # Pass reader object to list() to get a list of lists
        masterPitchers = list(csv_reader)
        #print(list_of_rows)
    #Pop headers
    #masterPitchersHeaders = masterPitchers.pop(0)
    #Convert numerical data to float
    #Remove players from all but chosen team
    #for i in range(len(masterPitchers)):
    #    if (masterPitchers[i][7] != "Reuben"):
    #        #print(masterPitchers[i][7])
    #        masterPitchers.pop(i)

    #Convert DH WAR to float
    #This is extraneous, but I'm too lazy to remove it right now.
    for i in range(len(masterPitchers)):
        if masterPitchers[i][6] == ' ':
            masterPitchers[i][6] = 0
        masterPitchers[i][6] = float(masterPitchers[i][6])
    for i in range(len(masterPitchers)):
        for j in range(3,6):
            masterPitchers[i][j] = float(masterPitchers[i][j])


    #Innings and PA available for different positions
    #P,C,1B,2B,3B,SS,OF,DH
    PAavailDict = {'C':user_PA,'1B':user_PA,'2B':user_PA,'3B':user_PA,'SS':user_PA,'OF':user_PA*3,'DH':user_PA}
    #This is left over from when IP and PA were logged in the same table.
    IPavailDict = {'P':user_IP}


    #Positional eligibility. Necessary?
    #7: C
    #8: 1B
    #9: 2B
    #10: SS
    #11: 3B
    #12: OF
    #13: DH
    posArray = []
    #Here we are adding a dictionary of positional eligibility. Eligible: 1, Ineligible: 0
    while masterHitters != []:
        j = removePickID(masterHitters,masterHitters[0][0])
        posArray.append(masterHitters[0].copy())
        posArray[-1].append({'P': 0,'C':0,'1B':0,'2B':0,'3B':0,'SS':0,'OF':0,'DH':1})
        for i in sorted(j,reverse = True):
            if(masterHitters[i][2] != 'P'):
                posArray[-1][8][masterHitters[i][2]] = 1
            masterHitters.pop(i)

    #INITIALIZING CALCULATION FOR EACH OWNER IN THE LEAGUE
    for x in range(len(teamNames)):
        ownerInquiry = teamNames[x]#input("Which owner would you like to know about? ")
        print('Team: ' + teamNames[x])

        #Re-initialize PAavailDict
        #Innings and PA available for different positions
        #P,C,1B,2B,3B,SS,OF,DH
        PAavailDict = {'C':user_PA,'1B':user_PA,'2B':user_PA,'3B':user_PA,'SS':user_PA,'OF':user_PA*3,'DH':user_PA}
        IPavailDict = {'P':user_IP}
        hittersList = []
        pitchersList = []
        #Formerly: Split pitchers and hitters into separate lists.
        #Now we'll do this with separate CSVs.
        #This is still a list of players where they are duplicates if they are multi-position eligible.
        n = 0
        m = 0
        for x in range(len(posArray)):
            #print(posArray[x][7])
            if posArray[x][7] == ownerInquiry:
                hittersList.append([])
                hittersList[n] = posArray[x].copy()
                n += 1
        for y in range(len(masterPitchers)):
            #print(masterPitchers[y][7])
            if masterPitchers[y][7] == ownerInquiry:
                pitchersList.append([])
                pitchersList[m] = masterPitchers[y].copy()
                m += 1
                    

        
        

    #RUN CALCULATION
        #The pitching calculation is fairly straightforward:
        #We sort the list by prorated WAR.
        sortedPitchers = sorted(pitchersList, key=itemgetter(5), reverse=True)

        #print('This is how it looks when I order pitchers by WAR/IP first.')

        #Then, we just take the WAR off the top
        #Until the last available pitcher's IP exceed the IP available
        #Then we prorate their WAR.

        #Initialize a value to store pitcher value. Probably could do this more elegantly.
        pVal = 0
        #for i in range(len(playersList)):
        i = 0
        #print('Pitchers: ')
        
        while ((IPavailDict['P'] != 0) & (i < len(sortedPitchers))):
            if sortedPitchers[i][3] > IPavailDict['P']:
                prorated = IPavailDict['P']/sortedPitchers[i][3]*sortedPitchers[i][5]/200.0#Prorated WAR is calculated per 200 IP
                pVal += prorated
                print(sortedPitchers[i][1] + ', WAR: ' + str(round(prorated,1)) + ', IP: ' + str(round(IPavailDict['P'],1)))
                IPavailDict['P'] = 0
                break
            IPavailDict['P'] -= sortedPitchers[i][3]
            pVal += sortedPitchers[i][4]
            print(sortedPitchers[i][1] + ', WAR: ' + str(round(sortedPitchers[i][4],1)) + ', IP: ' + str(sortedPitchers[i][3]))
            i += 1

        print('Pitcher WAR: ' + str(round(pVal,1)))# + ' WAR, IP remaining: ' + str(IPavailDict['P']))

        print('\n')
        print('Unused IP:')
        for x in range(i+1,len(sortedPitchers)):
            print(sortedPitchers[x][1] + ', WAR: ' + str(round(sortedPitchers[x][4],1)) + ', IP: ' + str(sortedPitchers[x][3]))

        #Ok, here's the hard part. We need a decent first guess for hitters.
        #For our first guess, we will assign the players proportionally to their available positions
        #Since all players are DH eligible, 
            #we'll start sorting them by prorated DH WAR.
        sortedHitters = []
        for i in range(len(hittersList)):
            #if hittersList[7] == "Reuben":
            sortedHitters.append(hittersList[i].copy())
            #Need to convert prorated WAR and DH WAR to WAR/PA and DHWAR/PA
            if(sortedHitters[i][3] != 0):
                sortedHitters[i][5] = sortedHitters[i][4]/sortedHitters[i][3]
                sortedHitters[i][6] = sortedHitters[i][6]/sortedHitters[i][3]
            else:
                sortedHitters[i][5] = 0
                sortedHitters[i][6] = 0
        sortedHitters = sorted(sortedHitters, key=itemgetter(6), reverse=True)

        #This may not be the best choice, but will serve as a decent first guess.
        #How do we "assign" the hitters? Two options:
        #Keep a new bank of chosen players with their assigned PA.
        #Keep their assigned PA in the playerbank in an additional array.
        #The best answer is probably both.
        #The second option seems like it would be most easily manipulated for Monte Carlo
        #It also was how you just walked through it.
        #So let's append positional PAs to the players.
        #This is a dictionary for their accumulated PA at each position.
        for i in range(len(sortedHitters)):
            sortedHitters[i].append({'C':0,'1B':0,'2B':0,'3B':0,'SS':0,'OF':0,'DH':0,'Bench':sortedHitters[i][3]})

        #Ugh, I'm really tired of how complicated this is.
        #Right now, you are pulling the indeces from the list for each instance of the player
        #This is because they were pulled from the SQL query by position.
        #You don't have to do it this way
        #Now we have one instance with a positional array saved as hittersList

        sumPA = sum(list(PAavailDict.values()))
        m = 0
        print('\n')
        print('Hitters: ')
        resortDH = 'no'
        #print(str(sortedHitters[0][9]['Bench']))
        while sumPA > 0:
            if (PAavailDict['DH'] == 0) & (resortDH == 'no'):
                resortDH = 'yes'
                sortedHitters = sorted(sortedHitters, key=itemgetter(5), reverse=True)
                m = 0
            #pickID = sortedHitters[m][0]
            #j = removePickID(hittersList,pickID)
            removePA = 0
            noMorePA = 0
            while (removePA < sortedHitters[m][3]) & (sumPA != 0) & (noMorePA == 0):
                sumPA = sum(list(PAavailDict.values()))
                noMorePA = 1
                for key in PAavailDict:
                    #if sortedHitters[m][1] == 'Yasmani Grandal':
                    #    print(sortedHitters[m][1],', Pos: ',key,', ELIGIBLE? ', 1==sortedHitters[m][8][key])
                    #Put a PA in all non-filled positions
                    if (sortedHitters[m][9]['Bench'] == 0):
                        break
                    if (PAavailDict[key] > 0) & (sortedHitters[m][8][key] == 1):
                        #sortedHitters[j[i][8][sortedHitters[j[i]][2]] += 1                        
                        PAavailDict[key] -= 1
                        sortedHitters[m][9]['Bench'] -= 1
                        sortedHitters[m][9][key] += 1
                        noMorePA = 0
                if noMorePA == 1:
                    break
                    
                    #sortedHitters[m][8][sortedHitters[j[i]][2]] += 1
                #if PAavailDict['DH'] > 0:
                #    removePA += 1
                #    for i in range(len(j)):
                #        sortedHitters[j[i]][8]['DH'] += 1
                #    PAavailDict['DH'] -= 1
                 
                    
            
            #sortedHitters[m][9]['Bench'] -= removePA
            m += 1        
            sumPA = sum(list(PAavailDict.values()))
            if m == len(sortedHitters):
                break
            #print(m,' sumPA: ',sumPA)

    ###Here we have the Monte Carlo Calculation
    #The sortedHitters are returned each time with an improved score
        start_time = time.time()
        seconds = round(user_time*3600/8)
        n = 1
        weightedProb = []

        startVal = calcVal(sortedHitters)

        for i in range(len(sortedHitters)):
            weightedProb.append(sortedHitters[i][5])
            
        while True:
            current_time = time.time()
            elapsed_time = current_time - start_time
            #print('Monte Carlo Run #' + str(n))
            sortedHitters = monteCarlo(sortedHitters, PAavailDict, weightedProb)
            PAavailDict = calcPA(sortedHitters)
            n += 1
            midVal = calcVal(sortedHitters)
            #print(str(midVal) + ', midVal')
            if midVal < startVal:
                print("Lost Value??!")
                break
            if elapsed_time > seconds:
                #print("Finished iterating in: " + str(int(elapsed_time))  + " seconds after " + str(n) + " iterations")
                break

    #DISPLAY THE (INDIVIDUAL RESULTS GRAPHICALLY
        hVal = 0
        #Final calculation of improved score after iterations
        finVal = calcVal(sortedHitters)
        print(str(finVal) + ', finVal')
        for i in range(len(sortedHitters)):
            if sortedHitters[i][9]['C'] > 0:
                print(sortedHitters[i][1],', C, PA: ',str(sortedHitters[i][9]['C']),', WAR: ',str(round(sortedHitters[i][5]*sortedHitters[i][9]['C'],1)))
                hVal += sortedHitters[i][5]*sortedHitters[i][9]['C']
        for i in range(len(sortedHitters)):
            if sortedHitters[i][9]['1B'] > 0:
                print(sortedHitters[i][1],', 1B, PA: ',str(sortedHitters[i][9]['1B']),', WAR: ',str(round(sortedHitters[i][5]*sortedHitters[i][9]['1B'],1)))
                hVal += sortedHitters[i][5]*sortedHitters[i][9]['1B']
        for i in range(len(sortedHitters)):
            if sortedHitters[i][9]['2B'] > 0:
                print(sortedHitters[i][1],', 2B, PA: ',str(sortedHitters[i][9]['2B']),', WAR: ',str(round(sortedHitters[i][5]*sortedHitters[i][9]['2B'],1)))
                hVal += sortedHitters[i][5]*sortedHitters[i][9]['2B']
        for i in range(len(sortedHitters)):
            if sortedHitters[i][9]['SS'] > 0:
                print(sortedHitters[i][1],', SS, PA: ',str(sortedHitters[i][9]['SS']),', WAR: ',str(round(sortedHitters[i][5]*sortedHitters[i][9]['SS'],1)))
                hVal += sortedHitters[i][5]*sortedHitters[i][9]['SS']
        for i in range(len(sortedHitters)):
            if sortedHitters[i][9]['3B'] > 0:
                print(sortedHitters[i][1],', 3B, PA: ',str(sortedHitters[i][9]['3B']),', WAR: ',str(round(sortedHitters[i][5]*sortedHitters[i][9]['3B'],1)))
                hVal += sortedHitters[i][5]*sortedHitters[i][9]['3B']
        for i in range(len(sortedHitters)):
            if sortedHitters[i][9]['OF'] > 0:
                print(sortedHitters[i][1],', OF, PA: ',str(sortedHitters[i][9]['OF']),', WAR: ',str(round(sortedHitters[i][5]*sortedHitters[i][9]['OF'],1)))
                hVal += sortedHitters[i][5]*sortedHitters[i][9]['OF']
        for i in range(len(sortedHitters)):
            if sortedHitters[i][9]['DH'] > 0:
                print(sortedHitters[i][1],', DH, PA: ',str(sortedHitters[i][9]['DH']),', WAR: ',str(round(sortedHitters[i][6]*sortedHitters[i][9]['DH'],1)))
                hVal += sortedHitters[i][6]*sortedHitters[i][9]['DH']
        print('\n')
        print('Unused PA:')
        for i in range(len(sortedHitters)):
            if sortedHitters[i][9]['Bench'] == sortedHitters[i][3]:
                print(sortedHitters[i][1],', Bench, PA: ',str(sortedHitters[i][9]['Bench']),', WAR: ',str(round(sortedHitters[i][6]*sortedHitters[i][9]['Bench'],1)))
                

        print('Hitter WAR: ' + str(round(hVal,1)))

        hitterVal.append(hVal)
        pitcherVal.append(pVal)

        sumWAR = pVal + hVal

        print('Final WAR: ' + str(round(sumWAR,1)))
        print('\n')
        teamVal.append(sumWAR)

    #DISPLAY THE RESULTS 
    #Calculate standings
    #user_games has stored how many games have been played
    #Replacement level teams with 29.7% of games https://library.fangraphs.com/misc/war/replacement-level/
    repl_wins = .297*user_games
    #wins = round(repl_wins + teamVal[y])
    #losses = user_games - wins

    standings = []
    for i in range(len(teamNames)):
        standings.append([])
        standings[i].append(teamNames[i])
        standings[i].append(teamVal[i])
        standings[i].append(pitcherVal[i])
        standings[i].append(hitterVal[i])


    standings = sorted(standings, key=itemgetter(1), reverse=True)

    totalWAR = 0
    for y in range(len(standings)):
        totalWAR += standings[y][1]
        wins = round(repl_wins + standings[y][1])
        losses = round(user_games - wins)
        print(standings[y][0] + ', Record: ' + str(wins) + '-' + str(losses) + ', Pitcher WAR: ' + str(round(standings[y][2],1)) + ', Hitter WAR: ' + str(round(standings[y][3],1)))

    #print('Non-Drafted, Record: ' + str(round(repl_wins + teamVal[-1])) + '-' + str(user_games - round((repl_wins + teamVal[-1]))))
    #Calculate every other team's win loss record
    #WIN% is Wins/Games
    #WIN%(WAR) = (.297*Games + WAR)/Games
    #If every team had a 0.5 WIN%, total wins available above replacement would be:
    totWinsAvail = (.5*user_games - repl_wins)*30
    #The N teams in the league have collected totalWAR
    #The extra WAR over .500 they have collected is:
    leftoverWAR = totWinsAvail - totalWAR
    avgWins = round(repl_wins + leftoverWAR/(30 - 8))
    avgLoss = user_games - avgWins
    print('Remaining League Teams, Record: ' + str(avgWins) + '-' + str(avgLoss))

if __name__ == "__main__":
    main()

