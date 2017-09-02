#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2, bleach


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the match records from the database."""
    db = connect()
    cur = db.cursor()
    cur.execute("DELETE FROM matches")
    db.commit()
    db.close()

def deletePlayers():
    """Remove all the player records from the database."""
    db = connect()
    cur = db.cursor()
    cur.execute("DELETE FROM players")
    db.commit()
    db.close()


def countPlayers():
    """Returns the number of players currently registered."""
    db = connect()
    cur = db.cursor()
    cur.execute("SELECT count(playerid) FROM players")
    pcount = cur.fetchall()
    db.close()
    return pcount[0][0]


def registerPlayer(name):
    """Adds a player to the tournament database.

    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)

    Args:
      name: the player's full name (need not be unique).
    """
    db = connect()
    cur = db.cursor()
    cur.execute("INSERT INTO players(playername) VALUES (%s)", (bleach.clean(name),))
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
    cur = db.cursor()
    cur.execute("SELECT * FROM standings")
    results = cur.fetchall()

    #create list of player standings
    if (results[0][2] != 0) and (results[0][2] == results[1][2]):
        cur.execute("SELECT playerid, playername, won, played " \
                "FROM standings ORDER BY (cast(won AS DECIMAL)/played) DESC;")
        results = cur.fetchall()

    db.close()
    return results


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    db = connect()
    cur = db.cursor()

    #bleach input data
    winner = bleach.clean(winner, strip=True)
    loser = bleach.clean(loser, strip=True)

    cur.execute("INSERT INTO matches(winnerid, loserid) VALUES (%s, %s)", (winner,loser,))
    db.commit()
    db.close()


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
    db = connect()
    cur = db.cursor()
    cur.execute("SELECT * FROM standings")
    results = cur.fetchall()

    #create pairings
    pairings = []
    c = 0
    while c < len(results):
        if (results[c][2] == results[c+1][2]):
            pairings.append((results[c][0],results[c][1],results[c+1][0],results[c+1][1]))
            c += 2

    db.commit()
    db.close()
    return pairings
