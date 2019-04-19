# Andrew Colabella, Sean Foley, Peyton Sayasith
# Database Design
# NBA Statistics Project

import mysql.connector
from mysql.connector import Error
from mysql.connector import errorcode
import getpass
import PIL.Image
import PIL.ImageTk
import Tkinter as tk
from Tkinter import *
import tkFont

NBA_LOGO = "nbalogo.png"

# A function to execute a select statement
# in the database
def select(connection, statement):
    #cnx = mysql.connector.connect(**connection)

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
    #cnx = mysql.connector.connect(**connection)
    cur = connection.cursor()

    # Run the procedure
    cur.callproc(procName, argsArray)
    connection.commit()

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
            
        formatting = "{:<25}{:<4}{:<4}{:<5}{:<6}{:<6}{:<6}{:<6}{:<6}{:<6}{:<6}{:<6}{:<6}{:<6}"

        heading = formatting.format("Player Name", "Pos", "Age", "Team", "Games", "FG%", "3P%", "FT%", "Rbs", "Ast", "Stl", "Blk", "TO", "Pts")


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
        
        table.insert(END, formatting.format("ID", "Date", "Away Team", "Away Pts", "Home Team", "Home Pts"))

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

    
# Add or update a game
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

    
    
    submit_button = Button(add_window, text="Submit", font=("Courier", 12))
    submit_button.grid(row=6, column=2)

    if update:
        add_window.title('Update Game')
        home_pts_label = Label(add_window, text="Home Points: ", font=("Courier", 12)).grid(row=2, column=1)
        home_pts = Spinbox(add_window, from_=0, to=999, textvariable=homePointsVar).grid(row=2, column=2)
        away_pts_label = Label(add_window, text="Away Points: ", font=("Courier", 12)).grid(row=4, column=1)
        away_pts = Spinbox(add_window, from_=0, to=999, textvariable=awayPointsVar).grid(row=4, column=2)
        id_label = Label(add_window, text="ID: ", font=("Courier", 12)).grid(row=5, column=1)
        id_val = Label(add_window, text=entry[0], font=("Courier", 12)).grid(row=5, column=2)

        if (entry[-4].isdigit()):
            homePointsVar.set(entry[-4])
        else:
            homePointsVar.set(entry[-5])
            
        awayPointsVar.set(entry[-1])

        submit_button.configure(command=lambda: [add_window.destroy(), callProc(connection, 'update_game', [int(entry[0]), int(homePointsVar.get()), int(awayPointsVar.get())])])
        
    else:
        add_window.title('Add Game')
        date_label = Label(add_window, text="Date: ", font=("Courier", 12)).grid(row=0, column=1)
        day_entry = OptionMenu(add_window, dayVar, "Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun").grid(row=0,column=2)
        month_entry = OptionMenu(add_window, monthVar, "Oct", "Nov", "Dec", "Jan", "Feb", "Mar", "Apr", "May", "Jun").grid(row=0,column=3)
        date_entry = Spinbox(add_window, from_=1, to=31, textvariable=dateVar).grid(row=0, column=4)
        year_entry = OptionMenu(add_window, yearVar, "2017", "2018").grid(row=0,column=5)
        home_label = Label(add_window, text="Home Team: ", font=("Courier", 12)).grid(row=1, column=1)
        home_text = Entry(add_window, textvariable=homeVar, font=("Courier", 12)).grid(row=1, column=2)
        away_label = Label(add_window, text="Away Team: ", font=("Courier", 12)).grid(row=3, column=1)
        away_text = Entry(add_window, textvariable=awayVar, font=("Courier", 12)).grid(row=3, column=2)

        dateString = " ".join([dayVar.get(), monthVar.get(), dateVar.get(), yearVar.get()])
        submit_button.configure(command=lambda: [add_window.destroy(), callProc(connection, 'insert_game', [dateString, awayVar.get(), homeVar.get()])])
    
