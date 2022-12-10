# TNPG: It's Friday!, Roster: Erica Li, Verit Li, Daniel He, Samson Wu
# SoftDev
# P01

from flask import Flask, render_template, request, session, redirect, url_for
import sqlite3
import requests
from db_functions import *
from api_functions import *
from register_functions import * 
########## NOTES ###########

# Tables for database need to be created first before login/ register works 

########## NOTES ###########
app = Flask(__name__)
app.secret_key = b'kJu2hlllSnasd8a0a@(@2lask'

@app.route('/', methods=['GET', 'POST'])
def home():
    loginstatus = False #Samson: We should check session whether user is logged in
    return render_template("home.html", login_status = loginstatus)

@app.route('/login', methods=['GET', 'POST']) #, methods=['POST'])
def login():
    if request.method == 'POST':
        db = sqlite3.connect(DB_FILE, check_same_thread=False) #opens if file exists... if not, it will create one
        c = db.cursor() #be able to execute & operate 
        username = request.form['username']
        password = request.form['password']
        if check_userexists(username, c) and get_user_password(username, c) == password: #checks if user exists & password matches
            db.close()
            session['username'] = request.form['username'] #logs in user
            loginstatus = True 
            return redirect(url_for('home'))
        if not check_userexists(username, c): #checks if username exists 
            db.close()
            return render_template('login.html', FAILMSG ="Username does not exist")
        else: 
            db.close()
            return render_template('login.html', FAILMSG ="Username and password does not match")
    return render_template("login.html", FAILMSG = "")

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        print("checkpoint!")
        db = sqlite3.connect(DB_FILE, check_same_thread=False) #opens if file exists... if not, it will create one
        c = db.cursor() #be able to execute & operate 
        new_username = request.form['username']
        new_password = request.form['password']
    
        if check_userexists(new_username, c): #checks if the username is already taken
            return render_template("register.html", FAILMSG="Username already exists")
        
        if check_usernamerequirements(new_username): #checks if the username fulfills reqs 
            return render_template("register.html", FAILMSG="Username is not long enough")
       
        if check_passwordrequirements(new_password): #checks if the password fulfills reqs
            return render_template("register.html", FAILMSG="Password is not long enough")
       
        else:
            add_newuser(new_username, new_password) #adds user to the database
            session['username'] = request.form['username'] #logs in user
            loginstatus = True 
            return redirect(url_for('home'))
    return render_template("register.html", FAILMSG="")

@app.route('/logout')
def logout():
    return render_template("login.html")

@app.route('/profile')
def profile():
    loginstatus = False
    return render_template("profile.html", login_status = loginstatus)

@app.route('/match')
def match():
    loginstatus = False
    return render_template("match.html", login_status = loginstatus)

@app.route('/compatibility')
def compatibility():
    loginstatus = False
    return render_template("compatibility.html", login_status = loginstatus)


if __name__ == "__main__": #false if this file imported as module
    #enable debugging, auto-restarting of server when this file is modified
    app.debug = True 
    app.run()