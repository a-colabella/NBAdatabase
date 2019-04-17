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

# A function to execute a select statement
# in the database
def select(connection, statement):
    cur = connection.cursor()

    # Execute select
    cur.execute(statement)

    # Get output
    output = cur.fetchall()
    cur.close()

    return output

# A function to execute a procedure
# in the database
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

# Executed when the user presses search
def runSearch(connection, table, option, content):
    # Clear the table
    table.delete(0, END)

    # PLAYER
    if option == "player":
        if content:
            players = callProc(connection, "track_player", [content])
        # if the search is left blank, return all players
        else:
            players = callProc(connection, "all_player", [])
            
        formatting = "{:<25}{:<10}{:<5}{:<6}{:<7}{:<5}{:<5}{:<5}{:<5}{:<5}{:<5}{:<5}{:<5}{:<6}"

        heading = formatting.format("Player Name", "Position", "Age", "Team", "Games", "FG%", "3P%", "FT%", "Rbs", "Ast", "Stl", "Blk", "TO", "Pts")


        table.insert(END, heading)
        table.insert(END, "_"*100)

        for player in players:
            tmp = formatting.format(player[0], player[1], player[2], player[3], player[4], player[5], player[6], player[7], player[8], player[9], player[10], player[11], player[12], player[13])
            table.insert(END, tmp)
        
    # TEAM    
    elif option == "teams":
        if content:
            teams = callProc(connection, "track_team", [content])
        # if search left blank, return all teams
        else:
            teams = select(connection, "select * from teams")
        
        formatting = "{:<10}{:<30}{:<10}{:<10}"
        
        table.insert(END, formatting.format("Team Abr", "Team Name", "Division", "Conference"))

        table.insert(END, "_"*100)
        
        for team in teams:
            tmp = formatting.format(team[0], team[1], team[2], team[3])
            table.insert(END, tmp)

    # GAME
    elif option == "games":
        if content:
            games = callProc(connection, "team_games", [content])
        # if search left blank, return all games
        else:
            games = select(connection, "select * from games")

        formatting = "{:<5}{:<16}{:<25}{:<9}{:<25}{:<9}"
        
        table.insert(END, formatting.format("ID", "Date", "Home Team", "Home Pts", "Away Team", "Away Pts"))

        table.insert(END, "_"*100)
        
        for game in games:
            tmp = formatting.format(game[0], game[1], game[2], game[3], game[4], game[5])
            table.insert(END, tmp)
            
    # COACH
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

# Executed when all stars button is pressed
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

# Executed when awards button is pressed
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

def runUpdate(connection, table, rt):
    update_window = tk.Toplevel(rt)
    update_window.title('Update Data')
    

def runAddGame(connection, table, rt):
    add_window = tk.Toplevel(rt)
    add_window.title('Add Game')

    date_label = Label(add_window, text="Date: ").grid(row=0, column=1)
    home_label = Label(add_window, text="Home Team: ").grid(row=1, column=1)
    home_text = Entry(add_window).grid(row=1, column=2)
    home_pts_label = Label(add_window, text="Home Points: ").grid(row=2, column=1)
    home_pts = Spinbox(add_window, from_=0, to=999).grid(row=2, column=2)
    away_label = Label(add_window, text="Away Team: ").grid(row=3, column=1)
    away_text = Entry(add_window).grid(row=3, column=2)
    away_pts_label = Label(add_window, text="Away Points: ").grid(row=4, column=1)
    away_pts = Spinbox(add_window, from_=0, to=999).grid(row=4, column=2)
    submit_button = Button(add_window, text="Submit").grid(row=5, column=2)
    
def runAddTeam(connection, table, rt):
    add_window = tk.Toplevel(rt)
    add_window.title('Add Team')

    abr_label = Label(add_window, text="Team Abbreviation: ").grid(row=0,column=1)
    abr_entry = Entry(add_window).grid(row=0,column=2)
    name_label = Label(add_window, text="Team Name: ").grid(row=1,column=1)
    name_entry = Entry(add_window).grid(row=1,column=2)
    div_label = Label(add_window, text="Team Division: ").grid(row=2,column=1)
    div_entry= Entry(add_window).grid(row=2,column=2)
    conf_label = Label(add_window, text="Team Conference: ").grid(row=3, column=1)
    conf_entry=Entry(add_window).grid(row=3,column=2)
    submit_button = Button(add_window, text="Submit").grid(row=4, column=2)
    

