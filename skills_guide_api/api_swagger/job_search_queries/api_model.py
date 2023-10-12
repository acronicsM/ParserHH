from flask_restx import Namespace
from flask_restx.fields import Integer, Float, String, Nested
from . import model_name, description

ns = Namespace(name=model_name, validate=True, description=description)

request_model_queries_item = ns.model('queries_item_model', {
    'id': Integer(required=True, description='ID от поискового запроса.'),
    'name': String(required=True, description='Наименование поискового запроса.'),
    'count': Integer(required=True, description='Количество найденных вакансий.'),
    'min': Float(required=True, description='Минимальная указанная зарплата.'),
    'max': Float(required=True, description='Максимальная указанная зарплата.')
})

request_model_queries_list = ns.model('queries_list_model', {
    'queries': Nested(request_model_queries_item, description='Список поисковых запросов', as_list=True),
})

post_model_query = ns.model('post_query', {
    'name': String(required=True, description='Наименование поискового запроса.'),
})

delete_model_query = ns.model('delete_query', {
    'id': Integer(required=True, description='ID от поискового запроса.'),
})
