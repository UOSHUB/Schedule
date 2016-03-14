#!/usr/bin/env python

# import needed libraries
from scrape import Scrape
from calculate import Calculate


# A class for Interfacing between courses and data scraper,
# also for Interfacing between jinja2 and python
class Interface:
    # Initialize basic class variables
    def __init__(self):
        self.scrape = Scrape()
        self.schedule = {}
        self.semester = None

    # Empty schedule as student logs out
    def empty_schedule(self):
        self.schedule = {}

    # Verify login with provided credentials
    def verify_login(self):
        try:
            self.scrape.login()
            return self.scrape.br.title() == "Main Menu"
        except:
            return False

    # Gets and returns student name
    def get_name(self):
        return self.scrape.grab_username()

    # Gets and returns student schedule
    def get_schedule(self, semester):
        # Only fill schedule if it's empty or selected a different semester
        if self.schedule == {} or self.semester != semester:
            # When the login session has expired, it need to login again
            try:
                Calculate.reset_min_max()
                self.schedule = self.scrape.grab_schedule(semester)
                self.semester = semester
            except:
                self.schedule = {"Error!": []}
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
