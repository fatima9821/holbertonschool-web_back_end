#!/usr/bin/env python3
""" create simple route """


from flask import Flask, request, render_template, g
import os
from flask_babel import Babel

app = Flask(__name__)
babel = Babel(app)


class Config(object):
    """For configure Babel"""
    LANGUAGES = ['en', 'fr']
    BABEL_DEFAULT_LOCALE = 'en'
    BABEL_DEFAULT_TIMEZONE = 'UTC'


app.config.from_object(Config)

users = {
    1: {"name": "Balou", "locale": "fr", "timezone": "Europe/Paris"},
    2: {"name": "Beyonce", "locale": "en", "timezone": "US/Central"},
    3: {"name": "Spock", "locale": "kg", "timezone": "Vulcan"},
    4: {"name": "Teletubby", "locale": None, "timezone": "Europe/London"},
}


def get_locale():
    """get locale function"""
    locale = request.args.get('locale')
    if locale in app.config['LANGUAGES']:
        return locale
    return request.accept_languages.best_match(app.config['LANGUAGES'])


def get_user():
    """Returns a user dictionary or None"""
    user_id = request.args.get('login_as')
    if user_id is not None:
        user_id = int(user_id)
        return users.get(user_id)
    return None


@app.before_request
def before_request():
    """Before request function to get user"""
    g.user = get_user()


babel = Babel(app, locale_selector=get_locale)


@app.route('/', methods=['GET'])
def index():
    """ Get simple route and return html
    """
    return render_template('5-index.html')


if __name__ == "__main__":
    host = os.getenv("API_HOST", "0.0.0.0")
    port = os.getenv("API_PORT", "5000")
    app.run(host=host, port=port)
