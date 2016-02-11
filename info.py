#!/usr/bin/env python

import mechanize, cookielib
from bs4 import BeautifulSoup

br = None

def init_browser():
    # Instantiate browser
    br = mechanize.Browser()
    # Enable cookie support for urllib2
    br.set_cookiejar(cookielib.LWPCookieJar())
    # Browser options
    br.set_handle_equiv(True)
    br.set_handle_gzip(True)
    br.set_handle_redirect(True)
    br.set_handle_referer(True)
    br.set_handle_robots(False)
    br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time = 1)
    # Return browser object
    return br


def login(sid, pin):
    # Initialize browser
    br = init_browser()
    # Open original UOS UDC url
    br.open("https://uos.sharjah.ac.ae:9050/prod_enUS/twbkwbis.P_WWWLogin")
    # Fill up login form and submit
    br.select_form(nr=0)
    br["sid"] = sid
    br["PIN"] = pin
    br.submit()
    # Return browser object
    return br


def grab_username():
    # Enter Personal Information section
    br.open("https://uos.sharjah.ac.ae:9050/prod_enUS/twbkwbis.P_GenMenu?name=bmenu.P_GenMnu")
    # Get raw html from Directory Profile
    page = None
    br.follow_link()
    for link in br.links():
        if link.url == "/prod_enUS/bwgkoprf.P_ShowDiroItems":
            page = br.follow_link(link)
    # Extract and return Username from raw html
    soup = BeautifulSoup(page.read(), "lxml")
    return soup.find("td", class_="dedefault").string


