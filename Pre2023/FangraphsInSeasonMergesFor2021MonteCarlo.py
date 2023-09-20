#As it is, we first have to download:
    #Hitter Projections for the current year
    #Pitcher Projections for the current year
    #Fielding leaderboard from previous year (no minimum qualification)
    #Draft results with owner names
    
#The 2021 monte carlo file is needlessly complex and this file is just enabling that complexity, 
    #but it should work for now.

import pandas as pd
#cd db (make sure you're in the correct folder
#Upload the hitters projections cv from export data button on:
    #https://www.fangraphs.com/projections.aspx?pos=all&stats=bat&type=fangraphsdc
#Upload owners with playerids from the draft spreadsheet
owners = pd.read_csv('DraftAndForget2022 - Sheet1.csv')
owners = owners[['playerid', 'Owner']]
#Clear leading/trailing space from owner ames
mask = owners['Owner'].notna()
owners.loc[mask,'Owner'] = owners.loc[mask,'Owner'].apply(lambda x: x.strip())
#owners[owners['Owner'].notna()]['Owner'] = owners[owners['Owner'].notna()]['Owner'].apply(lambda x: x.strip())
hitters = pd.read_csv('Hitters202208.csv')
hitters['playerid'] = hitters['playerid'].map(str)


#We could also at this point calculate DH WAR, Runs/Win in 2021 was 9.973, -17.5 Runs for 162 game DH adjustment, here using 700 PA for simplicity
hitters['DHWAR'] = round(hitters['WAR'] - hitters['Def']/9.973 - hitters['PA']/700*(17.5/9.973), 1)
#This calculation still seems to include the positional adjustment. Off would give us offensive value, but it isn't available in depth charts proj.
#Let's grab ZIPS off stat
#We'll need to prorate their offensive value to the depth chart PA.
#offense = pd.read_csv('Offense.csv')[['playerid', 'Off', 'PA']]
#offense['prorOff'] = offense['Off']/offense['PA']
hitters['prorOff'] = hitters['Off']/hitters['PA']
#offense = offense[['playerid', 'prorOff']]
#hitters = pd.merge(hitters, offense, on='playerid', how='left')

hitters['DHWAR'] = round((hitters['BsR'] + hitters['prorOff']*hitters['PA'])/9.973 - hitters['PA']/700*(17.5/9.973), 1)

#Upload the pitcher projections cv  from export data button on:
    #https://www.fangraphs.com/projections.aspx?pos=all&stats=pit&type=fangraphsdc&team=0&lg=all&players=0
pitchers = pd.read_csv('Pitchers202208.csv')
pitchers['playerid'] = pitchers['playerid'].map(str)
#Rename the WAR column to pitcher WAR to distinguish from hitter WAR    
    #This was for when we weren't having repeat players.
#pitchers = pitchers.rename(columns={'WAR' : 'pWAR'})

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
#(Here's where we break from the leaderboard code):
#We just want pitchers to be pitchers, each case of a fielder becomes a unique hitter.

hitter_pos = pd.merge(hitters, eligible_fielders[['playerid', 'Pos']], on='playerid', how='left')
#The left join makes sure we don't lose our DHs or people who didn't play in 2021. 
    #They have NAs as their position.
#hitter_pos[hitter_pos['Pos'].isna()]['Pos']
#Let's set those to DH.
mask = hitter_pos['Pos'].isna()
hitter_pos.loc[mask,'Pos'] = 'DH'
#There were a couple hitters who had Depth charts projections, but no ZIPS projections
mask = hitter_pos['DHWAR'].isna()
hitter_pos.loc[mask,'DHWAR'] = 0
pitchers['Pos'] = 'P'

#Let's see if we can create a simulation of the final leaderboards from 2021's Monte Carlo code
#Column names without headers:
#playerID,Name,Pos,PA,WAR,proratedProj (700 PA),DHWAR (NULL for pitchers), OWNER
#Prorate hitter WAR, before this
hitter_pos['hWAR700PA'] = round(hitter_pos['WAR']/hitter_pos['PA']*700,1)
#Make prorated WAR zero for any PA zero
mask = hitter_pos['hWAR700PA'].isna()
hitter_pos.loc[mask,'hWAR700PA'] = 0
#Merge hitters with owners
hitter_pos = pd.merge(hitter_pos, owners, on='playerid', how='left')
hitter_pos[['playerid', 'Name', 'Pos', 'PA', 'WAR', 'hWAR700PA', 'DHWAR', 'Owner']].to_csv('FinalRankingsHitters.csv', sep=',', index=False, header=False)
#Merge pitchers with owners
pitchers = pd.merge(pitchers, owners, on='playerid', how='left')
#Prorate WAR
pitchers['pWAR200IP'] = round(pitchers['WAR']/pitchers['IP']*200,1)
mask = pitchers['pWAR200IP'].isna()
pitchers.loc[mask,'pWAR200IP'] = 0
#Create placeholder column
pitchers['DHWAR'] = 0
pitchers[['playerid', 'Name', 'Pos', 'IP', 'WAR', 'pWAR200IP', 'DHWAR', 'Owner']].to_csv('FinalRankingsPitchers.csv', sep=',', index=False, header=False)