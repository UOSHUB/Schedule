#!/usr/bin/env python

# import needed libraries
from __future__ import division
from datetime import date, timedelta


# A static class that'll host most of calculation methods
class Calculate:
    # init max to lowest value it can be
    _max_time = 0
    # init min to highest value it can be
    _min_time = 24 * 60

    ''' Beginning of Methods used in views.getter() response '''
    # Reinitialize min and max time
    @classmethod
    def reset_min_max(cls):
        cls._max_time = 0
        cls._min_time = 24 * 60

    # Returns week earliest course time with 30 minutes space below it
    @classmethod
    def week_bottom(cls):
        return cls._min_time - 30

    # Returns week latest course time with 30 minutes space above it
    @classmethod
    def week_top(cls):
        return cls._max_time + 30

    # Returns number of hours in schedule
    @classmethod
    def hour_count(cls):
        return (cls.week_top() - cls.week_bottom()) / 60

    # Returns hour by hour representing count array for the schedule
    @classmethod
    def hour_count_array(cls):
        count_array = []
        # sub_hour is the fractions before the first whole hour
        sub_hour = cls.week_bottom() % 60 / 60
        # First bit is either a fraction or a whole hour
        first_bit = sub_hour if sub_hour > 0 else 1
        # Add first bit to the array
        count_array.append(first_bit)
        # Add the remaining hours cumulatively
        for i in range(int(cls.hour_count() - first_bit)):
            count_array.append(1 + count_array[-1])
        return count_array

    # Returns length of an hour in schedule
    @classmethod
    def hour_length(cls, top_shift):
        return (100 - top_shift) / cls.hour_count()

    # Returns whole hours string labels in the schedule
    @classmethod
    def hours_labels(cls):
        labels = []
        # Adding (60 - cls.week_bottom() % 60) will roundup week bottom hour
        start_hour = (cls.week_bottom() + 60 - cls.week_bottom() % 60) // 60
        # It's morning if hour < 12, otherwise it's noon
        period = "AM" if start_hour < 12 else "PM"
        # Loop through hours between week top and bottom
        for hour in range(start_hour, 1 + (cls.week_top() - cls.week_top() % 60) // 60):
            # When it reaches 12, switch time period
            if hour == 12:
                period = "PM" if period != "PM" else "AM"
            # Otherwise, calculate hour e.g. (13 -> 1)
            else:
                hour %= 12
            # Add hour and period to array
            labels.append([hour, period])
        return labels

    # Returns today as int: (Sun = 0, Mon = 1 .... Sat = 6)
    @staticmethod
    def _today_as_int():
        # Originally it is: (Sun = 7, Mon = 1 .... Sat = 6)
        day_int = date.isoweekday(date.today())
        # Return 0 if it's 7 (Sun), otherwise return it a it is
        return 0 if day_int == 7 else day_int

    # Returns an array of weekday dates: ["MM/DD"]
    @classmethod
    def dates(cls):
        today_int = cls._today_as_int()
        today_date = date.today()
        # If it's a weekday, get current week
        if today_int < 5:
            # A day is defined by shifting week according to today's int
            def day(number): return today_date - timedelta(today_int - number)
        # If it's the weekend, get next week
        else:
            # A day is defined by shifting week according to today's int and a week after
            def day(number): return today_date + timedelta(7 - (today_int - number))
        # Loop five times a return formatted days array
        return [day(count).strftime("%-m/%-d") for count in range(5)]
    ''' End of Methods used in views.getter() response '''

    ''' Beginning of Methods used in getter.get_schedule() '''
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

    # Compare course time to get min
    @classmethod
    def find_min(cls, time):
        if time < cls._min_time:
            cls._min_time = time

    # Compare course time to get max
    @classmethod
    def find_max(cls, time):
        if time > cls._max_time:
            cls._max_time = time
    ''' End of Methods used in getter.get_schedule() '''
