from flask import Blueprint, render_template, flash, request, redirect, url_for, session

schedule = Blueprint("schedule", __name__, template_folder="static", static_folder="static")


@schedule.route('/')
def index():
    return render_template("schedule.html")
