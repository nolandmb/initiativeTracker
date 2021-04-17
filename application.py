import os
import mysql

from flask_sqlalchemy import SQLAlchemy
from flask import Flask, flash, redirect, render_template, request, session, url_for
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
from extras import *
from sqlalchemy import create_engine



app = Flask(__name__)

app.config['SECRET_KEY'] = os.urandom(24)

app.config["DEBUG"] = True
SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://{username}:{password}@{hostname}/{databasename}".format(
    username="nolandmb",
    password="Neededapassword",
    hostname="nolandmb.mysql.pythonanywhere-services.com",
    databasename="nolandmb$combat",
)
app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
app.config["SQLALCHEMY_POOL_RECYCLE"] = 299
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)
engine = create_engine('postgresql://usr:pass@localhost:5432/sqlalchemy')



@app.route("/login", methods=["GET", "POST"])
def login():
    # Log user in
    # Forget any user_id
    session.clear()
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return error("must provide username")

        # Ensure password was submitted
        elif not request.form.get("password"):
            return error("must provide password")

        # Query database for username
        getName = request.form.get("username")
        newResults = db.session.execute("SELECT * FROM users WHERE user = :getName", {'getName' :getName})
        rows = newResults.fetchall()
        results = []
        for row in rows:
            results = row

        # Ensure username exists and password is correct
        if results[1] != request.form.get("username") or not check_password_hash(results[2], request.form.get("password")):
            return error("invalid username and/or password")

        theUser = request.form.get("username")
        getID = db.session.execute("SELECT id FROM users WHERE user = :theUser", {'theUser'  :theUser})
        userID = getID.fetchone()

        # Remember which user has logged in
        session["user_id"] = userID[0]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    return render_template("login.html")


@app.route("/logout")
def logout():
    # Log user out
    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/register", methods=["GET", "POST"])
def register():
    # Register new user and handle errors
    if request.method == "POST":
        if not request.form.get("username"):
            return error("must provide username")
        elif not request.form.get("password"):
            return error("must provide password")
        elif not request.form.get("confirmation"):
            return error("must confirm password")
        elif request.form.get("password") != request.form.get("confirmation"):
            return error("passwords do not match")
        # create hash for the passwords instread of storeing the passwords
        passwordHash = generate_password_hash(request.form.get("password"), 'pbkdf2:sha256')
        checkUser = request.form["username"]

        # getting user names
        get_names = []
        get_names = db.session.execute("SELECT user FROM users")

        # checking to see if user name already exist
        for name in get_names:
            if name == checkUser:
                return error("username already used")

        # adding new user to the database

        db.session.execute("INSERT INTO users (user, hash) VALUES (:checkUser, :passwordHash)", {'checkUser' :checkUser, 'passwordHash' :passwordHash})
        db.session.commit()

        resault = db.session.execute("SELECT id FROM users WHERE user = :checkUser", {'checkUser' :checkUser})
        currentID = resault.fetchone()

        # keeping the user logged in for the session
        session['user_id'] = currentID[0]

        return render_template("index.html")

    return render_template("register.html")


@app.route("/", methods=["GET", "POST"])
@login_required
def index():
    GM = session['user_id']

    # pull the current users character list
    results = db.session.execute("SELECT name, initiative FROM chracters WHERE GM_id = :GM", {'GM' :GM})
    getResults = results.fetchall()
    list(getResults)
    characters = []
    i = 0
    for row in getResults:
        characters.append({"name": getResults[i][0], "modifier": getResults[i][1]})
        i += 1

    return render_template("index.html", characters=characters)


@app.route("/addCharacter/", methods=["GET", "POST"])
@login_required
def addCharacter():

    # log in and handles errors
    if request.method == "POST":
        getName = request.form.get("characterName")
        if request.form.get("characterName") == None:
            return error("must enter character username")
    if not request.form.get("initiativeMod"):
        initiative = 0
    else:
        initiative = request.form.get("initiativeMod")

    character = request.form.get("characterName")

    #check for ewxisting character in database
    getResult = []
    result = db.session.execute("SELECT name, GM_id FROM chracters WHERE name = :character", {'character' :character})
    getResult = result.fetchone()
    if getResult != None:
        GM = getResult[1]
        if character == getResult[0] and GM == session["user_id"]:
            return error("Character already exist")
    GM = session["user_id"]

    #add new character to database
    newCharacter = []
    newCharacter = db.session.execute("INSERT INTO chracters (name, initiative, GM_id) VALUES  (:character, :initiative, :GM)", {'character' :character, 'initiative' :initiative, 'GM' :GM})
    db.session.commit()

    return redirect("/updateCharacter")


@app.route("/deleteCharacter", methods=["GET", "POST"])
@login_required
def deletecharacter():

    # deletes charactrs from the data base
    if request.method == "POST":
        if not request.form.get("deleteName"):
            return error("must enter character username")

    character = request.form.get("deleteName")
    character
    checkChar =db.session.execute("SELECT name FROM chracters WHERE name = :character", {'character' :character})
    checkCharacters = checkChar.fetchone()
    checkCharacters = list(checkCharacters)
    checked = db.session.execute("SELECT GM_id FROM chracters WHERE name = :character", {'character' :character})
    getGM = checked.fetchone()
    getGM = list(getGM)
    if checkCharacters[0] != character:
        return error("Character not found")
    if character == checkCharacters[0] and getGM[0] == session["user_id"]:
        db.session.execute("DELETE FROM chracters WHERE name = :character", {'character' :character})
        db.session.commit()
    else:
        return error("Please enter a valid character")
    return render_template("updateCharacter.html")


@app.route("/modCharacter", methods=["GET", "POST"])
@login_required
def modcharacter():

    # update characters modifier in the data base
    if request.method == "POST":
        if not request.form.get("modName"):
            return error("must enter character username")
    character = request.form.get("modName")
    if not request.form.get("changeMod"):
        return error("must enter a new modifier")
    else:
        initiative = request.form.get("changeMod")

    result = db.session.execute("SELECT name FROM chracters WHERE name = :character", {'character' : character,})
    checkCharacters = result.fetchone()
    checkCharacters = list(checkCharacters)
    gmResult = db.session.execute("SELECT GM_id FROM chracters WHERE name = :character", {'character' : character,})
    GM = gmResult.fetchone()
    GM = list(GM)
    if character == checkCharacters[0] and GM[0] == session["user_id"]:
     db.session.execute("UPDATE chracters SET initiative = :initiative WHERE name = :character", {'initiative' : initiative, 'character' : character})

    else:
        return error("Character not avalible")

    return render_template("updateCharacter.html")


@app.route("/updateCharacter", methods=["GET", "POST"])
@login_required
def updatecharacter():

    return render_template("updateCharacter.html")
