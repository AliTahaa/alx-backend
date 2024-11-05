#!/usr/bin/env python3
"""Module to get locale from request using Flask and Babel"""

from flask import Flask, render_template, request
from flask_babel import Babel


class Config:
    """Configuration class for Flask app"""

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
    """Get best match for supported languages"""
    return request.accept_languages.best_match(app.config['LANGUAGES'])


@app.route('/')
def home() -> str:
    """Route for homepage"""
    return render_template("2-index.html")


if __name__ == "__main__":
    app.run()
