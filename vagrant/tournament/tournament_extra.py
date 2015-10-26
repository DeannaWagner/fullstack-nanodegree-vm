# !/usr/bin/env python
#
# Project 2: Tournament Results Application is copyright 2015 Deanna M. Wagner.
# tournament_extra.py is an implementation of a Swiss-system tournament, which
# takesplayers, pairs them for matches, reports matches and standings. Players
# and matches can be distinguished by tournament in this extra credit version.
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
    cursor.execute("DELETE FROM tournaments_players;")
    cursor.execute("DELETE FROM players;")
    db.commit()
    db.close()


def deleteTournaments():
    """Remove all the tournament records from the database."""
    db = connect()
    cursor = db.cursor()
    cursor.execute("DELETE FROM tournaments;")
    db.commit()
    db.close()


def countPlayers(tournament_id):
    """Returns the number of players registered in a given tournament.

    Args:
      tournament_id: the id of the tournament in which player will play.

    Returns:
      int(sum_player[0]) which represents current numer of players registered
        in a given tournament
    """
    db = connect()
    cursor = db.cursor()
    bleach.clean(tournament_id)
    cursor.execute("""
        SELECT player_count FROM vcount
        WHERE tournament_id = %s;""", (tournament_id,))
    sum_player = cursor.fetchone()
    if sum_player == None:
        sum_player = [0]
    db.close()
    return int(sum_player[0])


def registerTournament(name):
    """Adds a tournament to the tournament database and returns the id.

    Args:
      name: the tournament's name (need not be unique).

    Returns:
      tournament_id: the tournament's unique id (assigned by the database)
    """
    db = connect()
    cursor = db.cursor()
    bleach.clean(name)
    cursor.execute("""
        INSERT INTO tournaments (name) VALUES (%s) RETURNING id;""", (name, ))
    tournament_id = cursor.fetchone()[0];
    db.commit()
    db.close()
    return tournament_id


def registerPlayer(name, tournament_id):
    """Adds a player to the tournament database, associating them with the
    given tournament, and returns the player_id

    Args:
      name: the player's full name (need not be unique).
        tournament_id: the id of the tournament in which player will play.

    Returns:
      player_id: the player's unique id (assigned by the database)
    """
    db = connect()
    cursor = db.cursor()
    bleach.clean(name)
    cursor.execute("""
        INSERT INTO players (name) VALUES (%s) RETURNING id;""", (name,))
    player_id = cursor.fetchone()[0];
    bleach.clean(tournament_id)
    bleach.clean(player_id)
    cursor.execute("""
        INSERT INTO tournaments_players (tournament_id, player_id) 
        VALUES (%s, %s);""", (tournament_id, player_id))
    db.commit()
    db.close()
    return player_id


def playerStandings(tournament_id):
    """Returns a list of the players and their win records, sorted by wins
       only for a given tournament.

    The first entry in the list should be the player in first place, or the 
    player tied for first place if there is currently a tie.

    Args:
      tournament_id: the id of the tournament in which player will play.

    Returns:
      standings, a list of tuples, each containing (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    db = connect()
    cursor = db.cursor()
    bleach.clean(tournament_id)
    cursor.execute("""
        SELECT players.id,
        players.name,
        (SELECT count(*)
            FROM matches
            WHERE players.id = matches.winner_id AND tournament_id = %s) 
                AS wins,
        (SELECT count(*)
            FROM matches 
            WHERE (players.id = matches.winner_id
              OR players.id = matches.loser_id) AND tournament_id = %s ) 
                AS matches_played
        FROM tournaments_players JOIN players ON id = player_id
        WHERE tournament_id = %s
        ORDER BY wins DESC;
        """, (tournament_id, tournament_id, tournament_id))
    standings = cursor.fetchall()
    db.close()
    return standings


def reportMatch(winner, loser, tournament_id):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
      tournament_id: the id of the tournament in which player participated.
    """
    db = connect()
    cursor = db.cursor()
    bleach.clean(winner)
    bleach.clean(loser)
    bleach.clean(tournament_id)
    cursor.execute("""
        INSERT INTO matches (winner_id, loser_id, tournament_id)
        VALUES ( %s, %s, %s );""", (winner, loser, tournament_id))
    db.commit()
    db.close()


def swissPairings(tournament_id):
    """Returns a list of pairs of players for the next round of a match.

    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.

    Args:
      tournament_id: the id of the tournament in which player will play.

    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    standings = playerStandings(tournament_id)
    pairings = []
    p_id = 0 #first item in tuple
    name = 1 #second item in tuple
    i = 0
    while i < len(standings) - 1:
        pairings.append((standings[i][p_id], \
                             standings[i][name], \
                             standings[i+1][p_id], \
                             standings[i+1][name]))
        i += 2
    return pairings
