#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

from contextlib import contextmanager

import psycopg2


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    try:
        # return psycopg2.connect("dbname=tournament")
        return psycopg2.connect(database='tournament', user='postgres', password='cosplay222', host='127.0.0.1',
                                port='5432')
    except:
        print("Connection failed")


@contextmanager
def get_cursor():
    """
    Query helper function using context lib. Creates a cursor from a database
    connection object, and performs queries using that cursor.
    """
    DB = connect()
    cursor = DB.cursor()
    try:
        yield cursor
    except:
        raise
    else:
        DB.commit()
    finally:
        cursor.close()
        DB.close()

def deleteMatches():
    """Remove all the match records from the database."""
    with get_cursor() as cursor:
        cursor.execute("DELETE FROM matches")


def deletePlayers():
    """Remove all the player records from the database."""
    with get_cursor() as cursor:
        cursor.execute("DELETE FROM players")


def countPlayers():
    """Returns the number of players currently registered."""
    with get_cursor() as cursor:
        cursor.execute("SELECT COUNT(id) FROM players;")
        rows = cursor.fetchone()
    return rows[0]


def registerPlayer(name):
    """Adds a player to the tournament database.

    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)

    Args:
      name: the player's full name (need not be unique).
    """
    with get_cursor() as cursor:
        cursor.execute("INSERT INTO players (name) VALUES (%s)", (name,))


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
    with get_cursor() as cursor:
        cursor.execute("SELECT id,name,wins,matches FROM standings ORDER BY wins DESC;")
        rows = cursor.fetchall()
    return rows


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.
    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    with get_cursor() as cursor:
        cursor.execute("INSERT INTO matches (winner,loser) VALUES (%s,%s)", (winner, loser))


"""
>>> CODE HONOR <<<
The swissPairings method implementation was inspired by the project https://github.com/danielburkard/udacity_fullstack_project2
"""


def swissPairings():
    """
    Returns:

    """
    """
    Returns:

    """
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
    with get_cursor() as cursor:
        cursor.execute("SELECT id,name,wins FROM standings ORDER BY wins DESC;")
        rows = cursor.fetchall()

    pairings = []
    for i in range(0, len(rows), 2):
        # get the player a
        player_a_id = rows[i][0]
        player_a_name = rows[i][1]

        # get the player b
        player_b_id = rows[i + 1][0]
        player_b_name = rows[i + 1][1]

        # append the a and b players to the pairings list
        pairings.append((player_a_id, player_a_name, player_b_id, player_b_name))

    return pairings
