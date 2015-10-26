/* Tournament Results Application, Project 2 is copyright 2015 Deanna M. Wagner.
 * DATABASE definition for the tournament project is found in tournament.sql.
 * SQL 'CREATE TABLE' and 'CREATE VIEW' statements are in this file.
 */


DROP DATABASE IF EXISTS tournament;
CREATE database tournament;

\c tournament;

--Table players stores id and names of all players
CREATE TABLE players (
    id serial PRIMARY KEY NOT NULL,
	name text NOT NULL );

--Table matches stores the match ID, winner and loser, for any given match
CREATE TABLE matches (
    id serial PRIMARY KEY NOT NULL,
	winner_id integer REFERENCES players(id),
	loser_id integer REFERENCES players(id) );

--View v_standings queries each item which is returned by playerStandings()
CREATE VIEW vstandings AS
    SELECT players.id,
    players.name,
    (SELECT count(*)
        FROM matches 
        WHERE players.id = matches.winner_id) 
            AS wins,
    (SELECT count(*)
        FROM matches 
        WHERE players.id = matches.winner_id OR players.id = matches.loser_id) 
            AS matches_played
    FROM players
    ORDER BY wins DESC;

\q