# Add or update a player
def runAddPlayer(connection, update, rt, entry):
    add_window = tk.Toplevel(rt)
    add_window.title('Add Player')

    nameVar = StringVar()
    posVar = StringVar()
    ageVar = StringVar()
    teamVar = StringVar()
    gameVar = StringVar()
    fgVar = StringVar()
    fgAVar = StringVar()
    threePVar = StringVar()
    threePAVar = StringVar()
    ftVar = StringVar()
    ftAVar = StringVar()
    orbsVar = StringVar()
    drbsVar = StringVar()
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
    
    
    submit_button = Button(add_window, text="Submit", font=("Courier", 12))
    submit_button.grid(row=18, column=2)

    if update:
        add_window.title('Update Player')

        
        game_label = Label(add_window, text="Games: ", font=("Courier", 12)).grid(row=4, column=1)
        game_entry = Spinbox(add_window, from_=0, to=100, textvariable=gameVar).grid(row=4,column=2)
        fg_label = Label(add_window, text="FG: ", font=("Courier", 12)).grid(row=5, column=1)
        fg_entry = Spinbox(add_window, from_=0, to=10000, textvariable=fgVar).grid(row=5,column=2)
        fgA_label = Label(add_window, text="FGA: ", font=("Courier", 12)).grid(row=6, column=1)
        fgA_entry = Spinbox(add_window, from_=0, to=10000, textvariable=fgAVar).grid(row=6,column=2)
        threeP_label = Label(add_window, text="3P: ", font=("Courier", 12)).grid(row=7, column=1)
        threeP_entry = Spinbox(add_window, from_=0, to=10000, textvariable=threePVar).grid(row=7,column=2)
        threePA_label = Label(add_window, text="3PA: ", font=("Courier", 12)).grid(row=8, column=1)
        threePA_entry = Spinbox(add_window, from_=0, to=10000, textvariable=threePAVar).grid(row=8,column=2)
        ft_label = Label(add_window, text="FT: ", font=("Courier", 12)).grid(row=9, column=1)
        ft_entry = Spinbox(add_window, from_=0, to=10000, textvariable=ftVar).grid(row=9,column=2)
        ftA_label = Label(add_window, text="FTA: ", font=("Courier", 12)).grid(row=10, column=1)
        ftA_entry = Spinbox(add_window, from_=0, to=10000, textvariable=ftAVar).grid(row=10,column=2)
        orbs_label = Label(add_window, text="ORbs: ", font=("Courier", 12)).grid(row=11, column=1)
        orbs_entry = Spinbox(add_window, from_=0, to=10000, textvariable=orbsVar).grid(row=11,column=2)
        drbs_label = Label(add_window, text="DRbs: ", font=("Courier", 12)).grid(row=12, column=1)
        drbs_entry = Spinbox(add_window, from_=0, to=10000, textvariable=drbsVar).grid(row=12,column=2)
        ast_label = Label(add_window, text="Ast: ", font=("Courier", 12)).grid(row=13, column=1)
        ast_entry = Spinbox(add_window, from_=0, to=10000, textvariable=astVar).grid(row=13,column=2)
        stl_label = Label(add_window, text="Stl: ", font=("Courier", 12)).grid(row=14, column=1)
        stl_entry = Spinbox(add_window, from_=0, to=10000, textvariable=stlVar).grid(row=14,column=2)
        blk_label = Label(add_window, text="Blk: ", font=("Courier", 12)).grid(row=15, column=1)
        blk_entry = Spinbox(add_window, from_=0, to=10000, textvariable=blkVar).grid(row=15,column=2)
        TO_label = Label(add_window, text="TO: ", font=("Courier", 12)).grid(row=16, column=1)
        TO_entry = Spinbox(add_window, from_=0, to=10000, textvariable=TOVar).grid(row=16,column=2)
        Pts_label = Label(add_window, text="Pts: ", font=("Courier", 12)).grid(row=17, column=1)
        Pts_entry = Spinbox(add_window, from_=0, to=10000, textvariable=ptsVar).grid(row=17,column=2)

        getName = " ".join(entry[:-13])
        getTeam = entry[-11]
	
	playerInfo = callProc(connection, 'player_update_info', [getName, getTeam])[0]        
	
        
        nameVar.set(playerInfo[0])
        posVar.set(playerInfo[1])
        ageVar.set(playerInfo[2])
        teamVar.set(playerInfo[3])
        gameVar.set(playerInfo[4])
        fgVar.set(playerInfo[5])
        fgAVar.set(playerInfo[6])
        threePVar.set(playerInfo[7])
        threePAVar.set(playerInfo[8])
        ftVar.set(playerInfo[9])
        ftAVar.set(playerInfo[10])
        orbsVar.set(playerInfo[11])
        drbsVar.set(playerInfo[12])
        astVar.set(playerInfo[13])
        stlVar.set(playerInfo[14])
        blkVar.set(playerInfo[15])
        TOVar.set(playerInfo[16])
        ptsVar.set(playerInfo[17])

        submit_button.configure(command=lambda: [add_window.destroy(), callProc(connection, 'update_player', [int(playerInfo[18]), nameVar.get(), posVar.get(), int(ageVar.get()), int(gameVar.get()), int(fgVar.get()), int(fgAVar.get()), int(threePVar.get()), int(threePAVar.get()), int(ftVar.get()), int(ftAVar.get()), int(orbsVar.get()), int(drbsVar.get()), int(astVar.get()), int(stlVar.get()), int(blkVar.get()), int(TOVar.get()), int(ptsVar.get())])])

    else:
        add_window.title('Add Player')
        submit_button.configure(command=lambda: [add_window.destroy(), callProc(connection, 'insert_player', [nameVar.get(), posVar.get(), int(ageVar.get()), teamVar.get()])])
        
        team_label = Label(add_window, text="Team Abbreviation: ", font=("Courier", 12)).grid(row=3, column=1)
        team_entry = Entry(add_window, textvariable=teamVar, font=("Courier", 12)).grid(row=3,column=2)

