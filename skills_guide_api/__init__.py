from flask import Flask, Blueprint
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_restx import Api
from config import Config


app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)
migrate = Migrate(app, db)

blueprint = Blueprint('api', __name__,)
api = Api(blueprint,
          title="Example API application",
          description="An example API application using flask-restx",
          version="1.0",
          doc="/swagger/",
          validate=True
          )
app.register_blueprint(blueprint)

from . import models
from .utils.common import exists_and_makedir
from .parsers_models import HH
from .api_swagger import namespaces

exists_and_makedir(app.config['STATIC_FOLDER'])

app.config['AGGREGATORS']['HH'] = HH

for namespace in namespaces:
    api.add_namespace(namespace)



