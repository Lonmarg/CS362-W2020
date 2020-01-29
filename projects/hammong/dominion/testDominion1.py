# -*- coding: utf-8 -*-
"""
Created on Tue January 14 03:30 2020

@author: Geoffry Hammon
"""


import Dominion
import testUtility

# Get player names
player_names = testUtility.getplayernames(["Annie", "*Ben", "*Carla"])

# number of curses and victory cards
nV = 0  # testUtility.setupvictorycards(player_names)
nC = testUtility.setupcurses(player_names)

# Define box
box = testUtility.getboxes(nV)
supply_order = testUtility.setupsupplyorder()

# Pick 10 cards from box to be in the supply.
supply = testUtility.getrandomsupply(box, 10)

# The supply always has these cards
supply = testUtility.setupsupply(supply, player_names, nV, nC)

# initialize the trash
trash = testUtility.setuptrash()

# Costruct the Player objects
players = testUtility.constructplayerobjects(player_names)

# Play the game
turn = 0
while not Dominion.gameover(supply):
    turn += 1    
    print("\r")    
    for value in supply_order:
        print(value)
        for stack in supply_order[value]:
            if stack in supply:
                print(stack, len(supply[stack]))
    print("\r")
    for player in players:
        print(player.name, player.calcpoints())
    print("\rStart of turn " + str(turn))
    for player in players:
        if not Dominion.gameover(supply):
            print("\r")
            player.turn(players, supply, trash)
            

# Final score
dcs = Dominion.cardsummaries(players)
vp = dcs.loc['VICTORY POINTS']
vpMax = vp.max()
winners = []
for i in vp.index:
    if vp.loc[i] == vpMax:
        winners.append(i)
if len(winners) > 1:
    winString = ' and '.join(winners) + ' win!'
else:
    winString = ' '.join([winners[0], 'wins!'])

print("\nGAME OVER!!!\n" + winString + "\n")
print(dcs)