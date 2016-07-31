#!/usr/bin/env python

# Import needed libraries
import os
from flask import Flask, render_template, flash, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from scraper import scraper, login_required
from schedule.views import schedule

# Initialize with template folder in ./static
app = Flask(__name__, template_folder="static")
# Register schedule blueprint
app.register_blueprint(schedule, url_prefix="/schedule")
# configure app from object of current environment
app.config.from_object(os.environ["APP_SETTINGS"])
# Initialize SQLAlchemy database
db = SQLAlchemy(app)
# Import models after initializing database
from models import *


# Home page handling
@app.route("/", methods=["GET", "POST"])
def index():
    # If logged in, flash welcome back & go to dashboard
    if "name" in session:
        flash("Welcome back " + session["name"])
        return redirect(url_for("dashboard"))
    # Try to login if credentials are provided
    if request.method == "POST":
        # Store student credentials in session
        session["sid"] = request.form["sid"]
        session["pin"] = request.form["pin"]
        # login and check if it succeeded
        if scraper.login():
            # Grab student by id from database if existed
            student = Student.query.filter_by(sid=session["sid"]).first()
            # If student is new
            if student is None:
                # Grab student name and store it in session
                session["name"] = scraper.get_username()
                # Add student id and name to database
                db.session.add(Student(session["sid"], session["name"]))
                # Commit changes to database
                db.session.commit()
            else:  # If student has logged in before
                # Store student name in session from database
                session["name"] = student.name
            # Flash welcoming message and go to dashboard
            flash("Welcome " + session["name"])
            return redirect(url_for("dashboard"))
        else:
            # Clear wrong credentials
            session.clear()
            # Flash an error if login fails
            flash("Invalid ID or Password")
    # If no login, return to index page
    return render_template("index.html")


# Dashboard page code
@app.route("/dashboard/")
@login_required
def dashboard():
    return render_template("dashboard.html")


@app.route("/logout/")
@login_required
def logout():
    name = session["name"]
    # Clear student info
    session.clear()
    # Flash bye message
    flash("See you soon " + name + " ^_^")
    # Go back to home page
    return redirect(url_for("index"))


@app.route("/general/")
def general():
    return redirect(url_for("dashboard"))


@app.route("/about/")
def about():
    return redirect(url_for("dashboard"))


# Nicely handle all errors
@app.errorhandler(Exception)
@app.errorhandler(500)
@app.errorhandler(404)
@app.errorhandler(403)
def error(e):
    # If student logs in from error page
    if request.method == "POST":
        # Send code 307 to preserve the post request
        return redirect(url_for("index"), code=307)
    # Otherwise render appropriate error page
    return render_template("error.html", error=str(e))

# finalize configurations and run the app
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
