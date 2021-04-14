import psycopg2
import os

from flask_sqlalchemy import SQLAlchemy
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
from markupsafe import escape
from extras import *


app = Flask(__name__)
app.config["DEBUG"] = True
SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://{username}:{password}@{hostname}/{databasename}".format(
    username="nolandmb",
    password="Neededapassword",
    hostname="nolandmb.mysql.pythonanywhere-services.com",
    databasename="nolandmn$combat",
)
app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
app.config["SQLALCHEMY_POOL_RECYCLE"] = 299
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)
cur = db.cursor()


@app.route("/login", methods=["GET", "POST"])
def login():
    # Log user in
    # Forget any user_id
    session.clear()
    db = psycopg2.connect(DATABASE_URL, sslmode='require')
    cur = db.cursor()
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return error("must provide username")

        # Ensure password was submitted
        elif not request.form.get("password"):
            return error("must provide password")

        # Query database for username
        rows = cur.execute("SELECT * FROM users WHERE user = ?", request.form.get("username"))
        results = []
        for row in rows:
            results = row

        # Ensure username exists and password is correct
        if results[1] != request.form.get("username") or not check_password_hash(results[2], request.form.get("password")):
            return error("invalid username and/or password")

        cur.execute("SELECT id FROM users WHERE user = ?", request.form.get("username"))
        getID = cur.fetchone()
        userID = getID[0]

        # Remember which user has logged in
        session["user_id"] = userID

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
    db = psycopg2.connect(DATABASE_URL, sslmode='require')
    cur = db.cursor()
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
        user_names = []
        get_names = []
        user_names = cur.execute("SELECT user FROM users")
        get_names = cur.fetchall()

        # checking to see if user name already exist
        for name in get_names:
            if name == checkUser:
                return error("username already used")

        # adding new user to the database
        newUser = []
        newUser = cur.execute("INSERT INTO users (user, hash) VALUES (?, ?)", (checkUser, passwordHash))
        db.commit()

        cur.execute("SELECT id FROM users WHERE user = ?", (checkUser,))
        resault = cur.fetchone()
        currentID = resault[0]
        # keeping the user logged in for the session
        session['user_id'] = currentID

        return render_template("index.html")

    return render_template("register.html")


@app.route("/", methods=["GET", "POST"])
@login_required
def index():
    db = psycopg2.connect(DATABASE_URL, sslmode='require')
    cur = db.cursor()
    GM = session['user_id']

    # pull the current users character list
    cur.execute("SELECT name, initiative FROM characters WHERE GM_id = ?", (GM,))
    results = cur.fetchall()
    list(results)
    characters = []
    i = 0
    for row in results:
        characters.append({"name": results[i][0], "modifier": results[i][1]})
        i += 1

    return render_template("index.html", characters=characters)


@app.route("/addCharacter/", methods=["GET", "POST"])
@login_required
def addCharacter():
    db = psycopg2.connect(DATABASE_URL, sslmode='require')
    cur = db.cursor()

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

    cur.execute("SELECT name, GM_id FROM characters WHERE name = ?", (character,))
    resault = cur.fetchone()

    if resault != None:
        GM = resault[1]
        if character == resault[0] and GM == session["user_id"]:
            return error("Character already exist")
    GM = session["user_id"]

    newCharacter = []
    newCharacter = cur.execute("INSERT INTO characters (name, initiative, GM_id) VALUES  (?, ?, ?)", (character, initiative, GM))
    db.commit()

    return redirect("/updateCharacter")


@app.route("/deleteCharacter", methods=["GET", "POST"])
@login_required
def deletecharacter():
    db = psycopg2.connect(DATABASE_URL, sslmode='require')
    cur = db.cursor()

    # deletes charactrs from the data base
    if request.method == "POST":
        if not request.form.get("deleteName"):
            return error("must enter character username")

    character = request.form.get("deleteName")

    cur.execute("SELECT name, GM_id FROM characters WHERE name = ?", (character,))
    checkCharacters = cur.fetchone()
    getGM = checkCharacters[1]

    if not checkCharacters:
        return error("Character not found")
    if character == checkCharacters[0] and getGM == session["user_id"]:
        cur.execute("DELETE FROM characters WHERE name = ?", (character,))
        db.commit()
    else:
        return error("Please enter a valid character")
    return render_template("updateCharacter.html")


@app.route("/modCharacter", methods=["GET", "POST"])
@login_required
def modcharacter():
    db = psycopg2.connect(DATABASE_URL, sslmode='require')
    cur = db.cursor()

    # update characters modifier in the data base
    if request.method == "POST":
        if not request.form.get("modName"):
            return error("must enter character username")
    character = request.form.get("modrName")
    if not request.form.get("changeMod"):
        return error("must enter a new modifier")
    else:
        initiative = request.form.get("changeMod")
    if character == resault[0] and GM == session["user_id"]:
        cur.execute("UPDATE characters SET initiative = ? WHERE name = ?", (initiative, character))
        db.commit()
    else:
        return error("Character not avalible")

    return render_template("updateCharacter.html")


@app.route("/updateCharacter", methods=["GET", "POST"])
@login_required
def updatecharacter():

    return render_template("updateCharacter.html")
