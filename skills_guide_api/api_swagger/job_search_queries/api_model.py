from flask_restx.fields import Integer, Float, String, Nested
from . import model_name
from flask_restx import Namespace

ns = Namespace(name=model_name, validate=True, description='Поисковые запросы вакансий')

get_model_query = ns.model('query', {
    'id': Integer(required=True, description='ID от поискового запроса.'),
    'name': String(required=True, description='Наименование поискового запроса.'),
    'count': Integer(required=True, description='Количество найденных вакансий.'),
    'min': Float(required=True, description='Минимальная указанная зарплата.'),
    'max': Float(required=True, description='Максимальная указанная зарплата.')
})

request_list_model = ns.model('query_list', {
    'queries': Nested(
        get_model_query,
        description='Список поисковых запросов',
        as_list=True
    ),
})

post_model_query = ns.model('post_query', {
    'name': String(required=True, description='Наименование поискового запроса.'),
})

delete_model_query = ns.model('delete_query', {
    'id': Integer(required=True, description='ID от поискового запроса.'),
})
