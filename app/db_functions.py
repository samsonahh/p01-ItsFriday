# TNPG: It's Friday!, Roster: Erica Li, Verit Li, Daniel He, Samson Wu
# SoftDev
# P01

import sqlite3
from datetime import datetime
DB_FILE="ALC.db" #ALC = Anime Love Calculator 

## Samson: I recommend opening and closing/committing the database in every single function to make it easier in Flask.

def reset_database():
    db = sqlite3.connect(DB_FILE) #open if file exists, if not it will create a new db
    c = db.cursor() #creates db cursor to execute and fetch           

    c.execute("DROP TABLE IF EXISTS users;")

    #users table stores the username and password
    c.execute("CREATE TABLE IF NOT EXISTS users(username TEXT, password TEXT);")

    db.commit()
    db.close()

def add_user():
    data = (username, password)
    db = sqlite3.connect(DB_FILE) #open if file exists, if not it will create a new db
    c = db.cursor() #creates db cursor to execute and fetch           

    c.execute("INSERT INTO users VALUES(?,?)", data)
    db.commit() #Double-check if this is needed

def check_userexists(username, c):
    db = sqlite3.connect(DB_FILE) #open if file exists, if not it will create a new db      

    c.execute("SELECT * FROM users WHERE username=?", (username,))
    dic = fetchall()

    if dic == []:
        return False
    else:
        return True

def get_user_password(username, c):
    db = sqlite3.connect(DB_FILE) #open if file exists, if not it will create a new db          

    c.execute("SELECT * FROM users WHERE password=?", (password,))
    dic = fetchall()

    if dic == []:
        return False
    else:
        return True
