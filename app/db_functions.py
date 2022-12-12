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
    c.execute("DROP TABLE IF EXISTS history;")

    #users table stores the username and password
    c.execute("CREATE TABLE IF NOT EXISTS users(username TEXT, password TEXT);")
    c.execute("CREATE TABLE IF NOT EXISTS history(username TEXT, datetime TEXT);")

    db.commit()
    db.close()

#adds new user (username & password) into the database 
def add_newuser(username, password):
    data = (username, password)
    db = sqlite3.connect(DB_FILE) #open if file exists, if not it will create a new db
    c = db.cursor() #creates db cursor to execute and fetch           

    c.execute("INSERT INTO users VALUES(?,?)", data)
    db.commit() 

#checks whether the user already exists in the database
def check_userexists(username):
    db = sqlite3.connect(DB_FILE) #open if file exists, if not it will create a new db      

    c.execute("SELECT * FROM users WHERE username=?", (username,))
    dic = c.fetchone()

    return dic[1] #returns a password for the given username
    else:
        return ("User does not exist")

    db.commit()

#gets the user's password from the database
def get_user_password(username):
    db = sqlite3.connect(DB_FILE) #open if file exists, if not it will create a new db          

    c.execute("SELECT * FROM users WHERE password=?", (password,))
    dic = c.fetchall()

    if dic == []:
        return False
    else:
        return True

    db.commit()


