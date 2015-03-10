#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2
import bleach

def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the match records from the database."""
    DB = connect()
    cur = DB.cursor()

# Delete matches data

    cur.execute("Delete from Matches")
    DB.commit()
    DB.close()

def deletePlayers():
    """Remove all the player records from the database."""
    DB = connect()
    cur = DB.cursor()

# Delete player data

    cur.execute("Delete from Players")
    DB.commit()
    DB.close()

def countPlayers():
    """Returns the number of players currently registered."""
    DB = connect()
    cur = DB.cursor()

 # Count Players records

    sql = 'SELECT COUNT(player_id) FROM Players;'
    cur.execute(sql)
    results = cur.fetchone()
    DB.close()
#Return results storing Count of Players
    return results[0]


def registerPlayer(name):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """
# Call cleanContent method to ensure input is permittable  

    cleanedName = cleanContent(name)
    DB = connect()
    cur = DB.cursor()

# Insert player data

    cur.execute("insert into Players (player_name) values (%s)",(cleanedName,))
    DB.commit()
    DB.close()



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
    DB = connect()
    cur = DB.cursor()
# Gather standings records
    cur.execute("""SELECT p.player_id as id , p.player_name as name ,sum(case when m.winner_id = p.player_id then 1 else 0 end) as wins, count(m.match_id) as matches 
        FROM players p left join matches m ON p.player_id in (m.winner_id, m.loser_id) 
        GROUP BY p.player_id ORDER BY matches DESC""")
    standings = cur.fetchall()      

    DB.close()
# Return standings records
    return standings

def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
 # Call cleanContent method to ensure input is permittable     
    cleanedWinner = cleanContent(winner)
    cleanedLoser = cleanContent(loser)
    
    DB = connect()
    cur = DB.cursor()

# Insert player data
    sql = "insert into Matches (winner_id,loser_id) values (%s,%s)"
    args= cleanedWinner, cleanedLoser
    cur.execute(sql, args)

    DB.commit()
    DB.close()
 
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
    # Gather pairings records

    DB = connect()
    cur = DB.cursor()
    cur.execute("""SELECT r.id as id1 , r.name as name1 ,s.id as id2 , s.name as name2 
        FROM 
        (SELECT distinct p.player_id as id , p.player_name as name ,sum(case when m.winner_id = p.player_id then 1 else 0 end) as wins, count(m.match_id) as matches 
            FROM players p left join matches m ON p.player_id in (m.winner_id, m.loser_id)  
            group by p.player_id having sum(case when m.winner_id = p.player_id then 1 else 0 end) = 0 ORDER BY wins DESC) r, 
        (SELECT distinct p.player_id as id , p.player_name as name ,sum(case when m.winner_id = p.player_id then 1 else 0 end) as wins, count(m.match_id) as matches 
            FROM players p left join matches m ON p.player_id in (m.winner_id, m.loser_id)  
            group by p.player_id having sum(case when m.winner_id = p.player_id then 1 else 0 end) = 0 ORDER BY wins DESC) s 
            where s.wins = r.wins and r.id<s.id 
         union 
            SELECT r.id as id1 , r.name as name1 ,s.id as id2 , s.name as name2 
         FROM 
         (SELECT distinct p.player_id as id , p.player_name as name ,sum(case when m.winner_id = p.player_id then 1 else 0 end) as wins, count(m.match_id) as matches 
            FROM players p left join matches m ON p.player_id in (m.winner_id, m.loser_id) 
            group by p.player_id having sum(case when m.winner_id = p.player_id then 1 else 0 end) = 1 ORDER BY wins DESC) r, 
         (SELECT distinct p.player_id as id , p.player_name as name ,sum(case when m.winner_id = p.player_id then 1 else 0 end) as wins, count(m.match_id) as matches 
            FROM players p left join matches m ON p.player_id in (m.winner_id, m.loser_id) 
            group by p.player_id  having sum(case when m.winner_id = p.player_id then 1 else 0 end) = 1 ORDER BY wins DESC) s where s.wins = r.wins and r.id<s.id;""")

    pairings = cur.fetchall()      
    DB.close()
 # Return pairings records
    return pairings

def cleanContent(content):
    # Step 1 define lists
    tag_black_list = ['iframe', 'script', 'spam', 'tt.form.submit']
    tag_white_list = ['p','div']
    attr_white_list = {'*': ['title']}


    # Step two, with Bleach: Remove tags and attributes not in whitelists, leave tag contents.
    content = bleach.clean(content, strip="TRUE", attributes=attr_white_list, tags=tag_white_list)
    return content

