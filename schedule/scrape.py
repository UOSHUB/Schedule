#!/usr/bin/env python


# Scrape Student Detail Schedule from soup and return data in schedule
def detail_schedule(soup, schedule):
    # Loop through tables with datadisplaytable class
    for table in soup.find_all("table", class_="datadisplaytable"):
        # If it's the heading table
        if table.caption.string != "Scheduled Meeting Times":
            # Split table caption into three parts ["name", "key", "section"]
            name, key, section = table.caption.string.split(" - ")
            # Store dictionary key as course number after removing spaces
            key = key.replace(' ', '')
            # Store all table cells into cells array
            cells = table.find_all("td", class_="dddefault")
            # Store course info so far
            course = {"name": name, "section": section,
                      "crn": int(cells[1].string),
                      "ch": int(cells[5].string.strip()[0])}
        else:
            rows = table.find_all("tr")
            course.update(__extract_data(rows[1].find_all("td", class_="dddefault"), {"doctor": ["To Be Announced"] * 2}))
            if len(rows) > 2:
                course["lab"] = __extract_data(rows[2].find_all("td", class_="dddefault"), {})
            # If course key is new to schedule
            if schedule.get(key, None) is None:
                # Store the course with that key
                schedule[key] = course
            else:  # If the course already exists
                # Store it as a lab of the previous course
                schedule[key]["lab"] = course
    return schedule


#  Returns extracted data from cells as a dict
def __extract_data(cells, alt):
    return dict(
        # Upper case and split time string e.g. ["8:00 AM", "9:15 AM"]
        time = cells[1].string.upper().split(" - "),
        # Store class days in chars, e.g. ['M', 'W']
        days = list(cells[2].string),
        # Remove extra parts from place details, e.g. ["M10", "TH007"]
        place = __remove_extras(cells[3].string.split()),
        # If doctor info is valid store doctor name and email, e.g. ["Name", "Email"]
        **({"doctor": [cells[6].a.get("target"), cells[6].a.get("href")[7:]]} if cells[6].a else alt))


# Takes place details array e.g. ["M10:", "Engineering", "(Men)", "TH007"] and remove extra details
def __remove_extras(place):
    # From building only get first letter and the digits after it, and from room remove any duplicates
    return [place[0][0] + __get_digits(place[0][1:]), __get_digits(place[-1].split('-')[-1])]


# Takes a string and returns digits from it
def __get_digits(string):
    return ''.join([char for char in string if char.isdigit()])
