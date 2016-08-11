#!/usr/bin/env python

# import needed libraries
import get
from flask import Blueprint, render_template, request, json
from browser import login_required

# Instantiate schedule blueprint
schedule = Blueprint("schedule", __name__, template_folder="static", static_folder="static")


# Handle /schedule route
@schedule.route('/')
@login_required
def index():
    return render_template("schedule.html")


# Handle client side requests to get schedule
@schedule.route('/get_schedule', methods=["POST"])
@login_required
def get_schedule():
    # Return jsonified schedule dict of the requested semester
    return json.dumps(get.schedule(request.data))


# Handle client side requests to get available semesters
@schedule.route('/get_semesters', methods=["POST"])
@login_required
def get_semesters():
    # Return jsonified dict of available semesters
    return json.dumps(get.semesters())
