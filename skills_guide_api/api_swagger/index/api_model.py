from flask_restx import Namespace
from flask_restx.fields import Boolean, Integer, String, Nested
from . import model_name, description
from ..vacancies.api_model import request_model_vacancy_item

ns = Namespace(name=model_name, validate=True, description=description)

request_model_top_skills_item = ns.model('top_skills_item_model', {
    'id': Integer(required=True, description='ID навыка.'),
    'name': String(required=True, description='Наименование навыка.'),
    'min': Integer(required=True, description='Минимальная не нулевая зарплата.'),
    'max': Boolean(required=True, description='Максимальная не нулевая зарплата.'),
})

request_model_index = ns.model('index_model', {
    'count_vacancies': Integer(description='Общее количество вакансий.'),
    'count_skills': Integer(description='Общее количество навыков.'),
    'top_vacancies': Nested(request_model_vacancy_item, description='Топ вакансий', as_list=True),
    'top_skills': Nested(request_model_top_skills_item, description='Топ навыков', as_list=True),
})
