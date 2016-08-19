#!/usr/bin/env python

# import needed libraries
from mechanize import Browser as Mechanize, _http, LinkNotFoundError, ControlNotFoundError, URLError
from flask import session
from bs4 import BeautifulSoup
from functools import wraps


# login required decorator
def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if "sid" in session:
            return f(*args, **kwargs)
        else:
            return Exception
    return wrap


# A mechanize subclass with frequently use methods
class Browser(Mechanize):
    def __init__(self):
        # Instantiate superclass mechanize browser
        Mechanize.__init__(self)
        # Browser options
        self.set_handle_equiv(True)
        self.set_handle_redirect(True)
        self.set_handle_referer(True)
        self.set_handle_robots(False)
        self.set_handle_refresh(_http.HTTPRefreshProcessor(), max_time=1)

    # Gets UOS UDC link by providing sub url only
    def get(self, sub_url):
        try:
            self.open("https://uos.sharjah.ac.ae:9050/prod_enUS/twbkwbis.P_" + sub_url)
        except URLError:
            self.get(sub_url)

    # Follows a UOS UDC link by providing sub link only
    def follow(self, sub_link):
        try:
            self.follow_link(url="/prod_enUS/" + sub_link)
        except URLError:
            self.follow(sub_link)
        # Return false if link isn't found
        except LinkNotFoundError:
            return False
        # Otherwise return true
        else:
            return True

    # Returns BeautifulSoup object of current page
    def get_soup(self):
        return BeautifulSoup(self.response().read(), "lxml")

    # Login to official UOS UDC
    def login(self):
        # Open original UOS UDC login url
        self.get("WWWLogin")
        # Fill up login form
        self.select_form(nr=0)
        try:
            self["sid"] = session["sid"]
            self["PIN"] = session["pin"]
        except ControlNotFoundError:
            return self.login()
        # Submit and return login validation
        self.submit()
        return self.title() == "Main Menu"

    # Returns student's information
    def get_user_info(self):
        # Enter Student -> Student Account section
        self.get("GenMenu?name=bmenu.P_ARMnu")
        # Enter Statement of Fees page
        self.follow("UOS_PREFORMA.P_DispPreforma")
        # Extract and store info tables from soup
        tds = self.get_soup().find("div", class_="pagebodydiv").find_all("td", class_="dddefault", limit=7)
        name = tds[0].string.split()
        return {
            "name": ' '.join([name[0], name[-1]]),
            "major": tds[3].string,
            "ech": tds[6].string,
        }


# Instantiate a scraper object to be used
# in many different places (statically, kind of)
br = Browser()
