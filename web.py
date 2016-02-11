#!/usr/bin/env python

# import needed libraries
import os
from flask import Flask, render_template, flash, request
from info import login, grab_username

# initialize with template folder in /
app = Flask(__name__, template_folder='')

# handle url requests
@app.route("/", methods=["GET","POST"])
def index():
    info = ''
    # handle if user clicks login
    if request.method == "POST":
        sid = request.form["sid"]
        pin = request.form["pin"]
        # proceed if input isn't empty
        if sid != '' and pin != '':
            # login and check if it succeeded
            br = login(sid, pin)
            if br.title() == "Main Menu":
                flash("Welcome " + grab_username())
                info = br.title()
            else:
                flash("Invalid ID or Password")

    return render_template("index.html", data=info)

# finalize configurations and run the app
if __name__ == "__main__":
    app.secret_key = 'development key'
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
