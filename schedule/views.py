#!/usr/bin/env python

# import needed libraries
from flask import Blueprint, render_template, request, json
from scraper import login_required
from getter import get_schedule, Storage

# Instantiate schedule blueprint
schedule = Blueprint("schedule", __name__, template_folder="static", static_folder="static")


@schedule.route('/')
@login_required
def index():
    return render_template("schedule.html")


@schedule.route('/getter', methods=["POST"])
@login_required
def getter():
    # Only fill schedule if it's empty or selected a different semester
    if Storage.courses == {} or Storage.semester != request.data:
        # When the login session has expired, it need to login again
        try:
            Storage.courses = get_schedule(request.data)
        except Exception:
            Storage.courses = {}
            return Exception
        else:
            Storage.semester = request.data
    return json.dumps(Storage.courses)
