# fWARfantasybaseball
Home Brewed Draft-and-Forget Fantasy Baseball League Using Fangraphs WAR

Three step process to score a baseball fantasy league throughout the season:

1. CreateFangraphsDraftLeaderboard.py uses pandas to produce a csv file that one can use to draft players online through a shared google doc

2. FangraphsMergesFor2021MonteCarlo.py merges the resulting google doc with owners and munges the data for the Monte Carlo simulation

3. DraftForgetMonteCarlo2021.py is a script that takes all of the players on a given team and optimizes their use given their stats to provide a team win total
