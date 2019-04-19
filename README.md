NBA Database
=============

## Group Name: ColabellaFoleySayasith

## Group Members:
Andrew Colabella
Sean Foley
Peyton Sayasith

## Project Description:
Basketball is one of the America's most beloved and followed sports and is gaining increasing popularity the world over. As with any sport, teams of people are employed to record and analyze a plethora of statistics. Within the NBA, there is the opportunity to explore players, teams, and games.  We’re big NBA fans and are hoping to be able to create a resource that we will be able to use beyond this class.
We have provided a SQL database providing users the ability to store and update information about the NBA.  We will use Python’s Tkinter library to develop this application.

## How To Use:
For this program to run properly, the user must load the
Sql File: _FinalProject4181.sql_ into the MySQL workbench and
run the dump on their localhost server, thus creating the database.

Our program runs on Python 2

These are the following Python libraries our program uses:
* Tkinter
* Pillow
* mysql-connector
* tkFont
* getpass (should be built into Python)

To run the program, enter into the command line:
"python NBA.py"

A prompt will come up in the command line asking the user for their MySQL username and password.
When the credentials entered are correct, a GUI will open.

You will notice a search bar, search options, an empty table, and procedure buttons below.

1. Searching:
To search for any data, a search option must be selected (games, coaches, teams, players).
Leaving the searchbar blank and pressing search will return an entire table.
Searching for a specific team name under "games" will return all the games a specific team played in the season.
Searching for a specific coach, team, or player will return the stats for that row of the table.

2. Adding:
A game, a coach, and a player can be adding by clicking the corresponding green button below.
This will open a new window allowing the user to enter info to create the row.

Note:
A new player has no stats. These must be updated using the update feature.
A new game has no score because future games can be added before they occur. These must also be updated.

Once data is added, click the search button again to refresh the table.

3. Updating:
To update a game or player, select the player or game you want to update by clicking on it in the table (after you have searched for it).

For example: Select the "games" search option, click search which returns the entire list of games, and select the game you want to update.

Then click the yellow "Update Data" button.

Once data is updated, click the search button again to refresh the table.

4. Deleting:
To delete a game, player, or coach, select the game, player, or coach you want to delete by clicking on it in the table (after you have searched for it).

Then click the red "Delete Data" button.

Once data is deleted, click the search button again to refresh the table.


ENJOY!