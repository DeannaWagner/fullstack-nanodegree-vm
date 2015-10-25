Project2: Tournament Results Application - Deanna M. Wagner, October 22, 2015
================================

In this project, Python and SQL knowledge is used to build a database-backed Python module to run a game tournament. The database schema and code to implement an API for the project were completed.

Required Libraries, Files and Dependencies
-----------------------------------
The Tournament Results Application requires:

1.  Python
2.  PostreSQL with psql
3.  tournament.sql
4.  tournament.py
5.  tournament_test.py
6.  tournament_extra.sql
7.  tournament_extra.py
8.  tournament_test_extra.py

A virtual machine is available and contains all needed applications, explained below.


How to Run Project
------------------
To run the application using the virtual machine (VM):

1.  Follow the installation instructions found here:
	https://www.udacity.com/wiki/ud197/install-vagrant
    
2.  Instead of forking Udacity's repository at the section:
    "Use Git/GitHub to fetch the VM configuration," fork, download zip or clone:
    https://github.com/DeannaWagner/fullstack-nanodegree-vm  	
2.  Navigate to the tournament directory from the VM, go to pqsl prompt and run tournament.sql.
3.  Quit psql prompt and Run tournament_test.py 
4.  Run tournament_test_extra.py 
5.  View files by opening them in any editor


Extra Credit Description
------------------------
This project includes some features that exceed specifications.

1. VIEW vstandings was created to remove the complex query with two subqueries from the playerStandings() and place it in the sql file.

2. The extra credit program files handle multiple tournaments.  (In future releases: This application prevents the rematch of players in a given tournament, for all the rounds that might be played, in accordance with the number of registered players (log 2 n), player rematches are prevented to the extent possible.  View vno_rematches was created.)


Miscellaneous
-------------
This program assumes an even number of players to be registered, as it does not handle byes.
The Swiss pairings are random the first round by shuffling, in accordance with the requirements and for subsequent rounds using the adjacent grouping rules, except in some cases of rematch possibilities.

Some credit is rightfully due and offered to the Udacity discussion forum, where some of the minor help that was offered by students and coaches was used in the program. Specifically the idea of a match_id, and a rethinking of the logic to pair players according to Swiss rules without rematches - thanks to Coach Amanda - was very helpful.  Intro to Relational Databases was highly valuable, especially the effort of making tests see if the program prevented rematches for Swiss tournament, by offering mathematical foundations of a Swiss system. The course notes and links were very helpful.
     


