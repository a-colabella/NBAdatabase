# Andrew Colabella, Sean Foley, Peyton Sayasith
# Database Design
# NBA Statistics Project

import flask
import mysql.connector
import Tkinter as tk
from Tkinter import *

from PIL import Image, ImageTk

NBA_LOGO = "nbalogo.png"

def select(connection, statement):
    cur = connection.cursor()
    cur.execute(statement)
    output = cur.fetchall()
    cur.close()

    return output[0]

def callProc(connection, procName, argsArray):
    results = []
    # Get cursor
    cur = connection.cursor()

    # Run the stored procedure
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
        player = select(connection, "select * from lotr_character where character_name = '" + content + "'")
        table.insert(END, player)

        
    elif option == "teams":
        teams = callProc(connection, "track_character", [content])
        for team in teams:
            table.insert(END, team)

    return

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
        
        search_box = Entry(middleFrame, width=50, font=("Arial", 12))
        search_button = Button(middleFrame, text="Search", command= lambda: runSearch(cnx, mytable, search_option.get(), search_box.get()))

        # Radio buttons        
        search_player = Radiobutton(middleFrame, text="Player", value="player", var=search_option)
        search_teams = Radiobutton(middleFrame, text="Teams", value="teams", var=search_option)
        search_coaches = Radiobutton(middleFrame, text="Coaches", value="coaches", var=search_option)
        search_player.config(font=("Arial", 12))
        search_teams.config(font=("Arial", 12))
        search_coaches.config(font=("Arial", 12))
        search_box.pack(side="left")
        search_button.pack(side="left")
        search_player.pack(side="right", fill=NONE)
        search_teams.pack(side="right", fill=NONE)
        search_coaches.pack(side="right", fill=NONE)

        # List
        scrollbar = Scrollbar(bottomFrame, orient=VERTICAL)
        mytable = Listbox(bottomFrame, yscrollcommand=scrollbar.set, width=100, height=20, font=("Arial", 12))
        scrollbar.config(command=mytable.yview)
        scrollbar.pack(side=RIGHT, fill=Y)
        mytable.pack(side=TOP, fill=BOTH, expand=1)
        

        
    	root.mainloop()

    	return


if __name__ == '__main__':
    config = {
        'host' : 'localhost',
        'port' : 3306,
        'database': 'lotrfinal',
        'user': 'root',
        'password': 'root',
        'charset': 'utf8',
        'use_unicode': True,
        'get_warnings': True,
    }
    main(config)
