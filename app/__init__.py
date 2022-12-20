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

    if not 'username' in session and request.method == 'POST': # if you make a search result when not logged in
        return redirect(url_for("login"))

    if 'username' in session:
        loginstatus = True
        sessionusername = session['username']
        print('CCCCCCCCCCC')
        session['match_one'] = {'image': 'false', 'id': 'false', 'name': 'false'}
        session['match_two'] = {'image': 'false', 'id': 'false', 'name': 'false'}
        if request.method == 'POST':
            print(request.form)
            user_search = request.form['character_search'].strip()
            if len(user_search) > 0: # checks if the input is blank
                return redirect(url_for("search_results", media = "Character", input = user_search, page = 0))
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
            return render_template("register.html", FAILMSG="Username is not long enough!")
       
        if not check_passwordrequirements(new_password): #checks if the password fulfills reqs
            return render_template("register.html", FAILMSG="Password is not long enough!")

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

@app.route('/search/<input>/<page>', methods=['GET', 'POST']) # renders unique match pages for character searching 
def search_results(input, page):
    if not 'username' in session: #if someone tries to go here when not logged in
        return redirect(url_for('login'))
    # character_name = request.form['input']
    # return redirect(url_for('character_profile'), input = character_name)
    if request.method == 'POST':
        if 'input' in request.form: #if user is searching for a new character
            user_search = request.form['input'].strip()
            if len(user_search) > 0: # checks if the input is blank
                return redirect(url_for("search_results", media = 'Character', input = user_search, page = 1))
        # if 'character' in request.form: #if user is accessing a character profile
            #redirect to url of that character's profile

    diction = api.pagination_with_media(input, page, 'Character')
    return render_template("search_results.html", session_username = session['username'], diction = diction, media = 'Character')

@app.route('/profile')
def profile():
    if not 'username' in session: #if someone tries to go here when not logged in
        return redirect(url_for('login'))

    return render_template("profile.html", session_username = session['username'])

@app.route('/match', methods=['GET', 'POST'])
def match():
    if not 'username' in session: #if someone tries to go here when not logged in
        return redirect(url_for('login'))

    if request.method == 'POST': # process searching functionality for character in match.html
        if 'input' in request.form:
            user_search = request.form['input'].strip()
            if len(user_search) > 0: # checks if the input is blank
                return redirect(url_for("match_search", media = request.form['media'], input = user_search, page = 1))
        elif 'match_one' in request.form:
            session['match_one'] = {'image': 'false', 'id': 'false', 'name': 'false'}
            session.modified = True
            return redirect(request.referrer)
        elif 'match_two' in request.form:
            session['match_two'] = {'image': 'false', 'id': 'false', 'name': 'false'}
            session.modified = True
            return redirect(request.referrer)
    if request.method == 'GET':
        if 'media' in request.args:
            if request.args['media'] == 'Show':
                return redirect(url_for("match_search_show_character", id = request.args['id'], page = 1))
            else:
                if session['match_one']['image'] == 'false':
                    session['match_one'] = {'image': request.args['image'], 'id': request.args['id'], 'name': request.args['name']}
                    session.modified = True
                    return redirect(request.referrer) # returns to url the request was made from (so you still see the search results)
                elif session['match_two']['image'] == 'false':
                    session['match_two'] = {'image': request.args['image'], 'id': request.args['id'], 'name': request.args['name']}
                    session.modified = True
                    return redirect(request.referrer) # returns to url the request was made from (so you still see the search results)
    return render_template("match.html", session_username = session['username'], diction = None, media = "None")

