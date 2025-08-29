#!/usr/bin/env python3
""" create simple route """


from flask import Flask, render_template, request
from flask_babel import Babel, _

app = Flask(__name__)

# Config Babel
app.config['BABEL_DEFAULT_LOCALE'] = 'en'
app.config['BABEL_TRANSLATION_DIRECTORIES'] = 'translations'

babel = Babel(app)

# Sélecteur de langue simple via ?lang=fr|en
@babel.localeselector
def get_locale():
    return request.args.get('lang') or 'en'

@app.route('/')
def home():
    # Les chaînes dans le template seront marquées avec _
    return render_template('home.html')
    
if __name__ == '__main__':
    app.run(debug=True)