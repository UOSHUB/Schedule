#!/usr/bin/env python

# Import needed libraries
import os
from flask import Flask, render_template, flash, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from interface import Interface
from functools import wraps

# Initialize with template folder in ./static
app = Flask(__name__, template_folder="static")
# configure app from object of current environment
app.config.from_object(os.environ['APP_SETTINGS'])
# Initialize SQLAlchemy database
db = SQLAlchemy(app)
# Import models after initializing database
from models import *
# Instantiate an info object
interface = Interface()


# login required decorator
def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if "name" in session:
            return f(*args, **kwargs)
        else:
            flash("You need to login first!")
            return redirect(url_for("index"))
    return wrap


# Home page handling
@app.route("/", methods=["GET", "POST"])
def index():
    # If logged in, flash welcome back & go to dashboard
    if "name" in session:
        flash("Welcome back " + session["name"])
        return redirect(url_for("dashboard"))
    # Store login info and go to dashboard
    if request.method == "POST":
        # login and check if it succeeded
        if interface.verify_login(request.form["sid"], request.form["pin"]):
            # If logged in, store student name in session
            sid = request.form["sid"]
            # Grab student by id from database if existed
            student = Student.query.filter_by(sid=sid).first()
            # If student is new
            if student is None:
                # Grab student name and store it in session
                session["name"] = interface.get_name()
                # Add student id and name to database
                db.session.add(Student(sid, session["name"]))
                # Commit changes to database
                db.session.commit()
            else:  # If student has logged in before
                # Store student name in session from database
                session["name"] = student.name
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
    return render_template("dashboard.html", interface=interface)


@app.route("/logout/")
@login_required
def logout():
    # Flash bye message
    flash("See you soon " + session["name"] + " ^_^")
    # Delete student info
    session.pop("name", None)
    # Clean up schedule and go home
    interface.empty_schedule()
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
    app.run(host="0.0.0.0", port=port)
