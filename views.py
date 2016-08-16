# Import models after initializing database
from flask import render_template, flash, request, redirect, url_for, session
from browser import br, login_required
from models import Student
from web import app, db


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
        if br.login():
            # Grab student by id from database if existed
            student = Student.query.filter_by(sid=session["sid"]).first()
            # If student is new
            if student is None:
                # Grab student name and store it in session
                session["name"] = br.get_username()
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
@app.errorhandler(405)
@app.errorhandler(404)
@app.errorhandler(403)
def error(e):
    # If the error happened with a post request
    if request.method == "POST":
        # If it's login request from error page
        if "login" in request.form:
            # Send code 307 to preserve the post request
            return redirect(url_for("index"), code=307)
        # Otherwise just return an exception
        else:
            return Exception
    # Otherwise render appropriate error page
    return render_template("error.html", error=str(e))
