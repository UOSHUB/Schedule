#!/usr/bin/env python

# Import needed libraries
import os, warnings
from flask import Flask
from schedule.views import schedule
from flask_htmlmin import HTMLMIN
from flask_sqlalchemy import SQLAlchemy
from flask.exthook import ExtDeprecationWarning
warnings.simplefilter('ignore', ExtDeprecationWarning)
from flask_assets import Environment, Bundle

# Initialize with template folder in ./static
app = Flask(__name__, template_folder="static")
# Register schedule blueprint
app.register_blueprint(schedule, url_prefix="/schedule")
# Configure app from object of current environment
app.config.from_object(os.environ["APP_SETTINGS"])
# Initialize SQLAlchemy database
db = SQLAlchemy(app)
# Link app with html minifyer
HTMLMIN(app)
# Initialize flask assets environment
assets = Environment(app)

# A function to register bundles to flask assets environment
def register_bundle(lang, *names, **options):
    # Output name is eather sent or by default it's the first name
    output = options.pop("output", names[0])
    # File path is ether sent or by default it's the root path
    path = options.pop("path", '')
    # Register bundle to assets with the name "output.lang"
    assets.register("{}.{}".format(output, lang), Bundle(
        # Bundle files that are sent as *names after formatting their names
        *["{0}{1}/{2}.{1}".format(path, lang, name) for name in names],
        # Set bundle filter to specified language and set output file name
        filters="{}min".format(lang), output="{}min/{}.{}".format(path, output, lang)
    ))

# Nicely register bundles of css files
register_bundle("css", "font-awesome", "materialize", "general", output="common")
register_bundle("css", "schedule", path="schedule/")
register_bundle("css", "dashboard")
register_bundle("css", "layout")

# Same with js files
register_bundle("js", "jquery", "materialize", "angular", "angular-local-storage", output="common")
register_bundle("js", "app", "scripts", "process", output="schedule", path="schedule/")
register_bundle("js", "ganalytics")
register_bundle("js", "layout")

# Finalize configurations and run the app
if __name__ == "__main__":
    from views import *
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
