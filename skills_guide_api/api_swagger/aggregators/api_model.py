from flask_restx.fields import String, Nested
from . import model_name
from flask_restx import Namespace

ns = Namespace(name=model_name, validate=True, description='Агрегаторы вакансий')

get_model_item = ns.model('aggregator', {
    'id': String(required=True, description='ID агрегатора.'),
})

request_list_model = ns.model('aggregator_list', {
    'aggregators': Nested(
        get_model_item,
        description='Список агрегаторов',
        as_list=True
    ),
})

post_model = ns.model('post_aggregator', {
    'id': String(required=True, description='ID агрегатора.'),
})

delete_model = ns.model('delete_aggregator', {
    'id': String(required=True, description='ID агрегатора.'),
})