def runAddPlayer(connection, table, rt):
    add_window = tk.Toplevel(rt)
    add_window.title('Add Player')

    name_label = Label(add_window, text="Player Name: ").grid(row=0, column=1)
    name_entry = Entry(add_window).grid(row=0, column=2)
    pos_label = Label(add_window, text="Position: ").grid(row=1, column=1)
    pos_entry = Entry(add_window).grid(row=1,column=2)
    age_label = Label(add_window, text="Age: ").grid(row=2, column=1)
    age_entry = Spinbox(add_window,from_=1,to=100).grid(row=2,column=2)
    team_label = Label(add_window, text="Team Abbreviation: ").grid(row=3, column=1)
    team_entry = Entry(add_window).grid(row=3,column=2)
    game_label = Label(add_window, text="Games: ").grid(row=4, column=1)
    game_entry = Spinbox(add_window, from_=0, to=100).grid(row=4,column=2)
    fg_label = Label(add_window, text="FG%: ").grid(row=5, column=1)
    fg_entry = Spinbox(add_window, from_=0, to=100).grid(row=5,column=2)
    threeP_label = Label(add_window, text="3P%: ").grid(row=6, column=1)
    threeP_entry = Spinbox(add_window, from_=0, to=100).grid(row=6,column=2)
    ft_label = Label(add_window, text="FT%: ").grid(row=7, column=1)
    ft_entry = Spinbox(add_window, from_=0, to=100).grid(row=7,column=2)
    rbs_label = Label(add_window, text="Rbs: ").grid(row=8, column=1)
    rbs_entry = Spinbox(add_window, from_=0, to=100).grid(row=8,column=2)
    ast_label = Label(add_window, text="Ast: ").grid(row=9, column=1)
    ast_entry = Spinbox(add_window, from_=0, to=100).grid(row=9,column=2)
    stl_label = Label(add_window, text="Stl: ").grid(row=10, column=1)
    stl_entry = Spinbox(add_window, from_=0, to=100).grid(row=10,column=2)
    blk_label = Label(add_window, text="Blk: ").grid(row=11, column=1)
    blk_entry = Spinbox(add_window, from_=0, to=100).grid(row=11,column=2)
    TO_label = Label(add_window, text="TO: ").grid(row=12, column=1)
    TO_entry = Spinbox(add_window, from_=0, to=100).grid(row=12,column=2)
    Pts_label = Label(add_window, text="Pts: ").grid(row=13, column=1)
    Pts_entry = Spinbox(add_window, from_=0, to=100).grid(row=13,column=2)
    
    submit_button = Button(add_window, text="Submit").grid(row=14, column=2)

def runAddCoach(connection, table, rt):
    add_window = tk.Toplevel(rt)
    add_window.title('Add Coach')

    name_label = Label(add_window, text="Coach Name: ").grid(row=0, column=1)
    name_entry = Entry(add_window).grid(row=0, column=2)
    team_label = Label(add_window, text="Team Abbreviation: ").grid(row=1, column=1)
    team_entry = Entry(add_window).grid(row=1, column=2)
    submit_button = Button(add_window, text="Submit").grid(row=2, column=2)

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
        update_data_button = Button(bottomFrame, text="Update Data", command = lambda: runUpdate(cnx, mytable, root), bg="orange")
        add_game_button = Button(bottomFrame, text="Add Game", command = lambda:runAddGame(cnx, mytable, root), bg="green")
        add_coach_button = Button(bottomFrame, text="Add Coach", command = lambda:runAddCoach(cnx, mytable, root), bg="green")
        add_team_button = Button(bottomFrame, text="Add Team", command = lambda:runAddTeam(cnx, mytable, root), bg="green")
        add_player_button = Button(bottomFrame, text="Add Player", command = lambda:runAddPlayer(cnx, mytable, root), bg="green")
        scrollbar.config(command=mytable.yview)
        scrollbar.pack(side=RIGHT, fill=BOTH)
        mytable.pack(side=TOP, fill=BOTH, expand=1)
        allstar_button.pack(side=LEFT)
        awards_button.pack(side=LEFT)
        update_data_button.pack(side=LEFT)
        add_game_button.pack(side=LEFT)        
        add_coach_button.pack(side=LEFT)
        add_team_button.pack(side=LEFT)
        add_player_button.pack(side=LEFT)
        
    	root.mainloop()

    	return

# database config
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
