-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

--First create database tournament to hold Players and Matches table.
create database tournament;

\c tournament

--Create table players to hold Player data including id and name. Primary key is player_id.
create table Players (
player_id serial primary key, 
player_name text NOT NULL);

--Create table matches to hold Match data including players' ids and the winner's player_id.
--Primay key is match_id. For data integrity this table references players table on player ids.
create table Matches (
match_id serial primary key,
winner_id INTEGER REFERENCES Players,
loser_id INTEGER REFERENCES Players);


