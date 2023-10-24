from flask_restx import Namespace, reqparse
from flask_restx.fields import Boolean, Integer, Float, String, DateTime, Nested
from . import model_name, description

ns = Namespace(name=model_name, validate=True, description=description)

request_model_vacancy_detail = ns.model('vacancy_detail_model', {
    'id': Integer(required=True, description='ID вакансии.'),
    'name': String(required=True, description='Наименование вакансии.'),
    'salary_from': Float(required=True, description='Зарплата от.'),
    'salary_to': Float(required=True, description='Зарплата до.'),
    'requirement': String(required=True, description='Краткое описание вакансии.'),
    'published_at': DateTime(required=True, description='Дата публикации зарплаты.'),
    'experience': String(required=True, description='Опыт.'),
    'employment': String(required=True, description='Занятость.'),
    'description': String(required=True, description='Описание вакансии.'),
    'schedule': String(required=True, description='График.'),
    'url': String(required=True, description='URL адрес вакансии.'),
})

request_model_vacancy_item = ns.model('vacancy_item_model', {
    'id': Integer(required=True, description='ID вакансии.'),
    'name': String(required=True, description='Наименование вакансии.'),
    'salary_from': Float(required=True, description='Зарплата от.'),
    'salary_to': Float(required=True, description='Зарплата до.'),
    'requirement': String(required=True, description='Краткое описание вакансии.'),
    'published_at': DateTime(required=True, description='Дата публикации зарплаты.'),
    'url': String(required=True, description='URL адрес вакансии.'),
})

request_model_vacancies_list = ns.model('vacancies_list_model', {
    'found': Integer(description='Общее количество вакансий найденных по текущим параметрам.'),
    'result': Nested(request_model_vacancy_item, description='Список вакансий', as_list=True),
})

request_model_vacancy_skill = ns.model('vacancy_skill_model', {
    'id': Integer(required=True, description='ID навыка.'),
    'name': String(required=True, description='Наименование навыка.'),
    'key': Boolean(required=True, description='Признак ключевого навыка'),
    'description': Boolean(required=True, description='Признак наличия навыка в описании вакансии.'),
    'basic': Boolean(required=True, description='Признак базового навыка.'),
})

request_skills_list_model = ns.model('skills_list', {
    'skills': Nested(request_model_vacancy_skill, description='Список навыков', as_list=True),
})

get_model_list_vacancy = reqparse.RequestParser(bundle_errors=True)
get_model_list_vacancy.add_argument('per_page',
                                    type=int,
                                    location='args',
                                    default=10,
                                    help='Количество вакансий на странице.')

get_model_list_vacancy.add_argument('page',
                                    type=int,
                                    location='args',
                                    default=0,
                                    help='Текущая страница вакансий.')

get_model_list_vacancy.add_argument('tag_id',
                                    type=int,
                                    location='args',
                                    help='ID навыка.')

get_model_list_vacancy.add_argument('query_id',
                                    type=int,
                                    location='args',
                                    help='ID поискового запроса.')

get_model_list_vacancy.add_argument('new_vacancies',
                                    type=bool,
                                    location='args',
                                    help='Признак новый вакансий.')
