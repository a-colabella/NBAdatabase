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
        
        formatting = "{:<10}{:<30}{:<11}{:<10}"
        
        table.insert(END, formatting.format("Team Abr", "Team Name", "Conference", "Division"))

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

    

def runAddGame(connection, update, rt, entry):
    add_window = tk.Toplevel(rt)
    
    dayVar = StringVar()
    monthVar = StringVar()
    dateVar = StringVar()
    yearVar = StringVar()
    homeVar = StringVar()
    homePointsVar = StringVar()
    awayVar = StringVar()
    awayPointsVar = StringVar()
    
    dayVar.set("Mon")
    monthVar.set("Oct")
    yearVar.set("2017")

    date_label = Label(add_window, text="Date: ", font=("Courier", 12)).grid(row=0, column=1)
    day_entry = OptionMenu(add_window, dayVar, "Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun").grid(row=0,column=2)
    month_entry = OptionMenu(add_window, monthVar, "Oct", "Nov", "Dec", "Jan", "Feb", "Mar", "Apr", "May", "Jun").grid(row=0,column=3)
    date_entry = Spinbox(add_window, from_=1, to=31, textvariable=dateVar).grid(row=0, column=4)
    year_entry = OptionMenu(add_window, yearVar, "2017", "2018").grid(row=0,column=5)
    home_label = Label(add_window, text="Home Team: ", font=("Courier", 12)).grid(row=1, column=1)
    home_text = Entry(add_window, textvariable=homeVar, font=("Courier", 12)).grid(row=1, column=2)
    home_pts_label = Label(add_window, text="Home Points: ", font=("Courier", 12)).grid(row=2, column=1)
    home_pts = Spinbox(add_window, from_=0, to=999, textvariable=homePointsVar).grid(row=2, column=2)
    away_label = Label(add_window, text="Away Team: ", font=("Courier", 12)).grid(row=3, column=1)
    away_text = Entry(add_window, textvariable=awayVar, font=("Courier", 12)).grid(row=3, column=2)
    away_pts_label = Label(add_window, text="Away Points: ", font=("Courier", 12)).grid(row=4, column=1)
    away_pts = Spinbox(add_window, from_=0, to=999, textvariable=awayPointsVar).grid(row=4, column=2)
    submit_button = Button(add_window, text="Submit", font=("Courier", 12)).grid(row=6, column=2)

    if update:
        add_window.title('Update Game')
        id_label = Label(add_window, text="ID: ", font=("Courier", 12)).grid(row=5, column=1)
        id_val = Label(add_window, text=entry[0], font=("Courier", 12)).grid(row=5, column=2)
        dayVar.set(entry[1])
        monthVar.set(entry[2])
        dateVar.set(entry[3])
        yearVar.set(entry[4])
        homeVar.set(entry[5] + " " + entry[6])
        homePointsVar.set(entry[7])
        awayVar.set(entry[8] + " " + entry[9])
        awayPointsVar.set(entry[10])
    else:
        add_window.title('Add Game')
    
def runAddTeam(connection, update, rt, entry):
    add_window = tk.Toplevel(rt)
    add_window.title('Add Team')

    abrVar = StringVar()
    nameVar = StringVar()
    divVar = StringVar()
    confVar = StringVar()

    divVar.set("A")
    confVar.set("E")

    abr_label = Label(add_window, text="Team Abbreviation: ", font=("Courier", 12)).grid(row=0,column=1)
    abr_entry = Entry(add_window, textvariable=abrVar, font=("Courier", 12)).grid(row=0,column=2)
    name_label = Label(add_window, text="Team Name: ", font=("Courier", 12)).grid(row=1,column=1)
    name_entry = Entry(add_window, textvariable=nameVar, font=("Courier", 12)).grid(row=1,column=2)
    conf_label = Label(add_window, text="Team Conference: ", font=("Courier", 12)).grid(row=2, column=1)
    conf_entry=OptionMenu(add_window, confVar, "E", "W").grid(row=2,column=2)
    div_label = Label(add_window, text="Team Division: ", font=("Courier", 12)).grid(row=3, column=1)
    div_entry= OptionMenu(add_window, divVar, "A", "C", "P", "NW", "SW", "SE").grid(row=3,column=2)    
    submit_button = Button(add_window, text="Submit", font=("Courier", 12)).grid(row=5, column=2)

    if update:
        add_window.title('Update Team')
        id_label = Label(add_window, text="ID: ", font=("Courier", 12)).grid(row=4, column=1)
        id_val = Label(add_window, text="insert", font=("Courier", 12)).grid(row=4, column=2)
        abrVar.set(entry[0])
        nameVar.set(entry[1] + " " + entry[2])
        confVar.set(entry[3])
        divVar.set(entry[4])
    else:
        add_window.title('Add Team')
    

