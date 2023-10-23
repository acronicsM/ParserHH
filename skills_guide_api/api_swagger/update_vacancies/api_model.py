from flask_restx import Namespace, reqparse
from flask_restx.fields import String, Integer, Boolean, Nested
from . import model_name, description

ns = Namespace(name=model_name, validate=True, description=description)

request_model_update_item = ns.model('update_item_model', {
    'error': String(required=True, description='Признак ошибки при парсинге вакансий'),
    'new_vacancies': Integer(required=True, description='Количество новых вакансий'),
    'remotely_vacancies': Integer(required=True, description='Количество удаленных вакансий'),
    'total_pages': Integer(required=True, description='Количество обработанных страниц с вакансиями'),
    'updated_details': Integer(required=True, description='Количество вакансий с обработанными детальными данными'),
    'vacancies_processed': Integer(required=True, description='Общее количество обработанных вакансий'),
})

request_model_update_dict = ns.model('update_dict_model', {
    'delete_vacancies': Integer(required=True, description='Количество удаленных вакансий'),
    'update_statistics': Boolean(required=True, description='Признак выполнения обновления статистики'),
    'result': Nested(request_model_update_item, description='Результат парсинга вакансий', as_list=True),
})

get_update = reqparse.RequestParser(bundle_errors=True)
get_update.add_argument('query_id',
                        type=int,
                        location='args',
                        help='ID поискового запроса.')
