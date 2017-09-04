#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2
import bleach


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    try:
        db = psycopg2.connect("dbname=tournament")
        cursor = db.cursor()
        return db, cursor
    except:
        print "error with connect function"


def deleteMatches():
    """Remove all the match records from the database."""
    db, cur = connect()
    q = "TRUNCATE matches CASCADE"
    cur.execute(q)
    db.commit()
    db.close()


def deletePlayers():
    """Remove all the player records from the database."""
    db, cur = connect()
    q = "TRUNCATE players CASCADE"
    cur.execute(q)
    db.commit()
    db.close()


def countPlayers():
    """Returns the number of players currently registered."""
    db, cur = connect()
    q = "SELECT count(playerid) FROM players"
    cur.execute(q)
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
    db, cur = connect()
    q = "INSERT INTO players(playername) VALUES (%s)"
    params = (bleach.clean(name),)
    cur.execute(q, params)
    db.commit()
    db.close()


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place,
    or a player tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    db, cur = connect()
    q1 = "SELECT * FROM standings;"
    cur.execute(q1)
    results = cur.fetchall()

    # create list of player standings
    if (results[0][2] != 0) and (results[0][2] == results[1][2]):
        q2 = """SELECT playerid, playername, won, played
            FROM standings ORDER BY
            (cast(won AS DECIMAL)/played) DESC"""
        cur.execute(q2)
        results = cur.fetchall()

    db.close()
    return results


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    db, cur = connect()
    q = "INSERT INTO matches(winnerid, loserid) VALUES (%s, %s)"
    params = (winner, loser, )

    # bleach input data
    winner = bleach.clean(winner, strip=True)
    loser = bleach.clean(loser, strip=True)

    cur.execute(q, params)
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
    db, cur = connect()
    q = "SELECT * FROM standings"
    cur.execute(q)
    results = cur.fetchall()

    # create pairings
    pairings = []
    while len(results) > 0:
        r1 = results.pop(0)
        c = 0
        f = True
        while c < len(results) and f:
            if (r1[2] == results[c][2]):
                r2 = results.pop(c)
                pairings.append((r1[0], r1[1], r2[0], r2[1]))
                c += 1
                f = False

    db.commit()
    db.close()
    return pairings
