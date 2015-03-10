=====================
Tournament Results
=====================
Tournament Results is a simple Python app that uses PostgreSQL database to store player and matches data. 
It also includes functionality to rank the players acording to their standings and pair them up in matches in a tournament.


Quick start
-----------

1. Database and table definitions are stored in the tournament.sql file.

2. The following Python functions are stored in tournament.py file:
	
	registerPlayer(name) - adds a player to the tournament by putting an entry in the database,

	countPlayers() - returns the number of currently registered players,

	deletePlayers() - clears out all the player records from the database,

	reportMatch(winner, loser) - stores the outcome of a single match between two players in the database,

	deleteMatches() - clears out all the match records from the database,

	playerStandings() - returns a list of (id, name, wins, matches) for each player, sorted by the number of wins each player has,

	swissPairings() - given the existing set of registered players and the matches they have played, generates and returns a list of pairings according to the Swiss system. Each pairing is a tuple (id1, name1, id2, name2), giving the ID and name of the paired players. 

3. In order to run the Tournament Results application follow the below steps:

	start vagrant vitrual machine by using 'vagrant up' command
	
	start vagrant shell using 'vagrant ssh' command
	
	connect to the PostgreSQL database using psql this will connect you to the default vagrant db

	import tournament.sql file using \i tournament.sql file - this will create your tournament database, connect to the tournament db and create required tables
	
	exit the database using \q command
	
	to connect back to the tournament db from command line use 'psql tournament' command

	
	from the ssh command line execute the test suite included in the tournament_test.py file - this can be accomplished by using 	'python tournament_test.py'command.

4. Expected output:

	1. Old matches can be deleted.
	2. Player records can be deleted.
	3. After deleting, countPlayers() returns zero.
	4. After registering a player, countPlayers() returns 1.
	5. Players can be registered and deleted.
	6. Newly registered players appear in the standings with no matches.
	7. After a match, players have updated standings.
	8. After one match, players with one win are paired.
	Success!  All tests pass!

	