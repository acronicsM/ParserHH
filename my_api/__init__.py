from flask_sqlalchemy import SQLAlchemy
from flask import Flask


app = Flask(__name__)
app.config.from_object('config.Config')

db = SQLAlchemy(app)

from . import routes, models
from .utils.common import exists_and_makedir

exists_and_makedir(app.config['STATIC_FOLDER'])
