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
        if 'sid' in session:
            return f(*args, **kwargs)
        else:
            flash('You need to login first!')
            return redirect(url_for('index'))
    return wrap

# Home page handling
@app.route("/", methods=["GET","POST"])
def index():
    # handle if user clicks login
    if request.method == "POST":
        sid = request.form["sid"]
        pin = request.form["pin"]
        # proceed if input isn't empty
        if sid != '' and pin != '':
            # login and check if it succeeded
            br = login(sid, pin)
            if br.title() == "Main Menu":
                flash("Welcome " + grab_username(br))
                session['sid'] = sid
                return redirect(url_for('dashboard'))
            else:
                # Flash an error if it fails
                flash("Invalid ID or Password")
    # Return index page if it didn't login
    return render_template("index.html")

# Dashboard page code
@app.route("/dashboard/")
@login_required
def dashboard():
    return render_template("dashboard.html")


@app.route("/logout/")
@login_required
def logout():
    session.pop('sid', None)
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
