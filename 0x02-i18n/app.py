#!/usr/bin/env python3
"""Basic Flask app with i18n."""
import pytz
from typing import Union, Dict
from flask_babel import Babel, format_datetime
from flask import Flask, render_template, request, g


class Config:
    """Babel config."""
    LANGS = ["en", "fr"]
    DEFAULT_LOCALE = "en"
    DEFAULT_TZ = "UTC"


app = Flask(__name__)
app.config.from_object(Config)
app.url_map.strict_slashes = False
babel = Babel(app)
user_data = {
    1: {"name": "Balou", "locale": "fr", "timezone": "Europe/Paris"},
    2: {"name": "Beyonce", "locale": "en", "timezone": "US/Central"},
    3: {"name": "Spock", "locale": "kg", "timezone": "Vulcan"},
    4: {"name": "Teletubby", "locale": None, "timezone": "Europe/London"},
}


def fetch_user() -> Union[Dict, None]:
    """Fetch user by id."""
    uid = request.args.get('login_as', '')
    if uid:
        return user_data.get(int(uid), None)
    return None


@app.before_request
def before_req() -> None:
    """Before request."""
    g.user = fetch_user()


@babel.localeselector
def select_locale() -> str:
    """Select locale."""
    queries = request.query_string.decode('utf-8').split('&')
    query_dict = dict(map(
        lambda x: (x if '=' in x else '{}='.format(x)).split('='),
        queries,
    ))
    loc = query_dict.get('locale', '')
    if loc in app.config["LANGS"]:
        return loc
    user_info = getattr(g, 'user', None)
    if user_info and user_info['locale'] in app.config["LANGS"]:
        return user_info['locale']
    header_loc = request.headers.get('locale', '')
    if header_loc in app.config["LANGS"]:
        return header_loc
    return app.config['DEFAULT_LOCALE']


@babel.timezoneselector
def select_tz() -> str:
    """Select timezone."""
    tz = request.args.get('timezone', '').strip()
    if not tz and g.user:
        tz = g.user['timezone']
    try:
        return pytz.timezone(tz).zone
    except pytz.exceptions.UnknownTimeZoneError:
        return app.config['DEFAULT_TZ']


@app.route('/')
def index() -> str:
    """Home."""
    g.time = format_datetime()
    return render_template('index.html')


if __name__ == '__main__':
    app.run()
