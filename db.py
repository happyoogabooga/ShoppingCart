# db.py
import psycopg
from flask import g, current_app

def get_db():
    """Opens a new database connection if there isn't one for the current request."""
    if 'db' not in g:
        # Connect using your PostgreSQL connection string
        g.db = psycopg.connect(current_app.config['DATABASE_URL'])
    return g.db

def close_db(e=None):
    """Closes the database connection at the end of the request."""
    db = g.pop('db', None)
    if db is not None:
        db.close()

def init_app(app):
    """Register database teardown with the Flask app."""
    app.teardown_appcontext(close_db)