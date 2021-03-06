#!/usr/bin/env python
#
# Project 2: Tournament Results Application by 2015 Deanna M. Wagner.
# Test cases for tournament_extra.py, which were modified from the original
# test module that was provided by Udacity for testing the main program
# functionality.
#


from tournament_extra import *


def testDeleteMatches():
    deleteMatches()
    print "1. Old matches can be deleted."


def testDelete():
    deleteMatches()
    deletePlayers()
    deleteTournaments()
    print "2. All records can be deleted."


def testCount():
    tournament_id = registerTournament("2015 Biffy's Wrestling Extraordinaire")
    c = countPlayers(tournament_id)
    if c == '0':
        raise TypeError(
            "countPlayers() should return numeric zero, not string '0'.")
    if c != 0:
        raise ValueError("After deleting, countPlayers should return zero.")
    print "3. After deleting, countPlayers() returns zero."


def testRegister():
    deleteMatches()
    deletePlayers()
    deleteTournaments()
    tournament_id = registerTournament("2015 UT Dallas Chess Invitational")
    registerPlayer("Chandra Nalaar", tournament_id)
    c = countPlayers(tournament_id)
    if c != 1:
        raise ValueError(
            "After one player registers, countPlayers() should be 1.")
    print "4. After registering a player, countPlayers() returns 1."


def testRegisterCountDelete():
    deleteMatches()
    deletePlayers()
    tournament_id = registerTournament("2015 UT Dallas Chess Invitational")
    registerPlayer("Markov Chaney", tournament_id)
    registerPlayer("Joe Malik", tournament_id)
    registerPlayer("Mao Tsu-hsi", tournament_id)
    registerPlayer("Atlanta Hope", tournament_id)
    tournament_id2 = registerTournament("2015 Ft. Worth TKD Invitational")
    registerPlayer("Chong Jeong", tournament_id2)
    registerPlayer("Inseom Kim", tournament_id2)
    registerPlayer("Won Park", tournament_id2)
    registerPlayer("Roy Kurban", tournament_id2)
    registerPlayer("Stephen Lopez", tournament_id2)
    registerPlayer("Erik Farfan", tournament_id2)
    c1 = countPlayers(tournament_id)
    c2 = countPlayers(tournament_id2)
    if c1 != 4 or c2 != 6:
        raise ValueError(
            "After registering players, countPlayers was incorrect.")
    deletePlayers()
    c1 = countPlayers(tournament_id)
    c2 = countPlayers(tournament_id2)
    if c1 != 0 or c2 != 0:
        raise ValueError("After deleting, countPlayers should return zero.")
    print "5. Players can be registered and deleted."


def testStandingsBeforeMatches():
    deleteMatches()
    deletePlayers()
    tournament_id = registerTournament("2015 UT Dallas Chess Invitational")
    registerPlayer("Melpomene Murray", tournament_id)
    registerPlayer("Randy Schwartz", tournament_id)
    standings = playerStandings(tournament_id)
    if len(standings) < 2:
        raise ValueError("Players should appear in playerStandings even before"
                         " they have played any matches.")
    elif len(standings) > 2:
        raise ValueError("Only registered players should appear in standings.")
    if len(standings[0]) != 4:
        raise ValueError("Each playerStandings row should have four columns.")
    [(id1, name1, wins1, matches1), (id2, name2, wins2, matches2)] = standings
    if matches1 != 0 or matches2 != 0 or wins1 != 0 or wins2 != 0:
        raise ValueError(
            "Newly registered players should have no matches or wins.")
    if set([name1, name2]) != set(["Melpomene Murray", "Randy Schwartz"]):
        raise ValueError("Registered players' names should appear in standings, "
                         "even if they have no matches played.")
    print "6. Newly registered players appear in the standings with no matches."


def testReportMatches():
    deleteMatches()
    deletePlayers()
    tournament_id= registerTournament("2015 UT Dallas Chess Invitational")
    registerPlayer("Bruno Walton", tournament_id)
    registerPlayer("Boots O'Neal", tournament_id)
    registerPlayer("Cathy Burton", tournament_id)
    registerPlayer("Diane Grant", tournament_id)
    standings = playerStandings(tournament_id)
    [id1, id2, id3, id4] = [row[0] for row in standings]
    reportMatch(id1, id2, tournament_id)
    reportMatch(id3, id4, tournament_id)
    standings = playerStandings(tournament_id)
    for (i, n, w, m) in standings:
        if m != 1:
            raise ValueError("Each player should have one match recorded.")
        if i in (id1, id3) and w != 1:
            raise ValueError("Each match winner should have one win recorded.")
        elif i in (id2, id4) and w != 0:
            raise ValueError("Each match loser should have zero wins recorded.")
    print "7. After a match, players have updated standings."


def testPairings(tournament_id):
    registerPlayer("Twilight Sparkle", tournament_id)
    registerPlayer("Fluttershy", tournament_id)
    registerPlayer("Applejack", tournament_id)
    registerPlayer("Pinkie Pie", tournament_id)
    standings = playerStandings(tournament_id)
    [id1, id2, id3, id4] = [row[0] for row in standings]
    reportMatch(id1, id2, tournament_id)
    reportMatch(id3, id4, tournament_id)
    pairings = swissPairings(tournament_id)
    if len(pairings) != 2:
        raise ValueError(
            "For four players, swissPairings should return two pairs.")
    [(pid1, pname1, pid2, pname2), (pid3, pname3, pid4, pname4)] = pairings
    correct_pairs = set([frozenset([id1, id3]), frozenset([id2, id4])])
    actual_pairs = set([frozenset([pid1, pid2]), frozenset([pid3, pid4])])
    if correct_pairs != actual_pairs:
        raise ValueError(
            "After one match, players with one win should be paired.")
    print "8. After one match, players with one win are paired."


if __name__ == '__main__':
    testDeleteMatches()
    testDelete()
    testCount()
    testRegister()
    testRegisterCountDelete()
    testStandingsBeforeMatches()
    testReportMatches()
    deleteMatches()
    deletePlayers()
    deleteTournaments()
    tournament_id = registerTournament("2015 Queens of Bridge Takedown")
    testPairings(tournament_id)
    tournament_id = registerTournament("2015 Gaming World Championship")
    testPairings(tournament_id)
    print "Success!  All tests pass!"
