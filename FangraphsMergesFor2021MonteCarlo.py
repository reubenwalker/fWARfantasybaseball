#Next steps are to automatically pull the necessary csv files from fangraphs.
#As it is, we first have to download:
    #Hitter Projections for the current year
    #Pitcher Projections for the current year
    #Fielding leaderboard from previous year (no minimum qualification)

import pandas as pd
#cd db (make sure you're in the correct folder
#Upload the hitters projections cv from export data button on:
    #https://www.fangraphs.com/projections.aspx?pos=all&stats=bat&type=fangraphsdc
hitters = pd.read_csv('Hitters2022.csv')
#Rename the WAR column to distinguish from pitcher WAR 
    #(almost exclusively to make one Ohtani player later)
hitters = hitters.rename(columns={'WAR' : 'hWAR'})

#We could also at this point calculate DH WAR, Runs/Win in 2021 was 9.973, -17.5 Runs for 162 game DH adjustment, here using 700 PA for simplicity
hitters['DHWAR'] = round(hitters['hWAR'] - hitters['Fld']/9.973 - hitters['PA']/700*(17.5/9.973), 1)
#This calculation still seems to include the positional adjustment. Off would give us offensive value, but it isn't available in depth charts proj.
#Let's grab ZIPS off stat
#We'll need to prorate their offensive value to the depth chart PA.
offense = pd.read_csv('Offense.csv')[['playerid', 'Off', 'PA']]
offense['prorOff'] = offense['Off']/offense['PA']
offense = offense[['playerid', 'prorOff']]
hitters = pd.merge(hitters, offense, on='playerid', how='left')

hitters['DHWAR'] = round((hitters['BsR'] + hitters['prorOff']*hitters['PA'])/9.973 - hitters['PA']/700*(17.5/9.973), 1)

#Upload the pitcher projections cv  from export data button on:
    #https://www.fangraphs.com/projections.aspx?pos=all&stats=pit&type=fangraphsdc&team=0&lg=all&players=0
pitchers = pd.read_csv('Pitchers2022.csv')
#Rename the WAR column to pitcher WAR to distinguish from hitter WAR    
    #Again, this is almost exclusively for Ohtani later.
pitchers = pitchers.rename(columns={'WAR' : 'pWAR'})
#Dowload the fielders stats from previous year
    #Make sure to change minimum PA to 0
    #https://www.fangraphs.com/leaders.aspx?pos=all&stats=bat&lg=all&qual=0&type=8&season=2021&month=0&season1=2021&ind=0&team=&rost=&age=&filter=&players=&startdate=&enddate=fielders = pd.read_csv('Fielders2021.csv')
fielders = pd.read_csv('Fielders2021.csv')
#Need to change LF, CF, RF to OF
fielders['Pos'][(fielders['Pos'] == 'LF') | (fielders['Pos'] ==  'CF') | (fielders['Pos'] == 'RF')] = 'OF'
#Change playerid to string for later merges:
fielders['playerid'] = fielders['playerid'].map(str)
#Now we need to combine outfield innings
fielders_of = fielders.groupby(['playerid','Pos','Name'],as_index=False).sum()
fielders_of

#What is our Innings threshold for eligibility. 
    #Games played isn't an option!
    #20 Games played is ESPN's standard
    #10 Games played was the 2020 version
    #10 Games* 9 innings
#eligible_fielders = fielders_of[fielders_of['Inn'] > 20]
eligible_fielders = fielders_of[fielders_of['Inn'] > 90]
#Could it be possible to take the highest innings played as their default, 
    #THEN remove any positions less than 90 IP?
#Create a string that combines all positions for easy readibility in-draft
eligible_fielders['Pos_string'] = eligible_fielders.groupby('playerid')['Pos'].transform(lambda x:','.join(x))
#Let's also do a dummy variable for later analysis for position eligibility.
pos_dummies = pd.get_dummies(eligible_fielders['Pos'])
pos_elig_binary = pd.concat([eligible_fielders[['playerid','Pos_string']],pos_dummies],axis=1)
#All we need for this position eligibility DataFrame is playerid, pos_string and their binary positions
pos_elig_final = pos_elig_binary[['playerid','Pos_string', 'C', '1B', '2B', 'SS', '3B', 'OF']]
#Finally, we'll group all players by their playerid with the string, summing over those binary positions.
pos_elig_final = pos_elig_final.groupby(by=['playerid','Pos_string'],as_index=False).sum()
pos_elig_final
#All projected hitters get 'Pos' DH = 1
hitters['DH'] = 1
#later, doubles (2B) and triples (3B) as columns will get in the way of a merge, so we'll rename them
hitters = hitters.rename(columns={'2B' : 'doubles','3B' : 'triples'})
#The data type for fielding are int64, I think all major league players have integer playerids
    #Some minor league players are projected for playing time
    #We'll map the integer pos_elig playerid to a string
    #Let's go back and just do this for the fielders DF.
