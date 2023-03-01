# flask imports
from flask import Flask
import os

# DB Imports
from flask_sqlalchemy import SQLAlchemy

# Migration imports -> pip install Flask-Migrate
from flask_migrate import Migrate
from sqlalchemy import MetaData

# Login Imports -> pip install flask-login
from flask_login import LoginManager

# create flask app, __name__ = tell flask where to look
app = Flask(__name__)

# Add this secret key when you create database and forms
# Get Random letters from python terminal
# import secrets -> secrets.token_hex(16)
app.config['SECRET_KEY'] = '92bb1cc78650ae59ae9b8266bac43d93'

# db configs , /// = current directory
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

metadata = MetaData(naming_convention=convention)
db = SQLAlchemy(app, metadata=metadata)
# from .models import *
migrate = Migrate(app, db, render_as_batch=True)
login_manager = LoginManager(app)
login_manager.login_view = "users.login"

from myPackage import routes
from myPackage.routes import users
app.register_blueprint(users)