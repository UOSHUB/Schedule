#!/usr/bin/env python

# import needed libraries
import os
from flask import Flask, render_template

# initialize with template folder in /
app = Flask(__name__, template_folder='')

# handle url requests
@app.route("/")
def index():
    return render_template("index.html")

# finalize configurations and run the app
if __name__ == "__main__":
    app.secret_key = 'development key'
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
