# 3rd-party packages
from flask import Flask, render_template, request, redirect, url_for
from flask_mongoengine import MongoEngine
from flask_login import (
    LoginManager,
    current_user,
    login_user,
    logout_user,
    login_required,
)
from flask_bcrypt import Bcrypt
from werkzeug.utils import secure_filename

# stdlib
from datetime import datetime
import os

from flask import Flask, session
from flask_session import Session


db = MongoEngine()
login_manager = LoginManager()
bcrypt = Bcrypt()

from .users.routes import users
from .passwords.routes import passwords

def page_not_found(e):
    return render_template("404.html"), 404


def create_app(test_config=None):
    app = Flask(__name__)
    app.static_folder = 'static'
    app.config.from_pyfile("config.py", silent=False)
    if test_config is not None:
        app.config.update(test_config)

    db.init_app(app)
    login_manager.init_app(app)
    bcrypt.init_app(app)

    app.register_blueprint(users)
    app.register_blueprint(passwords)
    app.register_error_handler(404, page_not_found)

    login_manager.login_view = "users.login"

    SESSION_TYPE = 'redis'
    app.config['SECRET_KEY'] = "a"
    app.config.from_object(__name__)
    Session(app)

    return app
