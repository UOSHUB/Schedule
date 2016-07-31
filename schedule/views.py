#!/usr/bin/env python

# import needed libraries
from flask import Blueprint, render_template, request, json
from scraper import login_required
from getter import get_schedule

# Instantiate schedule blueprint
schedule = Blueprint("schedule", __name__, template_folder="static", static_folder="static")


@schedule.route('/')
@login_required
def index():
    return render_template("schedule.html")


@schedule.route('/getter', methods=["POST"])
@login_required
def getter():
    return json.dumps(get_schedule(request.data))
