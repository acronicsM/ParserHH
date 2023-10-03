from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_restx import Api
from config import Config


app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)
migrate = Migrate(app, db)

api = Api(version='1.0', title='АПИ проекта "Что хотят от джуна"')
api.init_app(app)

from . import routes, models
from .utils.common import exists_and_makedir
from .parsers_models import HH

exists_and_makedir(app.config['STATIC_FOLDER'])

app.config['AGGREGATORS']['HH'] = HH

api.add_namespace(routes.ns)
