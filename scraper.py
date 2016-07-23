#!/usr/bin/env python

# import needed libraries
from mechanize import Browser, _http, LinkNotFoundError
from flask import session, flash, url_for, redirect
from bs4 import BeautifulSoup
from functools import wraps


# login required decorator
def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if "name" in session:
            return f(*args, **kwargs)
        else:
            flash("You need to login first!")
            return redirect(url_for("index"))
    return wrap


class Scraper(Browser):
    def __init__(self):
        # Instantiate superclass mechanize browser
        Browser.__init__(self)
        # Browser options
        self.set_handle_equiv(True)
        self.set_handle_redirect(True)
        self.set_handle_referer(True)
        self.set_handle_robots(False)
        self.set_handle_refresh(_http.HTTPRefreshProcessor(), max_time=1)

    def get(self, sub_url):
        self.open("https://uos.sharjah.ac.ae:9050/prod_enUS/twbkwbis.P_" + sub_url)

    def follow(self, sub_link):
        try:
            self.follow_link(url="/prod_enUS/" + sub_link)
        except LinkNotFoundError:
            return False
        return True

    def get_soup(self):
        return BeautifulSoup(self.response().read(), "lxml")

    # Login to official UOS UDC
    def login(self):
        # Open original UOS UDC login url
        self.get("WWWLogin")
        # Fill up login form
        self.select_form(nr=0)
        self["sid"] = session["sid"]
        self["PIN"] = session["pin"]
        # Submit and return login validation
        self.submit()
        return self.title() == "Main Menu"

    # Returns student's first name
    def get_username(self):
        # Enter Personal Information section
        self.get("GenMenu?name=bmenu.P_GenMnu")
        # Enter Directory Profile page
        self.follow("bwgkoprf.P_ShowDiroItems")
        # Extract and return student name from soup
        return self.get_soup().find("td", class_="dedefault").string.split()[0]

scraper = Scraper()