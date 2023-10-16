from flask_restx import Resource
from http import HTTPStatus

from .api_functions import index_data
from .api_model import ns, request_model_index


@ns.route("")
@ns.response(int(HTTPStatus.INTERNAL_SERVER_ERROR), 'Internal Server Error')
class IndexRouter(Resource):
    @ns.response(int(HTTPStatus.OK), 'Retrieved list.', request_model_index)
    @ns.doc(description="Обобщенные данные")
    def get(self):
        """ Общие данные для главной страницы """

        return index_data()
