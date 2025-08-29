#!/usr/bin/env python3
""" create simple route """


from flask import Flask, request, render_template, g
import os
from flask_babel import Babel


app = Flask(__name__)

# Mock database
users = {
    1: {"name": "Balou", "locale": "fr", "timezone": "Europe/Paris"},
    2: {"name": "Beyonce", "locale": "en", "timezone": "US/Central"},
    3: {"name": "Spock", "locale": "kg", "timezone": "Vulcan"},
    4: {"name": "Teletubby", "locale": None, "timezone": "Europe/London"},
}

# Get user function
def get_user():
    """Retrieve a user dictionary based on the login_as parameter."""
    try:
        user_id = request.args.get("login_as")
        if user_id:
            user_id = int(user_id)
            return users.get(user_id)
    except Exception:
        return None
    return None

# Before each request
@app.before_request
def before_request():
    """Set g.user to the logged-in user, if any."""
    g.user = get_user()

# Route
@app.route('/')
def index():
    if g.user:
        return render_template("5-index.html", username=g.user["name"])
    else:
        return render_template("5-index.html", username=None)

if __name__ == "__main__":
    app.run()