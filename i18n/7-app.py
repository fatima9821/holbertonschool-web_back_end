#!/usr/bin/env python3
""" create simple route """


from flask import Flask, render_template, request, g
from flask_babel import Babel, _
import pytz
from pytz.exceptions import UnknownTimeZoneError

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
        uid = request.args.get("login_as")
        return users.get(int(uid)) if uid else None
    except Exception:
        return None

@app.before_request
def before_request():
    g.user = get_user()

def get_locale():
    url_locale = request.args.get("locale")
    if url_locale in app.config["LANGUAGES"]:
        return url_locale

    user = getattr(g, "user", None)
    if user and user.get("locale") in app.config["LANGUAGES"]:
        return user["locale"]

    best = request.accept_languages.best_match(app.config["LANGUAGES"])
    return best or app.config["BABEL_DEFAULT_LOCALE"]

# --- New: timezone selection with validation ---
def _validated_tz(tzname: str | None) -> str | None:
    if not tzname:
        return None
    try:
        pytz.timezone(tzname)
        return tzname
    except UnknownTimeZoneError:
        return None

# Set up Babel first so we can use the decorator
babel = Babel()

@babel.timezoneselector
def get_timezone():
    """
    Resolve timezone with priority:
    1) URL ?timezone=...
    2) Logged-in user's timezone
    3) Default UTC
    Validates timezones via pytz.timezone, ignoring unknown ones.
    """
    # 1) URL parameter (validate)
    tz = _validated_tz(request.args.get("timezone"))
    if tz:
        return tz

    # 2) User setting (validate)
    user = getattr(g, "user", None)
    if user:
        tz = _validated_tz(user.get("timezone"))
        if tz:
            return tz

    # 3) Default
    return app.config["BABEL_DEFAULT_TIMEZONE"]

# Register Babel with both selectors
babel.init_app(app, locale_selector=get_locale, timezone_selector=get_timezone)

@app.route("/")
def index():
    if g.user:
        return render_template("5-index.html", username=g.user["name"])
    return render_template("5-index.html", username=None)

if __name__ == "__main__":
    app.run()