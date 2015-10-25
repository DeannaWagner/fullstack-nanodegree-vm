# !/usr/bin/env python
# Project 2: Tournament Results Application is copyright 2015 Deanna M. Wagner.
# Test determines if the prevention of rematches extra credit option, found in
# in tournament.py is functioning as it should.
#


from tournament import *
import math


def matchCount(player1, player2):
    """Counts time players have had matches in a given tournament.

    Args: 
      player1: id of first player
      player2: id of second player

    Returns:
      Integer indicating the number of matches the players have played
      together
    """
    db = connect()
    cursor = db.cursor()
    cursor.execute("""
        SELECT count(*) AS numMatches
        FROM matches
        WHERE (%s = matches.winner_id OR %s = matches.loser_id)
          AND (%s = matches.winner_id OR %s = matches.loser_id)""", \
          (player1, player1, player2, player2))
    numMatches = cursor.fetchone()
    db.close()
    return numMatches[0]




def swissPairingsNoRematches():
    """Returns a list of pairs of players for the next round of a match.

    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings, unless those players have already completed
    a match together.

    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    
#    standings = playerStandings()
#    wins_col = 2
#    if standings[0][wins_col] == 0: #if no wins, then 1st round, shuffle
#        shuffle(standings)
    db = connect()
    cursor = db.cursor()
    cursor.execute("""
        SELECT a_id, a_name, b_id, b_name
        FROM vno_rematch;
        """)
    pairings = cursor.fetchall()
    db.close()

    return pairings   

def testRematches():
    """Tests functionality of swissPairingsNoRematches().  Player count can be
    changed to any even number greater than or equal to 4. Many print lines
    to help see how rounds progress."""
    deleteMatches()
    deletePlayers()
    playerCount = 8
    i = 0
    while i < playerCount:
        registerPlayer("P%d" % i)
        i += 1
    tour_round = 1
    rounds = 1 #math.log(playerCount, 2)
    print "Rounds=%d" % rounds
    rematchError = False;
    while tour_round <= rounds:
        pairings = swissPairingsNoRematches()
        i = 0
        print "Pairings:"
        print pairings
        while i < len(pairings):
            reportMatch(pairings[i][0], pairings[i][2])
            players_matched = matchCount(pairings[i][0], pairings[i][2])
            print players_matched
            if players_matched > 1:
                rematchError = True
                print "1. After one match, players should not be paired again!"
            i += 1
        tour_round += 1
    print "Standings:"
    print playerStandings()
    if rematchError:
        raise ValueError("Players should only meet in one match.")



if __name__ == '__main__':
    testRematches()
    print "Success!  Tests for extra credit  pass!"


# --View vno_rematch queries for pairing players based on wins and match history
# CREATE VIEW vno_rematch AS
#     SELECT DISTINCT ON(a.wins < b.wins) a.id AS a_id,
#     a.name AS a_name,
#     b.id AS b_id,
#     b.name AS b_name,
#     a.wins AS a_wins,
#     b.wins AS b_wins,
#     (SELECT count(*) AS numMatches
#         FROM matches
#         WHERE (a.id = matches.winner_id OR a.id = matches.loser_id)
#           AND (b.id = matches.winner_id OR b.id = matches.loser_id))
#     FROM vstandings AS a, vstandings AS b      
#     WHERE a.id < b.id
#     ORDER BY a.wins < b.wins, abs(a.wins - b.wins); 