def runAddPlayer(connection, update, rt, entry):
    add_window = tk.Toplevel(rt)
    add_window.title('Add Player')

    nameVar = StringVar()
    posVar = StringVar()
    ageVar = StringVar()
    teamVar = StringVar()
    gameVar = StringVar()
    fgVar = StringVar()
    threePVar = StringVar()
    ftVar = StringVar()
    rbsVar = StringVar()
    astVar = StringVar()
    stlVar = StringVar()
    blkVar = StringVar()
    TOVar = StringVar()
    ptsVar = StringVar()

    name_label = Label(add_window, text="Player Name: ", font=("Courier", 12)).grid(row=0, column=1)
    name_entry = Entry(add_window, textvariable=nameVar, font=("Courier", 12)).grid(row=0, column=2)
    pos_label = Label(add_window, text="Position: ", font=("Courier", 12)).grid(row=1, column=1)
    pos_entry = Entry(add_window, textvariable=posVar, font=("Courier", 12)).grid(row=1,column=2)
    age_label = Label(add_window, text="Age: ", font=("Courier", 12)).grid(row=2, column=1)
    age_entry = Spinbox(add_window,from_=1,to=100, textvariable=ageVar).grid(row=2,column=2)
    team_label = Label(add_window, text="Team Abbreviation: ", font=("Courier", 12)).grid(row=3, column=1)
    team_entry = Entry(add_window, textvariable=teamVar, font=("Courier", 12)).grid(row=3,column=2)
    game_label = Label(add_window, text="Games: ", font=("Courier", 12)).grid(row=4, column=1)
    game_entry = Spinbox(add_window, from_=0, to=100, textvariable=gameVar).grid(row=4,column=2)
    fg_label = Label(add_window, text="FG%: ", font=("Courier", 12)).grid(row=5, column=1)
    fg_entry = Spinbox(add_window, from_=0, to=1, increment=.01, format="%.02f", textvariable=fgVar).grid(row=5,column=2)
    threeP_label = Label(add_window, text="3P%: ", font=("Courier", 12)).grid(row=6, column=1)
    threeP_entry = Spinbox(add_window, from_=0, to=1, increment=.01, format="%.02f", textvariable=threePVar).grid(row=6,column=2)
    ft_label = Label(add_window, text="FT%: ", font=("Courier", 12)).grid(row=7, column=1)
    ft_entry = Spinbox(add_window, from_=0, to=1, increment=.01, format="%.02f", textvariable=ftVar).grid(row=7,column=2)
    rbs_label = Label(add_window, text="Rbs: ", font=("Courier", 12)).grid(row=8, column=1)
    rbs_entry = Spinbox(add_window, from_=0, to=100, increment=.01, format="%.02f", textvariable=rbsVar).grid(row=8,column=2)
    ast_label = Label(add_window, text="Ast: ", font=("Courier", 12)).grid(row=9, column=1)
    ast_entry = Spinbox(add_window, from_=0, to=100, increment=.01, format="%.02f", textvariable=astVar).grid(row=9,column=2)
    stl_label = Label(add_window, text="Stl: ", font=("Courier", 12)).grid(row=10, column=1)
    stl_entry = Spinbox(add_window, from_=0, to=100, increment=.01, format="%.02f", textvariable=stlVar).grid(row=10,column=2)
    blk_label = Label(add_window, text="Blk: ", font=("Courier", 12)).grid(row=11, column=1)
    blk_entry = Spinbox(add_window, from_=0, to=100, increment=.01, format="%.02f", textvariable=blkVar).grid(row=11,column=2)
    TO_label = Label(add_window, text="TO: ", font=("Courier", 12)).grid(row=12, column=1)
    TO_entry = Spinbox(add_window, from_=0, to=100, increment=.01, format="%.02f", textvariable=TOVar).grid(row=12,column=2)
    Pts_label = Label(add_window, text="Pts: ", font=("Courier", 12)).grid(row=13, column=1)
    Pts_entry = Spinbox(add_window, from_=0, to=100, increment=.01, format="%.02f", textvariable=ptsVar).grid(row=13,column=2)
    
    submit_button = Button(add_window, text="Submit", font=("Courier", 12)).grid(row=15, column=2)

    if update:
        add_window.title('Update Player')
        id_label = Label(add_window, text="ID: ", font=("Courier", 12)).grid(row=14, column=1)
        id_val = Label(add_window, text="insert", font=("Courier", 12)).grid(row=14, column=2)
        nameVar.set(entry[0] + " " + entry[1])
        posVar.set(entry[2])
        ageVar.set(entry[3])
        teamVar.set(entry[4])
        gameVar.set(entry[5])
        fgVar.set(entry[6])
        threePVar.set(entry[7])
        ftVar.set(entry[8])
        rbsVar.set(entry[9])
        astVar.set(entry[10])
        stlVar.set(entry[11])
        blkVar.set(entry[12])
        TOVar.set(entry[13])
        ptsVar.set(entry[14])
    else:
        add_window.title('Add Player')

