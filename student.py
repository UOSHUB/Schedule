#!/usr/bin/env python

# import needed libraries
from __future__ import division
from scraper import Scrape
from course import Course


# A class for Student users
class Student:
    # Initialize basic class variables
    def __init__(self):
        self.scrape = Scrape()
        self.schedule = {}
        self.name = None

    # Reinitialize as new = destroy
    def reinitialize(self):
        self.scrape = Scrape()
        self.schedule = {}
        self.name = None

    # Verify login with provided credentials
    def verify(self, sid, pin):
        try:
            self.scrape.login(sid, pin)
            return self.scrape.br.title() == "Main Menu"
        except:
            return False

    # Gets and returns student name
    def get_name(self):
        self.name = self.scrape.grab_username()
        return self.name

    # Gets and returns student schedule
    def get_schedule(self):
        # Only fill schedule if it's empty
        if self.schedule == {}:
            self.schedule = self.scrape.grab_schedule()
        return self.schedule

    # Get week earliest course time with 30 minutes space below it
    def week_bottom(self):
        return Course.min_time - 30

    # Get week latest course time with 30 minutes space above it
    def week_top(self):
        return Course.max_time + 30

    # Get number of hours in schedule
    def hour_count(self):
        return (self.week_top() - self.week_bottom()) / 60

    # Get hour by hour representing count array
    def hour_count_array(self):
        count_array = []
        count = self.hour_count()
        # sub_hour is the fractions before the first whole hour
        sub_hour = self.week_bottom() % 60 / 60
        # If there are fractions
        if sub_hour > 0:
            # Add them to the array
            count_array.extend([sub_hour])
            # Subtract them from hours count
            count -= sub_hour
        # For every hour put one in the array
        while count > 0:
            if count >= 1:
                count_array.extend([1])
            else:
                # If fractions are left add the fraction
                count_array.extend([count])
            count -= 1
        return count_array

    # Get length of an hour in schedule
    def hour_length(self):
        return 100 / self.hour_count()
