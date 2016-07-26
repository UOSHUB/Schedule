#!/usr/bin/env python

# import needed libraries
from scraper import scraper
from calculate import Calculate as Calc


class Storage:
    courses = {}
    semester = None


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
            # Store courses info
            course = {"name": caption[0], "section": caption[2], "crn": row[1].string, "prof_name": prof_name,
                      "prof_email": prof_email, "credit_hours": int(row[5].string.split()[0][0])}
            # If course key is new to schedule
            if schedule.get(key, None) is None:
                # Store the course with that key
                schedule[key] = course
            else:  # If the course already exists
                # Store it as a lab of the previous course
                schedule[key]["lab"] = course
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
            # Store course time interval
            time = [Calc.minutes_from_string(time) for time in row[5].string.split(" - ")]
            # Fix if location info is divided into parts or repeated
            location = split_location(row[6].string)
            # collect other details as: ([days in chars], [building, room], [start/end class time], length)
            data = {"days": list(row[4].string), "location": location, "time": time}
            # If key isn't empty
            if key != " ":
                # Add short name to data then add data to course
                data["short_name"] = row[1].string
                # If key isn't repeated, it's dedicated course, otherwise consider it a lab
                (schedule[key] if key != previous_key else schedule[key]["lab"]).update(data)
            else:  # If key is empty, consider course as a lab
                # Add prof name to data if it exists and not TBA
                if row[7].string not in ("To Be Announced", None):
                    data["prof_name"] = row[7].string
                # Assign collected data as a lab for the previous course
                schedule[previous_key]["lab"] = data
            # Check if course timing is min or max
            Calc.find_min(time[0])
            Calc.find_max(time[1])
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
