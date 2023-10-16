from flask_jwt_extended import jwt_required
from flask_restx import Resource
from http import HTTPStatus

from .api_functions import retrieve_queries_list, create_query, remove_query, get_query
from .api_model import ns, request_model_queries_list, post_model_query, request_model_queries_item, delete_model_query
from ...utils.common import only_admins


@ns.route("")
@ns.response(int(HTTPStatus.INTERNAL_SERVER_ERROR), 'Internal Server Error')
class Queries(Resource):
    @ns.response(int(HTTPStatus.OK), 'Retrieved list.', request_model_queries_list)
    @ns.doc(description="Возвращает список всех поисковых запросов")
    def get(self):
        """ Список поисковых запросов вакансий"""
        return retrieve_queries_list()

    @ns.response(int(HTTPStatus.BAD_REQUEST), 'Validation error.')
    @ns.response(int(HTTPStatus.CONFLICT), 'Id already exists.')
    @ns.response(int(HTTPStatus.CREATED), 'Added new.', request_model_queries_item)
    @ns.expect(post_model_query)
    @jwt_required()
    @only_admins
    @ns.doc(description="Записывает новый поисковый запрос")
    def post(self):
        """ Запись нового поискового запроса """
        return create_query(ns.payload)

    @ns.response(int(HTTPStatus.BAD_REQUEST), 'Validation error.')
    @ns.response(int(HTTPStatus.OK), 'Removed.')
    @ns.response(int(HTTPStatus.CONFLICT), 'Id not exists.')
    @ns.expect(delete_model_query)
    @jwt_required()
    @only_admins
    @ns.doc(description="Удаляет поисковый запрос")
    def delete(self):
        """ Удаление поискового запроса """
        return remove_query(ns.payload)


@ns.route("/<int:query_id>")
@ns.response(int(HTTPStatus.INTERNAL_SERVER_ERROR), 'Internal Server Error')
class QueryItem(Resource):
    @ns.response(int(HTTPStatus.OK), 'Retrieved item.', request_model_queries_item)
    @ns.doc(description="Возвращает данные поискового запроса")
    def get(self, query_id):
        """ Детальные данные запроса вакансий"""
        return get_query(query_id)
