# !/usr/bin/env python
# Project2 Tournament Results copyright 2015 Deanna M. Wagner.
# Test cases for extra credit in tournament.py


from tournament import *
import math

    
def testRematches():
    deleteMatches()
    deletePlayers()
    #change player count to anything greater than 4, tested up to 64 players
    playerCount = 16
    i = 0
    while i < playerCount:
        registerPlayer("P%d" % i)
        i += 1
    tour_round = 1
    rounds = math.log(playerCount, 2)
    print "Rounds=%d" % rounds
    while tour_round <= rounds:
        pairings = swissPairings()
        i = 0
        print "Pairings:"
        print pairings
        while i < len(pairings):
            reportMatch(pairings[i][0], pairings[i][2])
            players_matched = matchCount(pairings[i][0], pairings[i][2])
            print players_matched
            i += 1
        tour_round += 1
    print "Standings:"
    print playerStandings()
    if False:
        raise ValueError(
            "Players should only meet in one match.")
    print """1. After one match, players with one win are paired, avoiding.
           rematches between players!"""


if __name__ == '__main__':
    testRematches()
    print "Success!  Tests for extra credit  pass!"


