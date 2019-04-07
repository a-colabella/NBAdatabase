# Andrew Colabella, Sean Foley, Peyton Sayasith
# Database Design
# NBA Statistics Project

import flask
import mysql.connector
import Tkinter as tk
from Tkinter import *

BACKGROUND_IMAGE = "basketball_clipart.jpg"
WIDTH = 800
HEIGHT = 800

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
	w, h = WIDTH, HEIGHT
	root.geometry("%dx%d+0+0" % (w, h))

	#Frame
	topFrame = Frame(root)
	topFrame.pack(side=TOP, fill=X)
	middleFrame = Frame(root)
	middleFrame.pack()
	bottomFrame = Frame(root)
	bottomFrame.pack(side=BOTTOM)

	#main menu
	menu_label = Label(topFrame, text="Main Menu")
	menu_label.config(font=("Arial", 20))
	menu_label.pack()
	    
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
