from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session
from functools import wraps



def login_required(f):
   # https://flask.palletsprojects.com/en/1.1.x/patterns/viewdecorators/

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function


def error(message):

    return render_template("error.html", message =  message)
