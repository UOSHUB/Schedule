#!/usr/bin/env python

# import needed libraries
import os
from flask import Flask, render_template, flash, request, redirect, url_for, session
from info import login, grab_username
from functools import wraps

# initialize with template folder in ./static
app = Flask(__name__, template_folder='static')
# configure security key
app.secret_key = 'development key'

# login required decorator
def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'sid' in session and 'pin' in session:
            return f(*args, **kwargs)
        else:
            flash('You need to login first!')
            return redirect(url_for('index'))
    return wrap

# Home page handling
@app.route("/", methods=["GET","POST"])
def index():
    # If user is logged in goto dashboard
    if 'sid' in session and 'pin' in session:
        return redirect(url_for('dashboard'))
    # Store login info and go to dashboard
    if request.method == "POST":
        session['sid'] = request.form["sid"]
        session['pin'] = request.form["pin"]
        session['post'] = True
        return redirect(url_for('dashboard'))
    # If no login, return index page
    return render_template("index.html")

# Dashboard page code
@app.route("/dashboard/")
@login_required
def dashboard():
    # Only if user posted login info
    if 'post' in session:
        session.pop('post', None)
        # login and check if it succeeded
        br = login(session['sid'], session['pin'])
        if br.title() == "Main Menu":
            session['name'] = grab_username(br)
            flash("Welcome " + session['name'])
        else: # If it fails to login
            # Remove credentials from session
            session.pop('sid', None)
            session.pop('pin', None)
            # Flash an error and go back home
            flash("Invalid ID or Password")
            return redirect(url_for('index'))
    else:
        flash("Welcome back " + session['name'])
    return render_template("dashboard.html")


@app.route("/logout/")
@login_required
def logout():
    session.pop('sid', None)
    session.pop('pin', None)
    flash('See you soon ^_^')
    return redirect(url_for('index'))


@app.route("/general/")
def general():
    return redirect(url_for('dashboard'))


@app.route("/about/")
def about():
    return redirect(url_for('dashboard'))

# finalize configurations and run the app
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
