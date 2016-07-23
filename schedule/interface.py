#!/usr/bin/env python

# import needed libraries
from .scrape import get_schedule
from calculate import Calculate


# A class for Interfacing between courses and data scraper,
# also for Interfacing between jinja2 and python
class Interface:
    # Initialize basic class variables
    def __init__(self):
        self.schedule = {}
        self.semester = None

    # Empty schedule as student logs out
    def empty_schedule(self):
        self.schedule.clear()

    # Gets and returns student schedule
    def get_schedule(self, semester=None):
        # Only fill schedule if it's empty or selected a different semester
        if self.schedule == {} or "Error!" in self.schedule or self.semester != semester:
            # When the login session has expired, it need to login again
            Calculate.reset_min_max()
            try:
                self.schedule = get_schedule(semester)
            except:
                self.schedule = {"Error!": []}
            else:
                self.semester = semester
        return self.schedule

    # Get hour length in schedule
    @staticmethod
    def get_hour_length(top_shift):
        return Calculate.hour_length(top_shift)

    # Get hours array for laying out hour lines
    @staticmethod
    def get_hours_array():
        return Calculate.hour_count_array()

    # Get whole hours labels for left header of schedule
    @staticmethod
    def get_hours_labels():
        return Calculate.hours_labels()

    # Get weekdays dates that'll be displayed
    @staticmethod
    def get_dates():
        return Calculate.dates()

interface = Interface()
