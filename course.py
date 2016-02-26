#!/usr/bin/env python


# A class to store course details
class Course:
    # Set max to lowest value it can be
    max_time = 0
    # Set max to highest value it can be
    min_time = 24 * 60

    # Initialize variables which are scrapped from the first page
    def __init__(self, name, section, crn, prof_name, prof_email, credit_hours):
        self.name = name
        self.section = section
        self.crn = crn
        self.prof_name = prof_name
        self.prof_email = prof_email
        self.credit_hours = credit_hours
        self.days = []
        self.time_string = []
        self.time = []
        self.location = []

    # Initialize other variables from the second page
    def set_others(self, days, time, location):
        self.days = days
        self.time_string = time
        self.location = location
        # Store minutes equivalent of time string
        self.time = [self.calculate_minutes(time[0]), self.calculate_minutes(time[1])]
        # Compare every course time to get min and max
        self.find_min(self.time[0])
        self.find_max(self.time[1])

    # Calculate minutes in time (eg. "1:30 pm" = 810 minute)
    @staticmethod
    def calculate_minutes(time):
        # Store "1:30" in clock and "pm" in period
        clock, period = time.split()
        # Store "1" in hours and "30" in minutes
        hours, minutes = clock.split(":")
        # Calculate minutes without considering period
        total_minutes = int(minutes) + int(hours) * 60
        # If it's "pm" then add 12 * 60
        if period == "pm" and hours != "12":
            total_minutes += 720
        # Return final result
        return total_minutes

    # Compare course time to get min
    @staticmethod
    def find_min(time):
        if time < Course.min_time:
            Course.min_time = time

    # Compare course time to get max
    @staticmethod
    def find_max(time):
        if time > Course.max_time:
            Course.max_time = time
