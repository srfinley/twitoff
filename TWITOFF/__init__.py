""" Entry point for twitoff flask app"""

from .app import create_app

APP = create_app()

# run in terminal with FLASK_APP=TWITOFF:APP flask run 