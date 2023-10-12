from flask_restx import Namespace
from . import model_name, description

ns = Namespace(name=model_name, validate=True, description=description)
