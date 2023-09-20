#Comparison for ROS from Fangraphs
s = pd.read_csv('season_h.csv')
r = pd.read_csv('ROS_h.csv')
s.loc[:, 'PlayerId'] = s.loc[:, 'PlayerId'].astype('str')
#Prorate dollars to PA
s['D'] = s['Dollars']/s['PA']
r['D_'] = r['Dollars']/s['PA']

comp_h = pd.merge(s[['PlayerId','D']],r[['PlayerId','Name','D_']], on='PlayerId')
comp_h['D_f'] = comp_h['D_'] - comp_h['D']
comp_h = comp_h[comp_h['D_'] > 0]
comp_h.sort_values('D_f',ascending=False).head(50)

#Values
comp_h = pd.merge(s[['PlayerId','Dollars']],r[['PlayerId','Name','Dollars']], on='PlayerId')
comp_h['D_f'] = comp_h['Dollars_y'] - comp_h['Dollars_x']
comp_h = comp_h[comp_h['Dollars_y'] > 0]
comp_h.sort_values('D_f',ascending=False).head(50)
###Overperformers
comp_h = pd.merge(s[['PlayerId','Dollars']],r[['PlayerId','Name','Dollars']], on='PlayerId')
comp_h['D_f'] = comp_h['Dollars_y'] - comp_h['Dollars_x']
comp_h = comp_h[comp_h['Dollars_x'] > 0]
comp_h.sort_values('D_f').head(50)

###Pitchers
#Comparison for ROS from Fangraphs
s = pd.read_csv('season.csv')
r = pd.read_csv('ROS.csv')
s.loc[:, 'PlayerId'] = s.loc[:, 'PlayerId'].astype('str')
#Prorate dollars to PA
s['D'] = s['Dollars']/s['IP']
r['D_'] = r['Dollars']/s['IP']

comp_p = pd.merge(s[['PlayerId','D']],r[['PlayerId','Name','D_']], on='PlayerId')
comp_p['D_f'] = comp_p['D_'] - comp_p['D']
comp_p = comp_p[comp_p['D_'] > 0]
comp_p.sort_values('D_f',ascending=False).head(50)

#Values
comp_p = pd.merge(s[['PlayerId','Dollars']],r[['PlayerId','Name','Dollars']], on='PlayerId')
comp_p['D_f'] = comp_p['Dollars_y'] - comp_p['Dollars_x']
comp_p = comp_p[comp_p['Dollars_y'] > 0]
comp_p.sort_values('D_f',ascending=False).head(50)
###Overperformers
comp_p = pd.merge(s[['PlayerId','Dollars']],r[['PlayerId','Name','Dollars']], on='PlayerId')
comp_p['D_f'] = comp_p['Dollars_y'] - comp_p['Dollars_x']
comp_p = comp_p[comp_p['Dollars_x'] > 0]
comp_p.sort_values('D_f').head(50)