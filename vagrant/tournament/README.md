#Project2: Tournament Results Application
#####Deanna M. Wagner, October 22, 2015

In this project, Python and SQL are used to build a database-backed Python module to run a Swiss style game tournament. The database schema, the code to implement an API for the project and the extra credit to handle multiple tournaments are included.


##Required Libraries, Files and Dependencies

The Tournament Results Application requires:

*  Python
*  PostreSQL with psql
*  `tournament.sql`
*  `tournament.py`
*  `tournament_test.py`
*  `tournament_extra.sql`
*  `tournament_extra.py`
*  `tournament_test_extra.py`

A virtual machine is available that contains all needed applications, explained below.


##Installation

To run the application using the virtual machine (VM):

1.  Follow the installation instructions found here:
	https://www.udacity.com/wiki/ud197/install-vagrant  
    But, instead of forking Udacity's repository at the section:
    "Use Git/GitHub to fetch the VM configuration," fork, download zip or clone:
    [DeannaWagner's Repository](https://github.com/DeannaWagner/fullstack-nanodegree-vm)  	
2.  Navigate to the tournament directory from the VM, go to pqsl prompt and import `tournament.sql`
3.  Quit psql prompt and run `tournament_test.py` 
4.  Go to pqsl prompt and import `tournament_extra.sql`
5.  Quit psql prompt and run `tournament_test_extra.py` 
6.  View files by opening them in any editor


##Extra Credit Description

This project includes some features that exceed specifications:

*  View vstandings in `tournament.sql` is a complex query in the `tournament.py`
 file needed to return the `playerStandings()` tuples, which is then incorporated
 in the `swissPairings()`

* VIEW vcount in `tournament_extra.sql` was created to query `countPlayers(tournament_id)`.

* The extra credit program files handle multiple tournaments; all of those files contain the word 'extra' in their titles.  


##Miscellaneous

This program assumes an even number of players to be registered, as it does not handle byes.
The Swiss pairings are by registration order, in accordance with the requirements. Subsequent rounds use the adjacent, or 'King of the Hill' grouping rules, also specified.  An extra credit test module was created since many of the functions needed a `tournament_id` parameter to differentiate between tournaments.

Some credit is rightfully due and offered to the Udacity discussion forum and supporting course instructor, where some of the minor help that was offered by students, coaches and the instructor was used in the program.  All the code in this application was developed by the author, except for that which was already provided by Udacity.  The `tournament_test.py` remains unchanged, to the best of the author's knowledge.

