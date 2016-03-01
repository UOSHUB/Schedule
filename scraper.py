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
        self.br.open("https://uos.sharjah.ac.ae:9050/prod_enUS/twbkwbis.P_WWWLogin")
        # Fill up login form and submit
        self.br.select_form(nr=0)
        self.br["sid"] = sid
        self.br["PIN"] = pin
        self.br.submit()

    # Returns student's first name
    def grab_username(self):
        # Enter Personal Information section
        self.br.open("https://uos.sharjah.ac.ae:9050/prod_enUS/twbkwbis.P_GenMenu?name=bmenu.P_GenMnu")
        # Enter Directory Profile page
        self.br.open(self.br.click_link(url="/prod_enUS/bwgkoprf.P_ShowDiroItems"))
        # Use BeautifulSoup to extract info from raw html
        soup = BeautifulSoup(self.br.response().read(), "lxml")
        # Extract and return student name from soup
        return soup.find("td", class_="dedefault").string.split()[0]

    # Returns student's schedule
    def grab_schedule(self):
        # When the login session has expired, it need to login again
        try:
            # Enter Student -> Registration section
            self.br.open("https://uos.sharjah.ac.ae:9050/prod_enUS/twbkwbis.P_GenMenu?name=bmenu.P_RegMnu")
            # Enter Student Detail Schedule page
            self.br.open(self.br.click_link(url="/prod_enUS/bwskfshd.P_CrseSchdDetl"))
        except:
            return {"Error!": []}
        # When requesting the above link twice, the below form won't exist
        try:
            # Select current semester to be displayed
            self.br.select_form(nr=1)
            self.br.submit()
        except mechanize._mechanize.FormNotFoundError:
            pass
        # Use BeautifulSoup to extract info from raw html
        soup = BeautifulSoup(self.br.response().read(), "lxml")
        # Declare course schedule & key holders
        schedule = {}
        key = None
        # Loop through tables with datadisplaytable class
        for table in soup.find_all("table", class_="datadisplaytable"):
            # If it's the heading table
            if table.caption.string != "Scheduled Meeting Times":
                # Split table caption into three parts ['name', 'number', 'section']
                caption = table.caption.string.split(" - ")
                # Store array key as course number after removing spaces
                key = caption[1].replace(' ', '')
                # Store all table cells into row array
                row = table.find_all("td", class_="dddefault")
                # Store courses info as: schedule[number] = [name, section, CRN, prof_name, prof_email, credit_hours]
                schedule[key] = Course(caption[0], caption[2], row[1].string, row[3].a.get("target"),
                                       row[3].a.get("href").split(':')[1], int(row[5].string.split()[0][0]))
        # Return to Student -> Registration section
        self.br.open("https://uos.sharjah.ac.ae:9050/prod_enUS/twbkwbis.P_GenMenu?name=bmenu.P_RegMnu")
        # Enter Student Detail Schedule page
        self.br.open(self.br.click_link(url="/prod_enUS/uos_dispschd.P_DispCrseSchdSum"))
        # Use BeautifulSoup to extract info from raw html
        soup = BeautifulSoup(self.br.response().read(), "lxml")
        # Loop through TR tags of tables with datadisplaytable class
        for table in soup.find_all("table", class_="datadisplaytable")[1].find_all("tr"):
            # Exclude rows with TH tag or that doesn't have valign attribute
            if table.th is None and table.has_attr("valign"):
                # Store all table cells into row array
                row = table.find_all("td", class_="dddefault")
                # Try and fix if location info is divided into parts
                try:
                    # Split and store the location info
                    location = row[6].string.split()
                    # If building is repeated in room info
                    if location[0] in location[1]:
                        # Store only the actual room info
                        room = location[1].split('-')[1]
                    else:
                        # Otherwise store the room info as is
                        room = location[1]
                # If this fails for some reason
                except Exception:
                    # Store the whole location string as is
                    location = [row[6].string]
                    # Set where room should be that room info is within location
                    room = ""
                # Add more info to schedule as: [[days in chars], [start/end class time], [building, room]]
                schedule[row[0].string].set_other_details(row[1].string, list(row[4].string),
                                                          row[5].string.split(" - "), [location[0], room])
        # Return the complete student schedule
        return schedule