@app.route('/match/<media>/<input>/<page>', methods=['GET', 'POST']) # renders unique match pages for character searching 
def match_search(media, input, page):
    if not 'username' in session: #if someone tries to go here when not logged in
        return redirect(url_for('login'))
    # character_name = request.form['input']
    # return redirect(url_for('character_profile'), input = character_name)
    diction = api.pagination_with_media(input, page, media)
    page = int(page)
    if page > diction[1]:
        page = diction[1] # ISSUE: STILL ALLOWS URL TO GO BEYOND MAX
    if page < 1:
        page = 1
    previous_ellipsis = True
    future_ellipsis = True
    previous = []
    future = []
    for i in range(2):
        if page - (2 - i) == 1:
            previous.append(page - (2 - i))
            previous_ellipsis = False
        elif page - (2 - i) < 1:
            previous_ellipsis = False
            pass
        else: 
            previous.append(page - (2 - i))
        if page + (i + 1) == diction[1]:
            future.append(page + (i+1))
            future_ellipsis = False
        elif page + (i + 1) > diction[1]:
            future_ellipsis = False
            pass
        else:
            future.append(page + (i+1))
    pagination = {'previous_ellipsis': previous_ellipsis, 'future_ellipsis': future_ellipsis, 'previous': previous, 'future': future, 'page': page}
    return render_template("match.html", session_username = session['username'], diction = diction, media = media, pagination = pagination, input = input)

@app.route('/match/<id>/<page>', methods=['GET', 'POST']) # display characters from a specific show
def match_search_show_character(id, page):
    if not 'username' in session: #if someone tries to go here when not logged in
        return redirect(url_for('login'))
        
    diction = api.pagination_id(id, page)
    page = int(page)
    if page > diction[1]:
        page = diction[1]
    if page < 1:
        page = 1
    previous_ellipsis = True
    future_ellipsis = True
    previous = []
    future = []
    for i in range(2):
        if page - (2 - i) == 1:
            previous.append(page - (2 - i))
            previous_ellipsis = False
        elif page - (2 - i) < 1:
            previous_ellipsis = False
            pass
        else: 
            previous.append(page - (2 - i))
        if page + (i + 1) == diction[1]:
            future.append(page + (i+1))
            future_ellipsis = False
        elif page + (i + 1) > diction[1]:
            future_ellipsis = False
            pass
        else:
            future.append(page + (i+1))
    pagination = {'previous_ellipsis': previous_ellipsis, 'future_ellipsis': future_ellipsis, 'previous': previous, 'future': future, 'page': page}
    return render_template("match.html", session_username = session['username'], diction = diction, media = "Character", pagination = pagination)

@app.route('/match/test')
def match_test():
    if not 'username' in session: #if someone tries to go here when not logged in
        return redirect(url_for('login'))

    diction = []
    for i in range(12):
        diction.append({"name": 'girl', "description": 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vestibulum fermentum tellus vitae quam ornare, vel mattis lacus lobortis. Pellentesque gravida hendrerit congue. Curabitur nisi erat, tincidunt ut commodo ac, imperdiet ac libero. In at diam vitae turpis maximus dapibus. Ut non nulla sit amet odio volutpat egestas. Ut pharetra odio nulla. Nulla non eleifend risus. Vestibulum non elit quam. Duis vel dolor nunc. Quisque euismod semper lorem in lacinia.', "image": "https://media.kitsu.io/characters/images/8266/original.jpg", "id": i})
    diction = (diction, "12")
    return render_template("match.html", session_username = session['username'], diction = diction, media = "Character")

@app.route('/profile/Character/<id>', methods=['GET', 'POST']) #character profiles 
def character_profile(id):
    if not 'username' in session: #if someone tries to go here when not logged in
        return redirect(url_for('login'))
    
    dictionary = api.get_char_info_by_id(int(id))

    print(dictionary)


    return render_template("profile.html", session_username = session['username'], dict = dictionary)


@app.route('/compatibility', methods=['GET', 'POST'])
def compatibility():
    if not 'username' in session: #if someone tries to go here when not logged in
        return redirect(url_for('login'))
    if request.method == 'POST':
        char_one = session['match_one']
        char_two = session['match_one']
        session['match_one'] = {'image': 'false', 'id': 'false', 'name': 'false'}
        session['match_two'] = {'image': 'false', 'id': 'false', 'name': 'false'}
        session.modified = True
        return render_template("compatibility.html", session_username = session['username'], char_one = char_one, char_two = char_two)
    return render_template("compatibility.html", session_username = session['username'])


if __name__ == "__main__": #false if this file imported as module
    #enable debugging, auto-restarting of server when this file is modified
    app.debug = True 
    app.run()
