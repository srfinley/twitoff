from flask import Flask
from .models import DB

# app factory

def create_app():
    app = Flask(__name__)

    # add config
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'

    # tell database about app
    DB.init_app(app)

    @app.route('/')
    def root():
        return 'Welcome to Twitoff'

    return app