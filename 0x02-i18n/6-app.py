#!/usr/bin/env python3
"""Task 6: Use user locale"""

from typing import Dict, Union
from flask import Flask, render_template, request, g
from flask_babel import Babel


class Config:
  """Cfg"""

  DEBUG = True
  LANGUAGES = ["en", "fr"]
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


def get_user() -> Union[Dict, None]:
  """Get usr"""
  uid = request.args.get('login_as')
  if uid:
    return users.get(int(uid))
  return None


@app.before_request
def before_request() -> None:
  """B4 rqst"""
  g.user = get_user()


@babel.localeselector
def get_locale() -> str:
  """Get loc"""
  loc = request.args.get('locale')
  if loc in app.config['LANGUAGES']:
    return loc
  if g.user and g.user['locale'] in app.config["LANGUAGES"]:
    return g.user['locale']
  hdr_loc = request.headers.get('locale', '')
  if hdr_loc in app.config["LANGUAGES"]:
    return hdr_loc
  return request.accept_languages.best_match(app.config['LANGUAGES'])


@app.route('/')
def index() -> str:
  """Idx"""
  return render_template("6-index.html")


if __name__ == "__main__":
  app.run()
