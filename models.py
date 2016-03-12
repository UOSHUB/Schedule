#!/usr/bin/env python

# Import needed libraries
from web import db


# Database schema class for student
class Student(db.Model):
    # Declare table name as students
    __tablename__ = 'students'

    # Declare student id as primary key (10 characters)
    sid = db.Column(db.String(10), primary_key=True)
    # Declare student name (15 characters)
    name = db.Column(db.String(15))

    # Initialize class with sid and name
    def __init__(self, sid=None, name=None):
        self.sid = sid
        self.name = name

    # Print class as < name, ID: sid>
    def __repr__(self):
        return "<" + self.name + ", ID: " + self.sid + ">"
