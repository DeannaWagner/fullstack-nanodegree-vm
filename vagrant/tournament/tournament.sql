/* Tournament Project 2 is copyright 2015 Deanna M. Wagner.
 * DATABASE definition for the tournament project is found in tournament.sql file.
 * SQL 'CREATE TABLE' statements are in this file.
 */


DROP DATABASE IF EXISTS tournament;
CREATE database tournament;

\c tournament;

CREATE TABLE players (
    id serial PRIMARY KEY NOT NULL,
	name varchar(80) NOT NULL );

CREATE TABLE matches (
    match_id serial PRIMARY KEY NOT NULL,
	winner_id integer REFERENCES players(id),
	loser_id integer REFERENCES players(id) );
	
CREATE TABLE tournaments (
    tour_id serial PRIMARY KEY NOT NULL,
	tour_name varchar(80) NOT NULL );
	
CREATE TABLE tournaments_players (
    tournament_id integer REFERENCES tournaments(tour_id),
    player_id integer REFERENCES players(id) );

--Create View standings query

\q