#pos_elig_final['playerid'] = pos_elig_final['playerid'].map(str)
#Here we finally join hitters with their position eligibility
hitter_pos = pd.merge(hitters,pos_elig_final, on='playerid', how='left')
#THIS is the spot to create the DH eligibility in the string column. We do this for all hitters
hitter_pos['Pos_string'] = hitter_pos['Pos_string'] + ',DH'
#For all projected hitters who weren't position eligible last year, they get a DH
hitter_pos['Pos_string'].loc[hitter_pos['Pos_string'].isna()] = 'DH'
#hitter_pos[hitter_pos['Pos_string'].isna()].loc['Pos'] = 'DH'
hitter_pos.head()

#Need to do the same for pitchers' position
pitchers[['P','Pos_string']] = [1,'P']
#Here we concatenate the hitter (with pos-eligibility) and pitchers
leaderboard = pd.concat([hitter_pos, pitchers])
#The final draft leaderboard will have Name, Position, pitching WAR, hitting WAR, PA, IP, playerid, AND some calculated values
    #We'll leave the dummy variable versions in case we want that later.
#leaderboard_final = leaderboard[['Name','Pos_string','pWAR','hWAR','P','C','1B','2B','SS','3B','OF','DH','playerid']]
leaderboard_final = leaderboard[['Name','Pos_string','pWAR','hWAR', 'DHWAR', 'PA','IP','playerid']]
leaderboard_final
#leaderboard_final = leaderboard_final.fillna(0)
# leaderboard_final = leaderboard_final.groupby(['playerid'],as_index=False).agg({'Name' : 'first',
                                                                               # 'Pos_string': 'first',
                                                                               # 'pWAR' : 'sum',
                                                                               # 'hWAR' : 'sum',
                                                                               # 'P' : 'sum',
                                                                               # 'C' : 'sum',
                                                                               # '1B' : 'sum',
                                                                               # '2B' : 'sum',
                                                                               # 'SS' : 'sum',
                                                                               # '3B' : 'sum',
                                                                               # 'OF' : 'sum',
                                                                               # 'DH' : 'sum'})
#This is essentially the Ohtani merge:
leaderboard_final = leaderboard_final.groupby(['playerid'],as_index=False).agg({'Name' : 'first',
                                                                               'Pos_string': 'first',
                                                                               'pWAR' : 'sum',
                                                                               'hWAR' : 'sum',
                                                                               'DHWAR' : 'sum',
                                                                               'IP' : 'first',
                                                                               'PA' : 'first'})
leaderboard_final
#Now we add the hitting and pitching WAR together (for Ohtani)
leaderboard_final['WAR'] = leaderboard_final['hWAR'].fillna(0) + leaderboard_final['pWAR'].fillna(0)
#Because of the league scoring, it's important for everyone to see prorated WAR in the draft. 
    #Arbitrarily choosing 200IP and 700PA
leaderboard_final['pWAR200IP'] = round(leaderboard_final['pWAR']/leaderboard_final['IP']*200,1)
leaderboard_final['hWAR700PA'] = round(leaderboard_final['hWAR']/leaderboard_final['PA']*700,1)
leaderboard_final['DHWAR700PA'] = round(leaderboard_final['DHWAR']/leaderboard_final['PA']*700,1)
leaderboard_final
leaderboard_final.sort_values('WAR', ascending=False)
#leaderboard_final = leaderboard_final[['Name','hWAR','pWAR','WAR','P','C','1B','2B','SS','3B','OF','DH','playerid']].sort_values(by='WAR',ascending=False,ignore_index=True)
leaderboard_final = leaderboard_final[['Name','Pos_string','WAR','PA','IP','hWAR','pWAR', 'DHWAR','hWAR700PA','pWAR200IP', 'DHWAR700PA', 'playerid']].sort_values(by='WAR',ascending=False,ignore_index=True).fillna(0)
#Change Pos_string column to Pos
leaderboard_final = leaderboard_final.rename(columns={'Pos_string' : 'Pos'})
#The index is arbitrary for a table that is going to be sorted. Let's just make it the playerid
leaderboard_final = leaderboard_final.set_index('playerid')

ask = input('Do you need to merge with owners? y/n: ')
if ask.lower() == 'y':
    owners = pd.read_csv('DraftAndForget2022 - Sheet1.csv')
    owners = owners[['playerid', 'Owner']]
    leaderboard_final = pd.merge(leaderboard_final, owners, on='playerid', how='left')[['Name','Pos','WAR', 'Owner', 'PA','IP','hWAR','pWAR', 'DHWAR','hWAR700PA','pWAR200IP', 'DHWAR700PA', 'playerid']].sort_values(by='WAR',ascending=False,ignore_index=True).set_index('playerid')

#Let's send this to a csv:
leaderboard_final.to_csv('DraftLeaderboard2022.csv', sep=',')


