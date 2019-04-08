# Andrew Colabella, Sean Foley, Peyton Sayasith
# Database Design
# NBA Statistics Project

import flask
import mysql.connector
import Tkinter as tk
import ttk as ttk
from Tkinter import *
from PIL import Image, ImageTk
import tkFont

NBA_LOGO = "nbalogo.png"

def select(connection, statement):
    cur = connection.cursor()

    # Execute select
    cur.execute(statement)

    # Get output
    output = cur.fetchall()
    cur.close()

    return output

def callProc(connection, procName, argsArray):
    results = []
    cur = connection.cursor()

    # Run the procedure
    cur.callproc(procName, argsArray)

    # Get the data output
    for result in cur.stored_results():
        results.append(result.fetchall())

    cur.close()

    return list(results[0])

def runSearch(connection, table, option, content):
    # Clear the table
    table.delete(0, END)
    
    if option == "player":
        if content:
            players = callProc(connection, "track_player", [content])
        else:
            players = callProc(connection, "all_player", [])
            
        formatting = "{:<25}{:<10}{:<5}{:<6}{:<7}{:<5}{:<5}{:<5}{:<5}{:<5}{:<5}{:<5}{:<5}{:<6}"

        heading = formatting.format("Player Name", "Position", "Age", "Team", "Games", "FG%", "3P%", "FT%", "Rbs", "Ast", "Stl", "Blk", "TO", "Pts")


        table.insert(END, heading)
        table.insert(END, "_"*100)

        for player in players:
            tmp = formatting.format(player[0], player[1], player[2], player[3], player[4], player[5], player[6], player[7], player[8], player[9], player[10], player[11], player[12], player[13])
            table.insert(END, tmp)
        
                
    elif option == "teams":
        if content:
            teams = callProc(connection, "track_team", [content])
        else:
            teams = select(connection, "select * from teams")
        
        formatting = "{:<10}{:<30}{:<10}{:<10}"
        
        table.insert(END, formatting.format("Team Abr", "Team Name", "Division", "Conference"))

        table.insert(END, "_"*100)
        
        for team in teams:
            tmp = formatting.format(team[0], team[1], team[2], team[3])
            table.insert(END, tmp)

    elif option == "games":
        if content:
            games = callProc(connection, "team_games", [content])
        else:
            games = select(connection, "select * from games")

        formatting = "{:<5}{:<16}{:<25}{:<9}{:<25}{:<9}"
        
        table.insert(END, formatting.format("ID", "Date", "Home Team", "Home Pts", "Away Team", "Away Pts"))

        table.insert(END, "_"*100)
        
        for game in games:
            tmp = formatting.format(game[0], game[1], game[2], game[3], game[4], game[5])
            table.insert(END, tmp)
            
    else:
        if content:
            coaches = callProc(connection, "track_coach", [content])
        else:
            coaches = callProc(connection, "all_coach", [])
        
        formatting = "{:<30}{:<30}"

        table.insert(END, formatting.format("Coach Name", "Team Name"))
        table.insert(END, "_"*100)

        for coach in coaches:
            tmp = formatting.format(coach[0], coach[1])
            table.insert(END, tmp)

    return

def runAllStars(connection, table):
    # Clear the table
    table.delete(0, END)

    stars = callProc(connection, "get_allstars", [])

    formatting = "{:<30}{:<30}"

    table.insert(END, formatting.format("Player Name", "Team Name"))

    table.insert(END, "_"*100)

    for star in stars:
        tmp = formatting.format(star[0], star[1])
        table.insert(END, tmp)

def runAwards(connection, table):
    # Clear the table
    table.delete(0, END)

    stars = callProc(connection, "get_awards", [])

    formatting = "{:<30}{:<30}"

    table.insert(END, formatting.format("Award Name", "Player Name"))

    table.insert(END, "_"*100)

    for star in stars:
        tmp = formatting.format(star[0], star[1])
        table.insert(END, tmp)


def main(config):
   	# SQL Connection
    	cnx = mysql.connector.connect(**config)

    	#Main window
	root = Tk()
	root.title('NBA Statistics')
        w, h = root.winfo_screenwidth(), root.winfo_screenheight()
        root.geometry("%dx%d+0+0" % (w, h))

	#Frame
	topFrame = Frame(root)
	topFrame.pack(side=TOP, fill=X)
	middleFrame = Frame(root)
	middleFrame.pack()
	bottomFrame = Frame(root)
	bottomFrame.pack()

	#main menu
	load = Image.open(NBA_LOGO).resize((400, 200))
        render = ImageTk.PhotoImage(load)
        logo = Label(topFrame, image=render)
        logo.image = render
	logo.pack()

        # Search Box
        search_option = StringVar()
        mytable = ""
        
        search_box = Entry(middleFrame, width=50, font=("Courier", 12))
        search_button = Button(middleFrame, text="Search", command= lambda: runSearch(cnx, mytable, search_option.get(), search_box.get()))

        # Radio buttons        
        search_player = Radiobutton(middleFrame, text="Player", value="player", var=search_option)
        search_teams = Radiobutton(middleFrame, text="Teams", value="teams", var=search_option)
        search_coaches = Radiobutton(middleFrame, text="Coaches", value="coaches", var=search_option)
        search_games = Radiobutton(middleFrame, text="Games", value="games", var=search_option)
        search_player.config(font=("Courier", 12))
        search_teams.config(font=("Courier", 12))
        search_coaches.config(font=("Courier", 12))
        search_games.config(font=("Courier", 12))
        search_box.pack(side="left")
        search_button.pack(side="left")
        search_player.pack(side="right", fill=NONE)
        search_teams.pack(side="right", fill=NONE)
        search_coaches.pack(side="right", fill=NONE)
        search_games.pack(side="right", fill=NONE)

        # List
        scrollbar = Scrollbar(bottomFrame, orient=VERTICAL)
        mytable = Listbox(bottomFrame, yscrollcommand=scrollbar.set, width=100, height=20, font=("Courier", 12))
        allstar_button = Button(bottomFrame, text="All Stars", command= lambda: runAllStars(cnx, mytable))
        awards_button = Button(bottomFrame, text="Player Awards", command= lambda: runAwards(cnx, mytable))
        scrollbar.config(command=mytable.yview)
        scrollbar.pack(side=RIGHT, fill=BOTH)
        mytable.pack(side=TOP, fill=BOTH, expand=1)
        allstar_button.pack(side=LEFT)
        awards_button.pack(side=LEFT)

        

        
    	root.mainloop()

    	return


if __name__ == '__main__':
    config = {
        'host' : 'localhost',
        'port' : 3306,
        'database': 'nba',
        'user': 'root',
        'password': 'root',
        'charset': 'utf8',
        'use_unicode': True,
        'get_warnings': True,
    }
    main(config)
