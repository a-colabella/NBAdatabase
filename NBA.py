# Andrew Colabella, Sean Foley, Peyton Sayasith
# Database Design
# NBA Statistics Project

import flask
import mysql.connector
import Tkinter as tk

def select(connection, statement):
    cur = connection.cursor()
    cur.execute(statement)
    output = cur.fetchall()
    cur.close()

    return output

def main(config):
    # SQL Connection
    cnx = mysql.connector.connect(**config)

    # Main window
    mainwin = tk.Tk()
    mainwin.title("NBA Statistics")

    # Background frame
    back = tk.Frame(master=mainwin, width=800, height=800)
    back.pack()


    
    mainwin.mainloop()

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
