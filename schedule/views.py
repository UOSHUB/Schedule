#!/usr/bin/env python

# import needed libraries
import get
from flask import Blueprint, render_template, request, json
from browser import login_required

# Instantiate schedule blueprint
schedule = Blueprint("schedule", __name__, template_folder="static", static_folder="static")


@schedule.route('/')
@login_required
def index():
    return render_template("schedule.html")


@schedule.route('/get_schedule', methods=["POST"])
@login_required
def get_schedule():
    return json.dumps(get.schedule(request.data))


@schedule.route('/get_semesters', methods=["POST"])
@login_required
def get_semesters():
    return json.dumps(get.semesters())
