#!/usr/bin/env python3
""" create simple route """


from flask import Flask, request, render_template
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


def get_locale():
    """get locale function"""
    return request.accept_languages.best_match(app.config['LANGUAGES'])


babel = Babel(app, locale_selector=get_locale)


@app.route('/', methods=['GET'])
def index():
    """ Get simple route and return html
    """
    return render_template('3-index.html')


if __name__ == "__main__":
    host = os.getenv("API_HOST", "0.0.0.0")
    port = os.getenv("API_PORT", "5000")
    app.run(host=host, port=port)
