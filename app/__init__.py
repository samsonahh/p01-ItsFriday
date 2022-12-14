# TNPG: It's Friday!, Roster: Erica Li, Verit Li, Daniel He, Samson Wu
# SoftDev
# P01

from flask import Flask, render_template, request, session, redirect, url_for
import sqlite3
import requests
from db_functions import *
import api_functions as api
from register_functions import * 
########## NOTES ###########

# OUR PRESET ACCOUNTS:
# samson: samson123
# daniel: daniel123
# erica: erica123
# verit: verit123

########## NOTES ###########

generate_preset_database()

app = Flask(__name__)
app.secret_key = b'kJu2hlllSnasd8a0a@(@2lask'

@app.route('/', methods=['GET', 'POST'])
def home():
    loginstatus = False
    sessionusername = ''
    if 'username' in session:
        loginstatus = True
        sessionusername = session['username']
        #if request.method == 'POST':
            
    return render_template("home.html", login_status = loginstatus, session_username = sessionusername)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'username' in session: #if someone tries to login while already logged in
        return redirect(url_for('home'))

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if check_userexists(username) and get_user_password(username) == password: #checks if user exists & password matches
            session['username'] = request.form['username'] #logs in user
            return redirect(url_for('home'))
        if not check_userexists(username): #checks if username exists 
            return render_template('login.html', FAILMSG ="Username does not exist!")
        else: 
            return render_template('login.html', FAILMSG ="Username and password does not match!")
    return render_template("login.html", FAILMSG = "")

@app.route('/register', methods=['GET', 'POST'])
def register():
    if 'username' in session: #if someone tries to register while already logged in
        return redirect(url_for('home'))

    if request.method == 'POST':
        new_username = request.form['register_username'].strip() #strip removes whitespace. prevents accounts with blank usernames and passwords
        new_password = request.form['register_password'].strip()
        new_password_confirm = request.form['register_password_confirm'].strip()

        print(new_username, new_password, new_password_confirm)

        if check_userexists(new_username): #checks if the username is already taken
            return render_template("register.html", FAILMSG="Username already exists!")

        if not check_usernamerequirements(new_username): #checks if the username fulfills reqs 
            return render_template("register.html", FAILMSG="Username is not long enough")
       
        if not check_passwordrequirements(new_password): #checks if the password fulfills reqs
            return render_template("register.html", FAILMSG="Password is not long enough")

        if not new_password == new_password_confirm: #checks if the password matches the confirmation password
            return render_template("register.html", FAILMSG="Passwords don't match!")
       
        #if all the if statements above fail, do the last case: register the user to the database and logs in
        add_newuser(new_username, new_password) #adds user to the database
        session['username'] = new_username #logs in user
        return redirect(url_for('home'))
    return render_template("register.html", FAILMSG="")

@app.route('/logout')
def logout():
    # remove the username from the session/cookie if it's there
    session.pop('username', None)
    return redirect(url_for('home'))

@app.route('/profile')
def profile():
    loginstatus = False
    sessionusername = ''
    if 'username' in session:
        loginstatus = True
        sessionusername = session['username']
    return render_template("profile.html", login_status = loginstatus, session_username = sessionusername)

@app.route('/match', methods=['GET', 'POST'])
def match():
    loginstatus = False
    sessionusername = ''
    if 'username' in session:
        loginstatus = True
        sessionusername = session['username']
        if request.method == 'POST': # process searching functionality for character in match.html
            if len(request.form['input']) > 0: # checks if the input is blank
                return redirect(url_for("match_search", input = request.form['input'], media = request.form['media'], page = 0))
        if request.method == 'GET':
            if 'id' in request.args:
                return redirect(url_for("match_search_show_character", id = request.args['id'], page = 0))
    return render_template("match.html", login_status = loginstatus, session_username = sessionusername, diction = None, media = "None")

@app.route('/match/<media>/<input>/<page>', methods=['GET', 'POST']) # renders unique match pages for character searching 
def match_search(media, input, page):
    loginstatus = False
    sessionusername = ''
    if 'username' in session:
        loginstatus = True
        sessionusername = session['username']
        diction = api.pagination_with_media(input, page, media)
        return render_template("match.html", login_status = loginstatus, session_username = sessionusername, diction = diction, media = media)
    return render_template("match.html", login_status = loginstatus, session_username = sessionusername, diction = None, media = "None")

@app.route('/match/<id>/<page>', methods=['GET', 'POST']) # display characters from a specific show
def match_search_show_character(id, page):
    loginstatus = False
    sessionusername = ''
    if 'username' in session:
        loginstatus = True
        sessionusername = session['username']
        diction = api.pagination_id(id, page)
        return render_template("match.html", login_status = loginstatus, session_username = sessionusername, diction = diction, media = "Character")
    return render_template("match.html", login_status = loginstatus, session_username = sessionusername, diction = None, media = "None")

@app.route('/<media>/<input>/<page>', methods=['GET', 'POST']) # renders unique match pages for character searching 
def search_results(media, input, page):
    loginstatus = False
    sessionusername = ''
    if 'username' in session:
        loginstatus = True
        sessionusername = session['username']
        if media == 'Character':
            diction = api.pagination(input, page)
            return render_template("home.html", login_status = loginstatus, session_username = sessionusername, diction = diction)
    for i in diction:
        print (i)
    return render_template("home.html", login_status = loginstatus, session_username = sessionusername, diction = None)

@app.route('/compatibility')
def compatibility():
    loginstatus = False
    sessionusername = ''
    if 'username' in session:
        loginstatus = True
        sessionusername = session['username']
    return render_template("compatibility.html", login_status = loginstatus, session_username = sessionusername)


if __name__ == "__main__": #false if this file imported as module
    #enable debugging, auto-restarting of server when this file is modified
    app.debug = True 
    app.run()