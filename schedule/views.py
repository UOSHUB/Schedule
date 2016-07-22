#!/usr/bin/env python

# import needed libraries
from flask import Blueprint, render_template
from .interface import interface
from scraper import login_required

# Instantiate schedule blueprint
schedule = Blueprint("schedule", __name__, template_folder="static", static_folder="static")


@schedule.route('/')
@login_required
def index():
    return render_template("schedule.html", interface=interface)
