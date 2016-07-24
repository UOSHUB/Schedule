#!/usr/bin/env python

# import needed libraries
from flask import Blueprint, render_template, request, json
from scraper import login_required
from calculate import Calculate
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
        Storage.courses = {}
        Calculate.reset_min_max()
        try:
            [Storage.courses.update({key: course.dictionary()}) for key, course in get_schedule(request.data).items()]
        except Exception as e:
            print(e)
        else:
            Storage.semester = request.data
    return json.dumps({
        "courses": Storage.courses,
        "height": Calculate.hour_length(5),
        "labels": Calculate.hours_labels(),
        "fractions": Calculate.hour_count_array(),
        "dates": Calculate.dates()
    })
