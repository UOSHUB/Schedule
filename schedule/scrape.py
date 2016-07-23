#!/usr/bin/env python

# import needed libraries
from scraper import scraper
from course import Course


# Returns student's schedule
def get_schedule(semester):
    # Enter Student -> Registration section
    scraper.get("GenMenu?name=bmenu.P_RegMnu")
    # Enter Registration Term
    if not scraper.follow("bwskflib.P_SelDefTerm"):
        # Login if not logged then try again
        scraper.login()
        return get_schedule(semester)
    # Select the sent semester to be displayed
    scraper.select_form(nr=1)
    # Select semester if it was specified
    if semester:
        scraper.form["term_in"] = [semester]
    scraper.submit()
    # Enter Student Detail Schedule page
    scraper.follow("bwskfshd.P_CrseSchdDetl")
    # Scrape soup and store data instead of the empty {}
    schedule = scrape_detail_schedule(scraper.get_soup(), {})
    # Return to Student -> Registration section
    scraper.get("GenMenu?name=bmenu.P_RegMnu")
    # Enter Student Summarized Schedule page
    scraper.follow("uos_dispschd.P_DispCrseSchdSum")
    # Scrape soup and store data on top of schedule then return it
    return scrape_summarized_schedule(scraper.get_soup(), schedule)


# Scrape Student Detail Schedule from soup and return data in schedule
def scrape_detail_schedule(soup, schedule):
    # Loop through tables with datadisplaytable class
    for table in soup.find_all("table", class_="datadisplaytable"):
        # If it's the heading table
        if table.caption.string != "Scheduled Meeting Times":
            # Split table caption into three parts ["name", "number", "section"]
            caption = table.caption.string.split(" - ")
            # Store dictionary key as course number after removing spaces
            key = caption[1].replace(' ', '')
            # Store all table cells into row array
            row = table.find_all("td", class_="dddefault")
            # Get professor info and handle TBA
            prof = row[3].a
            if prof:
                prof_name = prof.get("target")
                prof_email = prof.get("href").split(':')[1]
            else:
                prof_name = prof_email = "To Be Announced"
            # Store courses info: Course(name, section, CRN, prof_name, prof_email, credit_hours)
            course = Course(caption[0], caption[2], row[1].string, prof_name,
                            prof_email, int(row[5].string.split()[0][0]))
            # If course key is new to schedule
            if schedule.get(key, None) is None:
                # Store the course with that key
                schedule[key] = course
            else:  # If the course already exists
                # Store it as a lab of the previous course
                schedule[key].lab = course
    return schedule


# Scrape Student Summarized Schedule from soup and store complete data in schedule
def scrape_summarized_schedule(soup, schedule):
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
            location = split_location(row[6].string)
            # If key isn't empty
            if key != " ":
                # If key isn't repeated, it's dedicated course, otherwise consider it a lab
                course = schedule[key] if key != previous_key else schedule[key].lab
                # set other details as: ([days in chars], [start/end class time], [building, room], short name)
                course.set_other_details(list(row[4].string), row[5].string.split(" - "), location, row[1].string)
            else:  # If key is empty, consider course as a lab
                # Add lab details as: set_course_lab([days in chars], [start/end class time], [building, room])
                schedule[previous_key].set_course_lab(row[7].string).set_other_details(
                                                      list(row[4].string), row[5].string.split(" - "), location)
            # Store course key for possible lab addition case
            previous_key = key
    return schedule


# Split location info and fix if it's repeated
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
