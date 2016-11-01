#!/usr/bin/env python

# import needed libraries
from browser import br
import scrape


# Returns student's schedule
def schedule(semester):
    # Enter Student -> Registration section
    br.get("GenMenu?name=bmenu.P_RegMnu")
    # Enter Registration Term
    if not br.follow("bwskflib.P_SelDefTerm"):
        # Login if not logged then try again
        br.login()
        return schedule(semester)
    # Select the sent semester to be displayed
    br.select_form(nr=1)
    # Select semester if it was specified
    if semester:
        br.form["term_in"] = [semester]
    else:  # Otherwise store selected semester to be returned
        extras = br.form["term_in"][0]
        # If the selected term is "Year"
        if extras.endswith('5'):
            # Change it to a single semester
            extras = extras[:-1] + '0'
            # Select that semester to be scraped
            br.form["term_in"] = [extras]
    br.submit()
    # Enter Student Detail Schedule page
    br.follow("bwskfshd.P_CrseSchdDetl")
    # Scrape soup and store data instead of the empty {} then return it
    return dict(courses=scrape.detail_schedule(br.get_soup(), {}),
                **({} if semester else {"semester": extras}))


# Returns student's available semesters
def semesters():
    # Enter Student -> Registration section
    br.get("GenMenu?name=bmenu.P_RegMnu")
    # Enter Registration Term
    if not br.follow("bwskhreg.p_reg_hist"):
        # Login if not logged then try again
        br.login()
        return semesters()
    # Scrape and return semesters
    return [semester.string for semester in br.get_soup().find_all(class_="fieldOrangetextbold")]
