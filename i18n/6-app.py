#!/usr/bin/env python3
""" create simple route """


from flask import Flask, request, render_template, g
import os
from flask_babel import Babel, _


app = Flask(__name__)

# Supported languages + defaults
app.config["LANGUAGES"] = ["en", "fr"]
app.config["BABEL_DEFAULT_LOCALE"] = "en"
app.config["BABEL_DEFAULT_TIMEZONE"] = "UTC"

# Mock database
users = {
    1: {"name": "Balou", "locale": "fr", "timezone": "Europe/Paris"},
    2: {"name": "Beyonce", "locale": "en", "timezone": "US/Central"},
    3: {"name": "Spock", "locale": "kg", "timezone": "Vulcan"},
    4: {"name": "Teletubby", "locale": None, "timezone": "Europe/London"},
}

def get_user():
    try:
        user_id = request.args.get("login_as")
        if user_id:
            return users.get(int(user_id))
    except Exception:
        pass
    return None

@app.before_request
def before_request():
    g.user = get_user()

def get_locale():
    """Resolve the locale with priority:
       URL param > user setting > header > default."""
    # 1) URL parameter
    url_locale = request.args.get("locale")
    if url_locale in app.config["LANGUAGES"]:
        return url_locale

    # 2) User setting
    user = getattr(g, "user", None)
    if user:
        user_locale = user.get("locale")
        if user_locale in app.config["LANGUAGES"]:
            return user_locale

    # 3) Accept-Language header
    best = request.accept_languages.best_match(app.config["LANGUAGES"])
    if best:
        return best

    # 4) Default
    return app.config["BABEL_DEFAULT_LOCALE"]

# Flask-Babel 3.x recommended pattern:
babel = Babel(app, locale_selector=get_locale)

@app.route("/")
def index():
    if g.user:
        return render_template("5-index.html", username=g.user["name"])
    return render_template("5-index.html", username=None)

if __name__ == "__main__":
    app.run()