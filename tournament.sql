-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

DROP DATABASE IF EXISTS tournament;

CREATE DATABASE tournament;

DROP VIEW IF EXISTS standings CASCADE;
DROP TABLE IF EXISTS matches CASCADE;
DROP TABLE IF EXISTS players CASCADE;


CREATE TABLE players ( playerid SERIAL PRIMARY KEY,
                        playername text );

CREATE TABLE matches ( matchid SERIAL PRIMARY KEY,
                        winnerid integer,
                        loserid integer,
                        FOREIGN KEY(winnerid) REFERENCES players(playerid),
                        FOREIGN KEY(loserid) REFERENCES players(playerid) );

CREATE VIEW standings AS SELECT p.playerid as playerid, p.playername,
                        (SELECT count(*) FROM matches WHERE matches.winnerid = p.playerid) as won,
                        (SELECT count(*) FROM matches WHERE p.playerid in (winnerid, loserid)) as played
                        FROM players p
                        GROUP BY p.playerid
                        ORDER BY won DESC;
