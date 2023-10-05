from flask_restx import Resource
from http import HTTPStatus

from .api_functions import retrieve_queries_list, create_query, remove_query
from .api_model import ns, request_list_model, post_model_query, get_model_query, delete_model_query


@ns.route("")
@ns.response(int(HTTPStatus.INTERNAL_SERVER_ERROR), 'Internal Server Error')
class Queries(Resource):
    @ns.response(int(HTTPStatus.OK), 'Retrieved list.', request_list_model)
    @ns.doc(description="Возвращает список всех поисковых запросов")
    def get(self):
        """ Список поисковых запросов вакансий"""
        return retrieve_queries_list()

    @ns.response(int(HTTPStatus.BAD_REQUEST), 'Validation error.')
    @ns.response(int(HTTPStatus.CONFLICT), 'Id already exists.')
    @ns.response(int(HTTPStatus.CREATED), 'Added new.', get_model_query)
    @ns.expect(post_model_query)
    @ns.doc(description="Записывает новый поисковый запрос")
    def post(self):
        """ Запись нового поискового запроса """
        return create_query(ns.payload)

    @ns.response(int(HTTPStatus.BAD_REQUEST), 'Validation error.')
    @ns.response(int(HTTPStatus.OK), 'Removed.')
    @ns.response(int(HTTPStatus.CONFLICT), 'Id not exists.')
    @ns.expect(delete_model_query)
    @ns.doc(description="Удаляет поисковый запрос")
    def delete(self):
        """ Удаление поискового запроса """
        return remove_query(ns.payload)
