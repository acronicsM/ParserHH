from flask_restx import Resource
from http import HTTPStatus

from .api_functions import get_all_vacancies, get_vacancy, get_vacancy_skills, get_description
from .api_model import (ns, request_model_vacancies_list, get_model_list_vacancy,
                        request_model_vacancy_detail, request_skills_list_model, request_description_model)


@ns.route("")
@ns.response(int(HTTPStatus.INTERNAL_SERVER_ERROR), 'Internal Server Error')
class Vacancies(Resource):
    @ns.response(int(HTTPStatus.OK), 'Retrieved list.', request_model_vacancies_list)
    @ns.expect(get_model_list_vacancy)
    @ns.doc(description="Возвращает список вакансий")
    def get(self):
        """ Список вакансий"""
        kwargs = get_model_list_vacancy.parse_args()

        return get_all_vacancies(**kwargs)


@ns.route("/<int:vacancy_id>/tags")
@ns.response(int(HTTPStatus.INTERNAL_SERVER_ERROR), 'Internal Server Error')
class VacanciesItem(Resource):
    @ns.response(int(HTTPStatus.OK), 'Retrieved item.', request_skills_list_model)
    @ns.doc(description="Возвращает навыки вакансии")
    def get(self, vacancy_id):
        """ Навыки вакансии"""
        return get_vacancy_skills(vacancy_id)


@ns.route("/<int:vacancy_id>/description/<aggregator>")
@ns.response(int(HTTPStatus.INTERNAL_SERVER_ERROR), 'Internal Server Error')
class VacanciesItem(Resource):
    @ns.response(int(HTTPStatus.OK), 'Retrieved description.', request_description_model)
    @ns.response(int(HTTPStatus.CONFLICT), 'Could not get detailed job details.')
    @ns.doc(description="Парсит и возвращает описание вакансии из агрегатора")
    def get(self, vacancy_id, aggregator):
        """ Метод парсит произвольную вакансию агрегатора и возвращает её описание """
        return get_description(vacancy_id, aggregator)


@ns.route("/<int:vacancy_id>")
@ns.response(int(HTTPStatus.INTERNAL_SERVER_ERROR), 'Internal Server Error')
class VacanciesItem(Resource):
    @ns.response(int(HTTPStatus.OK), 'Retrieved item.', request_model_vacancy_detail)
    @ns.doc(description="Возвращает данные вакансии")
    def get(self, vacancy_id):
        """ Детальные данные вакансии"""
        return get_vacancy(vacancy_id)
