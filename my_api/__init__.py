from flask_sqlalchemy import SQLAlchemy
from flask import Flask


app = Flask(__name__)
app.config.from_object('config.Config')
# app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:adminadmin@localhost:5432/hh"
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///base1.db"

db = SQLAlchemy(app)

from . import routes, models
