from flask_restx import Resource
from http import HTTPStatus

from .api_functions import retrieve_aggregators_list, create_aggregator, remove_aggregator
from .api_model import ns, request_list_model, get_model_item, post_model, delete_model


@ns.route("")
@ns.response(int(HTTPStatus.INTERNAL_SERVER_ERROR), 'Internal Server Error')
class Aggregators(Resource):
    @ns.response(int(HTTPStatus.OK), 'Retrieved list.', request_list_model)
    @ns.doc(description="Возвращает список всех агрегаторов")
    def get(self):
        """ Список агрегаторов вакансий """
        return retrieve_aggregators_list()

    @ns.response(int(HTTPStatus.BAD_REQUEST), 'Validation error.')
    @ns.response(int(HTTPStatus.CONFLICT), 'Id already exists.')
    @ns.response(int(HTTPStatus.CREATED), 'Added new.', get_model_item)
    @ns.expect(post_model)
    @ns.doc(description="Записывает новый агрегатор вакансий")
    def post(self):
        """ Запись нового поискового запроса """
        return create_aggregator(ns.payload)

    @ns.response(int(HTTPStatus.BAD_REQUEST), 'Validation error.')
    @ns.response(int(HTTPStatus.OK), 'Removed.')
    @ns.response(int(HTTPStatus.CONFLICT), 'Id not exists.')
    @ns.expect(delete_model)
    @ns.doc(description="Удаляет агрегатор вакансий")
    def delete(self):
        """ Удаление поискового запроса """
        return remove_aggregator(ns.payload)
