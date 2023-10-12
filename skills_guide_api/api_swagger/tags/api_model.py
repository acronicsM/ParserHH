from flask_restx import Namespace, reqparse
from flask_restx.fields import Boolean, Integer, String, Nested
from . import model_name, description
from ..vacancies.api_model import request_model_vacancy_item

ns = Namespace(name=model_name, validate=True, description=description)

request_model_skill_item = ns.model('skill_item_model', {
    'id': Integer(required=True, description='ID навыка.'),
    'name': String(required=True, description='Наименование навыка.'),
    'vacancies': Integer(required=True, description='Количество вакансий с навыком'),
    'key': Boolean(required=True, description='Признак ключевого навыка'),
    'description': Boolean(required=True, description='Признак наличия навыка в описании вакансии.'),
    'basic': Boolean(required=True, description='Признак базового навыка.'),
})

request_model_skills_list = ns.model('skills_list_model', {
    'found': Integer(description='Общее количество навыков.'),
    'result': Nested(request_model_vacancy_item, description='Список навыков', as_list=True),
})

request_model_skill_vacancies_list = ns.model('skill_vacancies_list_model', {
    'vacancies': Nested(request_model_vacancy_item, description='Список вакансий', as_list=True),
})

get_model_list_skills = reqparse.RequestParser(bundle_errors=True)
get_model_list_skills.add_argument('per_page',
                                   type=int,
                                   location='args',
                                   default=10,
                                   help='Количество навыков на странице.')

get_model_list_skills.add_argument('page',
                                   type=int,
                                   location='args',
                                   default=0,
                                   help='Текущая страница вакансий.')
