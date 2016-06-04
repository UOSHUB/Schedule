#!/usr/bin/env python

# Import needed libraries
import os


# App production configurations class
class Base(object):
    # Disable debugger
    DEBUG = False
    # Define a randomly generated secret key for flask session
    SECRET_KEY = os.environ["SECRET_KEY"]
    # Define database url according to the current environment
    SQLALCHEMY_DATABASE_URI = os.environ["DATABASE_URL"]
    # Disable SQLAlchemy track modifications to avoid warning
    SQLALCHEMY_TRACK_MODIFICATIONS = False


# App development configurations class
class Dev(Base):
    # Enable debugger
    DEBUG = True
