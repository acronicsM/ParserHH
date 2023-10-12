from flask_restx.fields import String, Nested
from . import model_name, description
from flask_restx import Namespace

ns = Namespace(name=model_name, validate=True, description=description)

request_model_aggregator_item = ns.model('aggregator_item_model', {
    'id': String(required=True, description='ID агрегатора.'),
})

request_model_aggregator_list = ns.model('aggregator_list_model', {
    'aggregators': Nested(request_model_aggregator_item, description='Список агрегаторов', as_list=True),
})

post_model = ns.model('post_aggregator', {
    'id': String(required=True, description='ID агрегатора.'),
})

delete_model = ns.model('delete_aggregator', {
    'id': String(required=True, description='ID агрегатора.'),
})
