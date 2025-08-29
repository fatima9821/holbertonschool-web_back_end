#!/usr/bin/env python3
""" create simple route """


from flask import Flask, request, render_template
from flask_babel import Babel, _

app = Flask(__name__)

# Configurer Babel
app.config['BABEL_DEFAULT_LOCALE'] = 'en'
app.config['BABEL_SUPPORTED_LOCALES'] = ['en', 'fr']

babel = Babel(app)

@babel.localeselector
def get_locale():
    # Vérifier si "locale" est passé en paramètre d'URL
    locale = request.args.get('locale')
    if locale in app.config['BABEL_SUPPORTED_LOCALES']:
        return locale
    # Sinon, on garde le comportement par défaut
    return request.accept_languages.best_match(app.config['BABEL_SUPPORTED_LOCALES'])

@app.route('/')
def index():
    return render_template("index.html")