# Add a coach
def runAddCoach(connection, rt, entry):
    add_window = tk.Toplevel(rt)
    add_window.title('Add Coach')
    
    nameVar = StringVar()
    teamVar = StringVar()
    
    name_label = Label(add_window, text="Coach Name: ", font=("Courier", 12)).grid(row=0, column=1)
    name_entry = Entry(add_window, textvariable=nameVar, font=("Courier", 12)).grid(row=0, column=2)
    team_label = Label(add_window, text="Team Abbreviation: ", font=("Courier", 12)).grid(row=1, column=1)
    team_entry = Entry(add_window, textvariable=teamVar, font=("Courier", 12)).grid(row=1, column=2)
    submit_button = Button(add_window, text="Submit", font=("Courier", 12))
    submit_button.grid(row=3, column=2)

    submit_button.config(command=lambda: [add_window.destroy(), callProc(connection, 'insert_coach', [nameVar.get(), teamVar.get()])])

# General update function that will call specific
# update functions
def runUpdate(connection, entry, rt, datatype):
    entry = entry.split(" ")
    fixed_entry = filter(None, entry)

    if datatype == "games":
        runAddGame(connection, True, rt, fixed_entry)
    elif datatype == "player":
        runAddPlayer(connection, True, rt, fixed_entry)

# General delete function that will delete
# data from database
def runDelete(connection, entry, rt, datatype):
    entry = entry.split(" ")
    fixed_entry = filter(None, entry)

    if datatype == "games":
        callProc(connection, 'delete_game', [fixed_entry[0]])
    elif datatype == "player":
        getName = " ".join(fixed_entry[:-13])
        getTeam = fixed_entry[-11]
        print(getName)
        print(getTeam)
        callProc(connection, 'delete_player', [getName, getTeam])
    elif datatype == "coaches":
        getName = " ".join(fixed_entry[:-1])
        getTeam = fixed_entry[-1]
        print(getName)
        print(getTeam)
        callProc(connection, 'delete_coach', [getName, getTeam])

# MAIN
def main(connection):
    # Connection
    cnx = connection

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
    load = PIL.Image.open(NBA_LOGO).resize((400, 200))
    render = PIL.ImageTk.PhotoImage(load)
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
    
    # Radio button configurations and packing
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
    add_coach_button = Button(bottomFrame, text="Add Coach", font=("Courier", 12), command = lambda:runAddCoach(cnx, root, None), bg="green")
    add_player_button = Button(bottomFrame, text="Add Player", font=("Courier", 12), command = lambda:runAddPlayer(cnx, False, root, None), bg="green")
    delete_button = Button(bottomFrame, text="Delete Data", font=("Courier", 12), command = lambda:runDelete(cnx, mytable.get(ACTIVE), root, search_option.get()), bg="tomato")
    
    # Configurations and packing
    scrollbar.config(command=mytable.yview)
    scrollbar.pack(side=RIGHT, fill=BOTH)
    mytable.pack(side=TOP, fill=BOTH, expand=1)
    allstar_button.pack(side=LEFT)
    awards_button.pack(side=LEFT)
    update_data_button.pack(side=LEFT)
    add_game_button.pack(side=LEFT)
    add_coach_button.pack(side=LEFT)
    add_player_button.pack(side=LEFT)
    delete_button.pack(side=LEFT)
    
    root.mainloop()
    
    
    return

# database config
if __name__ == '__main__':
    # Before main runs, we must prompt the user for username and password
    config = {
        'host' : 'localhost',
        'port' : 3306,
        'database': 'nba',
        'user': '',
        'password': '',
        'charset': 'utf8',
        'use_unicode': True,
        'get_warnings': True,
    }

    # SQL Connection
    connected = False
    while (not connected):
        myuser = raw_input("Please enter your MYSQL username: ")
        mypass = getpass.getpass("Please enter your MYSQL password: ")
        config['user'] = myuser
        config['password'] = mypass
        
        try:
            cnx = mysql.connector.connect(**config)
            connected = True
        except mysql.connector.Error as err:
            connected = False
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Invalid username or password.")
                
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("The database does not exist!")
            else:
                print(err)

    # Run GUI
    main(cnx)
