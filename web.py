#!/usr/bin/env python

# import needed libraries
import os
from flask import Flask, render_template, flash, request, redirect, url_for, session
from info import Info
from functools import wraps

# initialize with template folder in ./static
app = Flask(__name__, template_folder="static")
# configure security key
app.secret_key = "development key"
# instantiate an info object
info = Info()


# login required decorator
def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if "sid" in session:
            return f(*args, **kwargs)
        else:
            flash("You need to login first!")
            return redirect(url_for("index"))
    return wrap


# Home page handling
@app.route("/", methods=["GET", "POST"])
def index():
    # If logged in, flash welcome back & go to dashboard
    if "sid" in session:
        flash("Welcome back " + session["name"])
        return redirect(url_for("dashboard"))
    # Store login info and go to dashboard
    if request.method == "POST":
        # login and check if it succeeded
        info.login(request.form["sid"], request.form["pin"])
        if info.br.title() == "Main Menu":
            # If logged in, store sid and name in session
            session["sid"] = request.form["sid"]
            session["name"] = info.grab_username()
            # Flash welcoming message and go to dashboard
            flash("Welcome " + session["name"])
            return redirect(url_for("dashboard"))
        else:
            # Flash an error if login fails
            flash("Invalid ID or Password")
    # If no login, return to index page
    return render_template("index.html")


# Dashboard page code
@app.route("/dashboard/")
@login_required
def dashboard():
    # Try to grab student schedule and go to dashboard
    try:
        schedule = info.grab_schedule()
    except Exception:
        schedule = {"Error!": []}
    return render_template("dashboard.html", data=schedule)


@app.route("/logout/")
@login_required
def logout():
    # Flash bye message, delete student info and go home
    flash("See you soon " + session["name"] + " ^_^")
    session.pop("name", None)
    session.pop("sid", None)
    return redirect(url_for("index"))


@app.route("/general/")
def general():
    return redirect(url_for("dashboard"))


@app.route("/about/")
def about():
    return redirect(url_for("dashboard"))

# finalize configurations and run the app
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
