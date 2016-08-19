# Import models after initializing database
from flask import render_template, flash, request, redirect, url_for, session, json
from browser import br, login_required
# from models import Student
from web import app  # , db


# Home page handling
@app.route("/", methods=["GET"])
def index():
    # If already logged in, flash welcome back message
    if "sid" in session:
        flash("Welcome back " + session["sid"])
    # Return AngularJS app outer layout
    return render_template("index.html")


@app.route("/login", methods=["POST"])
def login():
    # Store student credentials in session
    session.update(json.loads(request.data))
    # Login and check if it succeeded
    if br.login():
        # Grab student name and return it
        return json.dumps(br.get_user_info())
    # Otherwise, clear wrong credentials
    session.clear()
    # Then return an error
    return Exception


# Dashboard page code
@app.route("/dashboard", methods=["POST"])
@login_required
def dashboard():
    return render_template("dashboard.html")


@app.route("/logout", methods=["POST"])
@login_required
def logout():
    # Clear student info
    session.clear()
    # Return no content flag
    return ('', 204)


@app.route("/general", methods=["POST"])
def general():
    return redirect(url_for("dashboard"))


@app.route("/about", methods=["POST"])
def about():
    return redirect(url_for("dashboard"))


# Nicely handle all errors
@app.errorhandler(Exception)
@app.errorhandler(500)
@app.errorhandler(405)
@app.errorhandler(404)
@app.errorhandler(403)
def error(e):
    # Return an exceptionIf the error happened with a post request, otherwise render appropriate error page
    return Exception if request.method == "POST" else render_template("error.html", error=str(e))
