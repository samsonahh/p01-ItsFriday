# TNPG: It's Friday!, Roster: Erica Li, Verit Li, Daniel He, Samson Wu
# SoftDev
# P01
# fetchall attempts to get everything while fetchone gets first line

import sqlite3
from datetime import datetime
DB_FILE="ALC.db" #ALC = Anime Love Calculator 

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
    db.close()

#checks whether the user already exists in the database
def check_userexists(username):
    db = sqlite3.connect(DB_FILE) #open if file exists, if not it will create a new db 
    c = db.cursor() #creates db cursor to execute and fetch      

    c.execute("SELECT * FROM users WHERE username=?", (username,))
    dict = c.fetchone()

    db.close()

    if dict == None: #if no user
        return False
    
    return True #if dict is not empty (meaning user exists)

#gets the user's password from the database
def get_user_password(username):
    db = sqlite3.connect(DB_FILE) #open if file exists, if not it will create a new db          
    c = db.cursor() #creates db cursor to execute and fetch      

    c.execute("SELECT * FROM users WHERE username=?", (username,))
    dict = c.fetchone()

    db.close()

    return dict[1]

def generate_preset_database():
    reset_database()
    add_newuser('samson', 'samson123')
    add_newuser('erica', 'erica123')
    add_newuser('verit', 'verit123')
    add_newuser('daniel', 'daniel123')