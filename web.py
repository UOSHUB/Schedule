#!/usr/bin/env python

# import needed libraries
import os, json
from flask import Flask, render_template, flash, request
from info import get_info

# initialize with template folder in /
app = Flask(__name__, template_folder='')

# handle url requests
@app.route("/", methods=["GET","POST"])
def index():
    info = ''
    try:
        if request.method == "POST":
            sid = request.form["sid"]
            pin = request.form["pin"]
            if sid != '' and pin != '':
                flash("Welcome " + sid)
                info = json.dumps(get_info(sid, pin))
        return render_template("index.html", data=info)

    # Temporarily print out any Exception for debugging
    except Exception as e:
        flash(e)
        return render_template("index.html")

# finalize configurations and run the app
if __name__ == "__main__":
    app.secret_key = 'development key'
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
