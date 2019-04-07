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

    return output

def main(config):
   	# SQL Connection
    	cnx = mysql.connector.connect(**config)

    	#Main window
	root = Tk()
	root.title('NBA Statistics')
	root.geometry("800x800")

	#Frame
	topFrame = Frame(root)
	topFrame.pack(side=TOP, fill=X)
	middleFrame = Frame(root)
	middleFrame.pack(fill=X)
	bottomFrame = Frame(root)
	bottomFrame.pack(side=BOTTOM)

	#main menu
	load = Image.open(NBA_LOGO).resize((300, 150))
        render = ImageTk.PhotoImage(load)
        logo = Label(topFrame, image=render)
        logo.image = render
	logo.pack()

        # Search
        search_box = Entry(middleFrame)
        search_player = Radiobutton(middleFrame, text="Player")
        search_games = Radiobutton(middleFrame, text="Games")
        search_teams = Radiobutton(middleFrame, text="Teams")
        search_coaches = Radiobutton(middleFrame, text="Coaches")
        search_player.config(font=("Arial", 12))
        search_games.config(font=("Arial", 12))
        search_teams.config(font=("Arial", 12))
        search_coaches.config(font=("Arial", 12))
        search_box.pack()
        search_player.pack(side="right", fill=NONE)
        search_games.pack(side="right", fill=NONE)
        search_teams.pack(side="right", fill=NONE)
        search_coaches.pack(side="right", fill=NONE)

        
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
