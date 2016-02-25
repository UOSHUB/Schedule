# A class to store course details
class Course:
    # Initialize variables which are scrapped from the first page
    def __init__(self, name, section, crn, prof_name, prof_email, credit_hours):
        self.name = name
        self.section = section
        self.crn = crn
        self.prof_name = prof_name
        self.prof_email = prof_email
        self.credit_hours = credit_hours
        self.days = []
        self.time = []
        self.location = []

    # Initialize other variables from the second page
    def set_others(self, days, time, location):
        self.days = days
        self.time = time
        self.location = location
