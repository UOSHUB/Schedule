#!/usr/bin/env python

# import needed libraries
from calculate import Calculate


# A class to store course details
class Course:
    # Initialize variables which are scraped from the first page
    def __init__(self, name, section, crn, prof_name, prof_email, credit_hours):
        self.name = name
        self.section = section
        self.crn = crn
        self.prof_name = prof_name
        self.prof_email = prof_email
        self.credit_hours = credit_hours
        # Initializing variables to be filled later
        self.short_name = None
        # Days letters eg. ["U", "T", "R"]
        self.days = []
        # Non-formatted time eg. ["9:30 am", "10:45 am"]
        self.time_string = []
        # Actual time in minutes eg. [570, 645]
        self.time = []
        # Building, Room of class eg. ["M10", "109"]
        self.location = []
        # Possible course lab
        self.lab = None

    # Initialize other variables from the second page
    def set_other_details(self, days, time, location, short_name=None):
        if short_name is not None:
            self.short_name = short_name
        self.days = days
        self.time_string = time
        self.location = location
        # Store minutes equivalent of time string
        self.time = [Calculate.minutes_from_string(time[0]), Calculate.minutes_from_string(time[1])]
        # Compare every course time to get min and max
        Calculate.find_min(self.time[0])
        Calculate.find_max(self.time[1])

    # If course has key-less lab, initialize lab course with same info as parent
    def set_course_lab(self, prof_name):
        # if professor's name is provided, use it instead
        if prof_name == "To Be Announced" or prof_name is None:
            prof_name = self.prof_name
        # Initialize a course lab with parent course info
        self.lab = Course(self.name + " Lab", self.section, self.crn, prof_name, self.prof_email, "")
        # Also use short course name from parent course
        self.lab.short_name = self.short_name + " Lab"
        return self.lab

    # Returns course length in hours
    def length(self):
        return Calculate.hours_between_minutes(self.time[1], self.time[0])

    # Returns left, top positions for course occurrences
    def coordinates(self, column_width, row_height, left_shift, top_shift):
        points = []
        for day in self.days:  # Calculate [x, y] coordinates and add them to points
            points.extend([[Calculate.class_x_coordinate(left_shift, day, column_width),
                            Calculate.class_y_coordinate(top_shift, row_height, self.time[0])]])
        return points