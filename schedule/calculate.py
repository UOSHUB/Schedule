#!/usr/bin/env python

# import needed libraries
from __future__ import division
from datetime import date, timedelta


# A static class that'll host most of calculation methods
class Calculate:
    # init max to lowest value it can be
    max_time = 0
    # init min to highest value it can be
    min_time = 24 * 60

    ''' Beginning of Methods used for Interface class '''
    # Reinitialize min and max time
    @classmethod
    def reset_min_max(cls):
        cls.max_time = 0
        cls.min_time = 24 * 60

    # Returns week earliest course time with 30 minutes space below it
    @classmethod
    def week_bottom(cls):
        return cls.min_time - 30

    # Returns week latest course time with 30 minutes space above it
    @classmethod
    def week_top(cls):
        return cls.max_time + 30

    # Returns number of hours in schedule
    @classmethod
    def hour_count(cls):
        return (cls.week_top() - cls.week_bottom()) / 60

    # Returns hour by hour representing count array for the schedule
    @classmethod
    def hour_count_array(cls):
        count_array = []
        count = cls.hour_count()
        # sub_hour is the fractions before the first whole hour
        sub_hour = cls.week_bottom() % 60 / 60
        # If there are fractions
        if sub_hour > 0:
            # Add them to the array
            count_array.extend([sub_hour])
            # Subtract them from hours count
            count -= sub_hour
        # For every whole hour put one in the array
        while count >= 1:
            count_array.extend([1])
            count -= 1
        return count_array

    # Returns length of an hour in schedule
    @classmethod
    def hour_length(cls, top_shift):
        return (100 - top_shift) / cls.hour_count()

    # Returns whole hours string labels in the schedule
    @classmethod
    def hours_labels(cls):
        # Adding (60 - cls.week_bottom() % 60) will roundup week bottom hour
        hour = int((cls.week_bottom() + 60 - cls.week_bottom() % 60) / 60)
        # The rest of the method is messed up, I'll optimize it later ;)
        if hour < 12:
            am_pm = "AM"
        else:
            am_pm = "PM"
        labels = []
        while hour <= int((cls.week_top() - cls.week_top() % 60) / 60):
            if hour == 12:
                if am_pm == "PM":
                    am_pm = "AM"
                else:
                    am_pm = "PM"
                labels.extend([[str(12), am_pm]])
            else:
                labels.extend([[str(hour % 12), am_pm]])
            hour += 1
        return labels

    # Returns today as int: (Sun = 0, Mon = 1 .... Sat = 6)
    @staticmethod
    def today_as_int():
        # Originally it is: (Sun = 7, Mon = 1 .... Sat = 6)
        day_int = date.isoweekday(date.today())
        # To sort it my way, change Sun from 7 to 0
        if day_int == 7:
            return 0
        # Otherwise it's the correct index
        return day_int

    # Returns an array of weekday dates: ["MM/DD"]
    @classmethod
    def dates(cls):
        dates = []
        today_int = cls.today_as_int()
        # Check if it's weekday or weekend
        if today_int < 5:
            # If it's a weekday, get current week
            for count in range(0, 5):
                # Add days by shifting week according to today's int
                dates.extend([(date.today() - timedelta(today_int - count)).strftime("%-m/%-d")])
        else:
            # If it's the weekend, get next week
            for count in range(0, 5):
                # Add days by shifting week according to today's int and a week after
                dates.extend([(date.today() + timedelta(7 - (today_int - count))).strftime("%-m/%-d")])
        return dates
    ''' End of Methods used for Interface class '''

    ''' Beginning of Methods used for Course class '''
    # Calculate minutes in time (eg. "1:30 pm" = 810 minute)
    @staticmethod
    def minutes_from_string(time):
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

    # Calculates how many hour between given start/end minutes
    @staticmethod
    def hours_between_minutes(start_minute, end_minute):
        return (start_minute - end_minute) / 60

    # Switch alternative
    @staticmethod
    def switch(day):
        # Return day column number according to day's first letter
        return {"U": 0, "M": 1, "T": 2, "W": 3, "R": 4, "F": 5, "S": 6}[day]

    # Returns left (x) coordinate of the class box
    @classmethod
    def class_x_coordinate(cls, left_shift, day, column_width):
        # left: left shift + day column number * column width,
        return left_shift + cls.switch(day) * column_width

    # Returns top (y) coordinate of the class box
    @classmethod
    def class_y_coordinate(cls, top_shift, row_height, class_start_time):
        # top: top shift + row height * (course start time - schedule beginning) in hours
        return top_shift + row_height * (class_start_time - cls.min_time + 30) / 60

    # Compare course time to get min
    @classmethod
    def find_min(cls, time):
        if time < cls.min_time:
            cls.min_time = time

    # Compare course time to get max
    @classmethod
    def find_max(cls, time):
        if time > cls.max_time:
            cls.max_time = time
    ''' End of Methods used for Course class '''
