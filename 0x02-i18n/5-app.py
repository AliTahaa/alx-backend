#!/usr/bin/env python3
"""T4: Force locale with URL param"""

from typing import Dict, Union
from flask import Flask, render_template, request, g
from flask_babel import Babel


class Config:
    """Cfg class"""

    DEBUG = True
    LANGS = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = "en"
    BABEL_DEFAULT_TIMEZONE = "UTC"


app = Flask(__name__)
app.config.from_object(Config)
app.url_map.strict_slashes = False
babel = Babel(app)

users = {
    1: {"name": "Balou", "locale": "fr", "timezone": "Europe/Paris"},
    2: {"name": "Beyonce", "locale": "en", "timezone": "US/Central"},
    3: {"name": "Spock", "locale": "kg", "timezone": "Vulcan"},
    4: {"name": "Teletubby", "locale": None, "timezone": "Europe/London"},
}


def get_usr() -> Union[Dict, None]:
    """Get usr by id"""
    usr_id = request.args.get('login_as')
    if usr_id:
        return users.get(int(usr_id))
    return None


@app.before_request
def before_req() -> None:
    """Before req"""
    g.user = get_usr()


@babel.localeselector
def get_loc() -> str:
    """Get loc"""
    loc = request.args.get('locale')
    if loc in app.config['LANGS']:
        return loc
    return request.accept_languages.best_match(app.config['LANGS'])


@app.route('/')
def idx() -> str:
    """Idx route"""
    return render_template("5-index.html")


if __name__ == "__main__":
    app.run()