def runAddCoach(connection, update, rt, entry):
    add_window = tk.Toplevel(rt)

    nameVar = StringVar()
    teamVar = StringVar()
    
    name_label = Label(add_window, text="Coach Name: ", font=("Courier", 12)).grid(row=0, column=1)
    name_entry = Entry(add_window, textvariable=nameVar, font=("Courier", 12)).grid(row=0, column=2)
    team_label = Label(add_window, text="Team Abbreviation: ", font=("Courier", 12)).grid(row=1, column=1)
    team_entry = Entry(add_window, textvariable=teamVar, font=("Courier", 12)).grid(row=1, column=2)
    submit_button = Button(add_window, text="Submit", font=("Courier", 12)).grid(row=3, column=2)
    
    if update:
        add_window.title('Update Coach')
        id_label = Label(add_window, text="ID: ", font=("Courier", 12)).grid(row=2, column=1)
        id_val = Label(add_window, text="insert", font=("Courier", 12)).grid(row=2, column=2)
        nameVar.set(entry[0] + " " + entry[1])
        teamVar.set(entry[2])
    else:
        add_window.title('Add Coach')
    

def runUpdate(connection, entry, rt, datatype):
    entry = entry.split(" ")
    entry = filter(None, entry)

    if datatype == "games":
        runAddGame(connection, True, rt, entry)
    elif datatype == "player":
        runAddPlayer(connection, True, rt, entry)
    elif datatype == "teams":
        runAddTeam(connection, True, rt, entry)
    else:
        runAddCoach(connection, True, rt, entry)
                    
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
        search_button = Button(middleFrame, text="Search", font=("Courier", 12), command= lambda: runSearch(cnx, mytable, search_option.get(), search_box.get()))

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
        allstar_button = Button(bottomFrame, text="All Stars", font=("Courier", 12), command= lambda: runAllStars(cnx, mytable))
        awards_button = Button(bottomFrame, text="Player Awards", font=("Courier", 12), command= lambda: runAwards(cnx, mytable))
        update_data_button = Button(bottomFrame, text="Update Data", font=("Courier", 12), command = lambda: runUpdate(cnx, mytable.get(ACTIVE), root, search_option.get()), bg="orange")
        add_game_button = Button(bottomFrame, text="Add Game", font=("Courier", 12), command = lambda:runAddGame(cnx, False, root, None), bg="green")
        add_coach_button = Button(bottomFrame, text="Add Coach", font=("Courier", 12), command = lambda:runAddCoach(cnx, False, root, None), bg="green")
        add_team_button = Button(bottomFrame, text="Add Team", font=("Courier", 12), command = lambda:runAddTeam(cnx, False, root, None), bg="green")
        add_player_button = Button(bottomFrame, text="Add Player", font=("Courier", 12), command = lambda:runAddPlayer(cnx, False, root, None), bg="green")
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
