#!/usr/bin/env python3
"""Task 4: Force locale with URL parameter"""

from flask import Flask, render_template, request
from flask_babel import Babel


class Config:
  """Config class"""

  DEBUG = True
  LANGUAGES = ["en", "fr"]
  BABEL_DEFAULT_LOCALE = "en"
  BABEL_DEFAULT_TIMEZONE = "UTC"


app = Flask(__name__)
app.config.from_object(Config)
app.url_map.strict_slashes = False
babel = Babel(app)


@babel.localeselector
def select_locale() -> str:
  """Retrieve locale"""
  user_locale = request.args.get('locale')
  if user_locale in app.config['LANGUAGES']:
    return user_locale
  return request.accept_languages.best_match(app.config['LANGUAGES'])


@app.route('/')
def home() -> str:
  """Default route"""
  return render_template("4-index.html")

# Uncomment this line and comment the @babel.localeselector
# to get this error:
# AttributeError: 'Babel' object has no attribute 'localeselector'
# babel.init_app(app, locale_selector=select_locale)


if __name__ == "__main__":
  app.run()