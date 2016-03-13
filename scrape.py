#!/usr/bin/env python

# import needed libraries
import mechanize
from bs4 import BeautifulSoup
from course import Course


# A class to manage information flow
class Scrape:
    def __init__(self):
        # Instantiate an empty browser holder
        self.br = None
        # Store root url in shortcut variable as it's going to be use a lot
        self.root_url = "https://uos.sharjah.ac.ae:9050/prod_enUS"

    def initialize(self):
        # Instantiate mechanize browser
        self.br = mechanize.Browser()
        # Browser options
        self.br.set_handle_equiv(True)
        self.br.set_handle_redirect(True)
        self.br.set_handle_referer(True)
        self.br.set_handle_robots(False)
        self.br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)

    # Login to official UOS UDC
    def login(self, sid, pin):
        self.initialize()
        # Open original UOS UDC login url
        self.br.open(self.root_url + "/twbkwbis.P_WWWLogin")
        # Fill up login form and submit
        self.br.select_form(nr=0)
        self.br["sid"] = sid
        self.br["PIN"] = pin
        self.br.submit()

    # Returns student's first name
    def grab_username(self):
        # Enter Personal Information section
        self.br.open(self.root_url + "/twbkwbis.P_GenMenu?name=bmenu.P_GenMnu")
        # Enter Directory Profile page
        self.br.follow_link(url="/prod_enUS/bwgkoprf.P_ShowDiroItems")
        # Use BeautifulSoup to extract info from raw html
        soup = BeautifulSoup(self.br.response().read(), "lxml")
        # Extract and return student name from soup
        return soup.find("td", class_="dedefault").string.split()[0]

    # Returns student's schedule
    def grab_schedule(self, semester):
        # Enter Student -> Registration section
        self.br.open(self.root_url + "/twbkwbis.P_GenMenu?name=bmenu.P_RegMnu")
        # Enter Registration Term
        self.br.follow_link(url="/prod_enUS/bwskflib.P_SelDefTerm")
        # Select the sent semester to be displayed
        self.br.select_form(nr=1)
        self.br.form["term_in"] = [semester]
        self.br.submit()
        # Enter Student Detail Schedule page
        self.br.follow_link(url="/prod_enUS/bwskfshd.P_CrseSchdDetl")
        # Send raw Detail Schedule data soup to be scraped and stored instead of the empty {}
        schedule = self.scrape_detail_schedule(BeautifulSoup(self.br.response().read(), "lxml"), {})
        # Return to Student -> Registration section
        self.br.open(self.root_url + "/twbkwbis.P_GenMenu?name=bmenu.P_RegMnu")
        # Enter Student Summarized Schedule page
        self.br.follow_link(url="/prod_enUS/uos_dispschd.P_DispCrseSchdSum")
        # Send raw Summarized Schedule data soup to be scraped and stored on top of schedule then return it
        return self.scrape_summarized_schedule(BeautifulSoup(self.br.response().read(), "lxml"), schedule)

    # Scrape Student Detail Schedule from soup and return data in schedule
    @staticmethod
    def scrape_detail_schedule(soup, schedule):
        # Loop through tables with datadisplaytable class
        for table in soup.find_all("table", class_="datadisplaytable"):
            # If it's the heading table
            if table.caption.string != "Scheduled Meeting Times":
                # Split table caption into three parts ['name', 'number', 'section']
                caption = table.caption.string.split(" - ")
                # Store dictionary key as course number after removing spaces
                key = caption[1].replace(' ', '')
                # Store all table cells into row array
                row = table.find_all("td", class_="dddefault")
                # Store courses info: Course(name, section, CRN, prof_name, prof_email, credit_hours)
                course = Course(caption[0], caption[2], row[1].string, row[3].a.get("target"),
                                row[3].a.get("href").split(':')[1], int(row[5].string.split()[0][0]))
                # If course key is new to schedule
                if schedule.get(key, None) is None:
                    # Store the course with that key
                    schedule[key] = course
                else:  # If the course already exists
                    # Store it as a lab of the previous course
                    schedule[key].lab = course
        return schedule

    # Scrape Student Summarized Schedule from soup and store complete data in schedule
    @classmethod
    def scrape_summarized_schedule(cls, soup, schedule):
        # Declare previous course key holder
        previous_key = None
        # Loop through TR tags of tables with datadisplaytable class
        for table in soup.find_all("table", class_="datadisplaytable")[1].find_all("tr"):
            # Exclude rows with TH tag or that doesn't have valign attribute
            if table.th is None and table.has_attr("valign"):
                # Store all table cells into row array
                row = table.find_all("td", class_="dddefault")
                # Store dictionary key as course number
                key = row[0].string
                # Fix if location info is divided into parts or repeated
                location = cls.split_location(row[6].string)
                # If key isn't empty
                if key != " ":
                    # If key isn't repeated, it's dedicated course, otherwise consider it a lab
                    course = schedule[key] if key != previous_key else schedule[key].lab
                    # set other details as: ([days in chars], [start/end class time], [building, room], short name)
                    course.set_other_details(list(row[4].string), row[5].string.split(" - "), location, row[1].string)
                else:  # If key is empty, consider course as a lab
                    # Add lab details as: set_course_lab([days in chars], [start/end class time], [building, room])
                    schedule[previous_key].set_course_lab(row[7].string).set_other_details(list(row[4].string),
                                                                               row[5].string.split(" - "), location)
                # Store course key for possible lab addition case
                previous_key = key
        return schedule

    # Split location info and fix if it's repeated
    @staticmethod
    def split_location(raw_location):
        try:
            # Split and store the raw location info
            location = raw_location.split()
            # If building info is repeated in room info
            if location[0] in location[1]:
                # Remove repetition and return split location
                return [location[0], location[1].split('-')[1]]
            else:
                # Otherwise return split location info as is
                return location
        # If this fails for some reason
        except:
            # Return location without splitting
            return [raw_location, ""]
