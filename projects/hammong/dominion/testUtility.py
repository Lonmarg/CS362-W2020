"""
Created on Tue January 14 03:30 2020

@author: Geoffry Hammon
"""

import Dominion
import random
from collections import defaultdict


# Get player names
def getplayernames(namelist):
    playernames = []
    for name in namelist:
        playernames.append(name)

    return playernames


# number of curses and victory cards
def setupcurses(playernames):
    if len(playernames) > 2:
        nv = 12
    else:
        nv = 8

    return nv


def setupvictorycards(playernames):
    return -10 + 10 * len(playernames)


# Define box
def getboxes(nv):
    box = {}
    box["Woodcutter"] = [Dominion.Woodcutter()] * 10
    box["Smithy"] = [Dominion.Smithy()] * 10
    box["Laboratory"] = [Dominion.Laboratory()] * 10
    box["Village"] = [Dominion.Village()] * 10
    box["Festival"] = [Dominion.Festival()] * 10
    box["Market"] = [Dominion.Market()] * 10
    box["Chancellor"] = [Dominion.Chancellor()] * 10
    box["Workshop"] = [Dominion.Workshop()] * 10
    box["Moneylender"] = [Dominion.Moneylender()] * 10
    box["Chapel"] = [Dominion.Chapel()] * 10
    box["Cellar"] = [Dominion.Cellar()] * 10
    box["Remodel"] = [Dominion.Remodel()] * 10
    box["Adventurer"] = [Dominion.Adventurer()] * 10
    box["Feast"] = [Dominion.Feast()] * 10
    box["Mine"] = [Dominion.Mine()] * 10
    box["Library"] = [Dominion.Library()] * 10
    box["Gardens"] = [Dominion.Gardens()] * nv
    box["Moat"] = [Dominion.Moat()] * 10
    box["Council Room"] = [Dominion.Council_Room()] * 10
    box["Witch"] = [Dominion.Witch()] * 10
    box["Bureaucrat"] = [Dominion.Bureaucrat()] * 10
    box["Militia"] = [Dominion.Militia()] * 10
    box["Spy"] = [Dominion.Spy()] * 10
    box["Thief"] = [Dominion.Thief()] * 10
    box["Throne Room"] = [Dominion.Throne_Room()] * 10

    return box


def setupsupplyorder():
    supplyorder = {0: ['Curse','Copper'],2:['Estate','Cellar','Chapel','Moat'],
                   3: ['Silver','Chancellor','Village','Woodcutter','Workshop'],
                   4: ['Gardens','Bureaucrat','Feast','Militia','Moneylender','Remodel','Smithy','Spy','Thief','Throne Room'],
                   5: ['Duchy','Market','Council Room','Festival','Laboratory','Library','Mine','Witch'],
                   6: ['Gold','Adventurer'],8:['Province']}

    return supplyorder


# Pick 10 cards from box to be in the supply.
def getrandomsupply(box, count):
    boxlist = [k for k in box]
    random.shuffle(boxlist)
    randomcount = boxlist[:count]
    return defaultdict(list, [(k, box[k]) for k in randomcount])


# The supply always has these cards
def setupsupply(supply, playernames, nv, nc):
    supply["Copper"] = [Dominion.Copper()] * (60 - len(playernames) * 7)
    supply["Silver"] = [Dominion.Silver()] * 40
    supply["Gold"] = [Dominion.Gold()] * 30
    supply["Estate"] = [Dominion.Estate()] * nv
    supply["Duchy"] = [Dominion.Duchy()] * nv
    supply["Province"] = [Dominion.Province()] * nv
    supply["Curse"] = [Dominion.Curse()] * nc

    return supply


# initialize the trash
def setuptrash():
    trash = []
    return trash


# Costruct the Player objects
def constructplayerobjects(playernames):
    players = []

    for name in playernames:
        if name[0] == "*":
            players.append(Dominion.ComputerPlayer(name[1:]))
        elif name[0] == "^":
            players.append(Dominion.TablePlayer(name[1:]))
        else:
            players.append(Dominion.Player(name))

    return players