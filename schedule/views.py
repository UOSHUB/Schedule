#!/usr/bin/env python

# import needed libraries
from flask import Blueprint, render_template
from scraper import login_required
from .interface import interface

# Instantiate schedule blueprint
schedule = Blueprint("schedule", __name__, template_folder="static", static_folder="static")


@schedule.route('/')
@login_required
def index():
    return render_template("schedule.html", interface=interface)
