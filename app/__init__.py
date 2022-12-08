# TNPG: It's Friday!, Roster: Erica Li, Verit Li, Daniel He, Samson Wu
# SoftDev
# P01

from flask import Flask, render_template, request, session, redirect, url_for
import requests
from db_functions import *
from api_functions import *

app = Flask(__name__)
app.secret_key = b'kJu2hlllSnasd8a0a@(@2lask'

@app.route('/', methods=['GET', 'POST'])
def home():
    loginstatus = False #Samson: We should check session whether user is logged in
    return render_template("home.html", login_status = loginstatus)

@app.route('/login') #, methods=['POST'])
def login():
    if request.method == 'POST':
        db = sqlite3.connect(DB_FILE) #opens if file exists... if not, it will create one
        c = db.cursor #be able to execute & operate 
        username = request.form['username']
        password = request.form['password']
        

    return render_template("login.html")

@app.route('/register')
def register():
    return render_template("register.html")

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