# !/usr/bin/env python
# Tournament Project 2 is copyright 2015 Deanna M. Wagner.
# tournament.py is an implementation of a Swiss-system tournament.
# 
#


import psycopg2
import bleach


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the match records from the database."""
    db = connect()
    cursor = db.cursor()
    cursor.execute("DELETE FROM matches;")
    db.commit()
    db.close()


def deletePlayers():
    """Remove all the player records from the database."""
    db = connect()
    cursor = db.cursor()
    cursor.execute("DELETE FROM players;")
    db.commit()
    db.close()


def countPlayers():
    """Returns the number of players currently registered."""
    db = connect()
    cursor = db.cursor()
    cursor.execute("SELECT count(*) FROM players;")
    sum_player = cursor.fetchone()
    db.close()
    return sum_player[0]


def registerPlayer(name):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """
    db = connect()
    cursor = db.cursor()
    bleach.clean(name)
    cursor.execute("INSERT INTO players (name) VALUES (%s);", (name, ) )
    db.commit()
    db.close()


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    db = connect()
    cursor = db.cursor()
    cursor.execute("""
      SELECT players.id,
          players.name, 
          (SELECT count(*)
           FROM matches 
           WHERE players.id = matches.winner_id) 
               AS wins, 
          (SELECT count(*)
           FROM matches 
           WHERE players.id = matches.winner_id 
               OR players.id = matches.loser_id) 
               AS matches_played
      FROM players 
      ORDER BY wins DESC;""")
    standings = cursor.fetchall()
    db.close()
    return standings


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    db = connect()
    cursor = db.cursor()
    cursor.execute("""
        INSERT INTO matches (winner_id, loser_id) 
        VALUES ( %s, %s );""", (winner, loser) )
    db.commit()
    db.close()
 

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

 
def swissPairings():
    """Returns a list of pairs of players for the next round of a match.
  
    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.
  
    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    standings = playerStandings() #(id, name, wins, matches)
    pairings = []
    p_id = 0 #first item in tuple
    name = 1 #second item in tuple
    i = 0
    while i < len(standings) - 1:
        if matchCount(standings[i][p_id], standings[i+1][p_id]) > 0:
            if i == len(standings) - 2:
                print "We hit rematch with last pair"
                pairings.append((standings[i][p_id], \
                                 standings[i][name], \
                                 standings[i-2][p_id], \
                                 standings[i-2][name]))
                pairings.append((standings[i+1][p_id], \
                                 standings[i+1][name], \
                                 standings[i-1][p_id], \
                                 standings[i-1][name]))
            else:
                print "We hit rematch"
                pairings.append((standings[i][p_id], \
                                 standings[i][name], \
                                 standings[i+2][p_id], \
                                 standings[i+2][name]))
                pairings.append((standings[i+1][p_id], \
                                 standings[i+1][name], \
                                 standings[i+3][p_id], \
                                 standings[i+3][name]))
                print standings[i][name]
                print standings[i+2][name]
                print standings[i+1][name]
                print standings[i+3][name]

        else:
            pairings.append((standings[i][p_id], \
                             standings[i][name], \
                             standings[i+1][p_id], \
                             standings[i+1][name]))
        i += 2
    return pairings
